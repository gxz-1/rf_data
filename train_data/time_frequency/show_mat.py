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
    print(Pxx)
    #展示数据
    plt.figure(figsize=(10, 5))
    plt.pcolormesh(bins, freqs, 10 * np.log10(Pxx), shading='gouraud') #将功率谱密度值转换为 dB 以便更好地展示
    plt.colorbar(label='dB')
    plt.title(title)
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.savefig(title.replace('mat','png'))
    plt.close()  # 关闭图形以释放内存

#展示一张时频图
save_train_path = '/disk/datasets/rf_data/train_data/time_frequency/train/device_7'
save_test_path = '/disk/datasets/rf_data/train_data/time_frequency/val/snr_5/device_7'
filename='device_7_snr_8_sample_120.mat'
show_spectrogram(save_train_path+'/'+filename,filename)