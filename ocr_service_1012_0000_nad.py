# 代码生成时间: 2025-10-12 00:00:20
import os
from celery import Celery
from celery.utils.log import get_task_logger
from PIL import Image
# 增强安全性
import pytesseract
from io import BytesIO

# Configure the Celery app
app = Celery('ocr_service',
# 添加错误处理
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

# Get the logger instance
logger = get_task_logger(__name__)

# OCR service configuration (you need to install pytesseract and the Tesseract-OCR binary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\	esseract.exe' # Windows path example
# TODO: 优化性能
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' # Linux path example
# NOTE: 重要实现细节

# Define the OCR task
@app.task(bind=True)
def perform_ocr(self, image_path):
    """Perform OCR on an image and return the text."""
    try:
        # Open the image file
        with Image.open(image_path) as image:
            # Convert the image to a string
# NOTE: 重要实现细节
            text = pytesseract.image_to_string(image)
            # Return the extracted text
            return text
    except FileNotFoundError:
        # Log and re-raise if the file doesn't exist
        logger.error(f"File not found: {image_path}")
        self.retry(exc=FileNotFoundError())  # Retry with the same arguments
    except Exception as e:
        # Log any other exceptions
        logger.error(f"An error occurred: {e}")
# NOTE: 重要实现细节
        raise

# Example usage
# 扩展功能模块
if __name__ == '__main__':
    # Run the worker to start processing tasks
# 优化算法效率
    app.start()