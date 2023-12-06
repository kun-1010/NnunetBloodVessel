import os
import shutil
import random
'''
    划分训练集和验证集
'''
# 定义源路径和目标路径
src_path = r"F:\DATA\blood-vessel-segmentation\train"
dst_input_path = r"F:\DATA\blood-vessel-segmentation\test\input"
dst_output_path = r"F:\DATA\blood-vessel-segmentation\test\output"

# 读取input文件夹中的所有文件
input_files = os.listdir(os.path.join(src_path, "input"))

# 对于每个前缀，随机选择10%的文件进行移动
for prefix in set([file.split("_")[0] for file in input_files]):
    files_with_prefix = [file for file in input_files if file.startswith(prefix)]

    # 随机选择10%的文件
    num_files_to_move = int(len(files_with_prefix) * 0.1)
    files_to_move = random.sample(files_with_prefix, num_files_to_move)


    # 移动文件
    for file in files_to_move:
        input_file_path = os.path.join(src_path, "input", file)
        output_file_path = os.path.join(src_path, "output", file)

        dst_input_file_path = os.path.join(dst_input_path, file)
        dst_output_file_path = os.path.join(dst_output_path, file)

        shutil.move(input_file_path, dst_input_file_path)
        shutil.move(output_file_path, dst_output_file_path)