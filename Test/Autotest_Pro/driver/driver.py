from selenium import webdriver

def browser():
    driver = webdriver.Chrome()

    return driver

if __name__ == '__main__':
    browser()