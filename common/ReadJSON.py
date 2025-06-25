# -*- coding: utf-8 -*-

import json
from typing import Dict, Any, Optional
from Logger import EnhancedLogger

class ConfigJSON:
    """配置文件处理器（支持JSON）"""

    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.cached_data: Optional[Dict[str, Any]] = None
        self.logger = EnhancedLogger()  # 初始化日志

    def load_json(
            self,
            file_path: Optional[str] = None,
            encoding: str = 'utf-8',
            use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        读取JSON文件并返回字典
        :param file_path: 文件路径（优先用方法参数）
        :param encoding: 文件编码
        :param use_cache: 是否使用缓存
        :return: 字典格式的配置数据
        """
        target_path = file_path or self.file_path
        if not target_path:
            self.logger.info(f'JSON文件路径未提供: {target_path}')
            raise ValueError("JSON文件路径未提供")

        if use_cache and self.cached_data is not None:
            self.logger.info(f'使用缓存读取JSON文件: {target_path}')
            return self.cached_data

        try:
            with open(target_path, 'r', encoding=encoding) as f:
                config_data = json.load(f)  # 核心解析方法

            if not isinstance(config_data, dict):
                raise ValueError("JSON内容必须为字典结构")

            self.cached_data = config_data  # 更新缓存
            self.logger.info(f'成功读取JSON文件: {target_path}')
            return config_data

        except FileNotFoundError:
            err_msg = f"文件不存在: {target_path}"
            self.logger.error(err_msg)
            raise
        except json.JSONDecodeError as e:
            err_msg = f"JSON解析失败: {str(e)}"
            self.logger.error(err_msg)
            raise ValueError(err_msg)
        except Exception as e:
            self.logger.error(f"读取JSON异常: {str(e)}")
            raise


# 使用示例
if __name__ == '__main__':
    config = ConfigJSON("../config/data.json")  # 假设文件存在

    try:
        data = config.load_json()
        print("API密钥:", data.get('courses', {}))

        # print("API密钥:", data.get('courses', {}).get('key'))
        # 若JSON内容为：
        # {
        #   "api": {"key": "abc123", "url": "https://api.example.com"},
        #   "debug_mode": true
        # }
        # 输出: API密钥: abc123
    except Exception as e:
        print("配置加载失败:", str(e))