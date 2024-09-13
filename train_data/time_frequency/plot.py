import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft
from scipy.fft import fft
from matplotlib.font_manager import FontProperties

# 设置字体
font_prop = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')  # 确认字体路径

# 生成一维信号（频率随时间变化的正弦波）
fs = 1000  # 采样频率（Hz）
T = 1.0    # 信号持续时间（秒）
t = np.linspace(0, T, int(T * fs), endpoint=False)  # 时间轴
x = np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 100 * t * t)  # 生成的信号

# 添加高斯白噪声
noise = np.random.normal(0, 0.5, x.shape)  # 标准差为0.5的高斯白噪声
x_noisy = x + noise

# 计算信号功率和噪声功率 (功率定义为信号振幅的平方的平均值)
signal_power = np.mean(x ** 2)  # 原始信号功率
noise_power = np.mean(noise ** 2)  # 噪声功率

# 计算信噪比（SNR），以dB为单位
snr = 10 * np.log10(signal_power / noise_power)
print(f"SNR: {snr:.2f} dB")

# 计算时频图 (STFT)
f, t_stft, Zxx = stft(x_noisy, fs=fs, nperseg=256)  # 使用含噪声的信号计算
# nperseg：STFT的时间分辨率和频率分辨率依赖于窗口的大小。窗口越宽，频率分辨率越高，但时间分辨率越低

# 计算频谱图 (FFT)
X_f = fft(x_noisy)
freqs = np.fft.fftfreq(len(X_f), 1/fs)

# 绘制时域图、时频图、频谱图对比
plt.figure(figsize=(18, 6))

# 时域图
plt.subplot(1, 3, 1)
plt.plot(t, x_noisy)
plt.title('时域图', fontproperties=font_prop)  # 使用支持中文的字体
plt.ylabel('幅值', fontproperties=font_prop)
plt.xlabel('时间 [s]', fontproperties=font_prop)

# 时频图
plt.subplot(1, 3, 2)
plt.pcolormesh(t_stft, f, np.abs(Zxx), shading='gouraud')
plt.title('STFT 时频图', fontproperties=font_prop)  # 使用支持中文的字体
plt.ylabel('频率 [Hz]', fontproperties=font_prop)
plt.xlabel('时间 [s]', fontproperties=font_prop)
cbar = plt.colorbar()
cbar.set_label('幅值', fontproperties=font_prop)

# 在时频图上添加信噪比文本
plt.text(0.95, 0.05, f'SNR: {snr:.2f} dB', fontsize=12, ha='right', va='bottom', transform=plt.gca().transAxes, fontproperties=font_prop)

# 频谱图
plt.subplot(1, 3, 3)
plt.plot(freqs[:len(freqs)//2], np.abs(X_f[:len(X_f)//2]))
plt.title('FFT 频谱图', fontproperties=font_prop)
plt.ylabel('幅值', fontproperties=font_prop)
plt.xlabel('频率 [Hz]', fontproperties=font_prop)

# 保存图片而不是展示
plt.tight_layout()
plt.savefig('stft_fft_time_domain_comparison_with_noise.png')
plt.close()  # 关闭绘图窗口
