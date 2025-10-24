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


# --- Funciones auxiliares ---
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


def has_login_error(driver):
    errors = driver.find_elements(By.CLASS_NAME, "error-button")
    return len(errors) > 0


def product_available(driver, product_id):
    try:
        product = driver.find_element(By.ID, product_id)
        return product.is_displayed()
    except:
        return False


# --- Test parametrizado para todos los usuarios ---
@pytest.mark.parametrize("username,password", [
    ("standard_user", "secret_sauce"),   # válido
    ("admin", "1234"),                   # inválido
    ("mod", "123")                        # inválido
])
def test_login_flow(driver, username, password):
    login(driver, username, password)

    if has_login_error(driver):
        print(f"Error al iniciar sesión con: {username}")
        login_ok = False
    else:
        print(f"Login exitoso con: {username}")
        login_ok = True

    # --- Verificar mochila solo si login fue exitoso ---
    if login_ok:
        disponible = product_available(driver, "item_4_img_link")
        if disponible:
            print("Mochila disponible correctamente")
        else:
            print("Mochila no encontrada o página no cargó bien")
        assert disponible, f"El producto 'mochila' no está disponible para {username}"
    else:
        print(f"No se verificó la mochila porque login falló con {username}")