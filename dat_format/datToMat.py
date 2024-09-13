import os
import numpy as np
import scipy.io as io
import hdf5storage
directory= r'/home/lbt/dataset/dat_format/USRP/DDC/PCIE7'

datList=[]
for root, dirs, files in os.walk(directory):
    for file_name in files:
    	#  文件绝对路径
        file_path = os.path.join(root, file_name)
        print(file_path)

        # 读取原始IQ数据文件
        data = np.fromfile(file_path, dtype=np.uint32)

        # 调整字节顺序和位顺序
        data = np.flip(data.view(dtype=np.uint8).reshape(-1, 4), axis=1)

        # 复制数据以确保C连续顺序存储
        data = np.copy(data)

        # 提取I/Q数据并转换为有符号整数
        iq_data = data.view(dtype=np.int16).reshape(-1, 2)
        datList.append(iq_data)
        s = len(iq_data)
        print("hello", s)
# 合并所有dat数据
t=datList[0]
for i in range(len(datList)-1):
    t=np.vstack((t,datList[i+1]))
print("t 合并后的长度len:",len(t)," shape:",t.shape)
iq_data=t
# 将iq数据组合成复数
complex_numbers = iq_data[:, 0] + 1j * iq_data[:, 1]
print(type(complex_numbers))
# 将复数向量按每4096行组合成一个向量
allLen=len(complex_numbers)
print(allLen)
standard=allLen-allLen%4096
print("截断后的长度（能被4096整除）：",standard)
vectorized_array = complex_numbers[:standard].reshape(-1, 4096)

# 输出最终的二维数组大小
print("最终的二维数组大小：", vectorized_array.shape)
print("查看第几个数：",vectorized_array[0][0])
# 将数据保存到新文件PCIE4.mat
output_file_path = "/home/lbt/dataset/origin_data_lpf20240304/origin/PCIE7.mat"


hdf5storage.savemat(output_file_path,{'data':vectorized_array},format='7.3')

# hdf5storage.write(vectorized_array,output_file_path, matlab_compatible=True)
