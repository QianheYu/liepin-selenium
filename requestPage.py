from selenium import webdriver

from selenium.webdriver.common.keys import Keys

class Browser(object):
    def __init__(self, browser="Chrome"):
        try:
            if browser == "Chrome":
                self.driver = webdriver.Chrome()
            elif browser == "Firefox":
                self.driver = webdriver.Firefox()
            else:
                self.driver = webdriver.Safari()
        except Exception as error:
            print(error)

    # 虚函数,用于防止回调函数报错
    def parse(self, callback):
        pass
    # 仅用于网页爬取,使用回调函数进行处理
    def get_page(self, url, callback=parse):
        try:
            self.driver.get(url)
            callback(self.driver.page_source)
            return self.driver.page_source
        except Exception as error:
            return error

    def follow(self, url, callback=parse):
        try:
            if type(url) is str:
                    self.get_page(url, callback)
            elif type(url) is list:
                for aurl in url:
                    if type(aurl) is str:
                        self.get_page(aurl, callback)
        except Exception as error:

            return error


    def followall(self, urls, callback=parse):
        try:
            for url in urls:
                self.get_page(url, callback)
        except Exception as error:
            return error

    def find_element(self, label, value):
        return self.driver.find_element(label, value)


    def send_keys(self, element, value):
        try:
            element.send_keys(value)
        except Exception as error:
            print(error)
            print('The element param need a object of element.')
            return (error)

    def clear_content(self, element):
        try:
            element.clear()
        except Exception as error:
            print(error)
            print('The element param need a object of element.')
            return (error)



    def close(self):
        self.driver.close()



def parse(response):
    assert "Python" in browser.driver.title
    elem = browser.driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    browser.send_keys(elem, Keys.RETURN)
    assert "No resutls found." not in browser.driver.page_source
    print(type(elem))
    print(elem)
    browser.get_page("https://www.baidu.com/")


if __name__ == '__main__':
    browser = Browser("Firefox")
    browser.get_page("http://www.python.org/", parse)
    browser.close()


