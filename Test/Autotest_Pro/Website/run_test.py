import unittest
from BSTestRunner import  BSTestRunner
from function import *
import time

report_dir = './test_report'
test_dir = './test_case'

print('start run testcase ......... ')

# 运行测试报告生成的模块
dis = unittest.defaultTestLoader.discover(test_dir,pattern='test_login.py')
now =  time.strftime("%Y%m%d%H%M%S")
report_name = report_dir + '/' + now + 'result.html'

# 生成测试报告
print('start write test_report .......')
with open(report_name,'wb') as f:
    r = BSTestRunner(stream=f,title='test report',description='local Test')
    r.run(dis)

# 寻找最新报告并发送
print('find latest report')
la = latest_report(report_dir)
print('send email')
send_email(la)

print('test end')

