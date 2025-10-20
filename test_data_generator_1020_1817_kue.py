# 代码生成时间: 2025-10-20 18:17:44
import os
from celery import Celery, Task
from datetime import datetime, timedelta
def generate_test_data():
    """
    生成测试数据
    
    这个函数生成一些随机的测试数据并返回。
    """
    # 生成随机数据
    data = {
        'id': datetime.now().strftime("%Y%m%d%H%M%S"),
        'timestamp': datetime.now(),
        'value': os.urandom(16).hex()  # 生成随机十六进制字符串
    }
    return data


class TestDataGeneratorTask(Task):
    """
    Celery任务类，用于生成测试数据。
    """
    def run(self):
        """
        执行任务，生成测试数据。
        
        如果有任何异常发生，它将捕获异常并打印错误信息。
        """
        try:
            # 调用函数生成测试数据
            data = generate_test_data()
            print("Generated test data: ", data)
            return data
        except Exception as e:
            # 打印错误信息
            print("Error generating test data: ", str(e))
            return None


# 配置Celery
app = Celery('test_data_generator',
             broker='amqp://guest@localhost//',
             backend='rpc://')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # 接受的内容类型
    result_serializer='json',  # 结果序列化类型
    timezone='UTC',
    enable_utc=True
)

app.task(base=TestDataGeneratorTask)(TestDataGeneratorTask)

if __name__ == '__main__':
    # 启动Celery worker
    app.start()