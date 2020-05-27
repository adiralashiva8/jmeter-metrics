class SummaryResults():

    def __init__(self, soup, tbody, data_series):
        self.soup = soup
        self.tbody = tbody
        self.summary_column = data_series

    def generate_summary_results(self):
        self.aggregation = {
            'label': [('Label','first')],
            'elapsed': [('Samples','count'), ('Avg','mean'), ('Min','min'), ('Max','max'), ('Throughput', throughput)],
            'success': [('Error%', error_count)],
        }

        self.summary_result = (self.summary_column.groupby(['label']).agg(self.aggregation))

        self.results = self.summary_result.round(2).values.tolist()

        for item in self.results:

            table_tr = self.soup.new_tag('tr')
            self.tbody.insert(1, table_tr)

            table_td = self.soup.new_tag('td', style="word-wrap: break-word;max-width: 250px; white-space: normal; text-align:left")
            table_td.string = str(item[0])
            table_tr.insert(0, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[1])
            table_tr.insert(1, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[2])
            table_tr.insert(2, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[3])
            table_tr.insert(3, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[4])
            table_tr.insert(4, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[6])
            table_tr.insert(5, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[5])
            table_tr.insert(6, table_td)

def error_count(x):
    count = 0
    result = count
    for text in x:
        if not text:
            count += 1

    if count != 0:
        result = float(count)/len(x) * 100

    return str(round(result,2))

def throughput(x):
    avg = sum(x) / len(x)
    result = 1 / avg * 1000
    return result