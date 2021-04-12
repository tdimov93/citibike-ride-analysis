# City Rides - NY bike rides analysis

The general idea is to merge a given citibike dataset with a weather dataset for the same time frame and
attempt to extract relevant stats such as the impact of weather on bike rides.

### Dataset sources
- [Citybike NY Bike rides](https://www.citibikenyc.com/system-data)
- [Visualcrossing weather data](https://www.visualcrossing.com/weather/weather-data-services#/login)

### Merge/Join strategy
Transform both dataset timestamps to a common pre-defined format (%d-%m-%Y %H:%M), ignoring the seconds.
Since the weather data contains entries on a per-minute basis for the same time frame as the bike rides data,
there is inevitably going to be a matching weather entry for every bike ride.

**Note: the weather data for every bike ride refers to the time the ride was started.**

### Analysis

The following aspects are analyzed:
 - Weather (rain in particular) impact on bike rides
 - Number of bike rides per day, hour and total amount
 - Gender repartition of customers/riders

 Note: the rain impact calculations rely on a uni-varied and highly oversimplified analysis that can provide a general idea
 of the impact of such weather conditions but it is by no means precise.

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes.

### Prerequisites

Requirements for the software and other tools to build and run
- [Docker](https://www.docker.com/)

OR alternatively:
- [Python3](https://www.python.org/)
- [pip3](https://pypi.org/project/pip/)

### Installing

Building the docker image

    docker build -t citibike --rm .

OR alternatively: installing the pip requierments

    python3 -m pip install --user -r requirements.txt


## Running

Linux/MacOS:

    docker run --name citibike --rm -v $(pwd):/home/citibike citibike

Windows:

    docker run --name citibike --rm -v %pwd%:/home/citibike citibike

OR alternatively: running the python3 app directly:

    python3 app.py


### Example output

![Analysis Report](/images/example_output.png)
![Trip Duration Chart](/images/trip_duration_chart.png)
![Gender Repartition Piechart](/images/gender_repartition_piechart.png)

The JSON report as well as the generated charts are saved in the `output/` directory

### Architecture thoughts

The most natural solution for scaling such a system could be to deploy multiple nodes that each get fed bike ride and weather datasets 1 pair at a time.
The nodes can then independently perform the necessary operations for every dataset pair they receive: cleanup and merge the datasets, run the analysis and feed the partial report to a master node that aggregates all incoming data into a global report.


### Possible improvements

- Increase the depth of analysis. As it currently stands, the only thing taken into account with regards to the weather conditions is
the information at the time a given ride starts. It could be useful to also look at the conditions at the end (and perhaps during) the ride.
The time of day is also something that can have a significant impact on the outcome since weather conditions at night are far less likely to
affect bike rides (the majority of which take place during the day)

- Input flexibility: when launched, the program will analyze the 3 example dataset pairs found in the `datasets/` folder and exit. It would
be useful to allow for variable input

- Chart generation: the `plt.save_fig` call does not act in a consistent manner and sometimes generates strange/empty charts. Should probably
get to the bottom of this
There simply aren't enough "rainy rides" in the example datasets to justify the charts that the program currently generates so it might be
a good idea to find a more relevant way of visualizing the information

## Built With

  - [Python3](https://www.python.org/) - Code
  - [pandas](https://pandas.pydata.org/) - Data manipulation and analysis
  - [matplotlib](https://matplotlib.org/) - Chart visualization
  - [Docker](https://www.docker.com/) - Building and running


## Authors

  - **Theodor Dimov** - *Initial work* -
    [GitHub](https://github.com/tdimov93)
