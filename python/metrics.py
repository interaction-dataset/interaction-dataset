import os
import csv
import math
import random
import sys
import numpy as np
import pandas as pd
import argparse
import pdb

ErrOK = 'ErrOK'
ErrNotFound = 'ErrNotFound'
ErrBadParameter = 'ErrBadParameter'
ErrWrongFormat = 'ErrWrongFormat'
ErrUnknown = 'ErrUnknown'
ErrBadFileHeader = 'ErrBadFileHeader'
ErrMissingResults = 'ErrMissingResults'
ErrWrongPredictionHorizons = 'ErrWrongPredictionHorzion'


FLAG_CHECK_HORIZON = 0

class Error(object):
    def __init__(self, code, description=''):
        self._code = code
        self._description = description

    @property
    def code(self):
        return self._code

    @property
    def description(self):
        return self._description

    def __str__(self):
        return f'[{self._code}: {self._description}]'


def euclidean_distance(vec1, vec2):
    if len(vec1) != len(vec2):
        return -1

    sum = 0
    for i in range(4, len(vec1)):
        if vec1[i].isalpha() or vec2[i].isalpha():
            continue
        sum += (float(vec1[i]) - float(vec2[i])) ** 2
    return math.sqrt(sum)


def absolute_distance(vec1, vec2):
    if len(vec1) != len(vec2):
        return -1

    s = 0
    for i in range(4, len(vec1)):
        if vec1[i].isalpha() or vec2[i].isalpha():
            continue
        s += abs(float(vec1[i]) - float(vec2[i]))
    return s

def load_file(ground_file_path) -> (dict, Error):
    """
    Load the ground truth file to a dictionary, with entries:
    "title" : contains titles of the table
    "1"     : lines with case id 1
    "2"     : lines with case id 2
    ...
    All keys are string
    """

    if not os.path.exists(ground_file_path):
        return dict(), Error(ErrNotFound, 'Ground Truth File Does Not Exist')

    if os.path.splitext(ground_file_path)[1] != '.csv':
        return dict(), Error(ErrBadParameter, 'Invalid File Format')

    standard_header = ['case_id', 'frame_id', 'timestamp_ms', 'track_id', 'agent_role', 'agent_type']

    data_file = csv.reader(open(ground_file_path, 'r'))
    data = dict()
    cur_id = ''
    cur_list = []
    line_num = 0
    for line in data_file:
        '''initial check of the files for missing trajectories'''
        if len(line)<8:
            return dict(), Error(ErrMissingResults, 'Missing Results in Files')

        if line_num == 0:
            '''initial check of the files for wrong headers'''
            if line[0:6] == standard_header:
                data['title'] = line
                line_num += 1
                continue
            else:
                return dict(), Error(ErrBadFileHeader, 'Invalid Header in Files')

        if line[0] != cur_id and len(cur_list) != 0:
            if FLAG_CHECK_HORIZON:
                if len(cur_list) != 30:
                    print('case id = {}, horizon length = {}'.format(cur_list[0][0], len(cur_list)))
                    return dict(), Error(ErrWrongPredictionHorizons, 'Wrong Prediction Horizon')
            
            data[cur_id] = cur_list
            cur_id = line[0]
            cur_list = [line]
        elif line[0] != cur_id:
            cur_id = line[0]
            cur_list.append(line)
        else:
            cur_list.append(line)

    return data, Error(ErrOK)


