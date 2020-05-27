class TableResults():

    def __init__(self, soup, tbody, data_series):
        self.soup = soup
        self.tbody = tbody
        self.table_column = data_series

    def generate_table_results(self):
        self.table_result = self.table_column[['label', 'success', 'elapsed', 'failureMessage']]
        self.results = self.table_result.round(2).values.tolist()

        for item in self.results:

            table_tr = self.soup.new_tag('tr')
            self.tbody.insert(1, table_tr)

            table_td = self.soup.new_tag('td', style="word-wrap: break-word;max-width: 250px; white-space: normal; text-align:left")
            table_td.string = str(item[0])
            table_tr.insert(0, table_td)

            if item[1]:
                table_td = self.soup.new_tag('td', style="color: green")
                table_td.string = "PASS"
            else:
                table_td = self.soup.new_tag('td', style="color: red")
                table_td.string = "FAIL"
            table_tr.insert(1, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[2])
            table_tr.insert(2, table_td)

            table_td = self.soup.new_tag('td', style="word-wrap: break-word;max-width: 250px; white-space: normal; text-align:left")
            if str(item[3]) == "nan":
                table_td.string = ""
            else:
                table_td.string = str(item[3])
            table_tr.insert(3, table_td)