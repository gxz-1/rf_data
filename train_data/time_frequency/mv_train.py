import os
import shutil

# 定义源文件路径（文件已存在的路径）
source_path = '/disk/datasets/rf_data/train_data/time_frequency/train'

# 定义设备类别
devices = [-1,4, 5, 6, 7]


# 为每个设备创建一个子文件夹
for device in devices:
    device_folder = os.path.join(source_path, f'device_{device}')
    if not os.path.exists(device_folder):
        os.makedirs(device_folder)  # 如果文件夹不存在，创建它

# 遍历 source_path 中的所有文件
for filename in os.listdir(source_path):
    source_file = os.path.join(source_path, filename)
    # 检查文件是否为普通文件（跳过目录）
    if not os.path.isfile(source_file):
        continue
    # 检查文件是否包含设备编号
    for device in devices:
        if f'device_{device}_' in filename:
            # 找到相应设备的文件并移动到对应子文件夹
            source_file = os.path.join(source_path, filename)
            destination_folder = os.path.join(source_path, f'device_{device}')
            destination_file = os.path.join(destination_folder, filename)
            
            # 移动文件到对应的子文件夹
            shutil.move(source_file, destination_file)
            print(f"已将文件 {filename} 移动到 {destination_folder}")


