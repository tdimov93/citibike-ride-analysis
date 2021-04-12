
import logging
import pandas as pd

from analysis import run_analysis_suite
from dataset_utils import purify_rides_dataset
from dataset_utils import purify_weather_dataset
from report_utils import format_report
from report_utils import save_report
from utils import cleanup_filename
from utils import ensure_dir
from visualization import generate_charts

logging.basicConfig(level=logging.INFO)


def merge_weather_data(ride_data, weather_data):
    """
    Merge the 2 provided datasets on their common 'starttime'
    column. Both datasets have already gone through the cleanup
    phase which means their timestamps share the same format.
    """
    merged_data = ride_data.merge(weather_data, how='left', on='starttime')
    return merged_data


def handle_dataset_pair(ride_data_file, weather_data_file):
    """Load, clean, merge, analyze and visualize."""
    logging.info('loading {}'.format(ride_data_file))
    ride_data = pd.read_csv(ride_data_file)
    weather_data = pd.read_csv(weather_data_file)

    logging.info('purifying data')
    ride_data = purify_rides_dataset(ride_data)
    weather_data = purify_weather_dataset(weather_data)

    logging.info('merging datasets')
    ride_data = merge_weather_data(ride_data, weather_data)

    report = {
        'period_start': weather_data['starttime'][0],
        'period_end': weather_data['starttime'][len(weather_data) - 1]
    }
    ensure_dir('output/')
    file_prefix = 'output/{}'.format(cleanup_filename(ride_data_file))

    logging.info('running analysis')
    run_analysis_suite(ride_data, weather_data, report)

    logging.info('report: \n{}'.format(format_report(report)))
    save_report(report, file_prefix + '_report.json')

    logging.info('generating charts')
    generate_charts(report, file_prefix=file_prefix)


if __name__ == "__main__":
    # run the 3 example dataset pairs
    example_datasets = [
        (
            'datasets/JC-202102-citibike-tripdata.csv',
            'datasets/weather_data_202102_1min.csv'
        ),
        (
            'datasets/JC-202103-citibike-tripdata.csv',
            'datasets/weather_data_202103_1min.csv'
        ),
        (
            'datasets/JC-202005-citibike-tripdata.csv',
            'datasets/weather_data_202005_1min.csv'
        )
    ]

    for dataset_pair in example_datasets:
        try:
            handle_dataset_pair(dataset_pair[0], dataset_pair[1])
        except Exception as ex:
            logging.error(ex)
