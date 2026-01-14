import re
from collections import defaultdict

import requests


def parse():
    url = "https://www.worldometers.info/world-population/population-by-country/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    html_text = response.text
    return html_text


class ReParser():
    def __init__(self, raw_data = None):
        self.raw_data = raw_data or ""

        self.result = defaultdict(str)

    def parse(self):
        if not self.raw_data:
            raise Exception("No data")

        self._parse_table()
        self._parse_meta()
        self._parse_table_content()
        return self.result

    def _parse_table(self):
        pass

    def _parse_meta(self):
        pass

    def _parse_table_content(self):
        pass




class Bs4Parser:
    pass


if __name__ == '__main__':
    raw_data = parse()
    pop_re_parser = ReParser(raw_data)
    re_result = pop_re_parser.parse()

    pop_bs_parser = Bs4Parser(raw_data)
    bs_result = pop_bs_parser.parse()