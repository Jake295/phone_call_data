import os
import random
from datetime import datetime
from datetime import timedelta

phone_calls_dict = {}


def create_dev_set(full_data_dir, dev_data_dir, ratio=10):
    os.makedirs(dev_data_dir, exist_ok=True)
    for file_name in sorted(os.listdir(full_data_dir)):
        with open(f'{full_data_dir}/{file_name}') as file_full,\
                open(f'{dev_data_dir}/{file_name}', 'w') as file_dev:
            for line in file_full:
                rand_num = random.randint(0, 100)
                if rand_num < ratio:
                    file_dev.write(line)


def load_phone_calls_dict(data_dir):

    for phone_call_file in os.listdir(data_dir):
        full_path = os.path.join(data_dir, phone_call_file)
        with open(full_path, 'r') as file:
            for line in file:
                timestamp, phone_number = line.strip().split(": ", 1)  

                area_code = phone_number[3:6]
                
                if area_code not in phone_calls_dict:
                    phone_calls_dict[area_code] = {}

                if phone_number not in phone_calls_dict[area_code]:
                    phone_calls_dict[area_code][phone_number] = []

                dt_object = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

                if dt_object.hour >= 0 and dt_object.hour < 6:
                    phone_calls_dict[area_code][phone_number].append(dt_object)
    return phone_calls_dict


def generate_phone_call_counts(phone_calls_dict):
    phone_call_counts = {}
    for area_code in phone_calls_dict:
        for phone_number in phone_calls_dict[area_code]:
            phone_call_counts[phone_number] = len(phone_calls_dict[area_code][phone_number])
        
    return phone_call_counts


def most_frequently_called(phone_call_counts, top_n=10):
    most_frequently_called = []
    for phone_number in phone_call_counts:
        most_frequently_called.append((phone_number, phone_call_counts[phone_number]))

    most_frequently_called.sort(key=lambda x: (-x[1], x[0]))

    return most_frequently_called[:top_n]


def export_phone_call_counts(most_frequent_list, out_file_path):
    with open(out_file_path, 'w') as output_file:
        for phone_number, count in most_frequent_list:
            output_file.write(f'{phone_number}: {count}\n')


def format_time_diff(t1, t2):
    diff = t2 - t1
    mins, secs = divmod(diff.seconds, 60)
    hours, mins = divmod(mins, 60)
    return f'{str(mins).zfill(2)}:{str(secs).zfill(2)}'


def export_redials_report(phone_calls_dict, report_dir='reports'):
    os.makedirs(report_dir, exist_ok=True)

    for area_code, phone_numbers in phone_calls_dict.items():
        redials = []
        for phone_number, calls in phone_numbers.items():
            calls.sort()

            for i in range(len(calls) - 1):
                t1 = calls[i]
                t2 = calls[i + 1]

                if t2 - t1 <= timedelta(minutes = 10):
                    diff_str = format_time_diff(t1, t2)
                    t1_str = t1.strftime('%Y-%m-%d %H:%M:%S')
                    t2_str = t2.strftime('%H:%M:%S')
                    redials.append(f'{phone_number}: {t1_str} -> {t2_str} ({diff_str})')
        
        with open(f'{report_dir}/{area_code}.txt', 'w') as output_file:
            if redials:
                for redial in redials:
                    output_file.write(f'{redial}\n')    
