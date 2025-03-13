# -*- coding: utf-8 -*-
# @Time         : 2025/03/24 17:30
# @Author       : caitao@css.com.cn
# @Environment  : selenium: 4.29.0;  Chrome(webdriver) version: 134.0.6998.35; Python: 3.12.7
# @Download_addr: https://googlechromelabs.github.io/chrome-for-testing/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# init ChromeOptions -> list of arguments
options = webdriver.ChromeOptions()
# disable sandbox
options.add_argument('--no-sandbox')
# disable gpu acceleration
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(executable_path=r'C:\software\chrome-win64\chromedriver.exe'), options=options)
try:
    # full screen
    driver.maximize_window()
    driver.get("https://capacity.eu.org/jenkins/login")
    # wait elements load and login.
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "j_username"))
    ).send_keys("sysadmin")
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "j_password"))
    ).send_keys("password")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "Submit"))
    ).click()
    # wait loading jenkins-head-icon
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "jenkins-head-icon"))
    )
    print("login success!")
    time.sleep(1)
    driver.get("https://capacity.eu.org/jenkins/job/Get-Docker-Images/build?delay=0sec")
    appname_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#main-panel > form > div.parameters > div:nth-child(1) > div.setting-main > div > input.jenkins-input'))
    ).send_keys("nginx")
    # clear default value
    appversion_input=WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#main-panel > form > div.parameters > div:nth-child(2) > div.setting-main > div > input.jenkins-input'))
    ).clear()
    appversion_input=WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#main-panel > form > div.parameters > div:nth-child(2) > div.setting-main > div > input.jenkins-input'))
    ).send_keys("latest")
    # add crumb in Header to avoid crsf problem
    crumb = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Jenkins-Crumb"))
    ).get_attribute("value")
    driver.execute_script("""
        var originalOpen = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function() {
            this.setRequestHeader('Jenkins-Crumb', '%s');
            originalOpen.apply(this, arguments);
        };
    """ % (crumb))
    click_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#bottom-sticker > div > button"))
    ).click()
    # wait click initializing
    time.sleep(3)
    driver.get("https://capacity.eu.org/jenkins/job/Get-Docker-Images/lastBuild/console")
    time.sleep(3)
except Exception as e:
    print(f"request error:{e}")
finally:
    # delay 5 seconds before close browser
    time.sleep(5)
    driver.quit()
