import os
import sys
import csv

from utils import time_rearrange
from utils import segmentation


default_header = ['track_id', 'frame_id', 'timestamp_ms', 'agent_type', 'x', 'y', 'vx', 'vy', 'psi_rad', 'length', 'width']


def time_stamp_rearrange(train_set_dir, val_set_dir):

    if not os.path.exists(train_set_dir) and os.path.exists(val_set_dir):
        print("ERROR: Target Dir Does Not Exist")
        return

    train_csv_list = os.listdir(train_set_dir)
    val_csv_list = os.listdir(val_set_dir)

    i = 0
    print("Sort Training Set")
    for train in train_csv_list:
        i += 1
        print("\rProgress: {:>4}/{:>4}".format(i, len(train_csv_list)), end='')
        if os.path.splitext(train)[1] != '.csv':
            continue
        if not csv_header_check(train_set_dir + os.sep + train):
            print("ERROR: csv header does not match the standard header => " + train_set_dir + os.sep + train)
            continue
        time_rearrange.rearrange(train_set_dir + os.sep + train, mode='train')
    i = 0
    print("\nSort Validation Set")
    for val in val_csv_list:
        i += 1
        print("\rProgress: {:>4}/{:>4}".format(i, len(val_csv_list)), end='')
        if os.path.splitext(val)[1] != '.csv':
            continue
        if not csv_header_check(val_set_dir + os.sep + val):
            print("ERROR: csv header does not match the standard header => " + train_set_dir + os.sep + val)
            continue
        time_rearrange.rearrange(val_set_dir + os.sep + val, mode='validation')


def csv_header_check(csv_file_path):
    data_file = csv.reader(open(csv_file_path, 'r'))
    title = []

    for line in data_file:
        title = line
        break

    if len(title) != len(default_header):
        return False

    for i in range(len(title)):
        if title[i] != default_header[i]:
            return False

    return True


def main(command='default', file_path='', block_len=40, gap_between_seg=20, argc=0):

    if command.lower() == 'default':
        data_dir_list = [f.path for f in os.scandir(file_path) if (f.is_dir() and f.name[0:2]=='DR')]
        if len(data_dir_list) == 0:
            print("ERROR: Cannot find folder starting with DR_ under the given path\n")
            return 

        progress = 0
        print("Start\n")
        for folder in data_dir_list:
            main(command='dir', block_len=block_len, gap_between_seg=gap_len, argc=argv_len, file_path=folder)
            progress += 1
            print("Handling folder {}\n".format(os.path.basename(folder)))


    elif command.lower() == 'file':
        '''
        Single File Mode:
        command = file
        Usage: ./python segment_data.py file csv_file_path block_length gap_length
        '''
        #  = argv[2]
        # save_dir = argv[3]

        if os.path.splitext(file_path)[1] != '.csv':
            print("ERROR: Invalid file format. Must be .csv")
            return

        if argc < 4:
            print("ERROR: Invalid Arguments. Usage: ./python segment_data.py file csv_file_path block_length gap_length")
        elif not os.path.exists(file_path):
            print("ERROR: Target csv file does not exist.")
        elif not csv_header_check(file_path):
            print("ERROR: csv header does not match the standard header")
        else:
            sorted_file = time_rearrange.rearrange_single_file(file_path, os.path.dirname(file_path)+os.sep+ 'sorted')
            segmentation.single_file(sorted_file, block_len, gap_between_seg)

    elif command.lower() == 'dir':
        '''
        Directory Mode
        command = dir
        Usage: Usage: ./python segment_data.py dir csv_file_path block_length gap_length
        '''

        if argc < 4:
            print("ERROR: Invalid Arguments. Usage: ./python segment_data.py dir input_dir block_length gap_length")
        elif not os.path.exists(file_path):
            print("ERROR: Target folder does not exist.")
        else:
            csv_list = [f.path for f in os.scandir(file_path) if f.is_file() and os.path.basename(f)[-4:] == '.csv' and os.path.basename(f).split('_')[0] == 'vehicle']
            
            if len(csv_list) == 0:
                print("No csv file found in "+file_path+', trying to check train and val folders...\n')
                if os.path.exists(file_path+os.sep+'train'):
                    print('Train folder is found\n')
                    main(command='dir', block_len=block_len, gap_between_seg=gap_len, argc=argv_len, file_path=file_path+os.sep+'train')
                if os.path.exists(file_path+os.sep+'val'):
                    print('Train folder is found\n')
                    main(command='dir', block_len=block_len, gap_between_seg=gap_len, argc=argv_len, file_path=file_path+os.sep+'val')
                if not os.path.exists(file_path+os.sep+'train') and not os.path.exists(file_path+os.sep+'val'):
                    print('No csv files or train or val folders have been found\n')
                    return
            
            else:
                i = 0
                for file in csv_list:
                    i += 1
                    print("\tProgress: {:>4}/{:>4}".format(i, len(csv_list)), end='')
                    if not csv_header_check(file):
                        print("ERROR: csv header does not match the standard header => " + file)
                        continue
                    sorted_file = time_rearrange.rearrange_single_file(file, os.path.dirname(file)+os.sep+'sorted')
                    segmentation.single_file(sorted_file, block_len, gap_between_seg, file_path)

    else:
        print("ERROR: Invalid command. Use 'default', 'file', or 'dir'")


if __name__ == '__main__':
    command = sys.argv[1]

    if command == 'file' or command == 'dir' or command == 'default':
        file_path = sys.argv[2]
        block_len = int(sys.argv[3])
        gap_len = int(sys.argv[4])
        argv_len = len(sys.argv)
        main(command=command, block_len=block_len, gap_between_seg=gap_len, argc=argv_len, file_path=file_path)
    else:
        argv_len = len(sys.argv)
        main(command=command, argc=argv_len)
