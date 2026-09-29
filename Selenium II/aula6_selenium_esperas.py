# ============================================================
# RPA - SELENIUM II
# Aula 6 - Esperas, páginas dinâmicas e navegação controlada
# ============================================================

from pathlib import Path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

PASTA = Path(__file__).resolve().parent
ARQUIVO_HTML = PASTA / "pagina_dinamica_selenium.html"
PASTA_EVIDENCIAS = PASTA / "evidencias"
PASTA_EVIDENCIAS.mkdir(exist_ok=True)

EVIDENCIA_SUCESSO = PASTA_EVIDENCIAS / "evidencia_esperas_sucesso.png"
EVIDENCIA_ERRO = PASTA_EVIDENCIAS / "evidencia_esperas_erro.png"

TEMPO_ESPERA = 10
TEMPO_OBSERVACAO = 1

BTN_CARREGAR = (By.ID, "btnCarregar")
RESULTADO = (By.ID, "resultado")
LISTA = (By.CSS_SELECTOR, "#lista li")
BTN_DETALHE = (By.ID, "btnDetalhe")
DETALHE = (By.ID, "detalhe")

def salvar_evidencia(driver, caminho):
    try:
        screenshot_salvo = driver.save_screenshot(str(caminho))
        if screenshot_salvo and caminho.exists():
            print("\nEvidência salva com sucesso:\n", caminho)
            return True
        print("\nATENÇÃO: a evidência não foi confirmada.")
        return False
    except Exception as erro:
        print("\nNão foi possível salvar a evidência.\nDetalhes:", erro)
        return False

print("=" * 65)
print("RPA - SELENIUM II")
print("Esperas, páginas dinâmicas e navegação controlada")
print("=" * 65)
print("\n1. Verificando o arquivo HTML...")

if not ARQUIVO_HTML.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {ARQUIVO_HTML}")

print("Arquivo encontrado:\n", ARQUIVO_HTML)
PAGINA = ARQUIVO_HTML.as_uri()
driver = None
etapa_atual = "Preparação"

try:
    etapa_atual = "Abertura do navegador"
    print("\n2. Abrindo o Microsoft Edge...")
    driver = webdriver.Edge()
    driver.maximize_window()
    print("Navegador aberto.")
    
    wait = WebDriverWait(driver, TEMPO_ESPERA)
    
    etapa_atual = "Carregamento da página"
    print("\n3. Carregando a página dinâmica...")
    driver.get(PAGINA)
    wait.until(EC.title_contains("Página Dinâmica"))
    print("Página aberta corretamente.")
    print("Título:", driver.title)
    time.sleep(TEMPO_OBSERVACAO)
    
    etapa_atual = "Espera pelo botão Carregar dados"
    print("\n4. Esperando o botão 'Carregar dados' ficar clicável...")
    botao_carregar = wait.until(EC.element_to_be_clickable(BTN_CARREGAR))
    print("Botão pronto para clique.")
    
    etapa_atual = "Clique no botão Carregar dados"
    print("\n5. Clicando em 'Carregar dados'...")
    botao_carregar.click()
    print("Clique realizado.")
    
    etapa_atual = "Espera pelo texto de confirmação"
    print("\n6. Esperando a página concluir o carregamento...")
    wait.until(EC.text_to_be_present_in_element(RESULTADO, "Dados carregados com sucesso."))
    print("Mensagem de carregamento encontrada.")
    
    resultado = driver.find_element(*RESULTADO)
    print("\nResultado apresentado pela página:\n", resultado.text)
    
    etapa_atual = "Espera pela lista de itens"
    print("\n7. Esperando os itens da lista serem criados...")
    itens = wait.until(EC.presence_of_all_elements_located(LISTA))
    
    print("\nQuantidade de itens encontrados:", len(itens))
    print("Itens encontrados:")
    for numero, item in enumerate(itens, start=1):
        print(f"{numero}. {item.text}")
        
    print("\n" + "=" * 65)
    print("PAUSA PARA OBSERVAÇÃO")
    print("=" * 65)
    print("\nA página deve mostrar os dados carregados, os 3 nomes e o botão 'Abrir detalhe'.")
    input("\nPressione ENTER no Terminal para continuar...")
    
    janela_inicial = driver.current_window_handle
    print("\nAba principal registrada.")
    
    etapa_atual = "Espera pelo botão Abrir detalhe"
    print("\n8. Esperando o botão 'Abrir detalhe' ficar disponível...")
    botao_detalhe = wait.until(EC.element_to_be_clickable(BTN_DETALHE))
    print("Botão de detalhe disponível.")
    
    print("\n" + "=" * 65)
    print("PRÓXIMA ETAPA: NOVA ABA")
    print("=" * 65)
    input("\nPressione ENTER para abrir a aba de detalhes...")
    
    etapa_atual = "Abertura da nova aba"
    print("\nAbrindo nova aba...")
    botao_detalhe.click()
    wait.until(EC.number_of_windows_to_be(2))
    print("Nova aba detectada.")
    
    etapa_atual = "Troca de contexto"
    nova_janela = None
    for janela in driver.window_handles:
        if janela != janela_inicial:
            nova_janela = janela
            break
            
    if nova_janela is None:
        raise RuntimeError("A nova aba não foi identificada.")
        
    driver.switch_to.window(nova_janela)
    print("Controle transferido para a nova aba.")
    
    etapa_atual = "Leitura do detalhe"
    print("\nEsperando o conteúdo do detalhe...")
    detalhe = wait.until(EC.visibility_of_element_located(DETALHE))
    print("Detalhe carregado.")
    print("\nConteúdo encontrado na nova aba:\n", detalhe.text)
    
    print("\n" + "=" * 65)
    print("NOVA ABA CONTROLADA")
    print("=" * 65)
    input("\nPressione ENTER para gerar a evidência...")
    
    etapa_atual = "Geração da evidência"
    print("\n9. Salvando evidência...")
    salvar_evidencia(driver, EVIDENCIA_SUCESSO)
    
    print("\n" + "=" * 65)
    print("AUTOMAÇÃO CONCLUÍDA COM SUCESSO")
    print("=" * 65)
    
    input("\nPressione ENTER no Terminal para fechar o navegador...")

except TimeoutException as erro:
    print("\nTIMEOUT")
    print("Etapa em que a execução parou:\n", etapa_atual)
    if driver is not None:
        salvar_evidencia(driver, EVIDENCIA_ERRO)
    print("Detalhes técnicos:\n", erro)

except Exception as erro:
    print("\nFALHA DURANTE A AUTOMAÇÃO")
    print("Etapa em que a execução parou:\n", etapa_atual)
    if driver is not None:
        salvar_evidencia(driver, EVIDENCIA_ERRO)
    print("Detalhes:\n", erro)

finally:
    if driver is not None:
        print("\n10. Encerrando o navegador...")
        try:
            driver.quit()
        except:
            pass