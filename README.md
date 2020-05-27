# Jmeter Metrics Report

Creates awesome HTML (dashboard view) report by parsing Jmeter *.jtl file (Python + Pandas + Beautifulsoup)

[![PyPI version](https://badge.fury.io/py/jmeter-metrics.svg)](https://badge.fury.io/py/jmeter-metrics)
[![Downloads](https://pepy.tech/badge/jmeter-metrics)](https://pepy.tech/project/jmeter-metrics)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)]()
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]()
[![Open Source Love png1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)]()
[![HitCount](http://hits.dwyl.io/adiralashiva8/jmeter-metrics.svg)](http://hits.dwyl.io/adiralashiva8/jmeter-metrics)

---

 - __Sample Report__ [link](https://jmetermetrics.netlify.com/)

---

#### How it Works:

1. Read *.jtl file (using pandas)

2. Get 'label', 'success', 'elapsed', 'failureMessage' values

3. Convert data to html report using Beautifulsoup

---

#### How to use in project:

> Install python

1. Install jmetermetrics

    > Case 1: Using pip
    ```
    pip install jmeter-metrics==1.0.1
    ```

    > Case 2: Using setup.py (clone project and run command within root)
    ```
    python setup.py install
    ```

    > Case 3: For latest changes use following command (pre-release or changes in master)
    ```
    pip install git+https://github.com/adiralashiva8/jmeter-metrics
    ```

2. Execute jmetermetrics command to generate report

    > Case 1: When log file name is result.jtl
    ```
    jmetermetrics
    ```

    > Case 2: When result.jtl file present under 'Result' folder
    ```
    jmetermetrics --inputpath ./Result/ --output result1.jtl
    ```

    > For more info on command line options use:

    ```
    jmetermetrics --help
    ```

3. Jmeter Metrics Report __metrics-timestamp.html__ file will be created in current folder | `-inputpath` if specified

    Command to customize name of result file
    ```
    jmetermetrics -M regression_metrics.html
    ```
---

#### Customize Report

Specify Logo in Jmeter metrics:

 - __Custom Logo__ : Customize your logo by using --logo command line option

     ```
     --logo "https://mycompany/logo.jpg"
     ```
---

#### Generate jmeter-metrics after execution

Execute jmetermetrics command after suite or test execution as follows:

 - Create .bat (or) .sh file with following snippet

    ```
    jmeter -n -t test.jmx -l result.jtl &&
    jmetermetrics [:options]
    ```

    > && is used to execute multiple command's in .bat file

  - Modify jmetermetrics command as required and execute .bat file

  - Jmeter metrics will be created after execution

---

Thanks for using jmeter-metrics!

 - What is your opinion of this report?

 - What’s the feature I should add?

If you have any questions / suggestions / comments on the report, please feel free to reach me at

 - Email: <a href="mailto:adiralashiva8@gmail.com?Subject=Jmeter%20Metrics" target="_blank">`adiralashiva8@gmail.com`</a> 

 - LinkedIn: <a href="https://www.linkedin.com/in/shivaprasadadirala/" target="_blank">`shivaprasadadirala`</a>

 - Twitter: <a href="https://twitter.com/ShivaAdirala" target="_blank">`@ShivaAdirala`</a>

---

:star: repo if you like it