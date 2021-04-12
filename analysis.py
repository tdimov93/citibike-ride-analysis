
import math

from dataset_utils import DATETIME_FORMAT
from datetime import datetime

# constants
PRECIPITATION_NONE = 0.0
GENDER_MALE = 1
GENDER_FEMALE = 2


def run_analysis_suite(ride_data, weather_data, report):
    run_rain_analysis(ride_data, weather_data, report)
    run_ride_duration_analysis(ride_data, report)
    run_rides_analysis(ride_data, report)
    run_gender_analysis(ride_data, report)


def run_rain_analysis(data, full_weather_data, report):
    """Perform basic analysis in order to establish the impact of rain on bike rides.

    The basic idea is to establish the % of rain time based on the full weather data
    for the given period and compare it to the % of bike rides *started* in rainy
    weather conditions.
    In an ideal (and severely oversimplified) world, the impact of rain could be
    measured by the ratio of these 2 percentages.
    """
    rain_rides = -1  # number of rides in rainy weather
    clear_rides = -1  # number of rides in clear weather
    rain_percentage = -1  # % of rain for the given time period
    rain_rides_percentage = -1  # % of rides started in rainy weather

    if len(data) >= 1 and len(full_weather_data) >= 1:
        rain_data = data[data.precipitation > PRECIPITATION_NONE]  # ride data in rainy weather
        clear_data = data[data.precipitation == PRECIPITATION_NONE]  # ride data in clear weather
        rain_weather_data = full_weather_data[full_weather_data.precipitation > PRECIPITATION_NONE]

        rain_rides = len(rain_data)
        clear_rides = len(clear_data)
        rain_percentage = (len(rain_weather_data) / (len(full_weather_data) - len(rain_data))) * 100
        rain_rides_percentage = (len(rain_data) / (len(data) - len(rain_data))) * 100

    report['rain_rides'] = rain_rides
    report['clear_rides'] = clear_rides
    report['rain_percentage'] = rain_percentage
    report['rain_rides_percentage'] = rain_rides_percentage
    report['rain_influence_ratio'] = rain_percentage / rain_rides_percentage if rain_rides_percentage else -1


def run_ride_duration_analysis(data, report):
    """ Extract ride duration statistics broken down into:

        - average ride duration
        - average ride duration in rainy conditions
        - average ride duration in clear weather conditions
    """
    avg_ride_duration = -1  # overall average ride duration
    avg_rain_ride_duration = -1  # average duration of "rainy" rides
    avg_clear_ride_duration = -1  # average duration of "clear" rides

    if len(data) >= 1:
        rain_data = data[data.precipitation > PRECIPITATION_NONE]
        clear_data = data[data.precipitation == PRECIPITATION_NONE]

        avg_ride_duration = data['tripduration'].mean()
        avg_rain_ride_duration = rain_data['tripduration'].mean()
        avg_clear_ride_duration = clear_data['tripduration'].mean()

    avg_ride_duration = avg_ride_duration if not math.isnan(avg_ride_duration) else 0
    avg_rain_ride_duration = avg_rain_ride_duration if not math.isnan(avg_rain_ride_duration) else 0
    avg_clear_ride_duration = avg_clear_ride_duration if not math.isnan(avg_clear_ride_duration) else 0
    report['avg_ride_duration'] = avg_ride_duration
    report['avg_rain_ride_duration'] = avg_rain_ride_duration
    report['avg_clear_ride_duration'] = avg_clear_ride_duration


def run_rides_analysis(data, report):
    """Extract basic ride statistics such as:

        - total rides for the given time frame
        - rides per day on average
        - rides per hour on average
    """
    total_rides = -1
    rides_per_day = -1
    rides_per_hour = -1

    if len(data) >= 1:
        start_date = datetime.strptime(report['period_start'], DATETIME_FORMAT)
        end_date = datetime.strptime(report['period_end'], DATETIME_FORMAT)
        delta = end_date - start_date
        days_between = delta.days
        hours_between = days_between * 24

        total_rides = len(data)
        rides_per_day = total_rides / days_between
        rides_per_hour = total_rides / hours_between

    report['total_rides'] = total_rides
    report['rides_per_day'] = rides_per_day
    report['rides_per_hour'] = rides_per_hour


def run_gender_analysis(data, report):
    """Extract gender-related ride statistics:

        - number of bike rides by male customers
        - number of bike rides by female customers
    """
    male_rides = -1
    female_rides = -1

    if len(data) >= 1:
        male_data = data[data.gender == GENDER_MALE]
        female_data = data[data.gender == GENDER_FEMALE]

        male_rides = len(male_data)
        female_rides = len(female_data)

    report['male_rides'] = male_rides
    report['female_rides'] = female_rides
