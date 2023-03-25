import os
import xml.etree.ElementTree as ET
from collections import defaultdict, namedtuple

import pendulum

from github_poster.loader.base_loader import BaseLoader

# func is a lambda that converts the "value" attribute of the record to a numeric value.
RecordMetadata = namedtuple("RecordMetadata", ["type", "unit", "track_color", "func"])


SUPPORTED_HEALTH_RECORD_TYPES = {
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
    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.number_by_date_dict = defaultdict(int)
        self.apple_health_export_file = kwargs.get("apple_health_export_file")
        self.apple_health_record_type = kwargs.get("apple_health_record_type")

    @classmethod
    def add_loader_arguments(cls, parser, optional):
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
            choices=SUPPORTED_HEALTH_RECORD_TYPES.keys(),
            default="move",
            help="Apple Health Record Type",
        )

    def make_track_dict(self):
        record_metadata = SUPPORTED_HEALTH_RECORD_TYPES[self.apple_health_record_type]
        self.__class__.unit = record_metadata.unit
        self.__class__.track_color = record_metadata.track_color

        in_target_section = False
        for _, elem in ET.iterparse(self.apple_health_export_file, events=["end"]):
            if elem.tag != "Record":
                continue

            if elem.attrib["type"] == record_metadata.type:
                in_target_section = True
                create_date = pendulum.from_format(
                    elem.attrib["creationDate"], "YYYY-MM-DD HH:mm:ss ZZ"
                )
                if (
                    create_date.year >= self.from_year
                    and create_date.year <= self.to_year
                ):
                    self.number_by_date_dict[
                        create_date.to_date_string()
                    ] += record_metadata.func(elem.attrib["value"])
            elif in_target_section:
                break

            elem.clear()

        self.number_by_date_dict = {
            k: int(v) for k, v in self.number_by_date_dict.items()
        }
        self.number_list = list(self.number_by_date_dict.values())

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
