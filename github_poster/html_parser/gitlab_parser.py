import html.parser


class GitLabParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.lis = []

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            self.lis.append(1)
