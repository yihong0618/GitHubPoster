import json
import os
import xml.etree.ElementTree as ET
from collections import defaultdict, namedtuple
from numbers import Number
from typing import Dict

import pendulum

from github_poster.loader.base_loader import BaseLoader

# func is a lambda that converts the "value" attribute of the record to a numeric value.
RecordMetadata = namedtuple("RecordMetadata", ["type", "unit", "track_color", "func"])


HEALTH_RECORD_TYPES = {
    "move": RecordMetadata(
        "HKQuantityTypeIdentifierActiveEnergyBurned",
        "kCal",
        "#ED619C",
        lambda x: float(x),
    ),
    "exercise": RecordMetadata(
        "HKQuantityTypeIdentifierAppleExerciseTime", "mins", "#D7FD37", lambda x: int(x)
    ),
    "stand": RecordMetadata(
        "HKCategoryTypeIdentifierAppleStandHour",
        "hours",
        "#62F90B",
        lambda x: 1 if "HKCategoryValueAppleStandHourStood" else 0,
    ),
}


class AppleHealthLoader(BaseLoader):
    HISTORY_FILE = os.path.join("IN_FOLDER", "apple_history.json")

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.archive: Dict[str, Dict[str, Number]] = {}
        self.number_by_date_dict: Dict[str, Number] = {}
        self.apple_health_export_file = kwargs.get("apple_health_export_file")
        self.apple_health_record_type = kwargs.get("apple_health_record_type")
        self.apple_health_date = kwargs.get("apple_health_date")
        self.apple_health_value = kwargs.get("apple_health_value")
        self.apple_health_mode = kwargs.get("apple_health_mode")
        self.record_metadata = HEALTH_RECORD_TYPES[self.apple_health_record_type]

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--apple_health_date",
            dest="apple_health_date",
            type=str,
            help="Apple Health record date",
        )
        parser.add_argument(
            "--apple_health_value",
            dest="apple_health_value",
            type=str,
            help="Apple Health record value",
        )
        parser.add_argument(
            "--apple_health_mode",
            dest="apple_health_mode",
            choices=["backfill", "incremental"],
            default="incremental",
            help="Apple Health loader mode, backfill will read from export records, incremental will read from input",
        )
        parser.add_argument(
            "--apple_health_export_file",
            dest="apple_health_export_file",
            type=str,
            default=os.path.join("IN_FOLDER", "apple_health_export", "export.xml"),
            help="Apple Health export file path",
        )
        parser.add_argument(
            "--apple_health_record_type",
            dest="apple_health_record_type",
            choices=HEALTH_RECORD_TYPES.keys(),
            default="move",
            help="Apple Health Record Type",
        )

    def _load_apple_health_history(self):
        if os.path.exists(self.HISTORY_FILE):
            with open(self.HISTORY_FILE, "r") as f:
                self.archive = json.load(f)
                self.number_by_date_dict = self.archive.get(
                    self.apple_health_record_type, {}
                )

    def _write_apple_health_history(self):
        self.archive[self.apple_health_record_type] = self.number_by_date_dict
        with open(self.HISTORY_FILE, "w") as f:
            json.dump(self.archive, f, sort_keys=True)

    def make_track_dict(self):
        self.__class__.unit = self.record_metadata.unit
        self.__class__.track_color = self.record_metadata.track_color

        self._load_apple_health_history()
        getattr(self, self.apple_health_mode)()
        self._write_apple_health_history()
        self.number_list = list(self.number_by_date_dict.values())

    def incremental(self):
        date_str = pendulum.parse(self.apple_health_date).to_date_string()
        value = self.record_metadata.func(self.apple_health_value)
        self.number_by_date_dict[date_str] = value

    def backfill(self):
        from_export = defaultdict(int)

        in_target_section = False
        for _, elem in ET.iterparse(self.apple_health_export_file, events=["end"]):
            if elem.tag != "Record":
                continue

            if elem.attrib["type"] == self.record_metadata.type:
                in_target_section = True
                created = pendulum.from_format(
                    elem.attrib["creationDate"], "YYYY-MM-DD HH:mm:ss ZZ"
                )
                if created.year >= self.from_year and created.year <= self.to_year:
                    from_export[created.to_date_string()] += self.record_metadata.func(
                        elem.attrib["value"]
                    )
            elif in_target_section:
                break

            elem.clear()

        for k, v in from_export.items():
            if k not in self.number_by_date_dict:
                self.number_by_date_dict[k] = v

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
