# Aula 3 - Script 1
# Objetivo: observar o ambiente antes de controlar qualquer coisa.
import time
import pyautogui
import pygetwindow as gw
# Mostra o tamanho da tela em pixels.
print("Tamanho da tela:", pyautogui.size())
# Mostra a posição atual do ponteiro do mouse.
print("Posicao atual:", pyautogui.position())
# Dá tempo para mover o mouse e comparar as coordenadas.
print("Aponte o mouse para um ponto da tela.")
time.sleep(5)
print("Posicao depois de 5s:", pyautogui.position())
# Lista os títulos das janelas que o Windows está identificando.
print("Janelas abertas:")

for titulo in gw.getAllTitles():
# Ignora entradas sem texto.
    if titulo.strip():
        print("-", titulo)