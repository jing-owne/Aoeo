import os
import requests
import json as complexjson
from testProject.common.logger import logg
from testProject.Reader.readData import read_File_Data, baseDir

# 读取ini文件
iniPath = os.path.join(baseDir, 'config', 'setting.ini')
iniData = read_File_Data().load_ini(iniPath)
# 直接从iniData字典中获取[pytest]部分的'test_paths'值
api_admin_url = iniData.get('host', {}).get('api_admin_url', [])


class RestClient(object):
    def __init__(self, url_path, api_admin_url):
        if api_admin_url is None:
            api_admin_url = iniData.get('host', {}).get('api_admin_url', '')
            print("api_admin_url is not find")
        if not api_admin_url:
            raise ValueError("api_admin_url不能为空")
        self.api_admin_url = api_admin_url
        self.session = requests.session()
        self.url = self.api_admin_url + url_path

    # Get请求
    def get(self, **kwargs):
        return self.request("GET", **kwargs)

    # Post请求
    def post(self, headers=None, data=None,  json=None, **kwargs):
        return self.request("POST", headers=headers, data=data, json=json, **kwargs)

    # PUT 请求
    def put(self, headers=None, data=None, json=None, **kwargs):
        return self.request("PUT", headers=headers, data=data, json=json,**kwargs)

    # Delete请求
    def delete(self, headers=None, **kwargs):
        return self.request("DELETE", headers=headers,  **kwargs)

    def request(self, method, url=None, headers=None, params=None, data=None, json=None, **kwargs):
        headers = kwargs.get("headers", {}) or headers or {}
        params = kwargs.get("params", {}) or params or {}
        files = kwargs.get("files", {})
        cookies = kwargs.get("cookies", {})
        if method == "GET":
            return self.session.get(self.url, **kwargs)

        if method == "POST":
            req = requests.post(self.url, data, json, **kwargs)
            return req.json()

        if method == "PUT":
            if json:
                # PUT 和 PATCH 中没有提供直接使用json参数的方法，因此需要用data来传入
                data = complexjson.dumps(json)
            return self.session.put(url or self.url, data or {}, **kwargs)
        if method == "DELETE":
            return self.session.delete(url or self.url, **kwargs)

    def request_log(self, url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None, **kwargs):
        logg.info(f"接口请求参数 ==>>\n method：{method},\nurl:{url} ,\n headers:{headers}, \ndata:{data},\n params:{params},"
                  f"files:\n{files}, \n json:{json}, \ncookies:{cookies}")


if __name__ == '__main__':
    urlPath = '/portal/grade/listUser'
    re = RestClient(urlPath, api_admin_url)
    print(api_admin_url)

    # 此处尝试通过cev读取
    # payload = {
    #     'pageNum': '1',
    #     'pageSize': '10',
    #     'mobile': '18039537200'}
    # headers = {
    #     'Authentication-Admin-Web-Token': '91a3763b8eb940a0bed7bbae7e3e01f5'
    # }

    # res = re.get(headers=headers, params=payload)
    # print(res.text)  # 打印原始响应文本

    # print(RestClient.request.url)
    # logg.info(res)



    """re = RestClient('https://testlawson.yorentown.com/group')
    # url = api_group_url + urlPath
    # print(url)
    data = {'query': 'cat'}
    res = re.post('/langdetect', json=data)
    # print(url)
    logg.info(res)"""

