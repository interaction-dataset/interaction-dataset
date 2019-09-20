# Interaction Dataset Python Scripts

* these scripts assist you in processing the Interaction Dataset
* for details about and access to the dataset, visit https://interaction-dataset.com/
* both `python2` and `python3` are supported

## Required Python Packages
* `csv`: for reading the csv track files
* to work with the map:
  * either `lanelet2` for most convenient map usage
    * see https://github.com/fzi-forschungszentrum-informatik/Lanelet2 for details
  * or
    * `pyproj`
    * `xml`
* `math`, `numpy`, `os`,`argparse`, `time` and `matplotlib` for visualizing the scenarios
* use `test_imports.py` to test whether you have all necessary packages installed

## Usage

* copy/download the data into the right place
  * copy/download the track files into the folder `recorded_tracks`, keep one folder per scenario, as in your download
  * copy/download the maps into the folder `maps`
  * your folder structure should look like in [folder-structure.md](doc/folder-structure.md)
* to visualize the data
  * run `./main_visualize_data.py <scenario_name> <trackfile_number (default=0)>` from folder `python` to visualize scenarios
* if you only want to load and work with the track files
  * run `./main_load_track_file.py <tracks_filename>` from folder `python` to load tracks

## Test Usage without Dataset

* to test the visualization
  * run `./main_visualize_data.py .TestScenarioForScripts`
* to test loading the data
  * run `./main_load_track_file.py ../recorded_trackfiles/.TestScenarioForScripts/vehicle_tracks_000.csv`
