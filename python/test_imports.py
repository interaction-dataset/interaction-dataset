#!/usr/bin/env python

try:
    print("Trying to import csv (for loading track files).")
    import csv
    print("ok")
except ImportError:
    print("Could not import csv, but it's needed to load the track files.")

lanelet2_ok = False
try:
    print("\nTrying to import lanelet2 (for loading maps).")
    import lanelet2
    print("ok")
    lanelet2_ok = True
except ImportError:
    string = "Could not import lanelet2. It must be built and sourced, " + \
             "see https://github.com/fzi-forschungszentrum-informatik/Lanelet2 for details." + \
             "For visualization, the fallback is utils.map_vis_without_lanelet.py."
    print(string)

try:
    print("\nTrying to import xml (for loading maps without lanelet2).")
    import xml.etree.ElementTree as xml
    print("ok")
except ImportError:
    print("Could not import xml.")
    if lanelet2_ok:
        print("  Not too bad, since you have lanelet2 to load the map.")
    else:
        print("  Since lanelet2 also does not work, you need to install this to be able to load and visualize maps.")

try:
    print("\nTrying to import pyproj (for loading maps without lanelet2).")
    import pyproj
    print("ok")
except ImportError:
    print("Could not import pyproj.")
    if lanelet2_ok:
        print("  Not too bad, since you have lanelet2 to load the map.")
    else:
        print("  Since lanelet2 also does not work, you need to install this to be able to load and visualize maps.")


try:
    print("\nTrying to import argparse (argument parsing for loading and visualizing tracks).")
    import argparse
    print("ok")
except ImportError:
    print("Could not import argparse.")

try:
    print("\nTrying to import os (check file existence for loading and visualizing tracks).")
    import os
    print("ok")
except ImportError:
    print("Could not import os.")

try:
    print("\nTrying to import time (for scenario playback).")
    import time
    print("ok")
except ImportError:
    print("Could not import time.")

try:
    print("\nTrying to import math (for visualizing tracks).")
    import math
    print("ok")
except ImportError:
    print("Could not import math.")

try:
    print("\nTrying to import matplotlib (for visualizing tracks).")
    import matplotlib
    print("ok")
except ImportError:
    print("Could not import matplotlib.")

try:
    print("\nTrying to import numpy (for visualizing tracks).")
    import numpy
    print("ok")
except ImportError:
    print("Could not import numpy.")
