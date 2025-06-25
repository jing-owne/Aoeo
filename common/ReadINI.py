# -*- coding: utf-8 -*-

from configparser import ConfigParser
from typing import Dict, Any, Optional
from Logger import EnhancedLogger


class ConfigINI:
    """INI 配置文件处理器（支持读取/写入/缓存）"""

    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.cached_data: Optional[Dict[str, Any]] = None
        self.parser = ConfigParser()
        self.logger = EnhancedLogger()

    def load_ini(
            self,
            file_path: Optional[str] = None,
            encoding: str = 'utf-8',
            use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        读取 INI 文件并返回字典
        :param file_path: 文件路径（优先使用方法参数，其次实例属性）
        :param encoding: 文件编码
        :param use_cache: 是否使用缓存
        :return: 嵌套字典格式的配置数据
        """
        target_path = file_path or self.file_path
        if not target_path:
            raise ValueError("INI 文件路径未提供")

        if use_cache and self.cached_data is not None:
            self.logger.info(f'使用缓存读取INI文件: {target_path}')
            return self.cached_data

        try:
            self.parser.clear()
            # 关键修复：正确检查文件是否存在
            read_result = self.parser.read(target_path, encoding=encoding)
            if not read_result:
                raise FileNotFoundError(f"文件不存在或无法读取: {target_path}")

            # 转换为嵌套字典
            config_data = {
                section: dict(self.parser.items(section))
                for section in self.parser.sections()
            }
            self.cached_data = config_data  # 仅在成功时更新缓存
            self.logger.info(f'成功读取INI文件: {target_path}')
            return config_data

        except UnicodeDecodeError as e:
            self.logger.error(f'编码错误: {target_path} - {str(e)}')
            raise
        except Exception as e:
            self.logger.error(f'读取INI文件失败: {str(e)}')
            raise



# # 使用示例（修正路径） 单独调试
# if __name__ == '__main__':
#     config_handler = ConfigINI("../config/setting.ini")  # 修复路径
#
#     try:
#         data = config_handler.load_ini()
#         print("读取结果:", data)
#         logger.info(f'读取结果: {data}')

        # # 提取 database 配置
        # database_config = data.get('Database', {})
        # host = database_config.get('mysql_host')
        # port = database_config.get('mysql_port')

        # print(f"数据库地址: {host}:{port}")  # 输出: 数据库地址: localhost:3306



    # except Exception as e:
    #     print(f"配置加载失败: {str(e)}")