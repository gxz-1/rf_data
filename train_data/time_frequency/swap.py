import os
import shutil

# 定义源文件路径
source_path = '/disk/datasets/rf_data/train_data/time_frequency/val'

# 遍历所有 device_X 文件夹
for device_folder in os.listdir(source_path):
    device_path = os.path.join(source_path, device_folder)
    
    # 确保 device_X 是一个目录
    if os.path.isdir(device_path) and device_folder.startswith('device_'):
        # 遍历 device_X 目录中的 snr_Y 文件夹
        for snr_folder in os.listdir(device_path):
            snr_path = os.path.join(device_path, snr_folder)
            
            # 确保 snr_Y 是一个目录
            if os.path.isdir(snr_path) and snr_folder.startswith('snr_'):
                # 遍历 snr_Y 目录中的所有文件
                for filename in os.listdir(snr_path):
                    source_file = os.path.join(snr_path, filename)
                    
                    # 创建新的目录结构：snr_Y/device_X
                    new_snr_folder = os.path.join(source_path, snr_folder)
                    new_device_folder = os.path.join(new_snr_folder, device_folder)
                    
                    # 如果新的 snr_Y 文件夹不存在，则创建
                    if not os.path.exists(new_snr_folder):
                        os.makedirs(new_snr_folder)
                    
                    # 如果新的 device_X 文件夹不存在，则创建
                    if not os.path.exists(new_device_folder):
                        os.makedirs(new_device_folder)
                    
                    # 构建目标文件路径
                    destination_file = os.path.join(new_device_folder, filename)
                    
                    # 移动文件到新的文件夹结构
                    shutil.move(source_file, destination_file)
                    print(f"已将文件 {filename} 移动到 {destination_file}")
                
                # 如果 snr_Y 目录中的文件都已移动，删除空的 snr_Y 目录
                os.rmdir(snr_path)
        
        # 如果 device_X 目录已经空了，删除 device_X 目录
        os.rmdir(device_path)
