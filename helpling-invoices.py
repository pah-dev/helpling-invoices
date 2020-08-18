from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome("./chromedriver.exe")


driver.get("https://app.helpling.de/mobile/provider/more")


user = "//"
passw = "//"

input_user = WebDriverWait(driver, 15).until(
    lambda d: d.find_element_by_xpath('//form//input[@name="username"]')
)
input_pass = driver.find_element_by_xpath('//form//input[@name="password"]')

input_user.send_keys(user)
input_pass.send_keys(passw)

btn_login = driver.find_element_by_xpath('//form//button[@type="submit"]')

btn_login.click()

links = driver.find_elements_by_xpath('//div[@class="menu__container-inline"]/div/a')

print(links)
