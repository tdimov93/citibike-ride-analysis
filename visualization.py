
import matplotlib.pyplot as plt


def generate_charts(report, file_prefix=''):
    generate_ride_count_chart(report, file_prefix=file_prefix)
    generate_duration_chart(report, file_prefix=file_prefix)
    generate_gender_piechart(report, file_prefix=file_prefix)


def make_title(title, report):
    return title + '\n({} - {})'.format(
        report['period_start'],
        report['period_end']
        )


def generate_duration_chart(report, file_prefix=''):
    """Generate a bar chart on the average ride duration in:

        - rainy weather
        - clear weather
        - overall
    """
    labels = ['Rain', 'Clear weather', 'Overall']
    data = [
        report['avg_rain_ride_duration'],
        report['avg_clear_ride_duration'],
        report['avg_ride_duration']
    ]
    plt.cla()
    plt.title(make_title('Average ride duration (in seconds)', report))
    plt.bar(labels, data)
    plt.savefig('{}_ride_duration_barchart.png'.format(file_prefix))


def generate_ride_count_chart(report, file_prefix=''):
    """Generate a piechart to illustrate the proportions of:

        - rides started in rainy weather
        - rides started in clear weather
    """
    labels = ['Rain', 'Clear weather']
    data = [report['rain_rides'], report['clear_rides']]
    colors = ['green', 'orange']
    plt.cla()
    plt.title(make_title('Number of bike rides', report))
    plt.pie(data, labels=labels, shadow=True, colors=colors)
    plt.savefig('{}_ride_count_piechart.png'.format(file_prefix))


def generate_gender_piechart(report, file_prefix=''):
    """Generate a piechart to illustrate the proportions of:

        - rides by male customers
        - rides by female customers
        - rides by customers of unknown gender
    """
    labels = ['Male', 'Female', 'Unknown']
    data = [
        report['male_rides'],
        report['female_rides'],
        report['total_rides'] - (report['male_rides'] + report['female_rides'])
    ]
    colors = ['green', 'orange', 'magenta']
    plt.cla()
    plt.title(make_title('Number of bike rides per gender', report))
    plt.pie(data, labels=labels, shadow=True, colors=colors)
    plt.savefig('{}_gender_piechart.png'.format(file_prefix))
