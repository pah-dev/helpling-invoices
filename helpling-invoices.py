from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import env
import os
import time

chrome_options = Options()
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": 'D:',
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}
)

driver = webdriver.Chrome("./chromedriver.exe", options=chrome_options)

driver.get("https://app.helpling.de/mobile/provider/login")

print("::: PROCESS STARTING :::")

user = env.getUsr()
passw = env.getPass()

print("::: USER: " + user)

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

link = WebDriverWait(driver, 10).until(
    lambda d: d.find_element_by_xpath(
        '//div[@class="transfers-paid__load-more"]/a')
)
link.click()

time.sleep(5)

file = open("invoices_data.txt", "w")

transfers = driver.find_elements_by_xpath(
    '//div[@class="transfer-item"]/a')

print("::: TRANSFERS: " + str(len(transfers)))

for transNum in range(1, len(transfers) + 1):
    time.sleep(1.5)
    transfers = driver.find_elements_by_xpath(
        '//div[@class="transfer-item"]/a')
    print("::: WORKING...")
    lnk_tr = transfers[transNum-1].get_attribute(
        "href").replace("https://app.helpling.de/", "")
    trans = WebDriverWait(driver, 15).until(
        lambda d: d.find_element_by_xpath(
            '//a[contains(@href, "' + lnk_tr + '")]')
    )
    driver.execute_script("arguments[0].click()", trans)
    time.sleep(1)
    payments = WebDriverWait(driver, 15).until(
        lambda d: d.find_elements_by_xpath(
            '//a[@class="payment-item"]')
    )
    for payNum in range(1, len(payments) + 1):
        time.sleep(2)
        payments = WebDriverWait(driver, 15).until(
            lambda d: d.find_elements_by_xpath(
                '//a[@class="payment-item"]')
        )
        lnk_py = payments[payNum-1].get_attribute(
            "href").replace("https://app.helpling.de/", "")
        pay = WebDriverWait(driver, 15).until(
            lambda d: d.find_element_by_xpath(
                '//a[contains(@href, "' + lnk_py + '")]')
        )
        driver.execute_script("arguments[0].click()", pay)
        time.sleep(2)
        trs = WebDriverWait(driver, 15).until(
            lambda d: d.find_elements_by_xpath(
                "//tbody/tr")
        )
        str_data = "T" + str(transNum) + ";P" + str(payNum) + ";"
        customer = driver.find_element_by_xpath(
            '//div[@class="event-details__content"]/div[1]/div[2]').text
        address = driver.find_element_by_xpath(
            '//div[@class="event-details__content"]/div[1]/div[4]/a/span').text
        e_date = driver.find_element_by_xpath(
            '//div[@class="event__customer-name"]').text
        e_time = driver.find_element_by_xpath(
            '//div[@class="event__time"]').text
        frec = driver.find_element_by_xpath(
            '//div[@class="event__time event-details__frequency"]/span').text
        str_data += customer + ";" + address + ";" + \
            e_date + ";" + e_time + ";" + frec + ";"
        data = driver.find_elements_by_xpath(
            '//ul/li[@class="options-group__item "]/div')
        for item in range(1, len(data)):
            str_data += data[item].text + ";"
        for row in range(0, len(trs)):
            tds = driver.find_elements_by_xpath(
                "//tbody/tr["+str(row+1)+"]/td")
            for col in range(0, len(tds)):
                str_data += tds[col].text + ";"
            lnk_inv = driver.find_element_by_xpath(
                "//tbody/tr["+str(row+1)+"]/td[last()]/a")
            str_data += lnk_inv.get_attribute("href") + ";"
            lnk_inv.click()
            time.sleep(1)
        file.write(str_data + "\n")
        driver.back()
    driver.back()
print("::: PROCESS FINISHED :::")

file.close()
driver.close()
