from collections import defaultdict
import tkinter as tk
import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from collections import namedtuple

from requests import HTTPError

default_pad = 10

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
        """
        Fetch, parse, and instantiate IndexedTable objects.
        :param url:
        """
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
                        if cell.name == 'th' or section_tag == 'thead':
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


class TKinterDisplay:
    """
    TKinter GUI display class for HTML table data.
    encapsulate all GUI construction, widget configuration, event binding, and update logic.
    """

    def __init__(self, indexed_table: IndexedTable):
        if indexed_table is None:
            raise ValueError("IndexedTable instance is required to initialize TKinterDisplay.")
        self.header, *self.indexed_table = indexed_table # First row is header
        self.root = tk.Tk()
        self.listbox = None
        self.label = None

    def run(self):
        """
        start the TKinter main event loop
        """
        try:
            self._main_window()
            self.root.mainloop()
        except Exception as e:
            print(f"Error initializing main window: {e}")
            return

    def _main_window(self):
        """
        create the root window
        set the window title
        configure layout (grid or pack)
        store references to any external data sources (e.g., the BS4 class instance)
        """
        self.root.title("Country Population Viewer")
        self.root.geometry("350x400")
        self._list_box_widget()
        self._label_widget()
        self.root.resizable(False, False)

    def _list_box_widget(self):
        """
        populate the Listbox with country names provided by the BS4 class
        ensure the Listbox supports single‑selection mode
        configure scrolling if the list exceeds the window height
        store the Listbox as an instance attribute for later access
        """
        idx_county_name = 1

        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.listbox.pack(padx=default_pad, pady=default_pad, fill=tk.BOTH, expand=True)

        for row in self.indexed_table:
            country_name = row[idx_county_name]
            self.listbox.insert(tk.END, country_name)
        self.listbox.bind("<<ListboxSelect>>", self._on_listbox_select)

    def _on_listbox_select(self, event):
        item_idx = self._extract_selected_listbox_idex()
        if item_idx is not None:
            self._update_population_label(item_idx)
        else:
            self._update_population_label_error()

    def _label_widget(self):
        """
        initialize the Label with a placeholder value (e.g., “Select a country”)
        update the Label dynamically when a selection occurs
        ensure the Label is readable and positioned clearly in the layout
        """
        self.label = tk.Label(self.root, text="Select a country")
        self.label.pack(padx=default_pad, pady=default_pad)

    def _update_population_label(self, item_idx):
        idx_county_population = 2
        pop = self.indexed_table[item_idx][idx_county_population]
        text = f"Population: {pop}"
        self.label.config(text=text)

    def _update_population_label_error(self):
        self.label.config(text="Error: No selection")

    def _extract_selected_listbox_idex(self):
        """
        Safely extract the selected index from the Listbox
        """
        cs = self.listbox.curselection()
        return cs[0] if cs else None


if __name__ == '__main__':

    target_url = "https://www.worldometers.info/world-population/population-by-country/"
    print(f"{pallette.cyan}Strat fetching URL")

    try:
        bs4 = BS4(target_url)
        print(f"{pallette.cyan}{len(bs4.tables)} table found.{white}")
        print(f"{pallette.cyan}Using table_0 for the tests.")
        print("Parsing")
        table0 = bs4.tables['table_0']

        print(f"{pallette.green}Success: No. of rows {len(table0)} {white}\n")

        # Test dunders
        print(f"{pallette.yellow}[Test 1] Dunder {white}")
        print(f"__repr__:\n {repr(table0)}")
        print(f"__str__:\n{table0}")
        print(f"__len__: {len(table0)} rows")

        # Test Accessors
        country_name = table0.cell(1, 1)
        population = table0.cell(1, 2)
        print(f"Country name: {country_name}, Population: {population}")

        print(f"3rd column header: {table0.column_header(2)}")

        # Test Error Handling
        print(f"\n{pallette.yellow}[Test 3] Error Handling {white}")
        try:
            print("Causing error, row index 9999")
            table0.row(9999)
        except IndexError as e:
            print(f"{pallette.red}Caught expected error: {e}{white}")

        # Test Iteration
        print(f"\n{pallette.yellow}[Test 4] Iteration{white}")
        for i, row_list in enumerate(table0):
            if i >= 5:
                break
            print(f"{row_list[1]} ({row_list[2]})")

    except Exception as e:
        print(f"{pallette.red}Unexpected error. {e}{white}")

    TKinterDisplay(table0).run()
