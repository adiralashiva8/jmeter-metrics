class ErrorResults():

    def __init__(self, soup, tbody, data_series):
        self.soup = soup
        self.tbody = tbody
        self.error_column = data_series

    def generate_error_results(self):
        self.results = self.error_column.round(2).values.tolist()

        for item in self.results:

            if not item[4]:

                table_tr = self.soup.new_tag('tr')
                self.tbody.insert(1, table_tr)

                table_td = self.soup.new_tag('td', style="word-wrap: break-word;max-width: 250px; white-space: normal; text-align:left")
                table_td.string = str(item[0])
                table_tr.insert(0, table_td)

                table_td = self.soup.new_tag('td', style="word-wrap:break-word;max-width:250px;white-space:normal;text-align:left")
                # if " error:" in str(item[1]):
                #     table_td.string = str(item[1]).split(" code:", 1)[-1]
                # else:
                #     table_td.string = ""
                table_td.string = str(item[1])
                table_tr.insert(1, table_td)

                table_td = self.soup.new_tag('td', style="word-wrap: break-word;max-width: 250px; white-space: normal; text-align:left")
                if str(item[2]) == "nan":
                    table_td.string = ""
                else:
                    table_td.string = str(item[2])
                table_tr.insert(2, table_td)

                table_td = self.soup.new_tag('td', style="word-wrap: break-word;max-width: 250px; white-space: normal; text-align:left")
                table_td.string = str(item[3])
                table_tr.insert(3, table_td)