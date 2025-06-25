# -*- coding:utf-8 -*-
"""
    日志模块，打印运行中产生的日志*
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional


class EnhancedLogger:
    _instance: Optional['EnhancedLogger'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # 基础配置
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # 避免重复日志（关键修复点[1,6](@ref)）
        self.logger.propagate = False

        # 初始化处理器
        self._init_handlers()

    def _init_handlers(self):
        """配置多级别分流处理器"""
        # 调试日志处理器（按大小轮转[2,6](@ref)）
        debug_handler = RotatingFileHandler(
            filename='../logs/projectLog.log',
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.addFilter(lambda record: record.levelno <= logging.INFO)

        # 错误日志处理器
        error_handler = RotatingFileHandler(
            filename='../logs/errorLog.log',
            maxBytes=2 * 1024 * 1024,  # 2MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)

        # 严重错误专用处理器
        critical_handler = RotatingFileHandler(
            filename='../logs/criticalLog.log',
            maxBytes=1 * 1024 * 1024,  # 1MB
            backupCount=1,
            encoding='utf-8'
        )
        critical_handler.setLevel(logging.CRITICAL)

        # 控制台处理器（生产环境可关闭[1,7](@ref)）
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # 统一格式化（增强可读性[3,7](@ref)）
        formatter = logging.Formatter(
            '%(asctime)s - [%(filename)s:%(lineno)d] - %(name)s - %(levelname)s - %(message)s'
        )

        # 绑定格式化器
        for handler in [debug_handler, error_handler, critical_handler, console_handler]:
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    # 封装日志方法
    def debug(self, msg: str):
        self.logger.debug(msg)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str, exc_info: bool = True):
        self.logger.error(msg, exc_info=exc_info)

    def critical(self, msg: str):
        self.logger.critical(msg)
        # 严重错误触发通知（可扩展）
        # self._send_alert(msg)


# 使用示例
if __name__ == '__main__':
    logger = EnhancedLogger()

    logger.debug("调试信息")
    logger.info("状态信息")
    logger.warning("警告信息")
    logger.error("错误发生", exc_info=True)
    logger.critical("系统崩溃")
