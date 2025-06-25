import os, sys
sys.path.append(os.getcwd())
import allure
import pytest,os
from common.Logger import logger
from utils.httpclient import RestClient
from common.read_data import ReadFileData

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
yaml_path = os.path.join(BASE_DIR, 'data','test_data.yaml')
read_ymal = ReadFileData().load_yaml(yaml_path)

re = RestClient('https://fanyi.baidu.com')
class TestQuery:
    @pytest.mark.parametrize('udate', read_ymal)
    def test_query(self, udate):
        logger.info(f'开始执行{udate["name"]}用例')
        data = udate['data']
        base_url = udate['baseurl']
        res = re.post(base_url,json=data)
        assert res['msg'] == udate['except']
        logger.info('结束执行用例\n\n')

    # def test_dog(self):
    #     logger.info('开始执行第二条用例')
    #     data = {'query':'dog'}
    #     res = re.post('/langdetect',json=data)
    #     assert res['msg'] == 'ee'
    #     logger.info('结束执行用例\n\n')
    #
    # def test_tiger(self):
    #     logger.info('开始执行第三条用例')
    #     data = {'query':'tiger'}
    #     res = re.post('/langdetect',json=data)
    #     assert res['msg'] == 'success'
    #     logger.info('结束执行用例')
    # def test_banana(self):
    #     logger.info('开始执行第四条用例')
    #     data = {'query':'banana'}
    #     res = re.post('/langdetect',json=data)
    #     assert res['msg'] == 'success'
    #     logger.info('结束执行用例')
    # def test_train(self):
    #     logger.info('开始执行第五条用例')
    #     data = {'query':'train'}
    #     res = re.post('/langdetect',json=data)
    #     assert res['msg'] == 'success'
    #     logger.info('结束执行用例')

if __name__ == '__main__':
    pytest.main(['-s', '-q', 'test_query.py'])

