
class BS4Parser:
    def __init__(self, url):
        self.url=url
        #validate URL
        if self._valid_url(self.url):
            # raise invalid URL error
            pass
        # fetch HTML
        html = self._fetch_html(url)
        #initialize soup object
        #self.soup = BS4() #Store references to any external data source, Such as BS4 class instance
        pass

    def _valid_url(self,url):
        return True
        
    def __len__(self): #number of rows
        pass
        
    def __getitem__(self):# → row or cell access
        pass
        
    def __iter__(self):
        # → iterate over rows
        pass
        
    def __repr__(self):
        pass
        
    def __str__(self):
        # → concise structural summary
        pass
        
    def _structural_summary(self):
        pass
        
    def _fetch_html(self,url):
        #network error handling
        #invalid response
        #missing contents
        pass
        

class Parsed_table:
    #table:dict
    
    def table(self):
        pass
        
    def row(self, row_index):
        
        pass
    
    def _valid_row_index(self, row_index):
        #raise error
        return True
        
    def cell(self, row_index, col_index):
        # Handle missing table elements exception with default dictionaries
        pass
    
    #cell index validation

    def column_header(self, col_index):
        pass
    
    #column index validation
        
        
    def row_count(self):
        pass
        
    def col_count(self):
        pass
    pass


#error class out of range index
#missing table elements error
#malformed raw or cells
#inconsistent column length
#failed network request

if __name__ == '__main__':
    BS4_Parser = BS4Parser("https://example.com/table_page")
    
    
    