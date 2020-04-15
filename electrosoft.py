# Program for automating electricty bill.

import os
import electrosoftUserVariables
import time
import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import Select

if __name__ == '__main__':
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

    # Sleep for 3Sec to redirect  to next page and 3Sec to load page source
    print('Redirecting to AEDC page...')
    time.sleep(3)
    next_page = browser.page_source
    time.sleep(3)

    # Meter and buyer info
    parser = argparse.ArgumentParser(description='Electric bill amount')
    parser.add_argument('-a', '--amount', dest='amount', type=float, default=float(2000.0), help='Pass the amount for electric bill')
    args = parser.parse_args()

    print('Filling meter and buyer information...')
    meter_type = Select(browser.find_element_by_name('MeterType'))
    meter_type.select_by_value('Prepaid')

    meter_number = browser.find_element_by_name('meter_number')
    meter_number.clear()
    meter_number.send_keys(os.environ.get('meter_number'))

    phone_number = browser.find_element_by_name('phone')
    phone_number.clear()
    phone_number.send_keys(os.environ.get('phone_number'))

    email_address = browser.find_element_by_name('email')
    email_address.clear()
    email_address.send_keys(os.environ.get('email_address'))

    amount = browser.find_element_by_name('amount')
    amount.clear()
    amount.send_keys(str(args.amount))

    # Continue to next page for billing
    amount = browser.find_element_by_class_name('btn-warning')
    amount.click()

    bill = browser.find_element_by_id('ravepay-button')
    bill.click()

    # Sleep for 3Sec to redirect  to next page and 3Sec to load page source
    print('Redirecting to biilling page...')
    time.sleep(3)
    # next_page = browser.page_source
    # time.sleep(3)

    """NOTE: WIll put transaction detail in CSV in future update """

    # Billing information

