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
    def __init__(self, raw_data = ""):
        self.raw_data = raw_data

        self.result = defaultdict(str)

    def parse(self):
        if not self.raw_data:
            raise Exception("No data")

        table_pattern = r'<table.*?>.*?</table>'
        table_matches = re.findall(table_pattern, self.raw_data, re.DOTALL)
        for tb_idx, match in enumerate(table_matches):
            # Add table match to result dict
            self.result[f"table_{tb_idx}"] = match
            # Search inside table
            self._process_section(match, tb_idx, 'thead', 'th')
            self._process_section(match, tb_idx, 'tbody', 'td')
            self._process_section(match, tb_idx, 'tfoot', 'td')

        return self.result

    def _process_section(self, html, tb_idx, section_tag, cell_tag):
        section_pattern = rf'<{section_tag}.*?>(.*?)</{section_tag}>'
        sections = re.findall(section_pattern, html, re.DOTALL)

        for s_idx, s_content in enumerate(sections):
            self.result[f"{section_tag}_{tb_idx}_{s_idx}"] = s_content.strip()

            # Find rows
            row_matches = re.findall(r'<tr.*?>(.*?)</tr>', s_content, re.DOTALL)
            for tr_idx, tr_content in enumerate(row_matches):
                self.result[f"tr_{tb_idx}_{tr_idx}"] = tr_content.strip()

                # Find cells
                cell_pattern = rf'<{cell_tag}.*?>(.*?)</{cell_tag}>'
                cells = re.findall(cell_pattern, tr_content, re.DOTALL)
                for td_idx, c_content in enumerate(cells):
                    self.result[f"{cell_tag}_{tb_idx}_{tr_idx}_{td_idx}"] = c_content.strip()

class Bs4Parser:
    pass


if __name__ == '__main__':
    pop_url = "https://www.worldometers.info/world-population/population-by-country/"
    # raw_data = fetch_url(pop_url)
    raw_data = mock_fetch_url(pop_url)

    re_parser = ReParser(raw_data)
    re_result = re_parser.parse()
    print(re_result.keys())
    print(re_result['th_0_0_1'])


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