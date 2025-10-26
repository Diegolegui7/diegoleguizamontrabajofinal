import pytest
from login_module import driver, login
from inventario_module import verificar_mochila


@pytest.mark.parametrize("username,password,es_valido", [
    ("standard_user", "secret_sauce", True),  # válido
    ("admin", "1234", False),                 # inválido
    ("mod", "123", False)                     # inválido
])
def test_login(driver, username, password, es_valido):
    login(driver, username, password)

    if "inventory" in driver.current_url:
        print(f"✅ Login exitoso con {username}")
        if verificar_mochila(driver):
            print("🎒 Mochila disponible correctamente")
        else:
            print("⚠️ Mochila no encontrada")
        assert es_valido, f"El usuario {username} no debería haber podido iniciar sesión"
    else:
        print(f"❌ Error al iniciar sesión con {username}")
        assert not es_valido, f"El usuario {username} debería haber iniciado sesión correctamente"