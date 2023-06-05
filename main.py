import json
import os
import sys
import threading
import time

from queue import Queue, Empty


BASE_DIR = os.path.dirname(sys.argv[0])

JSON_PATH = os.path.join(BASE_DIR, 'files_found.json')

SCAN_PATH = r'C:\Users\dp2\Documents\projects\rename_pdb\images'


files_scanned = 0
matching_files = 0
scanning = False


def gather_files():
    global files_scanned
    global matching_files
    global scanning

    scanning = True

    output = Output()
    output.start()

    files_found = []

    for root, dirs, files in os.walk(SCAN_PATH):
        for file in files:
            if os.path.splitext(file)[1] == '.pdb':
                files_found.append(os.path.join(root, file))
                matching_files += 1
            files_scanned += 1

    scanning = False
    output.join()

    return files_found


def rename(file_path):
    path_without_pdb = os.path.splitext(file_path)[0]
    if os.path.isfile(path_without_pdb):
        file_root, ext = os.path.splitext(path_without_pdb)
        i = 1
        while True:
            new_path = f'{file_root}-{i}{ext}'
            if os.path.isfile(new_path):
                i += 1
            else:
                break
        os.rename(file_path, new_path)


class Output(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        start = time.time()
        while scanning:
            print(f'{time.time() - start} | {matching_files} / {files_scanned}')
            time.sleep(1)



if __name__ == '__main__':
    files_found = gather_files()

    print(files_found)

    with open(JSON_PATH, 'w+') as outfile:
        json.dump(files_found, outfile, indent=2) 

    text = input(f'Rename {len(files_found)} files? ')
    if len(text) > 0 and text[0].lower() == 'y':
        for file in files_found:
            rename(file)