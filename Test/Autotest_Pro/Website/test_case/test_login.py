from LoginPage import *
import unittest
from Model import function,myunit
from time import sleep

class LoginTest(myunit.StartEnd):
    def test1(self):
        '''user and passsword is normol'''
        po = LoginPage(self.driver)
        po.login_action('51zxw',123456)
        sleep(3)

        try:
            self.assertEqual(po.loginpass(),'我的空间')
        except:
            print('断言1检测错误')
        function.insert_screenshot('test1.jpg')
        print('test1 is end!')

    def test2(self):
        '''user is normol  password is empty'''
        po = LoginPage(self.driver)
        po.login_action('51zxw','')
        sleep(3)

        try:
            self.assertEqual(po.loginfail(),'')
        except:
            print('断言2检测错误')
        function.insert_screenshot('test2.jpg')
        print('test1 is end!')

    def test3(self):
        '''user and password is empty'''
        po = LoginPage(self.driver)
        po.login_action('','')
        sleep(3)

        try:
            self.assertEqual(po.loginfail(),'')
        except:
            print('断言3检测错误')
        function.insert_screenshot('test3.jpg')
        print('test3 is end!')

if __name__ == '__main__':
    unittest.main()
