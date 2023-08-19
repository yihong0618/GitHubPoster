import html.parser


class GitHubParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.recording = False
        self.rects = []

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.rects.append(dict(attrs))
            self.recording = True

    def handle_data(self, data):
        if self.recording:
            contributions_texts = data.split("contribution")
            if contributions_texts:
                self.rects[-1]["data-count"] = contributions_texts[0].rstrip()

    def handle_endtag(self, tag):
        if tag == "td":
            self.recording = False

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
