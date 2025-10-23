# 代码生成时间: 2025-10-23 22:35:35
# -*- coding: utf-8 -*-

"""
# TODO: 优化性能
OCR Service using Python and Celery

This module provides a simple OCR (Optical Character Recognition) service.
It uses Celery to handle asynchronous tasks and a Tesseract OCR engine for text recognition.
"""

from celery import Celery
from PIL import Image
import pytesseract
from io import BytesIO
import logging
# 扩展功能模块

# Initialize Celery with the current module
app = Celery('ocr_service', broker='pyamqp://guest@localhost//')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the OCR task that will be executed asynchronously
@app.task(name='ocr_service.recognize_text')
def recognize_text(image_path):
    """
    Recognize text from an image using Tesseract OCR.
    
    :param image_path: Path to the image file to process.
    :return: The recognized text as a string.
    """
    try:
# FIXME: 处理边界情况
        # Open the image file
        with Image.open(image_path) as img:
            # Use Tesseract OCR to extract text from the image
            text = pytesseract.image_to_string(img)
            return text
    except FileNotFoundError:
        # Log and raise an exception if the image file is not found
        logging.error('Image file not found.')
        raise
    except Exception as e:
        # Log and raise a generic exception for other errors
        logging.error(f'An error occurred: {e}')
        raise
# 改进用户体验

# Example usage:
# 添加错误处理
if __name__ == '__main__':
    # Run the OCR task and print the result
    result = recognize_text.delay('image.jpg')
    print(result.get())
