import numpy as np
import matplotlib.pyplot as plt
import pywt
import cv2

# 读取图像（确保将路径替换为您实际的图像路径）
image = cv2.imread('time_frequency_exp/a10.bmp', cv2.IMREAD_GRAYSCALE)

# 定义一个函数，用于使用DWT进行图像压缩
def dwt_compression(image, threshold):
    # 对图像进行二维离散小波变换
    coeffs = pywt.wavedec2(image, 'haar', level=4)
    
    # 对小波系数进行阈值处理
    coeffs_thresholded = [coeffs[0]]  # 保留低频部分
    # 对每个高频细节层次（水平、垂直、对角）应用阈值处理，确保每组保持为三元组格式
    for detail_level in coeffs[1:]:
        thresholded_level = tuple(pywt.threshold(c, threshold, mode='soft') for c in detail_level)
        coeffs_thresholded.append(thresholded_level)
    
    # 重构图像，使用二维逆小波变换，指定母小波为Haar，与DWT分解时一致
    compressed_image = pywt.waverec2(coeffs_thresholded, 'haar')
    return compressed_image

# 设置阈值并压缩图像
threshold_value = 30  # 压缩时的阈值
compressed_image = dwt_compression(image, threshold_value)

# 对图像进行归一化处理以便显示
compressed_image = np.clip(compressed_image, 0, 255).astype(np.uint8)

# 绘制原始图像和压缩后的图像
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("orgin")
plt.imshow(image, cmap='gray')  # 显示原始图像
plt.axis('off')  # 关闭坐标轴

plt.subplot(1, 2, 2)
plt.title("compress")
plt.imshow(compressed_image, cmap='gray')  # 显示压缩后的图像
plt.axis('off')  # 关闭坐标轴

plt.savefig('time_frequency_exp/img_compress.png')  # 保存图像
plt.close() 
