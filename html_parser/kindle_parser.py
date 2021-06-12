import json
from re import findall


def parse_kindle_text_to_list(text):
    """
    whole html file js -> [data1, data2, data3.........]
    """
    r = findall('"days_read":(.*),"goal_info"', text)
    if r:
        return json.loads(r[0])
    return []