class User:
    def __init__(self, metadata):
        self._submission_data = metadata
        self._ave_displacement_error = 0
        self._min_mean_square_error = 0
        self._min_mean_absolute_error = 0
        self._min_over_n = 0
        self._status = {}

    def __str__(self):
        return "Minimum MSE: {}\nMinimum MAE: {}\nADE: {}\nMinimum over N: {}".format(
            self._min_mean_absolute_error, self._min_mean_absolute_error, self._ave_displacement_error,
            self._min_over_n)

    def check_submission_file(self, ground_truth) -> Error:
        """
        further check whether the submission file is correct. 
        """
        if len(self._submission_data.keys()) != len(ground_truth.keys()):
            print(list(set(self._submission_data.keys())-set(ground_truth.keys())))
            return Error(ErrWrongFormat, 'missing test cases in the submission')
        return Error(ErrOK)

    def all_scores(self, ground_truth) -> (dict(), float, int):
        """
        returns score and total case number.
        the score is a dictionary, including 
            1. the sum of absolute distance error, 
            2. the sum of absoulte final distance error,
            3. the sum of MoN error
        """
        absolute_dis_err = []
        final_abs_dis_err = []
        min_abs_over_n_err = []

        total_case_number = len(ground_truth.keys())-1
        x_index = 6
        y_index = 7

        for case in ground_truth.keys():
            if case == 'title':
                continue

            if FLAG_CHECK_HORIZON:
                case_length = 30
                if len(ground_truth[case]) < case_length:
                    return -1, 1
                if len(self._submission_data[case]) < case_length:
                    return -1, 1
            else:
                case_length = min(len(self._submission_data[case]), len(ground_truth[case]))



            ''' if the submitted horizon length is longer, only the first case_length will be evaluated '''
            ground_truth_xy = (np.array(ground_truth[case])[:, x_index:y_index+1]).astype(np.float)
            submitted_trajs_xy = (np.array(self._submission_data[case])[:, x_index:]).astype(np.float)
            submitted_trajs_number = int(submitted_trajs_xy.shape[1]/2)

            diff_ground_sub_xys = submitted_trajs_xy - np.tile(ground_truth_xy, submitted_trajs_number)
            distance_xys = np.sqrt(diff_ground_sub_xys[:,::2]**2 + diff_ground_sub_xys[:,1::2]**2)
            absolute_dis_err.append(np.sum(distance_xys)/submitted_trajs_number/case_length)
            final_abs_dis_err.append(np.sum(distance_xys[-1, :])/submitted_trajs_number)
            min_abs_over_n_err.append(np.min(np.sum(distance_xys, 0)/case_length))


        score = {'mae': absolute_dis_err, 'fde': final_abs_dis_err, 'mon': min_abs_over_n_err}

        return score, total_case_number


def do_job(submission_file, ground_truth_file, save_statistics_path):
    score = -1
    mon_score = -1
    progress = 0.0
    ground_truth_data, err = load_file(ground_truth_file)
    if err.code == ErrOK:
        submission_data, err = load_file(submission_file)
        if err.code == ErrOK:
            participant = User(submission_data)
            err = participant.check_submission_file(ground_truth_data)
            if err.code == ErrOK:
                score, num_of_cases = participant.all_scores(ground_truth_data)

                print('Total {} test cases in submission_file {}\n'.format(num_of_cases, submission_file))
                print('average scores - mae: {}, fde: {}, mon: {}\n'.format(sum(score['mae'])/num_of_cases, sum(score['fde'])/num_of_cases, sum(score['mon'])/num_of_cases))
                print('worst scores - mae: {}, fde: {}, mon: {}\n'.format(max(score['mae']), max(score['fde']), max(score['mon'])))
                print('worst indices - mae: {}, fde: {}, mon: {}\n'.format(score['mae'].index(max(score['mae'])), score['fde'].index(max(score['fde'])), score['mon'].index(max(score['mon']))))

                err = Error(ErrOK, 'OK')

                if save_statistics_path == '':
                    return
                else:
                    df = pd.DataFrame.from_dict(score)
                    df.to_csv(save_statistics_path)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--option", type=str, help="you can specify single file or a folder (default).", default="folder", nargs="?")
    parser.add_argument("groundtruth_file_path", type=str, help="path of the groundtruth file", nargs="?")
    parser.add_argument("submission_file_path", type=str, help="path of the submission file path", nargs="?")
    parser.add_argument("--save_statistics_file_path", type=str, default = '', nargs="?")
    args = parser.parse_args()

    if args.groundtruth_file_path is None:
        raise IOError("You must specify a path to the groundtruth files")
    if args.submission_file_path is None:
        raise IOError("You must specify a path to the submission files")

    if args.option == "file":
        do_job(args.submission_file_path, args.groundtruth_file_path, args.save_statistics_file_path)
    else:
        '''
        the ground-truth files should be named in a format as DR_CHN_Merging_ZS_gt.csv
        and the submission files should be named correspondingly as DR_CHN_Merging_ZS_sub.csv
        '''
        gt_root_path = args.groundtruth_file_path
        sub_root_path = args.submission_file_path
        save_statistics_path = args.save_statistics_file_path
        for gt_file in os.scandir(gt_root_path):
            sub_file = os.path.join(sub_root_path, os.path.basename(gt_file).split('.')[0][0:-2]+'sub.csv')
            save_statistics_path = os.path.join(sub_root_path, os.path.basename(gt_file).split('.')[0][0:-2]+'statistics.csv')
            do_job(sub_file, gt_file, save_statistics_path)


