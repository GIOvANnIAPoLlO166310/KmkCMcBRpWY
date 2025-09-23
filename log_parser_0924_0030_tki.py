# 代码生成时间: 2025-09-24 00:30:55
import os
import re
from celery import Celery
from celery.utils.log import get_task_logger

# 配置Celery
app = Celery('log_parser',
             broker='pyamqp://guest@localhost//')
app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# 获取Celery的日志记录器
log = get_task_logger(__name__)

# 定义日志行的正则表达式模式
LOG_PATTERN = r'\[(.*?)\] (.*?): (.*)'

# 日志文件解析函数
def parse_log_line(line):
    """解析单个日志行。"""
    try:
        # 使用正则表达式匹配日志行
        match = re.match(LOG_PATTERN, line)
        if match:
            # 返回匹配的组
            return {"timestamp": match.group(1),
                    "level": match.group(2),
                    "message": match.group(3)}
        else:
            # 如果行不匹配模式，则返回None
            return None
    except Exception as e:
        # 记录任何异常
        log.error(f'Error parsing log line: {e}')
        return None

# 定义Celery任务
@app.task
def parse_log_file(file_path):
    """解析整个日志文件。"""
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f'File {file_path} does not exist.')

        logs = []
        with open(file_path, 'r') as file:
            for line in file:
                log_line = parse_log_line(line.strip())
                if log_line:
                    logs.append(log_line)

        return logs
    except FileNotFoundError as e:
        log.error(f'File not found: {e}')
        return []
    except Exception as e:
        log.error(f'An error occurred while parsing the file: {e}')
        return []

# 如果作为主程序运行，则测试日志文件解析
if __name__ == '__main__':
    # 测试文件路径（需要根据实际情况修改）
    test_file_path = 'path_to_log_file.log'
    results = parse_log_file.apply_async(args=[test_file_path])
    print(f'Tasks started: {results.id}')
