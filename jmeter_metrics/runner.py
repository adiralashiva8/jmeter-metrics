import os
import argparse
from .jmetermetrics import generate_report
from .version import __version__


def parse_options():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    general = parser.add_argument_group("General")
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        dest='version',
        help='Display application version information'
    )
    general.add_argument(
        '--logo',
        dest='logo',
        default='https://i.ibb.co/9qBkwDF/Testing-Fox-Logo.png',
        help="User logo (default: dummy image )"
    )

    general.add_argument(
        '-I', '--inputpath',
        dest='path',
        default=os.path.curdir,
        help="Path of result files"
    )

    general.add_argument(
        '-M', '--metrics-report-name',
        dest='metrics_report_name',
        help="Output name of the generate metrics report"
    )

    general.add_argument(
        '-O', '--output',
        dest='output',
        default="result.jtl",
        help="Name of *.jtl or *.csv file"
    )

    general.add_argument(
        '-K', '--ignoretableresult',
        dest='ignoretableresult',
        default="False",
        help="Ignore table report in metrics report"
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_options()

    if args.version:
        print(__version__)
        exit(0)

    generate_report(args)
