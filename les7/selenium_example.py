import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

if __name__ == '__main__':
    url = "https://habr.com/ru/"
    browser = webdriver.Firefox()

    # gecko = os.path.normpath(
    #     os.path.join(os.path.dirname(__file__), 'geckodriver'))
    # binary = FirefoxBinary(
    #     r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
    # browser = webdriver.Firefox(firefox_binary=binary,
    #                             executable_path=gecko + '.exe')

    browser.get(url)

    a = browser.find_element_by_xpath('//a[@class="post__title_link"]')
    a.click()
    search_form = browser.find_element_by_xpath(
        '//input[@id="search-form-field"]')
    search_form.send_keys('Hello Habr')
    search_form.send_keys(Keys.BACKSPACE)
    search_form.send_keys(Keys.CONTROL + 'A')
    search_form.send_keys(Keys.CONTROL + 'C')

    article = browser.find_element_by_xpath('//article')
    article.screenshot('some.png')

    # browser.title
    # browser.window_handles
    #
    # browser.switch_to.window('48')
    # browser.title
    print(1)
