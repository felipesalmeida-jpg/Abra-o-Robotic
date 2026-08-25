# Aula 3 - Script 3
# Objetivo: criar um alvo visual,
# exibi-lo e localizá-lo na tela.

from pathlib import Path
import tkinter as tk
from PIL import Image, ImageDraw
import pyautogui

# --------------------------------------------------
# PARTE 1 - DEFINIR ONDE A IMAGEM SERÁ SALVA
# --------------------------------------------------
PASTA = Path(__file__).resolve().parent
ARQUIVO = PASTA / "alvo_rpa.png"

# --------------------------------------------------
# PARTE 2 - CRIAR A IMAGEM-ALVO
# --------------------------------------------------
img = Image.new("RGB", (260, 120), "white")
draw = ImageDraw.Draw(img)

# Borda azul
draw.rectangle((8, 8, 252, 112), outline=(0, 90, 220), width=6)

# Texto dentro da imagem
draw.text((65, 45), "ALVO RPA", fill=(0, 90, 220))

img.save(ARQUIVO)
print("Imagem criada em:", ARQUIVO)

# --------------------------------------------------
# PARTE 3 - MOSTRAR O ALVO EM UMA JANELA
# --------------------------------------------------
root = tk.Tk()
root.title("Janela Alvo RPA")
root.geometry("360x220+250+180")

foto = tk.PhotoImage(file=str(ARQUIVO))
rotulo = tk.Label(root, image=foto)
rotulo.pack(padx=30, pady=30)

# --------------------------------------------------
# PARTE 4 - PROCURAR A IMAGEM NA TELA
# --------------------------------------------------
def procurar():
    print("Procurando alvo na tela...")
    try:
        posicao = pyautogui.locateOnScreen(str(ARQUIVO))
    except pyautogui.ImageNotFoundException:
        posicao = None

    if posicao:
        centro = pyautogui.center(posicao)
        print("Alvo encontrado.")
        print("Posicao:", posicao)
        print("Centro:", centro)
        pyautogui.moveTo(centro.x, centro.y, duration=0.5)
    else:
        print("Alvo nao encontrado.")
        print("Verifique se a janela esta visivel e sem outra janela por cima.")

# --------------------------------------------------
# PARTE 5 - AGUARDAR E EXECUTAR A BUSCA
# --------------------------------------------------
root.after(2000, procurar)
root.mainloop()
