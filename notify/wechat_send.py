import time

import requests, json, base64, hashlib

bot_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5a42271e-2973-44b8-921b-78adbad29d6d'

class Robot:
    def send_work_msg(self, projname,total,passed,failed,skipped):
        adress = 'http://localhost:63342/auto_test_project/result/index.html'
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        mkd_msg = f"""
                        # ** 各位同事, 测试结果通知 **:
                            >自动化用例执行完成，执行结果如下:
                            >用例执行完毕时间为：<font color=\"info\">{nowtime}</font>
                            >项目名称: <font color=\"info\">{projname}</font>
                            >用例运行总数: {total} 个
                            >通过用例个数: <font color=\"info\">{passed}</font> 个
                            >失败用例个数: <font color=\"red\">{failed}</font> 个
                            >跳过用例个数: {skipped} 个
                            >成  功   率: {(passed / total)*100} %
                            >allure报告链接：[allure报告，请点击后进入查看]({adress})                        
                        """
        data = {
            'msgtype': 'markdown',
            'markdown':
                {'content': mkd_msg}
        }
        return data

    def sendmessage(self,projname,total,passed,failed,skipped):
        data = self.send_work_msg(projname,total,passed,failed,skipped)
        r = requests.post(bot_url, data=json.dumps(data))






