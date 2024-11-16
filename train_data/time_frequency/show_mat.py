import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np
"""
读取mat数据保存时频图
"""
def show_spectrogram(matPath, title="Spectrogram"):
    # 读取保存的时频数据
    mat_data = sio.loadmat(matPath)
    # 提取 Pxx, freqs, bins 数据
    Pxx = mat_data['Pxx']
    freqs = mat_data['freqs'][0]  # freqs 和 bins 是列向量，所以提取一维数组
    bins = mat_data['bins'][0]
    # print(Pxx)
    # 时频图
    plt.figure(figsize=(10, 5))
    plt.pcolormesh(bins, freqs, 10 * np.log10(Pxx), shading='gouraud') #将功率谱密度值转换为 dB 以便更好地展示
    plt.colorbar(label='dB')
    plt.title(f"{title} - Spectrogram")
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.savefig(title.replace('.mat','_spectrogram.png'))
    plt.close()  # 关闭图形以释放内存

    # 频域图（功率谱密度）
    freqs_shifted = np.fft.fftshift(freqs)# 使用 np.fft.fftshift 重新排列频率，确保负频率在左，正频率在右
    Pxx_shifted = np.fft.fftshift(Pxx, axes=0)  # 对Pxx按频率轴重排
    
    # 频域图（功率谱密度） 
    plt.figure(figsize=(10, 5))
    plt.plot(freqs_shifted, 10 * np.log10(np.mean(Pxx_shifted, axis=1)))  # 平均功率谱密度
    plt.title(f"{title} - Frequency Domain")
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Power/Frequency [dB/Hz]')
    plt.savefig(title.replace('.mat','_frequency_domain.png'))
    plt.close()

#保存一张时频图 频域图
save_train_path = '/disk/datasets/rf_data/train_data/time_frequency/train/device_7'
save_test_path = '/disk/datasets/rf_data/train_data/time_frequency/val/snr_-10/device_6'
filename='device_6_snr_-10_sample_1000.mat'
show_spectrogram(save_test_path+'/'+filename,filename)