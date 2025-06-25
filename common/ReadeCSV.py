# -*- coding: utf-8 -*-

"""
        读取CSV文件内容，打印运行中产生的日志
"""

import csv
from Logger import EnhancedLogger
# 先创建实例，再调用方法
logger = EnhancedLogger()  # 实例化


class CSVReader:
    def __init__(self):
        self.columns = []

    def read_csv(self, file_path, mode='all', target=None):
        """
        读取CSV文件的多功能方法
        :param file_path: 文件路径
        :param mode: 模式选择（'row'按行，'col'按列，'cell'按单元格，'all'全数据）
        :param target: 目标参数（行号/列名/元组（行号,列名））
        """
        data = []

        with open(file_path, 'r', encoding='GBK') as csvfile:
            reader = csv.reader(csvfile)
            self.columns = next(reader)  # 获取标题行

            if mode == 'col':
                # 按列读取（支持列名或列索引）
                col_index = self._get_column_index(target)
                data = [row[col_index] for row in reader]
            elif mode == 'row':
                # 按行读取（支持绝对行号或相对偏移）
                data = self._get_specific_row(reader, target)
            elif mode == 'cell':
                # 按单元格读取（行号+列名）
                row_data = self._get_specific_row(reader, target[0])
                col_index = self._get_column_index(target[1])
                data = row_data[col_index] if row_data else None
            elif mode == 'all':
                # 全数据转换为字典列表
                data = [dict(zip(self.columns, row)) for row in reader]
        return data

    def _get_column_index(self, target):
        """验证列名或列索引是否存在"""

        if isinstance(target, int) and 0 <= target < len(self.columns):
            return target  # 支持数字索引
        elif isinstance(target, str) and target in self.columns:
            return self.columns.index(target)  # 支持列名
        else:
            raise ValueError(f"列名或索引不存在: {target}")


    def _get_specific_row(self, reader, row_number):
        """获取特定行（从0开始计数）"""
        for idx, row in enumerate(reader):
            if idx == row_number:
                return row
        raise IndexError(f"行号超出范围，文件总行数: {idx + 1}")


if __name__ == '__main__':
    reader = CSVReader()
    # 读取整列（支持列名或索引）
    column_data = reader.read_csv('../config/Https.csv', mode='col', target='method')


