import json
import logging

def save_report(report, filename):
    try:
        with open(filename, 'w') as outfile:
            json.dump(report, outfile, indent=4, sort_keys=False)
    except Exception as ex:
        print('oops, could not save json report {}'.format(filename))
        print(ex)


def format_report(report):
    return json.dumps(report, indent=4, sort_keys=False)


def print_report(report):
    logging.info(format_report(report))
