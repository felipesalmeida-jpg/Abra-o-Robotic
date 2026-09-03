"""
Atividade 3 - Bloco GUI (RPA)
Robo resiliente a janela inesperada
 
Grupo indicado: Grupo 3
ARQUIVO OFICIAL DE ENTREGA - revalidacao real, sem nenhum mecanismo de
falha forcada. O comportamento (sucesso ou falha) depende exclusivamente
do que acontecer de verdade com o foco da janela durante a execucao.
 
Fluxo:
CRIAR JANELA -> LOCALIZAR -> PREPARAR -> REVALIDAR -> DIGITAR (parte 1)
-> PAUSA PROGRAMADA (grupo muda o foco de proposito, na mao)
-> REVALIDAR -> RECUPERAR (se necessario) -> DIGITAR (parte 2) -> ARRASTAR
-> EVIDENCIA (sucesso ou falha)
"""
 
import platform
import threading
import time
from pathlib import Path
 
import tkinter as tk
from tkinter import messagebox
import pyautogui
import pygetwindow as gw
 
# ---------------------------------------------------------------------------
# 1. Seguranca e parametros gerais
# ---------------------------------------------------------------------------
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2
 
PASTA_DO_SCRIPT = Path(__file__).resolve().parent
EVIDENCIA_SUCESSO = PASTA_DO_SCRIPT / "evidencia_grupo3_sucesso.png"
EVIDENCIA_FALHA = PASTA_DO_SCRIPT / "evidencia_grupo3_falha.png"
 
TITULO_JANELA = "Painel Grupo 3 - Robo Resiliente"
PAUSA_CURTA = 0.8
TEMPO_INICIAL = 2
TEMPO_PARA_TROCAR_FOCO = 6  # segundos que o grupo tem para clicar em outra janela
 
 
# ---------------------------------------------------------------------------
# 2. Diagnostico do ambiente
# ---------------------------------------------------------------------------
def verificar_ambiente():
    sistema = platform.system()
    print("Sistema operacional identificado:", sistema)
    print("Resolucao da tela:", pyautogui.size())
    print("Posicao inicial do mouse:", pyautogui.position())
    print("Janelas com titulo valido:", [t for t in gw.getAllTitles() if t.strip()])
    return True
 
 
# ---------------------------------------------------------------------------
# 3. Janela controlada (area de texto + area visual de arraste)
# ---------------------------------------------------------------------------
def criar_painel_controlado():
    root = tk.Tk()
    root.title(TITULO_JANELA)
    root.geometry("720x560+120+80")
    root.attributes("-topmost", True)
    root.after(1000, lambda: root.attributes("-topmost", False))
 
    titulo = tk.Label(root, text="Painel Grupo 3 - Robo resiliente a janela inesperada",
                       font=("Arial", 14, "bold"))
    titulo.pack(pady=10)
 
    caixa_texto = tk.Text(root, width=78, height=10, font=("Consolas", 11))
    caixa_texto.insert("1.0", "Texto inicial. O robo deve limpar este campo antes de escrever.\n")
    caixa_texto.pack(padx=20, pady=8)
    root.caixa_texto = caixa_texto
 
    orientacao = tk.Label(root, text="Area de arraste: o alvo deve ser movido pelo PyAutoGUI ao final.",
                           font=("Arial", 11))
    orientacao.pack(pady=5)
 
    canvas = tk.Canvas(root, width=640, height=140, bg="#f1f5ff",
                        highlightthickness=1, highlightbackground="#2f6fed")
    canvas.pack(padx=20, pady=8)
    canvas.create_rectangle(60, 40, 180, 100, fill="#2f6fed", outline="#0f2a4d", width=2, tags="alvo")
    canvas.create_text(120, 70, text="ARRASTE", fill="white", font=("Arial", 12, "bold"), tags="alvo")
 
    estado_arraste = {"x": 0, "y": 0, "ativo": False}
 
    def iniciar_arraste(event):
        estado_arraste["ativo"] = True
        estado_arraste["x"] = event.x
        estado_arraste["y"] = event.y
 
    def mover_alvo(event):
        if not estado_arraste["ativo"]:
            return
        dx = event.x - estado_arraste["x"]
        dy = event.y - estado_arraste["y"]
        canvas.move("alvo", dx, dy)
        estado_arraste["x"] = event.x
        estado_arraste["y"] = event.y
 
    def finalizar_arraste(event):
        estado_arraste["ativo"] = False
 
    canvas.tag_bind("alvo", "<ButtonPress-1>", iniciar_arraste)
    canvas.bind("<B1-Motion>", mover_alvo)
    canvas.bind("<ButtonRelease-1>", finalizar_arraste)
 
    status = tk.Label(root, text="Aguardando inicio da automacao...", font=("Arial", 10), fg="#2f6fed")
    status.pack(pady=6)
    root.status_label = status
 
    return root
 
 
