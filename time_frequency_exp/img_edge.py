import cv2
import numpy as np

# 读取图像并转换为灰度
index=3
image = cv2.imread("time_frequency_exp/{}.png".format(index), cv2.IMREAD_GRAYSCALE)

# 使用 Sobel 算子计算垂直方向的梯度
sobel_x = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

# 计算梯度的绝对值并转换为8位图像（用于显示或叠加回原图）
sobel_x_abs = cv2.convertScaleAbs(sobel_x)

# 增强效果：将水平边缘增强叠加回原图
enhanced_image = cv2.addWeighted(image, 1, sobel_x_abs, 1, 0)
sobel_x_abs
# 保存增强后的图像
cv2.imwrite("time_frequency_exp/{}_enhanced.png".format(index), sobel_x_abs)

# 显示原图和增强后的图像
cv2.imshow("Original Image", image)
cv2.imshow("Horizontal Edges Enhanced", enhanced_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
