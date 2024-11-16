import os
import hdf5storage
import matplotlib.pyplot as plt
import scipy.io as sio
from scipy.signal import spectrogram,get_window
from scipy.interpolate import RectBivariateSpline
import numpy as np

random_create =True
file_path="/disk/datasets/rf_data/origin/PCIE{}_simple.mat"
save_train_path = '/disk/datasets/rf_data/train_data/time_frequency/train'
save_test_path = '/disk/datasets/rf_data/train_data/time_frequency/val'

'''
加噪声
作用：为输入信号 x 添加高斯白噪声。
snr (信噪比)：根据给定的信噪比调整噪声强度。
返回值：加噪声后的信号。
'''
def wgn(x, snr):
    snr = 10**(snr/10.0)
    xpower = np.sum(x**2)/len(x)
    npower = xpower / snr
    return np.random.randn(len(x)) * np.sqrt(npower)+x

'''
作用：为每一行的 I/Q 数据添加噪声。通过 wgn 函数处理数据中的每一行，将结果堆叠成新的数据集 A_1。
返回值：带噪声的 I/Q 数据矩阵。
'''
def getwgn(A1, snr):
    rows, cols = A1.shape  # 获取 A1 的行和列
    A_1 = np.empty((rows, cols), dtype=complex)  # 预先分配空间
    for i in range(rows):
        A_11 = wgn(A1[i, :], snr)  # 加噪声
        A_1[i, :] = A_11  # 直接赋值到预分配的数组中
    return A_1


"""
处理8000行，每行4096个数据作为一个样本，生成时频数据并保存.
"""
def convertDP(finallydata, savePath, device, snr):
    if not os.path.exists(savePath):
        os.makedirs(savePath) 
    num_samples = finallydata.shape[0]
    # for i in range(num_samples):
    #     data=finallydata[i,:]  # 取第 i 行数据
    for i in range(0,num_samples,4):# 每次取4行数据
        if i + 4 > num_samples:
            break  # 确保不超过数据范围    
        data = finallydata[i:i+4, :].reshape(-1)  # 将 4 行 4096 个数据拼接为一维数组,作为一个样本
        # 生成时频图数据
        freqs, bins, Pxx = spectrogram(data, nperseg=244, noverlap=178, fs=1, window=get_window('hann', 244))  
        # freqs, bins, Pxx = spectrogram(data, nperseg=256, noverlap=128, fs=1)  # 生成时频图数据
        # print(Pxx.shape)
        # print(Pxx)
        '''
        NFFT=256：将数据划分为 256 点的 FFT 块。
        Fs=1：采样率，假设为 1（可根据需要调整）。
        noverlap=128：指定窗口重叠 128 个点。
        window=使用 Hann 窗口
        
        Pxx: 时频图的功率谱密度矩阵。
        freqs: 频率向量。 （复信号）长度=窗长nperseg
        bins: 时间向量。   长度由窗长nperseg和重叠长度noverlap决定
        '''
        # 裁剪至244*244
        # freqs=freqs[:244]
        # bins=bins[:244]
        # Pxx=Pxx[:244,:244]
        # 保存时频图数据为 .mat 文件
        filename = f"device_{device}_snr_{snr}_sample_{i}.mat"
        filepath = os.path.join(savePath, filename)
        sio.savemat(filepath, {'data':data,  'Pxx': Pxx, 'freqs': freqs, 'bins': bins})
        if i  % 100 == 0:
            print(f"已处理 {i}/{num_samples} 个样本")
    print(f"所有样本已处理并保存到: {savePath}")




if __name__ == "__main__":
    if random_create:
        splitData=np.random.randn(400, 4096) + 1j * np.random.randn(400, 4096)
        print("train shape :",splitData.shape)
        snr=-1
        splitData=splitData.copy()
        splitData=getwgn(splitData,snr)
        convertDP(splitData,save_train_path,-1,snr)
    else:
        for l in range(4, 8):
            originData = hdf5storage.loadmat(file_path.format(l))['data'] 
            # 3 7划分数据集
            rows=round(originData.shape[0]*0.7) 
            print('row=',rows," columns=",originData.shape[1])
            #1. 生成训练集
            splitData=originData[:rows]
            print("train shape :",splitData.shape)
            # 加入噪声
            snr=8
            trainData=splitData.copy()
            trainData=getwgn(trainData,snr)
            convertDP(trainData,save_train_path,l,snr)
            #2. 生成测试集
            # splitData=originData[rows:]
            # print("test shape :",splitData.shape)
            # #加入5-10db噪声
            # for snr in range(-10,-1):
            #     testData=splitData.copy()
            #     testData=getwgn(testData,snr)
            #     convertDP(testData,save_test_path,l,snr)