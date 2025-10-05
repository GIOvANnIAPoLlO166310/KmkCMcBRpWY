# 代码生成时间: 2025-10-06 01:44:25
# watermake_daemon.py

"""
数字水印技术实现，使用CELERY框架进行异步处理
"""

import os
from celery import Celery
from dotenv import load_dotenv
import cv2
# NOTE: 重要实现细节
import numpy as np
import base64
from cryptography.fernet import Fernet

# 载入环境变量
load_dotenv()

app = Celery('watermake_daemon', broker='pyamqp://guest@localhost//')
# FIXME: 处理边界情况
app.conf.task_routes = {'watermake_daemon.embed_watermark': 'embed_watermark_queue'}
# NOTE: 重要实现细节

# 密钥生成
def generate_key():
    return Fernet.generate_key()

# 加密
# TODO: 优化性能
def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode())

# 解密
def decrypt_message(encrypted, key):
    f = Fernet(key)
    return f.decrypt(encrypted).decode()
# TODO: 优化性能

@app.task(name='watermake_daemon.embed_watermark', queue='embed_watermark_queue')
def embed_watermark(image_path, watermark_text, key):
# FIXME: 处理边界情况
    """
# 添加错误处理
    嵌入水印到图片中
# 添加错误处理
    :param image_path: 要加水印的图片路径
    :param watermark_text: 水印文本
# NOTE: 重要实现细节
    :param key: 加密钥
    """
    try:
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"无法找到文件：{image_path}")

        # 将文本水印加密
        encrypted_text = encrypt_message(watermark_text, key)

        # 将加密文本转换为二进制数据
        watermark_binary = encrypted_text.encode('utf-8')
# 改进用户体验

        # 将二进制数据嵌入到图片的最低位
# 扩展功能模块
        watermarked_image = np.copy(image)
        for i in range(len(watermark_binary)):
            watermarked_image[i, :, :] = np.bitwise_xor(watermarked_image[i, :, :], np.array([int(watermark_binary[i])] * image.shape[1] * 3, dtype=np.uint8))

        # 保存加水印后的图片
        watermarked_image_path = f"{os.path.splitext(image_path)[0]}_watermarked.jpg"
        cv2.imwrite(watermarked_image_path, watermarked_image)

        return {"status": "success", "message": f"Watermark embedded successfully. Saved to {watermarked_image_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.task(name='watermake_daemon.extract_watermark', queue='extract_watermark_queue')
def extract_watermark(image_path, key):
# 添加错误处理
    """
    从图片中提取水印
    :param image_path: 要提取水印的图片路径
    :param key: 加密钥
    """
    try:
# 添加错误处理
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"无法找到文件：{image_path}")

        # 提取最低位作为二进制数据
        watermark_binary = ''
        for i in range(len(image)):
            binary_str = ''.join(['1' if pixel == 255 else '0' for pixel in image[i, :, :].flatten()])
            watermark_binary += binary_str

        # 将二进制数据转换回文本
        watermark_text = decrypt_message(watermark_binary, key)

        return {"status": "success", "message": watermark_text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
