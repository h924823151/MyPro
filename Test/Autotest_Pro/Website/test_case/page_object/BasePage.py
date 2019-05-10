from time import sleep


class Page():
    def __init__(self,driver):
        self.driver = driver
        self.base_url = 'http://localhost/'
        self.timeout = 20

    def getpage(self,url):
        url = self.base_url + url
        print('Test url is %s' % url)
        self.driver.get(url)
        self.driver.maximize_window()
        sleep(2)

    def find_element(self,*list):
        return self.driver.find_element(*list)
    