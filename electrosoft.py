#! python3

# Program for automating electricty bill.

from selenium import webdriver
from selenium.webdriver.support.ui import Select

browser = webdriver.Firefox()
browser.get('https://www.vtpass.com/')

# Select category and service
categories = Select(browser.find_element_by_id('category'))
service = Select(browser.find_element_by_id('services'))
categories.select_by_value('7')
service.select_by_value('abuja-electric')

# Submit form
form = browser.find_element_by_tag_name('form')
form.submit()
