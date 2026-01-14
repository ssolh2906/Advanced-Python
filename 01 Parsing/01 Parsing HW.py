import re
from collections import defaultdict

import requests
import os


def fetch_url(url):

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    html_text = response.text
    return html_text

def mock_fetch_url(url):
    # Load raw_data from a file next to this script
    try:
        save_path = os.path.join(os.path.dirname(__file__), 'raw_data.html')
        with open(save_path, 'r', encoding='utf-8') as f:
            html_text = f.read()
        return html_text
    except Exception as e:
        print(f"Failed to load raw_data: {e}")
        return ""


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
    pop_url = "https://www.worldometers.info/world-population/population-by-country/"
    # raw_data = fetch_url(pop_url)
    raw_data = mock_fetch_url(pop_url)

    re_parser = ReParser(raw_data)
    re_result = re_parser.parse()
    print("ReParser Result:")
    print(re_result)

    # Save raw_data to a file next to this script
    # try:
    #     if not raw_data:
    #         print("No raw_data returned from parse(); nothing to save.")
    #     else:
    #         save_path = os.path.join(os.path.dirname(__file__), 'raw_data.html')
    #         with open(save_path, 'w', encoding='utf-8') as f:
    #             f.write(raw_data)
    #         print(f"Saved raw_data to: {save_path}")
    # except Exception as e:
    #     print(f"Failed to save raw_data: {e}")

    # pop_re_parser = ReParser(raw_data)
    # re_result = pop_re_parser.parse()
    #
    # pop_bs_parser = Bs4Parser(raw_data)
    # bs_result = pop_bs_parser.parse()