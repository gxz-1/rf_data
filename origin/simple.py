import pandas as pd
import numpy as np
import hdf5storage
# import 将origin_USRP0326文件夹下所有4开头的mat文件（1行4096列）合并为一个mat文件

file_path_prefix = "origin/PCIE7.mat"
new_file_path_prefix = "origin/PCIE7_simple.mat"

print('--------------------------------------------------')
print('切片采样开始！')
print('--------------------------------------------------')

# 加载原始MAT文件
origin_data = hdf5storage.loadmat(file_path_prefix)['data']

print('--------------------------------------------------')
print('每隔3w行取2w行，切片8w行，采样8000行')
print('--------------------------------------------------')
print('原始数据长度：',origin_data.shape)
print('原始数据每隔50000行数据：',origin_data[::50000][:3]) 

# 分段取数据
segments = []
for i in range(4):
    segment = origin_data[i*20000 + i*30000 : (i+1)*20000 + i*30000]
    segments.append(segment)

# 合并四个段的数据
segments = pd.DataFrame(np.reshape(segments,(80000,4096)))
merged_data = pd.concat([segments], ignore_index = True)

print('--------------------------------------------------')
print('切片数据长度：',merged_data.shape)
print('切片数据每隔20000行数据：',merged_data[::20000][:3])
print('若以上两组数据一致，则切片成功！')

print('切片数据每隔10行数据：',merged_data[::10][:3])

# 采样数据
sampled_data = merged_data.iloc[::10]#每隔10行选取一行，每行4096个数据，因此实际每隔40960个数据取4096个数据

print('--------------------------------------------------')
print('采样数据长度：',sampled_data.shape)
print('采样数据前3行数据：',sampled_data[:3])
print('若以上两组数据一致，则采样成功！')

# 保存最终数据到新的MAT文件
hdf5storage.savemat(new_file_path_prefix, {'data': sampled_data.values})
print('--------------------------------------------------')
print('切片采样结束！')
print('--------------------------------------------------')