# Cohort 2 Exploration

The following sections highlight focus areas and a subset of exploratory notebooks for each.

## Visualization

| Link    | Description |
|---------|-------------|
| [WiggleVis](https://mas-dse-c6sander.github.io/DSE_Cohort2_Traffic_Capstone/cohort2/vis/WiggleVis/index.html#map_settings) | Visualization of Wiggle and Speed |
| [HeuristicClusterHeatmap](https://public.tableau.com/profile/josh.duclos#!/vizhome/HeuristicClusterHeatmap/TimeScrub) | Heatmaps to exploration classification of traffic in Tableau |
| [Wiggles_AllStations_Weekdays](https://public.tableau.com/profile/miki.hardisty#!/vizhome/Wiggles_AllStations_Weekdays/Dashboard1) | Tableau Dashboard to visualize difference in wiggle flow and mean wiggle |
| [Traffic_Wiggles](https://public.tableau.com/profile/miki.hardisty#!/vizhome/traffic_wiggles/Dashboard1) | Tableau Dashboard to visualize the average smoothed vector over a freeway |
| [Wiggles_by_min](https://public.tableau.com/profile/cj6271#!/vizhome/wiggles_by_min/Dashboard1) | The "poor man's" Fourier Transform |
| [SensorHealth](https://public.tableau.com/profile/chris.sanders#!/vizhome/Station_day_analysis/Story1) | Tableau Dashboard of sensor health |

## Wavelets

| File    | Description |
|---------|-------------|
| [learning_fft.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/learning_fft.ipynb) | Discussion of Fourier transforms and application to traffic data. |
| [learning_fft_wavelets.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/learning_fft_wavelets.ipynb) | Initial exploration of Fourier transforms as applied to traffic flow. Brief look at wavelets (continued in the notebook below). |
| [learning_wavelet.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/learning_wavelet.ipynb) | Initial exploration into wavelets, wavelet transformation, and wavelet scale/shift. |
| [wiggles_wavelets_exploration2.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/wiggles_wavelets_exploration2.ipynb) | Exploration of wavelet forms and wavelet tuning as applied to the mean flow. Wavelet transform is then used to extract mean flow wiggles and visualize as wave propagation in time/space. |

## Wiggles

| File    | Description |
|---------|-------------|
| [wiggles_analyze_example.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/wiggles_analyze_example.ipynb) | Initial exploration of "wiggles" (oscillations in the mean flow).  Uses smoothed mean flow to extract the wiggle waveform. |
| [wiggles_speed_flow_occupancy.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/wiggles_speed_flow_occupancy.ipynb) | Analysis of wiggles for flow, speed, and occupancy. |
| [wiggle_ramp_relationships2.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/wiggle_ramp_relationships2.ipynb) | Exploration and analysis of on-ramp/off-ramp wiggles (mean flow) in relation to main-line wiggles. |
| [wiggles_across_multiple_years.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/wiggles_across_multiple_years.ipynb) | Exploration and visualization of wiggles and mean flow across multiple years. |
| [wiggles_magnitude_weekend_weekday.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/wiggles_magnitude_weekend_weekday.ipynb) | Analysis of weekend vs. weekday wiggle magnitudes. |

## Other

| File    | Description |
|---------|-------------|
| [data_exploration_with_sensor_health.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/data_exploration_with_sensor_health.ipynb) | Exploratory analysis of traffic meta data, specifically sensor health, measurement accuracy, and the implications of data imputation. |
| [traffic_flow_speed_occupancy_relationship.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/traffic_flow_speed_occupancy_relationship.ipynb) | Exploratory analysis of flow, speed, and occupancy relationships. |
| [traffic_flow_speed_occupancy_clustering.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/traffic_flow_speed_occupancy_clustering.ipynb) | Survey of clustering algorithms as applied to traffic data. |
| [traffic_clustering_i5s.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/traffic_clustering_i5s.ipynb) | Exploration of speed/occupancy/flow classification and clustering for I-5 south.  Includes Birch clustering and heuristic classification. |
| [traffic_fundamental_diagram.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/traffic_fundamental_diagram.ipynb) | Discussion of three-phase traffic theory and the fundamental diagram of traffic (including application to CalTrans traffic data).  |
| [traffic_jam_exploration.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/traffic_jam_exploration.ipynb) | Computer vision approach to traffic jam identification/classification using speed heatmap. |
| [traffic_prediction_model.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/traffic_prediction_model.ipynb) | Traffic flow prediction model (sources and sinks) exploration and analysis. |
| [traffic_statistics.ipynb](https://github.com/mas-dse-c6sander/DSE_Cohort2_Traffic_Capstone/blob/master/cohort2/exploration/traffic_statistics.ipynb) | Statistical analysis of flow, occupancy, and speed including heatmap visualizations. |
