import os
import csv
import sys
import functools


def load_csv(file_path) -> (list, list):
    data_file = csv.reader(open(file_path, 'r'))
    data = []
    title = []
    line_num = 0

    for line in data_file:
        if line_num == 0:
            title = line
            line_num += 1
        else:
            data.append(line)
    return title, data


def sort_by_time_stamp(line1, line2):
    frame_1 = int(line1[0].split('-')[1])
    frame_2 = int(line2[0].split('-')[1])
    track_1 = int(line1[2].split('-')[1])
    track_2 = int(line2[2].split('-')[1])
    file_1 = int(line1[2].split('-')[0].split('_')[2])
    file_2 = int(line2[2].split('-')[0].split('_')[2])

    if file_1 < file_2:
        return -1
    elif file_1 == file_2:
        if frame_1 < frame_2:
            return -1
        elif frame_1 == frame_2:
            if track_1 < track_2:
                return -1
            elif track_1 == track_2:
                return 0
    return 1


def sort_by_time_stamp_single(line1, line2):
    frame_1 = int(line1[0].strip())
    frame_2 = int(line2[0].strip())
    track_1 = line1[2].strip()
    track_2 = line2[2].strip()

    if frame_1 < frame_2:
        return -1
    elif frame_1 == frame_2:
        if track_1[0] == 'P' and track_2[0] != 'P':
            return -1
        elif track_1[0] != 'P' and track_2[0] == 'P':
            return 0
        elif track_1[0] == 'P' and track_2[0] == 'P':
            if int(track_1[1:]) < int(track_2[1:]):
                return -1
            elif int(track_1[1:]) == int(track_2[1:]):
                return 0
        elif track_1[0] != 'P' and track_2[0] != 'P':
            if int(track_1) < int(track_2):
                return -1
            elif int(track_1) == int(track_2):
                return 0
    return 1


def write_to_csv(title, data, target_path, dir_name):
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    save_path = target_path + os.sep + dir_name + '.csv'

    with open(save_path, 'w', encoding='utf-8', newline='') as out_csv:
        csv_writer = csv.writer(out_csv)
        csv_writer.writerow(title)

        for line in data:
            csv_writer.writerow(line)

        out_csv.close()


def rearrange(csv_file_path, mode=''):
    title, data = load_csv(os.getcwd() + os.sep + csv_file_path)
    title.insert(2, title.pop(0))

    for i in range(len(data)):
        data[i].insert(2, data[i].pop(0))

    data = sorted(data, key=functools.cmp_to_key(sort_by_time_stamp))
    csv_file_name = csv_file_path.split(os.sep)[-1].split('.')[0]
    target_save_path = '..' + os.sep + 'sorted' + os.sep + mode
    write_to_csv(title, data, target_save_path, csv_file_name)


def rearrange_single_file(csv_file_path, save_dir):
    '''
    re-arrange the csv files according to the frame_id instead of track_id
    added features on May 25, 2020:
        combine the pedestrian information and vehicle information into one sorted csv file
        the input "csv_file_path" is only the vehicle track file, need to find correponding pedestrian file
    '''
    title, data = load_csv(csv_file_path)
    ''' find the corresponding pedestrian csv file '''
    pedestrian_csv_file = os.path.dirname(csv_file_path)+os.sep+'pedestrian_tracks_'+os.path.basename(csv_file_path).split('_')[-1]
    
    if os.path.exists(pedestrian_csv_file):
        title_ped, data_ped = load_csv(pedestrian_csv_file)
        ''' merge pedestrian and vehicle tracks into data '''
        data = data + data_ped

    title.insert(2, title.pop(0))

    for i in range(len(data)):
        data[i].insert(2, data[i].pop(0))

    data = sorted(data, key=functools.cmp_to_key(sort_by_time_stamp_single))
    # csv_file_name = csv_file_path.lstrip('..' + os.sep).split(os.sep)[-1].split('.')[0]
    csv_file_name = 'tracks_'+os.path.basename(csv_file_path)[:-4].split('_')[-1]
    target_save_path = save_dir
    write_to_csv(title, data, target_save_path, csv_file_name)
    return target_save_path + os.sep + csv_file_name + ".csv"


def main(train_set_dir, val_set_dir):

    if not os.path.exists(train_set_dir) and os.path.exists(val_set_dir):
        print("ERROR: Target Dir Does Not Exist")
        return

    train_csv_list = os.listdir(os.getcwd() + train_set_dir)
    val_csv_list = os.listdir(os.getcwd() + val_set_dir)

    i = 0
    for train in train_csv_list:
        rearrange(train_set_dir + os.sep + train, mode='train')
        i += 1
        print("\rProgress: {:>4}/{:>4}".format(i, len(train_csv_list)), end='')
    i = 0
    for val in val_csv_list:
        rearrange(val_set_dir + os.sep + val, mode='validation')
        i += 1
        print("\rProgress: {:>4}/{:>4}".format(i, len(val_csv_list)), end='')


if __name__ == '__main__':

    command = sys.argv[1]

    if command.lower() == 'default':

        if len(sys.argv) != 4:
            train_set = os.sep + 'merged' + os.sep + 'train'
            val_set = os.sep + 'merged' + os.sep + 'validation'
        else:
            train_set = sys.argv[2]
            val_set = sys.argv[3]
        main(train_set, val_set)

    elif command.lower() == 'file':

        file_path = os.getcwd() + os.sep + sys.argv[2]
        save_dir = os.getcwd() + os.sep + sys.argv[3]

        if len(sys.argv) != 4:
            print("ERROR: Invalid Arguments. Usage: ./python time_stamp_rearrange.py file csv_file_path save_dir")
        elif not os.path.exists(file_path):
            print("ERROR: Target csv file does not exist.")
        else:
            rearrange_single_file(file_path, save_dir)

    elif command.lower() == 'dir':
        file_dir = os.getcwd() + os.sep + sys.argv[2]
        save_dir = os.getcwd() + os.sep + sys.argv[3]

        if len(sys.argv) != 4:
            print("ERROR: Invalid Arguments. Usage: ./python time_stamp_rearrange.py file csv_file_path save_dir")
        elif not os.path.exists(file_dir):
            print("ERROR: Target csv file does not exist.")
        else:
            csv_list = os.listdir(file_dir)
            i = 0
            for file in csv_list:
                pdb.set_trace()
                rearrange_single_file(file_dir + os.sep + file, save_dir)
                i += 1
                print("\rProgress: {:>4}/{:>4}".format(i, len(csv_list)), end='')



