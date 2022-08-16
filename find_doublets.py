import hashlib
import json
import os
import platform
import sys

from tqdm import tqdm

DIR = os.path.abspath(os.path.join(__file__, os.pardir))

def calc_md5(filename):
    with open(filename,"rb") as f:
        bytes = f.read() # read file as bytes
        readable_hash = hashlib.md5(bytes).hexdigest();
        return readable_hash


def find_duplicates(folder_path):
    files_md5 = {}
    print("Compute md5 sums for files in %s" % folder_path)
    for filename in tqdm(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            md5sum = calc_md5(file_path)
            if files_md5.get(md5sum):
                files_md5[md5sum].append(file_path)
            else:
                files_md5[md5sum] = [file_path]
        

    md5_path = os.path.join(folder_path, 'files_md5.json')
    print("Save files md5 to %s" % md5_path)
    with open(md5_path, "w") as fp:
        json.dump(files_md5, fp)

    files_to_keep = []
    files_to_delete = []
    print("Find files to keep and delete")
    for md5sum, filepaths in tqdm(files_md5.items()):
        files_to_keep.append(filepaths[0])
        files_to_delete += filepaths[1:]

    keep_path = os.path.join(folder_path, 'keep.json')
    print("Save files to keep: %s" % keep_path)
    with open(keep_path, "w") as fp:
        json.dump(files_to_keep, fp)

    delete_path = os.path.join(folder_path, 'delete.json')
    print("Save files to delete: %s" % delete_path)
    with open(delete_path, "w") as fp:
        json.dump(files_to_delete, fp)


if __name__ == "__main__": 
    for folder_path in sys.argv[1:]:
        if os.path.isdir(folder_path):
            find_duplicates(folder_path)
        else:
            print("Skipped %s" % folder_path)


