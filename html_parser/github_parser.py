import html.parser


class GitHubParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.rects = []

    def handle_starttag(self, tag, attrs):
        if tag == "rect":
            self.rects.append(dict(attrs))

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
