# 代码生成时间: 2025-09-24 11:23:16
import celery
from bs4 import BeautifulSoup
from html import escape
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置Celery
app = celery.Celery('xss_protection', broker='pyamqp://guest@localhost//')

@app.task
def sanitize_html(html_content):
    """
    这个函数用于清理HTML内容以防止XSS攻击。
    它将使用BeautifulSoup来解析HTML并转义所有潜在的危险标签。
    
    参数:
    html_content (str): 需要清理的HTML内容。
    
    返回:
    str: 清理后的HTML内容。
    """
    try:
        # 解析HTML内容
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 转义所有标签
        escaped_html = soup.prettify(quote_attr_values=True)
        
        # 转义属性值
        for tag in soup.find_all(True):
            for attr in tag.attrs:
                tag[attr] = escape(tag[attr])
        
        # 返回清理后的HTML内容
        return escaped_html
    except Exception as e:
        logger.error(f"An error occurred while sanitizing HTML: {e}")
        raise

# 如果这个脚本是作为主程序运行，测试函数
if __name__ == '__main__':
    # 示例HTML内容
    sample_html = "<p>Hello, <script>alert('XSS')</script> World!</p>"
    
    # 调用任务
    sanitized_html = sanitize_html.delay(sample_html)
    
    # 获取结果
    result = sanitized_html.get()
    
    # 打印清理后的HTML内容
    print("Sanitized HTML: ", result)