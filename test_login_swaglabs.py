import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# --- Fixture para el navegador ---
@pytest.fixture
def driver():
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# --- Función para login ---
def login(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    driver.delete_all_cookies()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )

    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)


# --- Función para verificar la mochila ---
def verificar_mochila(driver):
    try:
        driver.find_element(By.ID, "item_4_img_link")
        return True
    except:
        return False


# --- Test con varios usuarios ---
@pytest.mark.parametrize("username,password,es_valido", [
    ("standard_user", "secret_sauce", True),  # válido
    ("admin", "1234", False),                 # inválido
    ("mod", "123", False)                     # inválido
])
def test_login(driver, username, password, es_valido):
    login(driver, username, password)

    if "inventory" in driver.current_url:
        print(f" Login exitoso con {username}")
        if verificar_mochila(driver):
            print(" Mochila disponible correctamente")
        else:
            print(" Mochila no encontrada")
        assert es_valido, f"El usuario {username} no debería haber podido iniciar sesión"
    else:
        print(f" Error al iniciar sesión con {username}")
        assert not es_valido, f"El usuario {username} debería haber iniciado sesión correctamente"
