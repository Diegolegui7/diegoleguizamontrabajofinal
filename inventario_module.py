from selenium.webdriver.common.by import By

def verificar_mochila(driver):
    try:
        driver.find_element(By.ID, "item_4_img_link")
        return True
    except:
        return False