import unittest
import os
from python.utils import dataset_reader
from python.utils import dataset_types
from python.utils import dict_utils


class TestDatasetReader(unittest.TestCase):

    def test_dataset_reade(self):
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        tracks_dir = os.path.join(root_dir, "recorded_trackfiles")
        tracks_file = os.path.join(tracks_dir, ".TestScenarioForScripts/vehicle_tracks_000.csv")

        track_dictionary = dataset_reader.read_tracks(tracks_file)

        track = dict_utils.get_value_list(track_dictionary)[0]
        self.assertTrue(isinstance(track, dataset_types.Track))

        motion_state = track.motion_states[track.time_stamp_ms_first]
        self.assertTrue(isinstance(motion_state, dataset_types.MotionState))


if __name__ == '__main__':
    unittest.main()
