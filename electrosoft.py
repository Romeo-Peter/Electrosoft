# Program for automating electricty bill.

import os
import electrosoftUserVariables
import time
import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':
    browser = webdriver.Firefox()
    browser.get('https://www.vtpass.com/')

    # Select category and service
    print('Selecting category and service.')
    categories = Select(browser.find_element_by_id('category'))
    service = Select(browser.find_element_by_id('services'))
    categories.select_by_value('7')
    service.select_by_value('abuja-electric')

    # Submit form
    form = browser.find_element_by_tag_name('form')
    form.submit()

    # Sleep for 3Sec to redirect  to next page and 3Sec to load page source
    print('Redirecting to AEDC page...\n')
    time.sleep(3)
    next_page = browser.page_source # Transaction detail page
    time.sleep(3)

    # Meter and buyer info
    parser = argparse.ArgumentParser(description='Electric bill amount')
    parser.add_argument('-a', '--amount', dest='amount', type=float, default=float(2000.0), help='Pass the amount for electric bill')
    args = parser.parse_args()

    print('Filling meter and buyer information...\n')
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

    """NOTE: WIll put transaction detail in CSV in future update """

    # Continue to next page for billing
    amount = browser.find_element_by_class_name('btn-warning')
    amount.click()

    #  Billing information
    bill = browser.find_element_by_id('ravepay-button')
    bill.click()
    print('Loading billing modal...\n')

    # Switch to HTML iframe and load iframe element into view
    browser.switch_to.frame('checkout')
    wait = WebDriverWait(browser, 10)

    print('Card Credentials Form:')
    print('\tFilling card number...')
    card_number = wait.until(EC.visibility_of_element_located((By.NAME, 'cardNumber')))
    card_number.clear()
    card_number.send_keys(os.environ.get('card_number'))

    print('\tFilling card expiration date...')
    expiration = wait.until(EC.visibility_of_element_located((By.NAME, 'expiration')))
    expiration.clear()
    expiration.send_keys(os.environ.get('valid_till'))

    print('\tFilling CVV...')
    cvv = wait.until(EC.visibility_of_element_located((By.NAME, 'cvv')))
    cvv.clear()
    cvv.send_keys(os.environ.get('cvv'))

    print('\tSubmitting form...')
    submit_button = wait.until(EC.visibility_of_element_located((By.ID, 'paycard-btn')))
    submit_button.click()
