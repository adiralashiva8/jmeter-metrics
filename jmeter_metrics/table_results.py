class TableResults():

    def __init__(self, soup, tbody, data_series):
        self.soup = soup
        self.tbody = tbody
        self.table_column = data_series

    def generate_table_results(self):
        self.results = self.table_column.round(2).values.tolist()

        for item in self.results:

            table_tr = self.soup.new_tag('tr')
            self.tbody.insert(1, table_tr)

            table_td = self.soup.new_tag('td', style="word-wrap: break-word;max-width: 250px; white-space: normal; text-align:left")
            table_td.string = str(item[0])
            table_tr.insert(0, table_td)

            if str(item[1]) == "nan":
                table_td = self.soup.new_tag('td')
                table_td.string = ""
                table_tr.insert(1, table_td)
            elif not str(item[1]).isnumeric():
                table_td = self.soup.new_tag('td', style="word-wrap: break-word;max-width: 250px; white-space: normal; text-align:left")
                table_td.string = str(item[1])
                table_tr.insert(1, table_td)
            else:
                table_td = self.soup.new_tag('td')
                table_td.string = str(item[1])
                table_tr.insert(1, table_td)

            if item[2]:
                table_td = self.soup.new_tag('td', style="color: green")
                table_td.string = "PASS"
            else:
                table_td = self.soup.new_tag('td', style="color: red")
                table_td.string = "FAIL"
            table_tr.insert(2, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[3])
            table_tr.insert(3, table_td)

            table_td = self.soup.new_tag('td', style="word-wrap: break-word;max-width: 250px; white-space: normal; text-align:left")
            table_td.string = str(item[4])
            table_tr.insert(4, table_td)