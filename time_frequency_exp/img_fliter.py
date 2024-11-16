from PIL import Image, ImageFilter


index=2
img = Image.open("time_frequency_exp/{}.png".format(index))

# 1.应用高斯滤波，radius 控制模糊程度
# gaussian_filtered = img.filter(ImageFilter.GaussianBlur(radius=2))
# gaussian_filtered.save("time_frequency_exp/{}_filtered.png".format(index))
# 2.应用中值滤波，size 决定滤波窗口的大小
# median_filtered = img.filter(ImageFilter.MedianFilter(size=5))
# median_filtered.save("time_frequency_exp/{}_filtered.png".format(index))
# 3.应用均值滤波
# mean_filtered = img.filter(ImageFilter.BoxBlur(radius=2))
# mean_filtered.save("time_frequency_exp/{}_filtered.png".format(index))


