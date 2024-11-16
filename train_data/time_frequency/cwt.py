# https://pywavelets.readthedocs.io/en/latest/ref/cwt.html#

import numpy as np
import matplotlib.pyplot as plt
import pywt
import scipy.io

# 加载数据
data = scipy.io.loadmat('signal.mat')
data_signal = data['data_signal'].flatten()

# 设置参数
sampling_rate = 4e6  # 4 MHz
dt = 1 / sampling_rate
scales = np.linspace(1, 512, num=100)  # 选择合适的尺度范围
wavelet_types = ['cmor1.5-1.0', 'gaus1']  # 可选的母小波
# import pywt
# pywt.wavelist('coif')
# ['coif1', 'coif2', 'coif3', 'coif4', 'coif5', 'coif6', 'coif7', ...
# pywt.wavelist(kind='continuous')
# ['cgau1', 'cgau2', 'cgau3', 'cgau4', 'cgau5', 'cgau6', 'cgau7', ...

# 选择母小波
wavelet = pywt.ContinuousWavelet(wavelet_types[0])

# 连续小波变换
coefficients, frequencies = pywt.cwt(data_signal, scales, wavelet, sampling_period=dt)
# 根据scales对频率进行缩放 sampling_rate/scales ，生成不同尺度（频率）下的波形
# coefficients:（len(data_signal)*len(scales)） 
# frequencies: 每个尺度相对应的频率值
print(coefficients.shape)
print(frequencies)
# 绘制时频图
plt.figure(figsize=(12, 6))
plt.yscale('log')
plt.imshow(np.abs(coefficients), extent=[0, len(data_signal) * dt,  frequencies[-1], frequencies[0]], aspect='auto', cmap='jet')
# 设置色条与标签
plt.colorbar(label='Magnitude')
# 标题和坐标轴标签
plt.title(f'CWT Time-Frequency using {wavelet_types[0]} wavelet')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.grid()

# 保存图像到当前目录
plt.savefig('CWT_time_frequency.png', bbox_inches='tight')
plt.close()  # 关闭图像，释放内存
