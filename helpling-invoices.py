from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import env
import os
import time

driver = webdriver.Chrome("./chromedriver.exe")


driver.get("https://app.helpling.de/mobile/provider/login")

user = env.getUsr()
passw = env.getPass()

input_user = WebDriverWait(driver, 15).until(
    lambda d: d.find_element_by_xpath('//form//input[@name="username"]')
)
input_pass = driver.find_element_by_xpath('//form//input[@name="password"]')

input_user.send_keys(user)
input_pass.send_keys(passw)

btn_login = driver.find_element_by_xpath('//form//button[@type="submit"]')

btn_login.click()

time.sleep(5)

link = WebDriverWait(driver, 10).until(
    lambda d: d.find_element_by_xpath('//a[contains(@href, "/more")]')
)

link.click()

link = WebDriverWait(driver, 10).until(
    lambda d: d.find_element_by_xpath(
        '//a[contains(@href, "/bank_transfers")]')
)

link.click()

item = WebDriverWait(driver, 10).until(
    lambda d: d.find_element_by_xpath('//*[@class="transfer-item"]')
)


file = open("invoices.txt", "w")

transfers = len(driver.find_elements_by_xpath(
    '//div[@class="transfer-item"]/a'))

print("TRANSF: " + str(transfers))

file.write("Transfers: " + str(transfers) + os.linesep)

for transNum in range(1, transfers + 1):
    print(str(transNum))
    trans = WebDriverWait(driver, 15).until(
        lambda d: d.find_element_by_xpath(
            '//*[@class="transfer-item"]/a[' + str(transNum) + ']')
        # EC.presence_of_element_located(
        #     (By.XPATH,
        #      '//div[@class="transfer-item"][position()=' + str(transNum) + ']')
        # )
    )
    print(trans.text)
    file.write(trans.text + os.linesep)
    trans.click()
    # driver.implicitly_wait(10)
    time.sleep(2)
    payments = len(
        WebDriverWait(driver, 15).until(
            lambda d: d.find_elements_by_xpath('//a[@class="payment-item"]')
        )
    )
    print("PAYS: " + str(payments))
    # file.write("Payments: " + str(payments) + os.linesep)
    # for payNum in range(1, payments + 1):
    #     pay = WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, '//a[@class="payment-item"][' + str(payNum) + "]")
    #         )
    #     )
    #     # print(pay.text)
    #     pay.click()
    #     time.sleep(3)
    #     invoice = WebDriverWait(driver, 15).until(
    #         lambda d: d.find_element_by_xpath(
    #             "//tbody/tr[last()]/td[last()]/a")
    #     )
    #     file.write(
    #         str(payNum)
    #         + ";"
    #         + invoice.text
    #         + ";"
    #         + invoice.get_attribute("href")
    #         + os.linesep
    #     )
    #     print(str(payNum) + " - " + invoice.text)
    #     driver.back()
    driver.back()


file.close()
