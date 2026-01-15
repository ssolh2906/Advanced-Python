# Please run with Colors.py in the same directory
import re
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

from Colors import Color as C


def fetch_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    html_text = response.text
    return html_text


class ReParser:
    def __init__(self, raw_data=""):
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
    def __init__(self, raw_data=""):
        self.raw_data = raw_data

        self.result = defaultdict(str)

    def parse(self):
        if not self.raw_data:
            raise Exception("No data")
        soup = BeautifulSoup(raw_data, "html.parser")

        tables = soup.find_all('table')
        for tb_idx, table in enumerate(tables):
            self.result[f"table_{tb_idx}"] = str(table)

            # Process thead, tbody, tfoot
            for section_tag in ['thead', 'tbody', 'tfoot']:
                section = table.find(section_tag)
                if section:
                    self.result[f"{section_tag}_{tb_idx}"] = str(section.text.strip())

                    # Find rows
                    rows = section.find_all('tr')
                    for tr_idx, row in enumerate(rows):
                        self.result[f"tr_{tb_idx}_{tr_idx}"] = str(row.text.strip())
                        # Find cells
                        cells = row.find_all(['th', 'td'])
                        for td_idx, cell in enumerate(cells):
                            self.result[f"{cell.name}_{tb_idx}_{tr_idx}_{td_idx}"] = str(cell.text.strip())

        return self.result


def printHeader(funcname, *parameters):
    print(f'\n{C.white}function: {funcname}')
    for item in parameters:
        print(f'{C.yellow}parameter: {item}')


def test_re_parser(raw_data):
    parser = ReParser(raw_data)
    result = parser.parse()

    printHeader("ReParser.parse")
    print(f'{C.yellow}First 5 keys:')
    print(f'{C.green}{list(result.keys())[:5]}')
    print(f'{C.yellow}Last 5 keys:')
    print(f'{C.green}{list(result.keys())[-5:]}')
    print(f'{C.yellow}Table 0, Row 3, Cell 2:')
    print(f'{C.green}{result["td_0_3_2"]}')


def test_bs_parser(raw_data):
    parser = Bs4Parser(raw_data)
    result = parser.parse()

    printHeader("Bs4Parser.parse")
    print(f'{C.yellow}First 5 keys:')
    print(f'{C.green}{list(result.keys())[:5]}')
    print(f'{C.yellow}Last 5 keys:')
    print(f'{C.green}{list(result.keys())[-5:]}')
    print(f'{C.yellow}Table 0, Row 3, Cell 2:')
    print(f'{C.green}{result["td_0_3_2"]}')


if __name__ == '__main__':
    pop_url = "https://www.worldometers.info/world-population/population-by-country/"
    raw_data = fetch_url(pop_url)

    re_parser = ReParser(raw_data)
    re_result = re_parser.parse()

    bs_parser = Bs4Parser(raw_data)
    bs_result = bs_parser.parse()

    test_re_parser(raw_data)
    test_bs_parser(raw_data)

    printHeader("Comparison")
    print("RE and BS4 produce same results with given URL.")
    print("However, the code is much shorter and clearer, using BS4.")
    print("while inside of BS4 functions, has more thorough, exception handling logics.")
    print("The parser using RE might not cover very wide range of situations. For example, malformed HTML.")
    print("beautiful soup library is widely used and keeps updating to cover more edge cases.")
    print("therefore, for more universal use, BS4 parser would be more stable and can cover more extraordinary situations.")
    print("Also, since the code using BS4 is more readable and short, it will be easier to maintain.")