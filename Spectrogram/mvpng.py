import os
import shutil

def merge_and_rename_directories(base_dir):
    signal_type_map = {"大信号": "大", "中信号": "中", "小信号": "小"}
    
    for category in os.listdir(base_dir):
        category_path = os.path.join(base_dir, category)
        if os.path.isdir(category_path):
            merged_dirs = {"大": [], "中": [], "小": []}
            
            # Step 1: 合并并重命名第二级目录
            for signal_type in os.listdir(category_path):
                signal_path = os.path.join(category_path, signal_type)
                if os.path.isdir(signal_path):
                    for key, new_name in signal_type_map.items():
                        if key in signal_type:
                            merged_dirs[new_name].append(signal_path)
                            break

            # 创建新的目录并合并内容
            for new_name, paths in merged_dirs.items():
                if paths:
                    merged_path = os.path.join(category_path, new_name)
                    if not os.path.exists(merged_path):
                        os.makedirs(merged_path)
                    for path in paths:
                        for item in os.listdir(path):
                            item_path = os.path.join(path, item)
                            target_path = os.path.join(merged_path, item)
                            if os.path.isdir(item_path):
                                shutil.move(item_path, merged_path)
                            else:
                                # 处理文件名冲突
                                counter = 1
                                while os.path.exists(target_path):
                                    name, ext = os.path.splitext(item)
                                    target_path = os.path.join(merged_path, f"{name}_{counter}{ext}")
                                    counter += 1
                                shutil.move(item_path, target_path)
                        shutil.rmtree(path)  # 删除原文件夹

            # Step 2: 移动“时间”子文件夹中的png文件
            for signal_folder in os.listdir(category_path):
                signal_folder_path = os.path.join(category_path, signal_folder)
                if os.path.isdir(signal_folder_path):
                    png_counter = 1  # 用于给每个png文件命名
                    for time_folder in os.listdir(signal_folder_path):
                        time_folder_path = os.path.join(signal_folder_path, time_folder)
                        if os.path.isdir(time_folder_path):
                            png_files = [f for f in os.listdir(time_folder_path) if f.endswith('.png')]
                            for png_file in png_files:
                                src_path = os.path.join(time_folder_path, png_file)
                                dst_path = os.path.join(signal_folder_path, f"{png_counter}.png")
                                shutil.move(src_path, dst_path)
                                png_counter += 1
                            shutil.rmtree(time_folder_path)  # 删除“时间”子文件夹

# 运行脚本
base_directory = "/disk/datasets/rf_data/Spectrogram/dataset"
merge_and_rename_directories(base_directory)
