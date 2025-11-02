import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

# --- Crear libro Excel ---
wb = Workbook()
ws = wb.active
ws.title = "Resultados"
ws.append(["Usuario", "Contraseña", "Login", "Mochila", "Resultado"])

# --- Fixture para el navegador ---
@pytest.fixture(scope="session")
def driver():
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
    # Guardar Excel al final de la sesión
    wb.save("resultados_tests.xlsx")
    print("\n Resultados guardados en 'resultados_tests.xlsx'")


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

def verificar_mochila(driver):
    try:
        driver.find_element(By.ID, "item_4_img_link")
        return True
    except:
        return False


# --- Test parametrizado ---
@pytest.mark.parametrize("username,password,es_valido", [
    ("standard_user", "secret_sauce", True),
    ("admin", "1234", False),
    ("mod", "123", False)
])
def test_login(driver, username, password, es_valido):
    login(driver, username, password)

    login_exitoso = "inventory" in driver.current_url
    mochila_ok = verificar_mochila(driver) if login_exitoso else False

    if login_exitoso:
        print(f" Login exitoso con {username}")
        if mochila_ok:
            print(" Mochila disponible correctamente")
        else:
            print("⚠ Mochila no encontrada")
        assert es_valido
    else:
        print(f" Error al iniciar sesión con {username}")
        assert not es_valido

    # Guardar resultado en Excel
    resultado = "PASSED" if es_valido == login_exitoso else "FAILED"
    ws.append([
        username,
        password,
        str(login_exitoso),
        str(mochila_ok),
        resultado
    ])
