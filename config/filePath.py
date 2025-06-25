# -*- coding:utf-8 -*-
import os

# 获取根目录项目的os.path.dir_name(目录)获取目录的上一级目录
dir_path = os.path.dirname(os.path.dirname(__file__))


# 用个字典存储路径特殊文件的路径
def file_paths():
    paths = {
        'test_data.yaml': os.path.join(dir_path, 'data', 'test_data.yaml'),
        'environment.xml': os.path.join(dir_path, 'configurations', 'environment.xml'),
        'config.ini': os.path.join(dir_path, 'configurations', 'config.ini'),
        'testcase': os.path.join(dir_path, 'testcase'),
        'allure_data': os.path.join(dir_path, 'report', 'allure_data'),
        'public_key': os.path.join(dir_path, 'handlers', 'handler_encryption', 'publicKeyStr.pem'),
        'private_key': os.path.join(dir_path, 'handlers', 'handler_encryption', 'privateKeyStr.pem')
    }

    return paths

    # if __name__ == '__main__':
    # 调用函数并接收返回的字典
    # paths_dict = file_paths()
    # 打印根目录项目路径
    # print("项目根目录路径:", dir_path)
    # 遍历字典并打印每个文件的路径
    # for filename, filepath in paths_dict.items():
    #     print(f"{filename} 的路径为: {filepath}")
