from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login(username, password):
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.saucedemo.com/")
    driver.delete_all_cookies()
    driver.maximize_window()
    driver.implicitly_wait(10)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-name")))

    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    try:
        error = driver.find_element(By.CLASS_NAME, "error-button")
        if error.is_displayed():
            print(f"{username} o {password} da error")
        else:
            print(f"{username} o {password} esta ok")
    except:
        print(f"{username} o {password} login exitoso")

    try:
        if driver.find_element(By.ID, "item_4_img_link").is_displayed():
            print("mochila esta disponible")
        else:
            print("mochila no esta disponible")
    except:
        print("no abrio o la mochila no esta disponible")

    driver.quit()

if __name__ == "__main__":
    usuarios = [
        ("standard_user", "secret_sauce"),
        ("admin", "1234"),
        ("mod", "123")
    ]
    for username, password in usuarios:
        test_login(username, password)