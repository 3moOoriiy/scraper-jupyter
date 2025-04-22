
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import random

def setup_driver():
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    return webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)

# تسجيل دخول لتويتر
def login_twitter(driver, username, password):
    driver.get("https://twitter.com/login")
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.NAME, "text"))).send_keys(username + Keys.RETURN)
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password + Keys.RETURN)
    time.sleep(5)

def scrape_twitter(url):
    driver = setup_driver()
    login_twitter(driver, "Nzly274477", "taha2025")
    driver.get(url)
    time.sleep(3)

    platform = "Twitter"
    name = "لا يوجد"
    bio = "لا يوجد"
    status = "Suspended"

    try:
        wait = WebDriverWait(driver, 10)
        try:
            name = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='UserName']//span"))).text
            status = "Active"
            try:
                bio = driver.find_element(By.XPATH, "//div[@data-testid='UserDescription']").text
            except:
                bio = "لا يوجد بايو"
        except:
            name = "لا يوجد"
            status = "Suspended"
    except Exception as e:
        print("Twitter error:", e)

    driver.quit()
    return {"Platform": platform, "Account Name": name, "Account Bio": bio, "Status": status, "Link": url}

def scrape_telegram(url):
    driver = setup_driver()
    driver.get(url)
    platform = "Telegram"
    name = "N/A"
    bio = "لا يوجد"
    status = "Active"
    try:
        wait = WebDriverWait(driver, 10)
        name = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@dir='auto']"))).text
        try:
            bio = driver.find_element(By.XPATH, "//div[@class='tgme_page_description']").text
        except:
            bio = "لا يوجد بايو"
        if "This account is unavailable" in driver.page_source:
            status = "Suspended"
    except Exception as e:
        print("Telegram error:", e)
        status = "Suspended"
    driver.quit()
    return {"Platform": platform, "Account Name": name, "Account Bio": bio, "Status": status, "Link": url}

def scrape_reddit(url):
    driver = setup_driver()
    driver.get(url)
    platform = "Reddit"
    name = "لا يوجد"
    bio = "لا يوجد"
    status = "Suspended"
    try:
        wait = WebDriverWait(driver, 10)
        name_elem = wait.until(EC.presence_of_element_located((By.XPATH, "//h1"))).text
        if "has been suspended" in name_elem:
            status = "Suspended"
        else:
            name = name_elem
            status = "Active"
            try:
                bio = driver.find_element(By.XPATH, "//p[@data-testid='profile-description']").text
            except:
                bio = "لا يوجد بايو"
    except Exception as e:
        print("Reddit error:", e)
    driver.quit()
    return {"Platform": platform, "Account Name": name, "Account Bio": bio, "Status": status, "Link": url}

def scrape_tiktok(url):
    url = re.sub(r'\?.*', '', url)
    driver = setup_driver()
    driver.get(url)
    time.sleep(random.uniform(2, 4))
    platform = "TikTok"
    name = "لا يوجد"
    bio = "لا يوجد"
    status = "Suspended"
    try:
        wait = WebDriverWait(driver, 10)
        try:
            name = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@data-e2e='user-title']"))).text
            status = "Active"
            try:
                bio = driver.find_element(By.XPATH, "//h2[@data-e2e='user-bio']").text
            except:
                bio = "لا يوجد بايو"
        except:
            name = "لا يوجد"
            status = "Suspended"
    except Exception as e:
        print("TikTok error:", e)
    driver.quit()
    return {"Platform": platform, "Account Name": name, "Account Bio": bio, "Status": status, "Link": url}
