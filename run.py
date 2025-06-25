import pytest
import time
import os
from notify.wechat_send import Robot
from pytest_jsonreport.plugin import JSONReport
if __name__ == '__main__':
    rb = Robot()
    plugin = JSONReport()
    pytest.main(plugins=[plugin])

    summary = plugin.report.get("summary")
    passed = summary.get("passed")
    failed = summary.get("failed")
    skipped = summary.get("skipped")
    total = summary.get("total")
    print('请稍后，正在为你生成allure报告......')
    time.sleep(3)
    os.system('allure generate ./report -o ./result --clean')
    rb.sendmessage('pytest自动化框架',total,passed,failed,skipped)
    print('已经成功生成allure报告，地址请进入企微查看～')