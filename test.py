from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import logging

logging.disable(logging.DEBUG)  # 关闭DEBUG日志的打印
logging.disable(logging.WARNING)  # 关闭WARNING日志的打印

# 初始化 PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch",debug=False)  # 使用中文模型，可根据需求更改为其他语言 (如 "en")

def ocr_test(image_path):
    """
    使用 PaddleOCR 识别图片中的文字，并将结果整理为字符串。
    
    参数:
        image_path (str): 图片文件的路径。
    
    返回:
        str: 提取并整理后的文字内容。
    """
    try:
        # 打开图片并转换为 numpy 数组
        image = Image.open(image_path)
        img_array = np.array(image)

        # 使用 PaddleOCR 进行文字识别
        result = ocr.ocr(img_array, cls=True)  # cls=True 表示启用文本方向分类

        print("OCR 原始结果:", result)

        # 提取文字内容并拼接为字符串
        extracted_text = "".join([item[1][0] for sublist in result for item in sublist])

        return extracted_text

    except Exception as e:
        print(f"OCR 错误: {str(e)}")
        return "OCR 提取失败，请检查图片内容"

# 测试代码

if __name__ == "__main__":
    # 指定图片路径
    image_path = "/Users/limo/Documents/作文1.jpeg"  # 替换为您的图片路径

    # 调用 OCR 测试函数
    text = ocr_test(image_path)

    # 输出提取的文字内容
    print("\n提取的文字内容:")
    print(text)
