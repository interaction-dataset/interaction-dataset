import os
import sys
import csv
import shutil

def read_validation_list(list_file_path):

    full_text = open(list_file_path).read()
    full_blocks = full_text.split("\n\n")

    ret = dict()

    for block in full_blocks:
        lines = block.split("\n")
        target_dir = lines[0].strip().strip('\n').strip()

        val_set = set()
        for i in range(1, len(lines)):
            val_set.add(lines[i].strip().strip('\n').strip().split('_')[-1])
        ret[target_dir] = val_set

    return ret

def split_files_into_folders(folder_dir, val_set_dict):
    csv_file_list = os.listdir(folder_dir)
    if len(csv_file_list) == 0:
        print("ERROR: no file is found under {}".format(folder_dir))
        return

    train_folder_flag = 0
    val_folder_flag = 0
    val_path = folder_dir+os.sep+'val'
    train_path = folder_dir+os.sep+'train'
    for csv_file in csv_file_list:
        if os.path.splitext(csv_file)[1] != '.csv':
            continue
        file_name = os.path.basename(csv_file)[:-4]
        if file_name.split('_')[-1] in val_set_dict[folder_dir.split(os.sep)[-1]]:
            if not os.path.exists(val_path) and not val_folder_flag:
                os.mkdir(val_path)
                val_folder_flag = 1
            shutil.move(folder_dir+os.sep+csv_file, val_path+os.sep+csv_file)
        else:
            if not os.path.exists(train_path) and not train_folder_flag:
                os.mkdir(train_path)
                train_folder_flag = 1
            shutil.move(folder_dir+os.sep+csv_file, train_path+os.sep+csv_file)
                

def import_train_val_set(val_set_dict, dataset_dir):

    data_dir_list = [f.path for f in os.scandir(dataset_dir) if (f.is_dir() and f.name[0:2]=='DR')]
    if len(data_dir_list) == 0:
        print("ERROR: Cannot find folder starting with DR_ under the given path\n")
        return 

    progress = 0
    for folder in data_dir_list:
        split_files_into_folders(folder, val_set_dict)
        progress += 1
        print("\rProgress: {}/{}".format(progress, len(data_dir_list)), end='')


def main(scenario_path='', instruction_file='', argc=3):
    instruction_type = instruction_file.strip().split(os.sep)[-1].split('.')[1]
    error_str = ''
    if argc != 3:
        error_str += "ERROR: Invalid usage\n"
        error_str += "Usage: ./python split_train_val.py instruction_file(.txt) scenario_path\n"
    if not os.path.isdir(scenario_path):
        error_str += "ERROR: Cannot find the target scenario folder\n"
    if not os.path.isfile(instruction_file):
        error_str += "ERROR: Cannot find the target instruction file\n"
    if not instruction_type == 'txt':
        error_str += "ERROR: Invalid instruction file type. Should be .txt\n"

    if error_str != '':
        print(error_str)
        return

    print("Split Training and Validation Sets")
    val_set_dict = read_validation_list(instruction_file)
    import_train_val_set(val_set_dict, scenario_path)
    print("\nDONE")


if __name__ == '__main__':
    instruction = sys.argv[1]
    path_to_record_files = sys.argv[2]
    argv_len = len(sys.argv)
    main(scenario_path=path_to_record_files, instruction_file=instruction, argc=argv_len)
