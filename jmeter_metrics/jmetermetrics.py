import os
import math
import time
import logging
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from .overview_results import OverviewResults
from .aggregate_results import AggregateResults
from .table_results import TableResults
from .error_results import ErrorResults


def generate_report(opts):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # URL or filepath of your company logo
    logo = opts.logo

    # input directory
    path = os.path.abspath(os.path.expanduser(opts.path))

    # files
    output_names = []
    if ( opts.output == "*.jtl" or opts.output == "*.csv"):
        for item in os.listdir(path):
            if os.path.isfile(item) and item.endswith('.jtl'):
                output_names.append(item)
            elif os.path.isfile(item) and item.endswith('.csv'):
                output_names.append(item)
    else:
        for curr_name in opts.output.split(","):
            curr_path = os.path.join(path, curr_name)
            output_names.append(curr_path)

    required_files = list(output_names)
    missing_files = [filename for filename in required_files if not os.path.exists(filename)]
    if missing_files:
        exit("Jmeter results file is missing: {}".format(", ".join(missing_files)))

    mt_time = datetime.now().strftime('%Y%m%d-%H%M%S')

    # Output result file location
    if opts.metrics_report_name:
        result_file_name = opts.metrics_report_name
    else:
        result_file_name = 'metrics-' + mt_time + '.html'
    result_file = os.path.join(path, result_file_name)

    # Read result.jtl file
    df_from_each_file = (pd.read_csv(f) for f in output_names)
    df = pd.concat(df_from_each_file, ignore_index=True)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # jtl file validation part
    try:
        df[['label', 'success', 'elapsed', 'failureMessage', 'responseCode', 'threadName']]
    except Exception:
        exit("Error: Missing one of the required columns in file")

    total_count = df[['success']].count().values

    if total_count == 0:
        exit("Error: File is invalid, Please retry with valid file")

    # actual flow
    logging.info(" Converting to .html file. This may take few minutes...")

    head_content = """
    <!DOCTYPE doctype html>
    <html lang="en">

    <head>
        <link href="https://img.icons8.com/color/48/000000/speed.png" rel="shortcut icon" type="image/x-icon" />
        <title>Jmeter Metrics</title>
        <meta charset="utf-8" />
        <meta content="width=device-width, initial-scale=1" name="viewport" />
        <link href="https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css" rel="stylesheet" />
        <link href="https://cdn.datatables.net/buttons/1.5.2/css/buttons.dataTables.min.css" rel="stylesheet" />
        <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet" />
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" />
        <script src="https://code.jquery.com/jquery-3.3.1.js" type="text/javascript"/>
        <!-- Bootstrap core Googleccharts -->
        <script src="https://www.gstatic.com/charts/loader.js" type="text/javascript"/>
        <script type="text/javascript">
            google.charts.load('current', {
                packages: ['corechart']
            });
        </script>
        <!-- Bootstrap core Datatable-->
        <script src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js" type="text/javascript"></script>
        <script src="https://cdn.datatables.net/buttons/1.5.2/js/dataTables.buttons.min.js" type="text/javascript"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js" type="text/javascript"></script>
        <script src="https://cdn.datatables.net/buttons/1.5.2/js/buttons.html5.min.js" type="text/javascript"></script>
        <script src="https://cdn.datatables.net/buttons/1.5.2/js/buttons.print.min.js" type="text/javascript"></script>
        <script src="https://cdn.datatables.net/buttons/1.6.1/js/buttons.colVis.min.js" type="text/javascript"></script>

        <style>
            body {
                font-family: -apple-system, sans-serif;
                background-color: #eeeeee;
            }

            .sidenav {
                height: 100%;
                width: 220px;
                position: fixed;
                z-index: 1;
                top: 0;
                left: 0;
                background-color: white;
                overflow-x: hidden;
            }

            .sidenav a {
                padding: 12px 10px 8px 12px;
                text-decoration: none;
                font-size: 18px;
                color: Black;
                display: block;
            }

            .main {
                padding-top: 10px;
            }

            @media screen and (max-height: 450px) {
                .sidenav {
                    padding-top: 15px;
                }
                .sidenav a {
                    font-size: 18px;
                }
            }

            .wrimagecard {
                margin-top: 0;
                margin-bottom: 0.6rem;
                border-radius: 10px;
                transition: all 0.3s ease;
                background-color: #f8f9fa;
            }

            .rowcard {
                padding-top: 10px;
                box-shadow: 12px 15px 20px 0px rgba(46, 61, 73, 0.15);
                border-radius: 15px;
                transition: all 0.3s ease;
                background-color: white;
            }

            .tablecard {
                background-color: white;
                font-size: 15px;
            }

            tr {
                height: 40px;
            }

            .dt-buttons {
                margin-left: 5px;
            }

            th, td, tr {
                text-align:center;
                vertical-align: middle;
            }

            .loader {
                position: fixed;
                left: 0px;
                top: 0px;
                width: 100%;
                height: 100%;
                z-index: 9999;
                background: url('https://i.ibb.co/cXnKsNR/Cube-1s-200px.gif') 50% 50% no-repeat rgb(249, 249, 249);
            }
        </style>
    </head>
    """
    if opts.ignoretableresult == "True":
        hide_keyword = "hidden"
    else:
        hide_keyword = ""

    soup = BeautifulSoup(head_content, "html.parser")
    body = soup.new_tag('body')
    soup.insert(20, body)
    icons_txt = """
    <div class="loader"></div>
    <div class="sidenav">
        <a> <img class="wrimagecard" src="%s" style="height:20vh;max-width:98%%;"/> </a>
        <a class="tablink" href="#" id="defaultOpen" onclick="openPage('dashboard', this, '#fc6666')"><i class="fa fa-dashboard" style="color:CORNFLOWERBLUE"></i> Dashboard</a>
        <a class="tablink" href="#" onclick="openPage('overviewMetrics', this, '#fc6666'); executeDataTable('#om',3)"><i class="fa fa-info-circle" style="color:STEELBLUE"></i> Overview</a>
        <a class="tablink" href="#" onclick="openPage('aggregateMetrics', this, '#fc6666'); executeDataTable('#am',2)"><i class="fa fa-th-large" style="color:CADETBLUE"></i> Aggregate Results</a>
        <a %s class="tablink" href="#" onclick="openPage('testMetrics', this, '#fc6666'); executeDataTable('#tm',3)"><i class="fa fa-th" style="color:CHOCOLATE"></i> Table Results</a>
        <a class="tablink" href="#" onclick="openPage('errorMetrics', this, '#fc6666'); executeDataTable('#em',0)"><i class="fa fa-exclamation-triangle" style="color:PALEVIOLETRED"></i> Failures</a>
    </div>
    """ % (logo, hide_keyword)

    body.append(BeautifulSoup(icons_txt, 'html.parser'))

    page_content_div = soup.new_tag('div')
    page_content_div["class"] = "main col-md-9 ml-sm-auto col-lg-10 px-4"
    body.insert(50, page_content_div)

    ### ============================ START OF Dashboard ======================================= ####

    # dashboard calculations

    logging.info(" Capturing dashboard content...")

    pass_count, fail_count, error_perct = 0, 0, 0

    for item in df[['success']].values.tolist():
        if item[0]:
            pass_count = pass_count + 1
        else:
            fail_count = fail_count + 1

    error_perct = float(fail_count) / float(total_count) * 100
    error_perct = round(error_perct, 2)

    dashboard_content = """
    <div class="tabcontent" id="dashboard">
        <div id="stats_screenshot_area">
        <div class="d-flex flex-column flex-md-row align-items-center p-1 mb-3 bg-light border-bottom shadow-sm rowcard">
            <h5 class="my-0 mr-md-auto font-weight-normal"><i class="fa fa-dashboard" style="color:CORNFLOWERBLUE"></i> Dashboard</h5>
        </div>

        <div class="row rowcard">
			<div class="col-md-6 border-right">
				<table style="width:100%;height:100px;text-align: center;">
					<tbody>
						<tr style="height:100%">
							<td>
								<table style="width:100%">
									<tbody>
										<tr style="height:100%">
											<td style="font-size:60px; color:rgb(105, 135, 219)">__TOTAL__</td>
											<td style="font-size:60px; color:#2ecc71">__PASS__</td>
										</tr>
										<tr>
											<td>
												<span style="color: #999999;font-size:12px">#Samples</span>
											</td>
											<td>
												<span style="color: #999999;font-size:12px">Pass</span>
											</td>
										</tr>
									</tbody>
								</table>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
			<div class="col-md-6 borders">
				<table style="width:100%;height:100px;text-align: center;">
					<tbody>
						<tr style="height:100%">
							<td>
								<table style="width:100%">
									<tbody>
										<tr style="height:100%">
											<td style="font-size:60px; color:#fc6666">__FAIL__</td>
											<td style="font-size:60px; color:#9E6B6A">__ERROR__</td>
										</tr>
										<tr>
											<td>
												<span style="color: #999999;font-size:12px">Fail</span>
											</td>
											<td>
												<span style="color: #999999;font-size:12px">Error%</span>
											</td>
										</tr>
									</tbody>
								</table>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
        <hr/>
        <div class="row rowcard">
            <div class="col-md-4" style="height:350px;width:auto;">
                <span style="font-weight:bold;color:gray">Status:</span>
                <div id="sampleChartID" style="height:280px;width:auto;"></div>
            </div>
            <div class="col-md-8" style="height:350px;width:auto;">
                <span style="font-weight:bold;color:gray">Top 5 Failed Samples:</span>
                <div id="failureBarID" style="height:300px;width:auto;"></div>
            </div>
        </div>
        <hr/>
        <div class="row rowcard">
            <div class="col-md-12" style="height:450px;width:auto;">
                <span style="font-weight:bold;color:gray">Top 10 Sample Avg Performance(ms):</span>
                <div id="aggBarID" style="height:400px;width:auto;"></div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12" style="height:25px;width:auto;">
                <p class="text-muted" style="text-align:center;font-size:9px">
                    <a href="https://github.com/adiralashiva8/jmeter-metrics" target="_blank" style="color:gray">jmeter-metrics</a>
                </p>
            </div>
        </div>
       <script>
            window.onload = function(){
                executeDataTable('#om',3);
                executeDataTable('#am',2);
                executeDataTable('#tm',2);
                executeDataTable('#em',0);
                createPieChart(__PASS__,__FAIL__,'sampleChartID','Status:');
 	            createBarGraph('#om',0,3,5,'failureBarID','Number of failures ','Sample');
                createBarGraph('#am',0,2,10,'aggBarID','Avg Elapsed Time (ms) ','Aggregate Report');
            };
       </script>
    </div>
    """

    dashboard_content = dashboard_content.replace("__TOTAL__", str(total_count[0]))
    dashboard_content = dashboard_content.replace("__PASS__", str(pass_count))
    dashboard_content = dashboard_content.replace("__FAIL__", str(fail_count))
    dashboard_content = dashboard_content.replace("__ERROR__", str(error_perct))
    dashboard_content = dashboard_content.replace("__KHIDE__", str(hide_keyword))

    page_content_div.append(BeautifulSoup(dashboard_content, 'html.parser'))

    ### ============================ END OF Dashboard ========================================= ####

    ### ============================ START OF Overview ======================================= ####
    logging.info(" Capturing results overview...")
    # Tests div
    ov_div = soup.new_tag('div')
    ov_div["id"] = "overviewMetrics"
    ov_div["class"] = "tabcontent"
    page_content_div.insert(50, ov_div)

    test_icon_txt = """
                    <h4><b><i class="fa fa-info-circle" style="color:STEELBLUE"></i> Overview</b></h4>
                    <hr></hr>
                    """
    ov_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))

    # Create table tag
    table = soup.new_tag('table')
    table["id"] = "om"
    table["class"] = "table row-border tablecard"
    ov_div.insert(10, table)

    thead = soup.new_tag('thead')
    table.insert(0, thead)

    tr = soup.new_tag('tr')
    thead.insert(0, tr)

    th = soup.new_tag('th')
    th.string = "Label"
    tr.insert(0, th)

    th = soup.new_tag('th')
    th.string = "Samples"
    tr.insert(1, th)

    th = soup.new_tag('th')
    th.string = "Pass"
    tr.insert(2, th)

    th = soup.new_tag('th')
    th.string = "Fail"
    tr.insert(3, th)

    th = soup.new_tag('th')
    th.string = "Fail%"
    tr.insert(4, th)

    ov_tbody = soup.new_tag('tbody')
    table.insert(11, ov_tbody)

    # GET Summary results
    summary_columns = df[['label', 'elapsed', 'success']]
    OverviewResults(soup, ov_tbody, summary_columns).generate_overview_results()

    test_icon_txt = """
    <div class="row">
        <div class="col-md-12" style="height:25px;width:auto;"></div>
    </div>
    """
    ov_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))
    ### ============================ END OF Overview ============================================ ####

    ### ============================ START OF Aggregate Report ======================================= ####
    logging.info(" Capturing aggregate report details...")

    # Tests div
    agg_div = soup.new_tag('div')
    agg_div["id"] = "aggregateMetrics"
    agg_div["class"] = "tabcontent"
    page_content_div.insert(50, agg_div)

    test_icon_txt = """
                    <h4><b><i class="fa fa-th-large" style="color:CADETBLUE"></i> Aggregate Report</b></h4>
                    <hr></hr>
                    """
    agg_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))

    # Create table tag
    table = soup.new_tag('table')
    table["id"] = "am"
    table["class"] = "table row-border tablecard"
    agg_div.insert(10, table)

    thead = soup.new_tag('thead')
    table.insert(0, thead)

    tr = soup.new_tag('tr')
    thead.insert(0, tr)

    th = soup.new_tag('th')
    th.string = "Label"
    tr.insert(0, th)

    th = soup.new_tag('th')
    th.string = "Samples"
    tr.insert(1, th)

    th = soup.new_tag('th')
    th.string = "Average (ms)"
    tr.insert(2, th)

    th = soup.new_tag('th')
    th.string = "90% Line"
    tr.insert(3, th)

    th = soup.new_tag('th')
    th.string = "95% Line"
    tr.insert(4, th)

    th = soup.new_tag('th')
    th.string = "99% Line"
    tr.insert(5, th)

    th = soup.new_tag('th')
    th.string = "Min (ms)"
    tr.insert(6, th)

    th = soup.new_tag('th')
    th.string = "Max (ms)"
    tr.insert(7, th)

    th = soup.new_tag('th')
    th.string = "Throughput"
    tr.insert(8, th)

    th = soup.new_tag('th')
    th.string = "Error %"
    tr.insert(9, th)

    suite_tbody = soup.new_tag('tbody')
    table.insert(11, suite_tbody)

    # GET Summary results
    summary_columns = df[['label', 'elapsed', 'success']]
    AggregateResults(soup, suite_tbody, summary_columns).generate_aggregate_results()

    test_icon_txt = """
    <div class="row">
        <div class="col-md-12" style="height:25px;width:auto;"></div>
    </div>
    """
    agg_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))
    ### ============================ END OF Aggregate Report ============================================ ####

    ### ============================ START OF Table Results ======================================= ####
    logging.info(" Capturing table results details...")

    # Tests div
    tm_div = soup.new_tag('div')
    tm_div["id"] = "testMetrics"
    tm_div["class"] = "tabcontent"
    page_content_div.insert(100, tm_div)

    test_icon_txt = """
    <h4><b><i class="fa fa-th" style="color:CHOCOLATE"></i> Table Results</b></h4>
    <hr></hr>
    """
    tm_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))

    # Create table tag
    table = soup.new_tag('table')
    table["id"] = "tm"
    table["class"] = "table row-border tablecard"
    tm_div.insert(10, table)

    thead = soup.new_tag('thead')
    table.insert(0, thead)

    tr = soup.new_tag('tr')
    thead.insert(0, tr)

    th = soup.new_tag('th')
    th.string = "Label"
    tr.insert(0, th)

    th = soup.new_tag('th')
    th.string = "Response Code"
    tr.insert(1, th)

    th = soup.new_tag('th')
    th.string = "Result"
    tr.insert(2, th)

    th = soup.new_tag('th')
    th.string = "Elapsed Time (ms)"
    tr.insert(3, th)

    th = soup.new_tag('th')
    th.string = "Thread Group"
    tr.insert(4, th)

    test_tbody = soup.new_tag('tbody')
    table.insert(11, test_tbody)

    # GET TEST METRICS
    if opts.ignoretableresult == "True":
        pass
    else:
        table_columns = df[['label', 'responseCode', 'success', 'elapsed', 'threadName']]
        TableResults(soup, test_tbody, table_columns).generate_table_results()

    test_icon_txt = """
    <div class="row">
        <div class="col-md-12" style="height:25px;width:auto;"></div>
    </div>
    """
    tm_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))

    ### ============================ END OF Table Results ============================================ ####

    ### ============================ START OF Error Results ======================================= ####
    logging.info(" Capturing failure details...")

    # Tests div
    tm_div = soup.new_tag('div')
    tm_div["id"] = "errorMetrics"
    tm_div["class"] = "tabcontent"
    page_content_div.insert(100, tm_div)

    test_icon_txt = """
    <h4><b><i class="fa fa-exclamation-triangle" style="color:PALEVIOLETRED"></i> Failures</b></h4>
    <hr></hr>
    """
    tm_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))

    # Create table tag
    table = soup.new_tag('table')
    table["id"] = "em"
    table["class"] = "table row-border tablecard"
    tm_div.insert(10, table)

    thead = soup.new_tag('thead')
    table.insert(0, thead)

    tr = soup.new_tag('tr')
    thead.insert(0, tr)

    th = soup.new_tag('th')
    th.string = "Label"
    tr.insert(0, th)

    th = soup.new_tag('th')
    th.string = "Error Message"
    tr.insert(1, th)

    th = soup.new_tag('th')
    th.string = "Assertion Message"
    tr.insert(2, th)

    th = soup.new_tag('th')
    th.string = "Thread Group"
    tr.insert(3, th)

    test_tbody = soup.new_tag('tbody')
    table.insert(11, test_tbody)

    # GET Error METRICS
    table_columns = df[['label', 'responseMessage', 'failureMessage', 'threadName', 'success']]
    ErrorResults(soup, test_tbody, table_columns).generate_error_results()

    test_icon_txt = """
    <div class="row">
        <div class="col-md-12" style="height:25px;width:auto;"></div>
    </div>
    """
    tm_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))

    ### ============================ END OF Error Results ============================================ ####

    # END OF LOGS
    script_text = """
        <script>
            function createPieChart(passed_count,failed_count,ChartID,ChartName){
                var status = [];
                status.push(['Status', 'Percentage']);
                status.push(['PASS',parseInt(passed_count)],['FAIL',parseInt(failed_count)]);
                var data = google.visualization.arrayToDataTable(status);

                var options = {
                pieHole: 0.6,
                legend: 'none',
                chartArea: {width: "95%",height: "90%"},
                colors: ['#2ecc71', '#fc6666'],
                };

                var chart = new google.visualization.PieChart(document.getElementById(ChartID));
                chart.draw(data, options);
            }
        </script>
        <script>
           function createBarGraph(tableID,keyword_column,time_column,limit,ChartID,Label,type){
            var status = [];
            css_selector_locator = tableID + ' tbody >tr'
            var rows = $(css_selector_locator);
            var columns;
            var myColors = [
                '#4F81BC',
                '#C0504E',
                '#9BBB58',
                '#24BEAA',
                '#8064A1',
                '#4AACC5',
                '#F79647',
                '#815E86',
                '#76A032',
                '#34558B'
            ];
            status.push([type, Label,{ role: 'annotation'}, {role: 'style'}]);
            for (var i = 0; i < rows.length; i++) {
                if (i == Number(limit)){
                    break;
                }
                //status = [];
                name_value = $(rows[i]).find('td');

                time=($(name_value[Number(time_column)]).html()).trim();
                keyword=($(name_value[Number(keyword_column)]).html()).trim();
                status.push([keyword,parseFloat(time),parseFloat(time),myColors[i]]);
              }
              var data = google.visualization.arrayToDataTable(status);

              var options = {
                legend: 'none',
                chartArea: {width: "92%",height: "75%"},
                bar: {
                    groupWidth: '90%'
                },
                annotations: {
                    alwaysOutside: true,
                    textStyle: {
                    //fontName: 'Comic Sans MS',
                    fontSize: 12,
                    //bold: true,
                    italic: true,
                    color: "black",     // The color of the text.
                    },
                },
                hAxis: {
                    textStyle: {
                        //fontName: 'Arial',
                        //fontName: 'Comic Sans MS',
                        fontSize: 10,
                    }
                },
                vAxis: {
                    gridlines: { count: 10 },
                    textStyle: {
                        //fontName: 'Comic Sans MS',
                        fontSize: 10,
                    }
                },
              };

                // Instantiate and draw the chart.
                var chart = new google.visualization.ColumnChart(document.getElementById(ChartID));
                chart.draw(data, options);
             }

        </script>

     <script>
      function executeDataTable(tabname,sortCol) {
        var fileTitle;
        switch(tabname) {
            case "#om":
                fileTitle = "Overview";
                break;
            case "#am":
                fileTitle =  "AggregateReport";
                break;
            case "#tm":
                fileTitle =  "TableReport";
                break;
            case "#em":
                fileTitle =  "Failures";
                break;
            default:
                fileTitle =  "metrics";
        }

        $(tabname).DataTable(
            {
                retrieve: true,
                "order": [[ Number(sortCol), "desc" ]],
                dom: 'l<".margin" B>frtip',
                buttons: [
                    {
                        extend:    'copyHtml5',
                        text:      '<i class="fa fa-files-o"></i>',
                        filename: function() {
                            return fileTitle + '-' + new Date().toLocaleString();
                        },
                        titleAttr: 'Copy',
                        exportOptions: {
                            columns: ':visible'
                        }
					},

                    {
                        extend:    'csvHtml5',
                        text:      '<i class="fa fa-file-text-o"></i>',
                        titleAttr: 'CSV',
                        filename: function() {
                            return fileTitle + '-' + new Date().toLocaleString();
                        },
                        exportOptions: {
                            columns: ':visible'
                        }
                    },

                    {
                        extend:    'excelHtml5',
                        text:      '<i class="fa fa-file-excel-o"></i>',
                        titleAttr: 'Excel',
                        filename: function() {
                            return fileTitle + '-' + new Date().toLocaleString();
                        },
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                    {
                        extend:    'print',
                        text:      '<i class="fa fa-print"></i>',
                        titleAttr: 'Print',
                        exportOptions: {
                            columns: ':visible',
                            alignment: 'left',
                        }
                    },
                    {
                        extend:    'colvis',
                        collectionLayout: 'fixed two-column',
                        text:      '<i class="fa fa-low-vision"></i>',
                        titleAttr: 'Hide Column',
                        exportOptions: {
                            columns: ':visible'
                        },
                        postfixButtons: [ 'colvisRestore' ]
                    },
                ],
                columnDefs: [ {
                    visible: false,
                } ]
            }
        );
    }
     </script>
    <script>
      function openPage(pageName,elmnt,color) {
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablink");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].style.color = "";
        }
        document.getElementById(pageName).style.display = "block";
        elmnt.style.color = color;

    }
    // Get the element with id="defaultOpen" and click on it
    document.getElementById("defaultOpen").click();
     </script>
     <script>
     // Get the element with id="defaultOpen" and click on it
    document.getElementById("defaultOpen").click();
    </script>
    <script>
        $(window).on('load',function(){$('.loader').fadeOut();});
    </script>
    """

    body.append(BeautifulSoup(script_text, 'html.parser'))

    # WRITE TO RF_METRICS_REPORT.HTML

    # Write output as html file
    with open(result_file, 'w') as outfile:
        outfile.write(soup.prettify())

    logging.info(" Results file created successfully and can be found at {}".format(result_file))