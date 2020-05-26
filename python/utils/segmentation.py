import os
import csv
import sys
import functools
import pdb

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


def cmp_track_id(id_1, id_2):

    if id_1.isdigit() and id_2.isdigit():
        if int(id_1) < int(id_2):
            return -1
        elif int(id_1) == int(id_2):
            return 0
        else:
            return 1

    file_id_1 = id_1.split('-')[0]
    track_id_1 = int(id_1.split('-')[1])
    file_id_2 = id_2.split('-')[0]
    track_id_2 = int(id_2.split('-')[1])

    if file_id_1 < file_id_2:
        return -1
    elif file_id_1 == file_id_2:
        if track_id_1 < track_id_2:
            return -1
        elif track_id_1 == track_id_2:
            return 0
    return 1


def all_vehicles(csv_data):
    title = csv_data[0]
    data = csv_data[1]

    track_id_index = title.index('track_id')
    ret = set()

    for line in data:
        track = line[track_id_index]
        # pdb.set_trace()
        if track[0] != 'P':
            ret.add(track)

    return sorted(list(ret), key=functools.cmp_to_key(cmp_track_id))


def write_segs_to_csv(csv_writer, seg_list):
    for block in seg_list:
        for line in block:
            csv_writer.writerow(line)


def segmentation(csv_data, block_length=40, gap_between_seg=20, csv_path='', mode='', dir_name=''):
    title = csv_data[0]
    data = csv_data[1]
    vehicles_list = all_vehicles(csv_data)
    cur_start_frame = 0

    new_title = title.copy()
    new_title.insert(3, 'agent_role')

    csv_name = csv_path.split(os.sep)[-1]
    save_dir = os.path.dirname(os.path.dirname(csv_path)) + os.sep + 'segmented'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    save_path = save_dir + os.sep + csv_name

    out_csv = open(save_path, 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(out_csv)
    csv_writer.writerow(new_title)

    # all_segs = []
    vehicle_count = 0

    for vehicle in vehicles_list:
        for i in range(len(data)):
            if data[i][2] == vehicle:
                if data[i][0].isdigit():
                    cur_start_frame = int(data[i][0])
                else:
                    cur_start_frame = int(data[i][0].split('-')[1])
                break

        end_of_vehicle = False
        while not end_of_vehicle:

            cur_line = 0
            for i in range(len(data)):
                if data[i][0].isdigit():
                    frame_id = int(data[i][0])
                else:
                    frame_id = int(data[i][0].split('-')[1])
                if frame_id == cur_start_frame:
                    cur_line = i
                    break

            segment = []
            block = []
            agent_flag = False
            cur_frame = cur_start_frame
            block_count = 0
            for i in range(cur_line, len(data)):
                if data[i][0].isdigit():
                    frame_id = int(data[i][0])
                else:
                    frame_id = int(data[i][0].split('-')[1])

                if (frame_id != cur_frame) and agent_flag:
                    segment.append(block)
                    block_count += 1
                    if block_count >= block_length:
                        break
                    block = []
                    cur_frame = frame_id
                    agent_flag = False
                elif frame_id != cur_frame:
                    end_of_vehicle = True
                    break

                if data[i][2] == vehicle:
                    agent_flag = True
                    new_line = data[i].copy()
                    new_line.insert(3, 'agent')
                else:
                    new_line = data[i].copy()
                    new_line.insert(3, 'others')

                block.append(new_line)
            # vehicle_segs.append(segment)
            write_segs_to_csv(csv_writer, segment)
            cur_start_frame += gap_between_seg
        # all_segs.append(vehicle_segs)
        vehicle_count += 1
        print("\r\tAgent Vehicle {:>5}/{:>5}".format(vehicle_count, len(vehicles_list)), end='')
    print()


def single_file(csv_file_path, block_length=40, gap_between_seg=20, dir_path=''):
    csv_data = load_csv(csv_file_path)
    file_name = csv_file_path.split(os.sep)[-1]
    segmentation(csv_data, block_length, gap_between_seg, csv_file_path, 'single', dir_name=dir_path)


def main(train_set_dir, val_set_dir, block_length=40, gap_between_seg=20):

    if not (os.path.exists(train_set_dir) and os.path.exists(val_set_dir)):
        print("ERROR: Target Dir Does Not Exist")
        return

    train_csv_list = os.listdir(train_set_dir)
    val_csv_list = os.listdir(val_set_dir)

    print("Start")
    i = 0
    for train in train_csv_list:
        i += 1
        print("Progress (Training Set): {:>4}/{:>4}".format(i, len(train_set_dir)))
        if os.path.splitext(train)[1] != '.csv':
            continue
        csv_data = load_csv(train_set_dir + os.sep + train)
        segmentation(csv_data, int(block_length), int(gap_between_seg), train, 'train')
    print()
    i = 0
    for val in val_csv_list:
        i += 1
        print("\nProgress (Validation Set): {:>4}/{:>4}".format(i, len(val_csv_list)))
        if os.path.splitext(val)[1] != '.csv':
            continue
        csv_data = load_csv(val_set_dir + os.sep + val)
        segmentation(csv_data, int(block_length), int(gap_between_seg), val, 'validation')


if __name__ == '__main__':
    # single_file(sys.argv[3], int(sys.argv[1]), int(sys.argv[2]))

    if len(sys.argv) != 5:
        train_dir = 'sorted_set' + os.sep + 'train'
        val_dir = 'sorted_set' + os.sep + 'validation'
        main(train_dir, val_dir, int(sys.argv[1]), int(sys.argv[2]))
    else:
        main(sys.argv[3], sys.argv[4], int(sys.argv[1]), int(sys.argv[2]))
