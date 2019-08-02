#!/usr/bin/env python

import matplotlib
import matplotlib.patches
import matplotlib.transforms
import numpy as np

from utils.dataset_types import Track, MotionState


def rotate_around_center(pts, center, yaw):
    return np.dot(pts - center, np.array([[np.cos(yaw), np.sin(yaw)], [-np.sin(yaw), np.cos(yaw)]])) + center


def polygon_xy_from_motionstate(ms, width, length):
    assert isinstance(ms, MotionState)
    lowleft = (ms.x - length / 2., ms.y - width / 2.)
    lowright = (ms.x + length / 2., ms.y - width / 2.)
    upright = (ms.x + length / 2., ms.y + width / 2.)
    upleft = (ms.x - length / 2., ms.y + width / 2.)
    return rotate_around_center(np.array([lowleft, lowright, upright, upleft]), np.array([ms.x, ms.y]), yaw=ms.psi_rad)


def update_objects_plot(timestamp, track_dict, patches_dict, text_dict, axes):
    for key, value in track_dict.items():
        assert isinstance(value, Track)
        if value.time_stamp_ms_first <= timestamp <= value.time_stamp_ms_last:
            # object is visible
            ms = value.motion_states[timestamp]
            assert isinstance(ms, MotionState)

            if key not in patches_dict:
                width = value.width
                length = value.length

                rect = matplotlib.patches.Polygon(polygon_xy_from_motionstate(ms, width, length), closed=True,
                                                  zorder=20)
                patches_dict[key] = rect
                axes.add_patch(rect)
                text_dict[key] = axes.text(ms.x, ms.y + 2, str(key), horizontalalignment='center', zorder=30)
            else:
                width = value.width
                length = value.length
                patches_dict[key].set_xy(polygon_xy_from_motionstate(ms, width, length))
                text_dict[key].set_position((ms.x, ms.y + 2))
        else:
            if key in patches_dict:
                patches_dict[key].remove()
                patches_dict.pop(key)
                text_dict[key].remove()
                text_dict.pop(key)
