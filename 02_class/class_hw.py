from collections import defaultdict
from typing import DefaultDict, Any

import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from collections import namedtuple

from requests import HTTPError

# Define color variables
red = '\033[1;91m'
yellow = '\033[1;49;93m'
green = '\033[1;92m'
cyan = '\033[1;96m'
blue = '\033[1;94m'
purple = '\033[1;95m'
white = '\033[1;97m'
black = '\033[1;90m'
orange = "\033[38;5;208m"
lavender = "\033[38;5;183m"
gray = "\033[38;5;245m"


class Color:
    red = '\033[1;91m'
    yellow = '\033[1;49;93m'
    green = '\033[1;92m'
    cyan = '\033[1;96m'
    blue = '\033[1;94m'
    purple = '\033[1;95m'
    white = '\033[1;97m'
    black = '\033[1;90m'
    orange = "\033[38;5;208m"
    lavender = "\033[38;5;183m"
    gray = "\033[38;5;245m"
    NAK = "\033[38;5;250m"


# List with color indices
colorsL = [red, orange, yellow, green, cyan, blue, lavender, purple, white, gray, black]

COLORS = namedtuple('COLORS',
                    ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'lavender', 'purple', 'white', 'gray',
                     'black'])
pallette = COLORS(*colorsL)


class BS4:
    """
    Encapsulate BeautifulSoup setup, parsing, and extraction logic.
    """

    def __init__(self, url):
        # Properties
        self.soup: BeautifulSoup = None
        self.url = url
        self.result = defaultdict(str)
        self.html = ""

    def parse(self):
        # validate URL
        if not self._valid_url(self.url):
            raise Exception('Invalid URL\nMake sure the URL is correct.\nURL: {url}')

        # fetch HTML
        self._fetch_html(self.url)
        # initialize soup object
        self.soup = BeautifulSoup(self.html,
                                  "html.parser")  # Store references to any external data source, Such as BS4 class instance
        tables = self.soup.find_all('table')
        self._parse_tables(tables)
        return self.result

    def _parse_tables(self, tables: ResultSet[Tag]):
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

    def _valid_url(self, url):
        if not url or url == "":
            return False
        elif not url.startswith('http') or url.startswith('https'):
            raise ValueError('Invalid URL\nUrl should be starting with http or https.\nURL: {url}')
        return True

    def _fetch_html(self, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            html_text = response.text
            self.html = html_text

            if not response.text.strip():
                raise ValueError("Value error: Empty HTML content.\nMake sure the URL is correct.\nURL: {url}")
        except ConnectionError:
            raise Exception("Network error: Failed to connect to the URL.\nMake sure the URL is correct.\nURL: {url}")
        except HTTPError as e:
            raise Exception(f"HTTP error: {e.response.status_code}\nMake sure the URL is correct.\nURL: {url}")
        except Exception as e:
            raise Exception(f"Failed to fetch URL: {e}\nMake sure the URL is correct.\nURL: {url}")


class IndexedTable:
    def __init__(self, parsed_table, tb_idx: int):
        # Init properties
        self.tb_idx = tb_idx
        self.indexed_table: DefaultDict[str, Any] = defaultdict(list)
        self.indexed_rows: DefaultDict[str, Any] = defaultdict(list)
        self.indexed_cells: DefaultDict[str, DefaultDict] = defaultdict()

        # Method calls
        self._index_table(parsed_table)

    def __len__(self):  # number of rows
        pass

    def __getitem__(self):  # → row or cell access
        pass

    def __iter__(self):
        # → iterate over rows
        pass

    def __repr__(self):
        pass

    def __str__(self):
        # → concise structural summary
        pass

    def _index_table(self, parsed_table):
    # store the results in an internal structure suitable for indexed access.
    # extract all child tags (thead, tbody, tr, th, td), and store the results in an internal structure suitable for indexed access.
    # Process thead, tbody, tfoot
        for section_tag in ['thead', 'tbody', 'tfoot']:
            sections = table.findall(section_tag)
            for s_idx, section in enumerate(sections):
                self.indexed_table[f"{section_tag}_{self.tb_idx}"] = str(section)

                # Find rows
                rows = section.find_all('tr')
                for tr_idx, row in enumerate(rows):
                    row_key = f"tr_{self.tb_idx}_{tr_idx}"
                    self.indexed_table[row_key] = str(row)
                    self.indexed_rows[row_key] = str(row)

                    # Find cells
                    cells = row.find_all(['th', 'td'])
                    self.indexed_cells[row_key] = defaultdict(list)
                    for td_idx, cell in enumerate(cells):
                        cell_key = f"{cell.name}_{self.tb_idx}_{tr_idx}_{td_idx}"
                        self.indexed_table[cell_key] = str(cell)
                        self.indexed_cells[row_key][cell_key] = str(cell)


    # Accessors
    def table(self):
        return self.indexed_table

    def row(self, row_index):
        return self.indexed_rows[row_index]

    def _valid_row_index(self, row_index):
        # raise error

        return True

    def cell(self, row_index, col_index):
        # Handle missing table elements exception with default dictionaries
        pass

    # cell index validation

    def column_header(self, col_index):
        pass

    # column index validation

    def row_count(self):
        pass

    def col_count(self):
        pass

    def _structural_summary(self):
        pass

    pass


# error class out of range index
# missing table elements error
# malformed raw or cells
# inconsistent column length
# failed network request

if __name__ == '__main__':
    # Parse tables using BS4
    bs4_parser = BS4("https://example.com/table_page")
    parsed_tables = bs4_parser.parse()

    # Index parsed tables
    tables_dd = defaultdict()
    for table_idx, table in parsed_tables:
        tables_dd[f'table_{table_idx}'] = IndexedTable(table)
