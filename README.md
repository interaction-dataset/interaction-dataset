[TOC]

# Python Scripts for the INTERACTION dataset 

* these scripts assist you to visualize the INTERACTION dataset.
* for details about and access to the dataset, visit https://interaction-dataset.com/
*  `python3` is supported

## Required Python Packages
* `csv`: for reading the csv track files
* to work with the map:
  * either `lanelet2` for most convenient map usage
    * see https://github.com/fzi-forschungszentrum-informatik/Lanelet2 for details
  * or
    * `pyproj`
    * `xml`
* `numpy`, `os`,  `sys`,  `functools`, `shutil` and`argparse` for processing the data
* `math`, `numpy`,`time` and `matplotlib` for visualizing the scenarios
* use `test_imports.py` to test whether you have all necessary packages installed

## Dataset Visualization

### Usage 

* copy/download the INTERACTION drone data into the right place
  * copy/download the track files into the folder `recorded_trackfiles`, keep one folder per scenario, as in your download
  * copy/download the maps into the folder `maps`
  * your folder structure should look like in [folder-structure.md](doc/folder-structure.md)
* to visualize the data
  * run `./main_visualize_data.py <scenario_name> <trackfile_number (default=0)>` from folder `python` to visualize scenarios
* if you only want to load and work with the track files
  * run `./main_load_track_file.py <tracks_filename>` from folder `python` to load tracks

### Test Usage without Dataset

* to test the visualization
  * run `./main_visualize_data.py .TestScenarioForScripts`
* to test loading the data
  * run `./main_load_track_file.py ../recorded_trackfiles/.TestScenarioForScripts/vehicle_tracks_000.csv`

## Participating the INTERPRET challenge

We have organized a trajectory prediction challenge ([the INTERPRET challenge] (http://challenge.interaction-dataset.com/prediction-challenge/intro)) based on the INTERACTION data. 

The INTERPRET challenge includes three tracks: 

* Regular track: prediction models are trained based on the released data. The test set in this track was sampled from the **same** traffic scenarios (e.g., maps and traffic conditions) as the released data. Observations of the test set are provided, and the prediction results will be submitted as csv files for performance evaluation.
* Generalizability track: prediction models are trained based on the released data. The test set in this track was sampled from **different and new** traffic scenarios (e.g., maps and traffic conditions) compared to those in the released data. Observations and maps of the test set are provided, and the prediction results will be submitted as csv files for performance evaluation.
* Closed-loop track: this track aims to evaluate the performance of prediction algorithms in a "prediction-->planning" pipeline so that the impacts of predictors to the closed-loop performance can be evaluated. Prediction models are trained based on the released data, and the models will be submitted as docker images. The submitted predictors, whose structures and parameters cannot be accessed by us, will be run in our simulator for "ego vehicles" in many challenging and interactive scenarios selected from the **same** traffic scenarios as the release data to evaluate their performance. Virtual, dynamic, and reactive agents are included in the simulator as the surrounding entities of the ego vehicle for each scenario. 

For detailed instructions for the "regular" and "generalizability" tracks, please visit [INTERPRET_challenge_regular_generalizability_track](https://github.com/interaction-dataset/INTERPRET_challenge_regular_generalizability_track).

For detailed instructions for the "Closed-loop" track, please visit [INTERPRET_challenge_Closed_loop](https://github.com/interaction-dataset/INTERPRET_challenge_Closed_loop).