# ---------------------------------------------------------------------------
# 4. Localizar a janela pelo titulo
# ---------------------------------------------------------------------------
def localizar_janela():
    print("Procurando a janela controlada...")
    janelas = gw.getWindowsWithTitle(TITULO_JANELA)
    if not janelas:
        print("Janela controlada nao encontrada.")
        return None
    print("Janela encontrada:", janelas[0].title)
    return janelas[0]
 
 
# ---------------------------------------------------------------------------
# 5. Verificar o foco atual
# ---------------------------------------------------------------------------
def janela_correta_esta_ativa():
    ativa = gw.getActiveWindow()
    if ativa is None:
        print("Nenhuma janela ativa foi identificada.")
        return False
    print("Janela ativa agora:", ativa.title)
    return TITULO_JANELA in ativa.title
 
 
# ---------------------------------------------------------------------------
# 6. Ativar com fallback (activate -> clique na barra de titulo)
# ---------------------------------------------------------------------------
def ativar_janela_com_fallback(janela):
    try:
        janela.activate()
    except Exception as erro:
        print("Ativacao automatica pelo PyGetWindow falhou:", erro)
 
    time.sleep(PAUSA_CURTA)
    if janela_correta_esta_ativa():
        return True
 
    print("Tentando recuperar o foco com um clique na barra de titulo...")
    x_titulo = janela.left + max(100, janela.width // 2)
    y_titulo = janela.top + 15
    try:
        pyautogui.click(x_titulo, y_titulo)
    except Exception as erro:
        print("Clique de recuperacao falhou:", erro)
        return False
 
    time.sleep(PAUSA_CURTA)
    return janela_correta_esta_ativa()
 
 
# ---------------------------------------------------------------------------
# 7. Preparar a janela
# ---------------------------------------------------------------------------
def preparar_janela(janela):
    print("Preparando a janela...")
    if janela.isMinimized:
        janela.restore()
        time.sleep(PAUSA_CURTA)
    if janela.isMaximized:
        janela.restore()
        time.sleep(PAUSA_CURTA)
 
    janela.resizeTo(720, 560)
    janela.moveTo(120, 80)
    time.sleep(PAUSA_CURTA)
 
    foco_ok = ativar_janela_com_fallback(janela)
    if foco_ok:
        print("Janela preparada e foco confirmado.")
    else:
        print("Janela preparada, mas o foco nao foi confirmado.")
    return foco_ok
 
 
# ---------------------------------------------------------------------------
# 8. Revalidar (ou recuperar) o foco antes de qualquer acao critica
# ---------------------------------------------------------------------------
def revalidar_ou_recuperar_foco(janela):
    if janela_correta_esta_ativa():
        print("Foco confirmado. Podemos continuar.")
        return True
 
    print("Foco incorreto. Tentando recuperar a janela controlada...")
    if ativar_janela_com_fallback(janela):
        print("Foco recuperado com sucesso.")
        return True
 
    print("O foco nao foi recuperado. A automacao deve parar.")
    return False
 
 
# ---------------------------------------------------------------------------
# 9. Escrever no campo de texto
# ---------------------------------------------------------------------------
def clicar_no_campo_de_texto(janela):
    x_texto = janela.left + 80
    y_texto = janela.top + 150
    pyautogui.click(x_texto, y_texto)
    time.sleep(PAUSA_CURTA)
 
 
def escrever_parte_1(janela):
    clicar_no_campo_de_texto(janela)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
 
    linhas = [
        "RELATORIO - GRUPO 3 - ROBO RESILIENTE",
        "Parte 1: janela localizada, preparada e focada",
        "Aguardando simulacao de mudanca de foco...",
    ]
    for linha in linhas:
        pyautogui.write(linha, interval=0.02)
        pyautogui.press("enter")
    print("Parte 1 do relatorio digitada.")
 
 
def escrever_parte_2(janela):
    clicar_no_campo_de_texto(janela)
    linhas = [
        "Parte 2: foco revalidado/recuperado com sucesso",
        "Teclado: hotkey, press e write utilizados",
        "Mouse: click, moveTo e dragTo demonstrados a seguir",
    ]
    for linha in linhas:
        pyautogui.write(linha, interval=0.02)
        pyautogui.press("enter")
    print("Parte 2 do relatorio digitada.")
 
 
# ---------------------------------------------------------------------------
# 10. Demonstrar arraste
# ---------------------------------------------------------------------------
def demonstrar_arraste(janela):
    x_inicio = janela.left + 120
    y_inicio = janela.top + 370
    x_final = janela.left + 470
    y_final = janela.top + 370
 
    pyautogui.moveTo(x_inicio, y_inicio, duration=0.5)
    pyautogui.click()
    time.sleep(PAUSA_CURTA)
    pyautogui.dragTo(x_final, y_final, duration=1.5, button="left")
    print("Arraste demonstrado com dragTo().")
 
 
# ---------------------------------------------------------------------------
# 11. Gerar evidencia
# ---------------------------------------------------------------------------
def gerar_evidencia(caminho, atualizar_status=None, mensagem_status=""):
    time.sleep(PAUSA_CURTA)
    if atualizar_status:
        atualizar_status(mensagem_status)
        time.sleep(0.3)
    pyautogui.screenshot(str(caminho))
    print("Evidencia salva em:", caminho)
 
 
def mostrar_erro_na_tela(root, titulo, mensagem):
    try:
        root.after(0, lambda: messagebox.showerror(titulo, mensagem))
    except Exception as e:
        print("Nao foi possivel mostrar a caixa de erro:", e)
    time.sleep(0.5)
 
 
# ---------------------------------------------------------------------------
# 12. Orquestracao do fluxo completo
# ---------------------------------------------------------------------------
def executar_automacao(root):
 
    def atualizar_status(texto):
        try:
            root.status_label.config(text=texto)
        except Exception:
            pass
 
    print("=" * 60)
    print("Iniciando automacao resiliente (Grupo 3) - ARQUIVO OFICIAL.")
    verificar_ambiente()
 
    janela = localizar_janela()
    if janela is None:
        print("Automacao encerrada: sem janela, sem acao.")
        return
 
    if not preparar_janela(janela):
        print("Automacao encerrada: nao foi possivel confirmar o foco inicial.")
        return
 
    if not revalidar_ou_recuperar_foco(janela):
        print("Automacao encerrada: foco inseguro antes da digitacao (parte 1).")
        return
 
    atualizar_status("Escrevendo parte 1 do relatorio...")
    escrever_parte_1(janela)
 
    atualizar_status(f"AGORA SIMULE MUDANCA DE FOCO ({TEMPO_PARA_TROCAR_FOCO}s)")
    print(f"\n>>> AGORA SIMULE MUDANCA DE FOCO. Clique em outra janela. "
          f"Voce tem {TEMPO_PARA_TROCAR_FOCO} segundos. <<<\n")
    time.sleep(TEMPO_PARA_TROCAR_FOCO)
 
    if not revalidar_ou_recuperar_foco(janela):
        print("Automacao encerrada: foco nao recuperado apos a pausa programada.")
        atualizar_status("FALHA: foco nao recuperado. Automacao interrompida.")
        mostrar_erro_na_tela(
            root, "Falha de foco - Grupo 3",
            "O robo perdeu o foco da janela controlada e nao\n"
            "conseguiu recupera-lo. Automacao interrompida\n"
            "por seguranca.",
        )
        gerar_evidencia(EVIDENCIA_FALHA, atualizar_status, "FALHA: foco nao recuperado.")
        print("=" * 60)
        return
 
    atualizar_status("Foco recuperado. Escrevendo parte 2...")
    escrever_parte_2(janela)
 
    if not revalidar_ou_recuperar_foco(janela):
        print("Automacao encerrada: foco inseguro antes do arraste.")
        atualizar_status("FALHA: foco inseguro antes do arraste.")
        mostrar_erro_na_tela(
            root, "Falha de foco - Grupo 3",
            "O foco mudou antes do arraste e nao foi\n"
            "recuperado. Automacao interrompida por\n"
            "seguranca.",
        )
        gerar_evidencia(EVIDENCIA_FALHA, atualizar_status, "FALHA: foco inseguro antes do arraste.")
        print("=" * 60)
        return
 
    demonstrar_arraste(janela)
 
    atualizar_status("Automacao concluida com sucesso.")
    gerar_evidencia(EVIDENCIA_SUCESSO, atualizar_status, "SUCESSO: automacao concluida.")
    print("Automacao finalizada com seguranca.")
    print("=" * 60)
 
 
def iniciar_automacao_em_thread(root):
    tarefa = threading.Thread(target=executar_automacao, args=(root,), daemon=True)
    tarefa.start()
 
 
def main():
    app = criar_painel_controlado()
    app.after(TEMPO_INICIAL * 1000, lambda: iniciar_automacao_em_thread(app))
    app.mainloop()
 
 
if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
#                          O ENTREGAVEL OFICIAL  
# 
# ROTEIRO DOS DOIS TESTES OBRIGATORIOS (para o relatorio/apresentacao)
# ---------------------------------------------------------------------------
#   1. Qual era o problema da atividade?
#Garantir que o robô não continue agindo numa janela errada quando o foco muda no meio da execução — testado provocando a perda de foco de propósito durante a pausa programada, sem nenhum atalho de código.
#
#   2. Qual condição precisava ser verdadeira antes de o robô agir?
#Que janela_correta_esta_ativa() retornasse True, comparando gw.getActiveWindow().title com "Painel Grupo 3 - Robo Resiliente".
#
#   3. Quais scripts ou comandos anteriores foram reaproveitados?
#localizar_janela, preparar_janela, janela_correta_esta_ativa e ativar_janela_com_fallback, praticamente idênticos ao script de fechamento do bloco GUI. revalidar_ou_recuperar_foco combina os dois: checa o foco e, se necessário, tenta o fallback antes de desistir.
#
#   4. O que foi alterado para tornar a solução mais robusta?
#A chamada a revalidar_ou_recuperar_foco passou a acontecer em três pontos: antes da Parte 1, logo depois da pausa programada, e antes do arraste — em vez de confiar só na checagem feita na preparação inicial.
#
#   5. Onde está o tratamento de falha?
#No try/except dentro de ativar_janela_com_fallback (captura falha de activate()), e nas duas ramificações de if not revalidar_ou_recuperar_foco(janela): dentro de executar_automacao — cada uma atualiza o rótulo de status pra "FALHA:...", chama gerar_evidencia(EVIDENCIA_FALHA, ...) e só depois retorna, encerrando a função.
#
#   6. Qual evidência comprova a execução?
#evidencia_grupo3_falha.png, tirado com pyautogui.screenshot() no momento exato da parada — mostrando o painel controlado com o rótulo de status já atualizado pra mensagem de falha (não tem popup nessa versão, então a evidência de que o robô "percebeu" o problema é o próprio texto de status na janela, junto com as mensagens do Terminal).
#
#   7. O que poderia falhar em outro computador?
#activate() pode se comportar diferente dependendo da política de foco do Windows (algumas versões bloqueiam troca de foco entre processos sem interação do usuário), fazendo o fallback ser acionado com mais ou menos frequência do que na máquina de vocês. Resolução e escala do Windows afetam as coordenadas fixas usadas nos cliques.
#
#   8. O que o grupo mudaria antes de usar em ambiente real?
#Adicionar mais tentativas de recuperação com espera progressiva, em vez de uma única tentativa de activate() seguida de um único clique de fallback. E registrar cada falha em arquivo de log, não só em print() no Terminal — pra ter rastreabilidade fora da demonstração ao vivo.