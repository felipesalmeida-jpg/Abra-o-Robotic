# Aula 3 - Script 2
# Objetivo:
# localizar o Bloco de Notas, preparar a janela,
# confirmar o foco e somente depois digitar.

import time
import pyautogui
import pygetwindow as gw

# --------------------------------------------------
# 1. SEGURANÇA
# --------------------------------------------------
pyautogui.FAILSAFE = True

# --------------------------------------------------
# 2. NOMES POSSÍVEIS DA JANELA
# --------------------------------------------------
TERMOS = [
    "Bloco de Notas",
    "Notepad",
    "Bloco de notas"
]

# --------------------------------------------------
# 3. PREPARAR A BUSCA
# --------------------------------------------------
print("Abra o Bloco de Notas.")
print("O programa iniciara a busca em 5 segundos.")
time.sleep(5)

# --------------------------------------------------
# 4. LOCALIZAR A JANELA
# --------------------------------------------------
janela = None
for termo in TERMOS:
    encontradas = gw.getWindowsWithTitle(termo)
    if encontradas:
        janela = encontradas[0]
        break

# --------------------------------------------------
# 5. VERIFICAR SE A JANELA FOI ENCONTRADA
# --------------------------------------------------
if janela is None:
    print("Bloco de Notas nao encontrado.")
    print("Execute o Script 1 e confira como o titulo da janela aparece no Terminal.")
    raise SystemExit

print("Janela encontrada:", janela.title)

# --------------------------------------------------
# 6. RESTAURAR A JANELA, SE NECESSÁRIO
# --------------------------------------------------
if janela.isMinimized or janela.isMaximized:
    janela.restore()
    time.sleep(1)

# --------------------------------------------------
# 7. TENTAR ATIVAR A JANELA
# --------------------------------------------------
try:
    janela.activate()
    print("Tentativa de ativacao realizada.")
except Exception as erro:
    print("Nao foi possivel ativar automaticamente.")
    print("Erro:", erro)
    print("Clique manualmente no Bloco de Notas. O programa aguardara 5 segundos.")
    time.sleep(5)

# --------------------------------------------------
# 8. AGUARDAR A TROCA DE FOCO
# --------------------------------------------------
time.sleep(2)

# --------------------------------------------------
# 9. ORGANIZAR A JANELA
# --------------------------------------------------
janela.resizeTo(800, 500)
janela.moveTo(100, 100)
time.sleep(1)

# --------------------------------------------------
# 10. CLICAR DENTRO DA JANELA
# --------------------------------------------------
x_clique = janela.left + 250
y_clique = janela.top + 180
print("Clicando dentro do Bloco de Notas:", x_clique, y_clique)
pyautogui.click(x_clique, y_clique)
time.sleep(1)

# --------------------------------------------------
# 11. DIGITAR
# --------------------------------------------------
pyautogui.write("Janela localizada e preparada.", interval=0.04)
pyautogui.press("enter")
pyautogui.write("Agora entendemos foco e janela.", interval=0.04)

# --------------------------------------------------
# 12. FINALIZAÇÃO
# --------------------------------------------------
print("Automacao concluida.")
