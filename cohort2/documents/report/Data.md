Data
====
[Introduction](../../) | Data | [Exploratory Analysis](../../exploration/) | [Interactive Visualizations](Visualizations.md)

## Data source

With almost 400 thousand lane-miles of highway and nearly double the number of cars as the next closest state, California provides an excellent case study in traffic and traffic incidents.  In particular, the San Diego region provides a good balance of highway types, distinct areas of commercial and residential focus, along with a large population. As a result, traffic patterns, and the corresponding impact of incidents, can be more easily identified.

The California Department of Transportation (CalTrans) operates an extensive highway sensor system, data archive, and tool repository known as the Performance Measurement System (PeMS, [http://pems.dot.ca.gov](http://pems.dot.ca.gov)).  The data used in this report are pulled from two related categories: 5-minute traffic data and station meta data.

#### PeMS Station Meta Data

Vehicles traveling on California state or interstate highways are recorded by inductive-loop traffic detectors located within the road in each lane. These detectors are connected in sets (typically all lanes at a particular point in the highway are part of a set). These sets are connected to a particular vehicle detector station (VDS). Throughout California, there are almost 17,000 stations, with over 1400 in the San Diego area alone.

Information describing each station is located in tab-delimited station metadata files which contain the following fields: station identifier, freeway, direction, county, city, state postmile, absolute postmile, latitude, longitude, length, type, lanes, name, and four user identifiers.

#### PeMS 5-Minute Traffic Data

Data captured by the inductive loops is collected into 30 second aggregated buckets at the detector station and sent to PeMS. The 30 second readings are further aggregated into 5 minute samples (at the station level) prior to archival. California-wide, the system records approximately 350 thousand measurements each day.

The data files provide the following comma-delimited data fields: date/time stamp, station identifier, district, freeway, direction, lane type, length, number of samples, percentage of non-imputed samples, total flow, average occupancy, average speed. Additionally, for each lane (up to 8), the following fields are optionally provided: number of samples, flow, average occupancy, average speed, percentage of non-imputed samples.

The 5-minute aggregated data is large.  Every station create 288 data points per year on a multitude of variables to include flow, speed, and occupancy.  Data is available from 1999 however we only plan to analyze data since 2008.  For San Diego district alone, PeMS generates approximately 20GB of 5-minute data per year.

## Data Acquisition

While PeMS provides access methods for the data, they are not robust to handle large volumes.  Accordingly, the dataset was scraped from the PeMS Clearing House website via a python based [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) script that finds each of the files for a range of years and downloads them. The script keeps a record of the files that have already been downloaded. The script was created by Cohort 1 and was re-run to collect the 2016 data.

To retrieve the elevation data a notebook was created to get the latitude and longitude values for each station id and then requested data from Google’s elevation api and exported the data into a consolidated csv file.

## Data Preparation

#### Data Quality

Data quality issues are still being discovered within the dataset. Since the PeMS data is preprocessed, it is difficult distinguish data quality issues from data collection or imputation issues. In raw data we could easily see that a value is missing or determine that a particular value is an outlier because it is multiple standard deviations from the mean, but in this case the data is preprocessed and missing data is filled in with either local or globally calculated values. Even though the occurrences of these issues appears to be low, the points where this has been determined shows the values at double the flow of the neighboring stations for the average year.  This might mean that the values are very further off during particular periods in time.  In general stations that are faulty tend to stay faulty for long periods of time, so the impact to that particular freeway by a single faulty station can last for over a year.

#### Data Transformation

The raw data needed to be transformed from values for every 30 seconds into something of a lower granularity so it could be processed by our laptops. In this case we aggregated the values from every 30 second interval into every 5 minute interval and then average each 5 minute interval across an entire year. This means that vector became an average station day, which has a dimensionality of 288 values for each of the 1541 stations in the San Diego district of which 839 are of the Main Line which is our primary focus for analysis purposes. The data was further partitioned into weekday and weekday which created a dimensionality of 576 by 839 by 5. From preliminary analysis the data on a per lane basis and everything but the main line was excluded. We’re hoping to scale back up to additional data as we transition to use AWS rather than our local machines for processing purposes.

As part of preprocessing duplicate data within the metadata for each station was dropped and only the last data was kept. This could inject some error in the location or other attributes of each station, but considering any movement of a station would be relatively small due to changes in the freeway, dropping this data shouldn’t have much of an impact to our analysis. Likewise from a visualization standpoint it would be extremely difficult to get background maps / tiles that were updated regularly enough to see the subtle differences within the freeway system do to improvements.  In order to get to this level a detail a much larger project would be needed with backing from organizations that have this type of data available. Most of the duplication in the metadata comes from the fact that Caltrans generates a new metadata file for the entire district any time a single station has any kind of change.  Because of this approach the majority of the data is the exact same from file to file.

In addition to handling duplicate data there are some latitudes and longitudes that are missing from the dataset for all entries of a particular station. This is obviously a data issue, and was resolved by manually inserting a latitude and longitude via google maps.  Although this is a very imprecise approach, it was considered to be a better approach than eliminating all data for a particular station when trying to do visualization where the stations are plotted on a map.

Preprocessing the data enabled us to do preliminary analysis on a smaller dataset on our local machines. Preprocessing also sets up the process for identifying issues and errors in the data set.  By using a small sample of the data consistently across the group we have been able to reduce data acquisition issues and maximize data exploration and developing insights.
