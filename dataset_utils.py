from datetime import datetime

DATETIME_FORMAT = '%d-%m-%Y %H:%M'  # output datetime format
CITIBIKE_DATETIME_FORMAT = '%Y-%m-%d %H:%M'  # citibike data input datetime format
WEATHER_DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S'  # weather data input datetime format


def purify_datetimes(data, column, input_dt_lambda, output_dt_lambda):
    """Cleanup and transform all data[column] entries using the provided
    datetime transformation functions.
    The goals is to parse each datetime into a datetime object and then
    format it using a standardized date format.
    All non-conforming entries are filtered out.

    Arguments:
        data {pd.DataFrame} -- data frame to work on
        column {str} -- name of the column containing date/timestamps
        input_dt_lambda {function} -- parses the entries
        output_dt_lambda {function} -- formats the output
    Returns:
        [pd.DataFrame] -- the original (but modified) data frame
    """
    invalid_entries = []
    for i in range(len(data)):
        try:
            input_datetime = input_dt_lambda(data[column][i])
            data.at[i, column] = output_dt_lambda(input_datetime)
        except:
            invalid_entries.append(i)
    if invalid_entries:  # drop all rows that could not be parsed
        data.drop(invalid_entries, inplace=True)
    return data


def purify_column_names(data):
    """Convert all column names to snake_case."""
    purified_columns = {}
    for column in data:
        purified_column = column.lower().replace(' ', '_')
        purified_columns[column] = purified_column
    data.rename(columns=purified_columns, inplace=True)


def purify_rides_dataset(ride_data):
    """
    Convert all timestamps to a standardized format.
    Filter out all non-conforming rows.
    """
    input_dt_lambda = lambda t: datetime.strptime(
        t[:-8],
        CITIBIKE_DATETIME_FORMAT
    )
    output_dt_lambda = lambda t: t.strftime(DATETIME_FORMAT)
    ride_data = purify_datetimes(
        ride_data,
        'starttime',
        input_dt_lambda,
        output_dt_lambda
    )
    return ride_data


def purify_weather_dataset(weather_data):
    """
    Convert all timestamps to a standardized format.
    Filter out all non-conforming rows
    Convert column names to snake_case
    """
    # raname Date time to starttime so the set shares the same column name
    # with the ride dataset
    weather_data.rename(columns={'Date time': 'starttime'}, inplace=True)
    purify_column_names(weather_data)

    input_dt_lambda = lambda t: datetime.strptime(t, WEATHER_DATETIME_FORMAT)
    output_dt_lambda = lambda t: t.strftime(DATETIME_FORMAT)
    weather_data = purify_datetimes(
        weather_data,
        'starttime',
        input_dt_lambda,
        output_dt_lambda
    )
    return weather_data
