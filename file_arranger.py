import os
import shutil  

path      = "/home/opstree/python_folder/testfolder"
threshold = 3 

def get_folders_present(path):
    present_folders = []
    file_types      = {}
    files_present   = os.listdir(path)
    for file in files_present:
        filepath    = path + "/" + file
        if os.path.isdir(filepath):
            present_folders.append(file)
    return present_folders

def get_files(path):
    files_present = os.listdir(path)
    regularfiles  = []
    for file in files_present:
        filepath  = path + "/" + file
        if os.path.isfile(filepath):
            regularfiles.append(file)
    return regularfiles


def get_file_types(path):
    file_types = {}
    all_files  = []
    all_files  = all_files + get_files(path) + get_files(path + "/" + "others")
    for file in all_files:
        file   = (file.split("."))
        if len(file) == 2:
            if file[1] not in file_types:
                file_types[file[1]] = 1
            else :
                file_types[file[1]] = file_types[file[1]] + 1
    return file_types 


def create_folder(folder_name, path):
    present_folders = get_folders_present(path)
    folder_path     = path + '/' + folder_name
    if folder_name not in present_folders:
        os.mkdir(folder_path)


def move_files(source_folder_name, destination_folder_name, path):
    files = get_files(path + "/" +source_folder_name)
    for file in files:
        source_file_path      = path + "/" + source_folder_name + "/" + file
        destination_file_path = path + "/" + destination_folder_name + "/" + file
        shutil.move(source_file_path, destination_file_path)

def check_threshold_of_filetypes(threshold, path):
    file_types      = get_file_types(path)
    present_folders = get_folders_present(path)
    for exension in file_types:
        if file_types[exension] >= threshold :
            create_folder(exension, path)


def send_files_to_respective_folders(path):
    all_files       = get_files(path + "/" + "others")
    present_folders = get_folders_present(path)
    for file in all_files:
        file_name   = file
        file        = file.split(".")
        if len(file) == 2:
            if file[1] in present_folders:
                source_file      = path + "/" + "others" + "/" + file_name
                destination_file = path + "/" + file[1] + "/" +file_name
                shutil.move(source_file, destination_file)

def remove_folders(folder_name, path):
    move_files(folder_name, "others", path)
    os.rmdir(path + "/" + folder_name)

def remove_folders_with_files_less_than_threshold(path):
    present_folders = get_folders_present(path)
    for current_folder in present_folders:
        files_in_current_folder = get_files(path + "/" + current_folder)
        if len(files_in_current_folder) < threshold:
            remove_folders(current_folder, path)            

def main(path, threshold):
    create_folder("others", path)
    move_files("", "others", path)
    check_threshold_of_filetypes(threshold, path)
    send_files_to_respective_folders(path)
    # remove_folders_with_files_less_than_threshold(path)

main(path, threshold)
