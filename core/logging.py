import os
from datetime import datetime
from typing import Literal, Optional
import inspect

LogLevel = Literal['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR']


class Logger:
    def __init__(self, module: str):
        self.module = module
        self.log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
        os.makedirs(self.log_dir, exist_ok=True)

    def _log(self, level: LogLevel, message: str) -> None:
        stack = inspect.stack()
        frame = stack[2] if len(stack) > 2 else stack[1]
        source = os.path.splitext(os.path.basename(frame.filename))[0]
        if 'self' in frame.frame.f_locals:
            class_name = type(frame.frame.f_locals['self']).__name__
        else:
            class_name = frame.function
        now = datetime.now()
        timestamp = now.strftime('%Y.%m.%d.%H:%M:%S.%f')[:-3]
        log_line = f"[{timestamp}] [{self.module}/{level}] [{source}/{class_name}]: {message}\n"
        log_file = os.path.join(self.log_dir, now.strftime('%Y-%m-%d.log'))
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)

    def trace(self, message: str) -> None:
        self._log('TRACE', message)

    def debug(self, message: str) -> None:
        self._log('DEBUG', message)

    def info(self, message: str) -> None:
        self._log('INFO', message)

    def warn(self, message: str) -> None:
        self._log('WARN', message)

    def error(self, message: str) -> None:
        self._log('ERROR', message)

# 简单测试代码
if __name__ == '__main__':
    logger = Logger('test')
    logger.debug('Logger 测试日志')
    logger.info('Logger Info 日志')
    logger.warn('Logger Warn 日志')
    logger.error('Logger Error 日志')
