# 代码生成时间: 2025-10-13 02:17:19
from celery import Celery
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import requests

# Celery configuration
app = Celery('code_highlighter', broker='pyamqp://guest@localhost//')

@app.task
def highlight_code(code, language):
    '''
    Celery task to highlight code using Pygments.

    :param code: The source code to be highlighted.
    :param language: The programming language of the code.
    :return: HTML formatted highlighted code.
    '''
    try:
        # Get the lexer for the specified language
        lexer = get_lexer_by_name(language)
        # Create a formatter to output HTML with line numbers
        formatter = HtmlFormatter()
        # Highlight the code and return the result
        return highlight(code, lexer, formatter)
    except Exception as e:
        # Handle any exceptions that occur during highlighting
        return f"Error highlighting code: {str(e)}"

# Example usage of the highlight_code task
if __name__ == '__main__':
    highlight_result = highlight_code.delay("print('Hello, World!')", 'python')
    print('Highlighted Code:', highlight_result.get())
