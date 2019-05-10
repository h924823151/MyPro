from driver import *
import  os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 截屏
def insert_screenshot(driver,filename):
    base_dir = os.path.dirname(__file__)
    base_dir = base_dir.replace('\\', '/')
    base_dir = base_dir.split('/Website')

    # 获取截图存放路径
    pathname = base_dir[0] + '/Website/test_report/screenshot/' + filename
    print(pathname)
    driver.get_screenshot_as_file(pathname)

# 发送邮件
def send_email(file):
    # 获取文件内容
    with open(file,'rb') as f:
        f = f.read()

    # 定义smtp服务器
    smtpserver = 'smtp.163.com'

    # 定义用户信息
    sender = '**********'
    password = '**********'
    recives = ['**********']

    # 定义附件内容
    m=MIMEText(f,'base64','utf-8')
    m['Content-Type'] = 'application/octet-stream'
    m["Content-Disposition"] = 'attachment;filename="%s"' % file

    # 定义文本内容
    msg = MIMEMultipart()
    msg.attach(MIMEText('<html>自动化测试报告结果</html>','html','utf-8'))
    msg['Subject'] = '测试内容报告'
    msg['From'] = sender
    msg['To'] = ','.join(recives)
    msg.attach(m)

    # 定义smtp
    smtp = smtplib.SMTP_SSL(smtpserver,465)
    smtp.helo(smtpserver)
    smtp.ehlo(smtpserver)
    smtp.login(sender,password)

    print('Start Send Msg')
    smtp.sendmail(sender,recives,msg.as_string())
    smtp.quit()
    print('End!')

# 获取最新测试报告
def latest_report(report_dir):
    lists = os.listdir(report_dir)
    lists.sort(key=lambda fn:os.path.getatime(report_dir+'\\'+fn))
    file = os.path.join(report_dir,lists[-1])
    print('the latest report is %s ' % file)

    return file

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("http://www.sogou.com")
    insert_screenshot(driver, "sogou.png")
    driver.quit()