from selenium import webdriver
import time

try:
    navegador = webdriver.Edge()
except Exception:
    navegador = webdriver.Chrome()

navegador.get("about:blank")
print("Navegador aberto com Selenium")

# Mantém o navegador aberto por 10 segundos
time.sleep(10)
navegador.quit()
