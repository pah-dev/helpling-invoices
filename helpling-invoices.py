from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import env
import os
import time
from selenium.webdriver.chrome.options import Options

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

link = WebDriverWait(driver, 10).until(
    lambda d: d.find_element_by_xpath(
        '//div[@class="transfers-paid__load-more"]/a')
)

link.click()

time.sleep(5)

file = open("invoices.txt", "w")

transfers = driver.find_elements_by_xpath(
    '//div[@class="transfer-item"]/a')

for transNum in range(1, len(transfers) + 1):
    time.sleep(2)
    transfers = driver.find_elements_by_xpath(
        '//div[@class="transfer-item"]/a')
    print("TRANSF: " + str(len(transfers)))
    lnk_tr = transfers[transNum-1].get_attribute(
        "href").replace("https://app.helpling.de/", "")
    print(str(transNum)+" - "+lnk_tr)
    trans = WebDriverWait(driver, 15).until(
        lambda d: d.find_element_by_xpath(
            '//a[contains(@href, "' + lnk_tr + '")]')
    )
    print(trans.text)
    driver.execute_script("arguments[0].click()", trans)
    time.sleep(2)
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
        print("PAYS: " + str(len(payments)))
        lnk_py = payments[payNum-1].get_attribute(
            "href").replace("https://app.helpling.de/", "")
        print(str(payNum)+" - "+lnk_py)
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
        data = driver.find_elements_by_xpath(
            '//ul/li[@class="options-group__item "]/div')
        str_data = str(transNum) + ";P;" + str(payNum) + ";"
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
        file.write(str_data + os.linesep)
        driver.back()
    driver.back()


file.close()
