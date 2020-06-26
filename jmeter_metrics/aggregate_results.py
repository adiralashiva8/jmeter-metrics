class AggregateResults():

    def __init__(self, soup, tbody, data_series):
        self.soup = soup
        self.tbody = tbody
        self.aggregate_column = data_series

    def generate_aggregate_results(self):
        self.aggregation = {
            'label': [('Label','first')],
            'elapsed': [('Samples','count'), ('Avg','mean'), ('90%',q90), ('95%',q95), ('99%',q99), ('Min','min'), ('Max','max'), ('Throughput', throughput)],
            'success': [('Error%', error_count)],
        }

        self.aggregate_result = (self.aggregate_column.groupby(['label']).agg(self.aggregation))

        self.results = self.aggregate_result.round(2).values.tolist()

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
            table_td.string = str(item[5])
            table_tr.insert(5, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[6])
            table_tr.insert(6, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[7])
            table_tr.insert(7, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[8])
            table_tr.insert(8, table_td)

            table_td = self.soup.new_tag('td')
            table_td.string = str(item[9])
            table_tr.insert(9, table_td)

def error_count(x):
    count = 0
    result = count
    for text in x:
        if not text:
            count += 1

    if count != 0:
        try:
            result = float(count)/len(x) * 100
        except ZeroDivisionError:
            result = 0

    return str(round(result,2))

def throughput(x):
    avg = sum(x) / len(x)
    try:
        avg = sum(x) / len(x)
    except ZeroDivisionError:
        avg = 0

    try:
        result = 1 / avg * 1000
    except ZeroDivisionError:
        result = 0
    return result

def q90(x):
    return x.quantile(0.90)

def q95(x):
    return x.quantile(0.95)

def q99(x):
    return x.quantile(0.99)