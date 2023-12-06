import os
import shutil
import random
'''
    给文件加前缀，并转移到指定文件夹等待划分训练集和验证集
'''
def process_folder(root_dir, input_folder_name='input', output_folder_name='output'):
    # 获取当前目录下所有的子文件夹
    folders = os.listdir(root_dir)

    # 创建input和output文件夹
    input_folder = os.path.join(root_dir, input_folder_name)
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    output_folder = os.path.join(root_dir, output_folder_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_count = 0
    label_count = 0

    for folder in folders:
        if folder.startswith('.'):
            continue
        images_folder = os.path.join(root_dir, folder, 'images')
        labels_folder = os.path.join(root_dir, folder, 'labels')
        if not os.path.exists(images_folder) or not os.path.exists(labels_folder):
            continue

        # 遍历images和labels文件夹中的文件
        for root, dirs, files in os.walk(images_folder):
            for file in files:
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(input_folder, f'{folder}_{file}')
                shutil.copy(old_file_path, new_file_path)
                image_count += 1

        for root, dirs, files in os.walk(labels_folder):
            for file in files:
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(output_folder, f'{folder}_{file}')
                shutil.copy(old_file_path, new_file_path)
                label_count += 1

    print(f'Transferred {image_count} images and {label_count} labels.')


# 调用函数处理train和test文件夹
process_folder(r"F:\DATA\blood-vessel-segmentation\train")

