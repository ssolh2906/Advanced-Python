from collections import defaultdict
from typing import DefaultDict, Any, Tuple

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
        self.url = url
        self.html = ""

        # Save all tables, tags
        self.result = defaultdict()

        # Save each table as IndexedTable instance
        self.tables = defaultdict()

        self.soup = self.parse()

        if self.soup:
            tables = self.soup.find_all('table')
            for tb_idx, table in enumerate(tables):
                self.result[f'table_{tb_idx}'] = str(table)
                self.tables[f'table_{tb_idx}'] = IndexedTable(table, tb_idx)

    def parse(self):
        # validate URL
        if not self._valid_url(self.url):
            raise Exception('Invalid URL\nMake sure the URL is correct.\nURL: {url}')

        # fetch HTML
        self._fetch_html(self.url)
        # initialize soup object
        result = BeautifulSoup(self.html, "html.parser")
        # Store references to any external data source, Such as BS4 class instance
        return result

    def _valid_url(self, url):
        if not url or url == "":
            return False
        elif not (url.startswith('http') or url.startswith('https')):
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
        except requests.exceptions.ConnectionError:
            raise Exception("Network error: Failed to connect to the URL.\nMake sure the URL is correct.\nURL: {url}")
        except HTTPError as e:
            raise Exception(f"HTTP error: {e.response.status_code}\nMake sure the URL is correct.\nURL: {url}")
        except Exception as e:
            raise Exception(f"Failed to fetch URL: {e}\nMake sure the URL is correct.\nURL: {url}")


class IndexedTable:
    """
    Structured table storage
    """

    def __init__(self, parsed_table, tb_idx: int):
        # Init properties
        self.tb_idx = tb_idx
        self.result = defaultdict(str)  # Flat table data storage
        self.row_data = []  # 2D list of rows and cells
        self.headers = []  # th, td headers
        self.shape = [0, 0]  # (rows, cols)

        # Method call
        self._index_table(parsed_table)

    def __len__(self):  # number of rows
        return len(self.row_data)

    def __getitem__(self, row: int, col=None):  # → row or cell access
        if row >= len(self):
            raise IndexError("Row index out of range")

        if col is None:  # Row access
            return self.row_data[row]

        else:  # Cell[row, col] access
            if row >= len(self):
                raise IndexError("Row index out of range.\nMaximum rows: {len(self)}")
            if col >= len(self.row_data[row]):
                raise IndexError("Column index out of range.\nData dimensions: {self.shape}")
            return self.row_data[row][col]

    def __iter__(self):
        return iter(self.row_data)

    def __repr__(self):
        return self._structural_summary()

    def __str__(self):
        return self._structural_summary()

    def _index_table(self, parsed_table):
        # store the results in an internal structure suitable for indexed access.
        # extract all child tags (thead, tbody, tr, th, td), and store the results in an internal structure suitable for indexed access.
        # Process thead, tbody, tfoot
        for section_tag in ['thead', 'tbody', 'tfoot']:
            sections = parsed_table.find_all(section_tag)
            for s_idx, section in enumerate(sections):
                self.result[f"{section_tag}_{self.tb_idx}_{s_idx}"] = section.text.strip()

                # Find rows
                rows = section.find_all('tr')
                for tr_idx, row in enumerate(rows):
                    row_key = f"tr_{self.tb_idx}_{tr_idx}"
                    self.result[row_key] = row.text.strip()

                    # Cells in this row
                    curr_cell_list = list()
                    # Find cells
                    cells = row.find_all(['th', 'td'])
                    for td_idx, cell in enumerate(cells):
                        cell_key = f"{cell.name}_{self.tb_idx}_{tr_idx}_{td_idx}"
                        self.result[cell_key] = str(cell)
                        if cell.name == 'th':
                            self.headers.append(cell.text.strip())
                        curr_cell_list.append(cell.text.strip())
                    self.row_data.append(curr_cell_list)

                    self._update_shape(col_len=len(curr_cell_list))
            self._update_shape(row_len=len(self.row_data))

    def _update_shape(self, row_len: int = 0, col_len: int = 0):
        if row_len > self.shape[0]:
            self.shape[0] = row_len
        if col_len > self.shape[1]:
            self.shape[1] = col_len

    # Accessors
    def table(self):
        return self.result

    def row(self, row_index):
        try:
            self._valid_row_index(row_index)
        except IndexError as e:
            raise e
        return self.row_data[row_index]

    def cell(self, row_index, col_index):
        self._valid_row_index(row_index)
        self._valid_col_index(col_index)
        return self.row_data[row_index][col_index]

    # cell index validation

    def column_header(self, col_index):
        try:
            self._valid_col_index(col_index)
        except IndexError as e:
            raise e
        return self.headers[col_index]

    def row_count(self):
        return self.shape[0]

    def col_count(self):
        return self.shape[1]

    def _structural_summary(self):
        summary = ""
        summary += f"Table Index: {self.tb_idx}\n"
        summary += f"Shape: {self.shape[0]} x {self.shape[1]}"
        return summary

    def _valid_row_index(self, row_index):
        if row_index < 0:
            raise IndexError("Row index should be non-negative.")
        elif row_index >= self.shape[0]:
            raise IndexError(f"Row index out of range. Maximum row index: {self.shape[0]}")
        else:
            return True

    def _valid_col_index(self, col_index):
        if col_index < 0:
            raise IndexError("Column index should be non-negative.")
        elif col_index >= self.shape[1]:
            raise IndexError(f"Column index out of range. Maximum column index: {self.shape[1]}")
        else:
            return True

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
