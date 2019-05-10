from BasePage import *
from selenium import webdriver
from selenium.webdriver.common.by import By

'''
    新闻页面登陆
'''

class LoginPage(Page):
    url = '/news/'

    # 元素定位参数
    global username,password,submit
    username = (By.NAME,'username')
    password = (By.NAME,'password')
    submit = (By.NAME,'Submit')

    # 元素点击函数
    def username_send(self,uname):
        self.find_element(*username).clear()
        self.find_element(*username).send_keys(uname)

    def password_send(self,pwd):
        self.find_element(*password).clear()
        self.find_element(*password).send_keys(pwd)

    def submit_click(self):
        self.find_element(*submit).click()

    def login_action(self,uname,pwd):
        self.getpage('/news/')
        self.username_send(uname)
        self.password_send(pwd)
        self.submit_click()

    # 设置断言检测是否登陆成功
    global LoginPass_ass,loginFail_ass
    LoginPass_ass = (By.LINK_TEXT, '我的空间')
    loginFail_ass = (By.NAME, 'username')

    def loginpass(self):
        return self.find_element(*LoginPass_ass).text

    def loginfail(self):
        return self.find_element(*loginFail_ass).text


