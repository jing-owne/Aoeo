# -*- coding: utf-8 -*-

import yaml
from typing import Dict, Any, Optional
from Logger import EnhancedLogger


class ConfigYaml:
    """配置文件处理器（支持YAML）"""
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.cached_data: Optional[Dict[str, Any]] = None
        self.logger = EnhancedLogger()  # 初始化日志

    def load_yaml(
        self,
        file_path: Optional[str] = None,
        encoding: str = 'utf-8'
        # use_cache: bool = True  # 貌似没用到
    ) -> Dict[str, Any]:
        """
        读取YAML文件并返回字典
        :param file_path: 文件路径（优先用方法参数）
        :param encoding: 文件编码
        # :param use_cache: 是否使用缓存
        :return: 字典格式的配置数据
        """
        target_path = file_path or self.file_path
        if not target_path:
            raise ValueError("YAML文件路径未提供")

        # if use_cache and self.cached_data is not None:
        #     logger.info(f'使用缓存读取YAML文件: {target_path}')
        #     return self.cached_data

        try:
            with open(target_path, 'r', encoding=encoding) as f:
                config_data = yaml.safe_load(f) or {}

            if not isinstance(config_data, dict):
                raise ValueError("YAML内容必须为字典结构")

            self.cached_data = config_data  # 更新缓存
            self.logger.info(f'成功读取YAML文件: {target_path}')
            return config_data

        except FileNotFoundError:
            err_msg = f"文件不存在: {target_path}"
            self.logger.error(err_msg)
            raise
        except yaml.YAMLError as err:
            err_msg = f"YAML解析失败: {str(err)}"
            self.logger.error(err_msg)
            raise ValueError(err_msg)
        except Exception as err:
            self.logger.error(f"读取YAML异常: {str(err)}")
            raise

# 使用示例
if __name__ == '__main__':
    config = ConfigYaml("../config/test_data.yaml")  # 假设文件存在

    try:
        data = config.load_yaml()
        EnhancedLogger().info(f'数据库地址: {data}')
        print("数据库地址:", data.get('database'))
        print("port打印结果:", data.get('database', {}).get('port'))



    except Exception as e:
        print("配置加载失败:", str(e))