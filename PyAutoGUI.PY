import time
import pyautogui

# Habilita o recurso de segurança (mover o mouse para o canto da tela cancela tudo)
pyautogui.FAILSAFE = True

# Aviso no terminal e pausa para dar tempo de você clicar no Bloco de Notas
print("O robô iniciará em 5 segundos.")
time.sleep(5)

# Digita a primeira mensagem (interval=0.05 cria uma pausa entre cada letra)
pyautogui.write("Meu primeiro robo de RPA.", interval=0.05)

# Pula para a linha de baixo
pyautogui.press("enter")

# Digita a segunda mensagem
pyautogui.write("Automacao executada com sucesso.", interval=0.05)
