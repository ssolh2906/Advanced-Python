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

            header_pattern = r'<thead>(.*?)</thead>'
            h_matches = re.findall(header_pattern, match, re.DOTALL)
            for h_idx, h_match in enumerate(h_matches):
                self.result[f"thead_{tb_idx}_{h_idx}"] = h_match.strip()
                th_pattern = r'<th.*?>(.*?)</th>'
                th_matches = re.findall(th_pattern, h_match, re.DOTALL)
                for th_idx, th_match in enumerate(th_matches):
                    self.result[f"th_{tb_idx}_{h_idx}_{th_idx}"] = th_match.strip()


            body_pattern = r'<tbody.*?>(.*?)</tbody>'
            b_matches = re.findall(body_pattern, match, re.DOTALL)
            for b_idx, b_match in enumerate(b_matches):
                self.result[f"tbody_{tb_idx}_{b_idx}"] = b_match.strip()
                tr_pattern = r'<tr.*?>(.*?)</tr>'

            foot_pattern = r'<tfoot.*?>(.*?)</tfoot>'
            f_matches = re.findall(foot_pattern, match, re.DOTALL)
            for f_idx, f_match in enumerate(f_matches):
                self.result[f"tfoot_{tb_idx}_{f_idx}"] = f_match.strip()

        return self.result

class Bs4Parser:
    pass


if __name__ == '__main__':
    pop_url = "https://www.worldometers.info/world-population/population-by-country/"
    # raw_data = fetch_url(pop_url)
    raw_data = mock_fetch_url(pop_url)

    re_parser = ReParser(raw_data)
    re_result = re_parser.parse()
    print(re_result.keys())
    #print(re_result['thead_1_1'])


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