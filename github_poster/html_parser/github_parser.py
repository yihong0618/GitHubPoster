import html.parser


class GitHubParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.recording = False
        self.rects = []
        self.date = None
        self.capture_data = False

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            # Extract date from the <td> tag
            for attr in attrs:
                if attr[0] == "data-date":
                    self.date = attr[1]
        elif tag == "tool-tip":
            # Prepare to capture the text within <tool-tip>
            self.capture_data = True

    def handle_data(self, data):
        if self.capture_data:
            rect = {}
            contributions_texts = data.split("contribution")
            if contributions_texts:
                self.capture_data = False
                rect["data-date"] = self.date
                rect["data-count"] = (
                    int(contributions_texts[0])
                    if contributions_texts[0].rstrip().isdigit()
                    else 0
                )
                self.rects.append(rect)

    def make_contribution_dict(self, text):
        self.feed(text)
        number_by_date_dict = {}
        for r in self.rects:
            if r.get("data-count"):
                try:
                    number = int(r.get("data-count"))
                    if number:
                        number_by_date_dict[r["data-date"]] = number
                except Exception:
                    # just ignore it
                    pass
        return number_by_date_dict
