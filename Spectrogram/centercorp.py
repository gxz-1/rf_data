from PIL import Image

def center_crop_image(input_image_path, output_image_path, crop_size=(500, 500)):
    """
    中心裁剪图像并保存
    Args:
        input_image_path (str): 输入图像路径
        output_image_path (str): 输出图像路径
        crop_size (tuple): 裁剪大小，默认是 (500, 500)
    """
    with Image.open(input_image_path) as img:
        width, height = img.size
        new_width, new_height = crop_size

        # 计算中心裁剪区域的左、上、右、下坐标
        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2

        # 裁剪图像
        cropped_img = img.crop((left, top, right, bottom))
        # 保存裁剪后的图像
        cropped_img.save(output_image_path)
        print(f"图片已成功裁剪并保存为：{output_image_path}")

# 使用示例
input_path = "/disk/datasets/rf_data/Spectrogram/dataset/大疆精灵/a/1.png"  # 替换为你的输入图片路径
output_path = "/disk/datasets/rf_data/Spectrogram/dataset/大疆精灵/a/1c.png"  # 替换为你的输出图片路径
center_crop_image(input_path, output_path)
