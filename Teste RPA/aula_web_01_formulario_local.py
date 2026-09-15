# ============================================================
# RPA - Automação Web com Selenium
# Aula 5 - Primeira automação Web
# ============================================================
from pathlib import Path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# ============================================================
# 1. CONFIGURAÇÕES
# ============================================================
# Tempo entre as principais etapas.
# Serve apenas para facilitar a observação durante a aula.
TEMPO_ETAPA = 2

# Descobre a pasta onde este script está salvo.
PASTA = Path(__file__).resolve().parent

# Arquivo HTML que será automatizado.
ARQUIVO_HTML = PASTA / "formulario_teste_selenium.html"

# Verifica se o HTML realmente existe.
if not ARQUIVO_HTML.exists():
    print("=" * 60)
    print("ERRO: arquivo HTML não encontrado.")
    print("O programa procurou em:")
    print(ARQUIVO_HTML)
    print("=" * 60)
    raise FileNotFoundError(f"Arquivo não encontrado: {ARQUIVO_HTML}")

# Converte o caminho do HTML para um endereço
# que o navegador consegue abrir.
PAGINA = ARQUIVO_HTML.as_uri()

# ============================================================
# 2. PASTA DE EVIDÊNCIAS
# ============================================================
PASTA_EVIDENCIAS = PASTA / "evidencias"

# Cria a pasta automaticamente se ela não existir.
PASTA_EVIDENCIAS.mkdir(exist_ok=True)

# Caminho completo da imagem.
EVIDENCIA = PASTA_EVIDENCIAS / "evidencia_web_01.png"

print("Arquivo HTML localizado:")
print(ARQUIVO_HTML)
print()
print("Pasta de evidências:")
print(PASTA_EVIDENCIAS)


# ============================================================
# 3. ABRIR O NAVEGADOR
# ============================================================
def abrir_navegador():
    try:
        print()
        print("Tentando iniciar o Microsoft Edge...")
        driver = webdriver.Edge()
        print("Navegador Edge iniciado.")
        return driver
    except Exception as erro_edge:
        print("Edge não iniciou.")
        print("Motivo:", erro_edge)
        print()
        print("Tentando iniciar o Google Chrome...")
        driver = webdriver.Chrome()
        print("Navegador Chrome iniciado.")
        return driver


# ============================================================
# 4. PREENCHER O FORMULÁRIO
# ============================================================
def preencher_formulario(driver):
    print()
    print("Localizando os elementos do formulário...")

    # --------------------------------------------------------
    # Nome - localizado por ID
    # --------------------------------------------------------
    campo_nome = driver.find_element(By.ID, "nome")

    # --------------------------------------------------------
    # E-mail - localizado por NAME
    # --------------------------------------------------------
    campo_email = driver.find_element(By.NAME, "email")

    # --------------------------------------------------------
    # Setor - localizado por CSS Selector
    # --------------------------------------------------------
    setor = driver.find_element(By.CSS_SELECTOR, "#setor")

    # --------------------------------------------------------
    # Prioridade - localizada por XPath
    # --------------------------------------------------------
    prioridade = driver.find_element(By.XPATH, "//select[@id='prioridade']")

    # --------------------------------------------------------
    # Checkbox
    # --------------------------------------------------------
    aceite = driver.find_element(By.CSS_SELECTOR, "input[name='aceite']")

    print("Elementos encontrados.")
    time.sleep(TEMPO_ETAPA)

    # ========================================================
    # PREENCHIMENTO
    # ========================================================
    print()
    print("Preenchendo o campo Nome...")
    campo_nome.clear()
    campo_nome.send_keys("Mariana Alves")
    time.sleep(TEMPO_ETAPA)

    print("Preenchendo o campo E-mail...")
    campo_email.clear()
    campo_email.send_keys("mariana@empresa.com")
    time.sleep(TEMPO_ETAPA)

    print("Selecionando o setor...")
    setor.send_keys("Suporte")
    time.sleep(TEMPO_ETAPA)

    print("Selecionando a prioridade...")
    prioridade.send_keys("Alta")
    time.sleep(TEMPO_ETAPA)

    print("Marcando a confirmação...")
    aceite.click()
    time.sleep(TEMPO_ETAPA)

    print()
    print("Formulário preenchido.")


# ============================================================
# 5. REGISTRAR RESULTADO
# ============================================================
def registrar_resultado(driver):
    print()
    print("Localizando o botão Registrar...")
    botao = driver.find_element(By.ID, "btnRegistrar")
    print("Botão localizado.")
    time.sleep(TEMPO_ETAPA)

    print("Executando clique...")
    botao.click()
    time.sleep(TEMPO_ETAPA)

    # ========================================================
    # LER O RESULTADO
    # ========================================================
    resultado = driver.find_element(By.ID, "resultado")
    print()
    print("Resultado apresentado pela página:")
    print(resultado.text)

    # ========================================================
    # SALVAR EVIDÊNCIA
    # ========================================================
    print()
    print("Gerando screenshot...")
    screenshot_salvo = driver.save_screenshot(str(EVIDENCIA))

    # Verificação dupla:
    # retorno do Selenium + existência do arquivo.
    if screenshot_salvo and EVIDENCIA.exists():
        print()
        print("EVIDÊNCIA CRIADA COM SUCESSO.")
        print("Arquivo:")
        print(EVIDENCIA)
    else:
        print()
        print("ATENÇÃO: a evidência não foi criada.")


# ============================================================
# 6. FLUXO PRINCIPAL
# ============================================================
driver = None
try:
    print()
    print("=" * 60)
    print("INICIANDO AUTOMAÇÃO WEB")
    print("=" * 60)

    # --------------------------------------------------------
    # Abrir navegador
    # --------------------------------------------------------
    driver = abrir_navegador()
    time.sleep(TEMPO_ETAPA)

    # --------------------------------------------------------
    # Abrir a página
    # --------------------------------------------------------
    print()
    print("Abrindo página de teste...")
    driver.get(PAGINA)
    print("Página carregada.")
    time.sleep(TEMPO_ETAPA)

    # --------------------------------------------------------
    # Preencher formulário
    # --------------------------------------------------------
    preencher_formulario(driver)

    # --------------------------------------------------------
    # Registrar resultado
    # --------------------------------------------------------
    registrar_resultado(driver)

    print()
    print("=" * 60)
    print("AUTOMAÇÃO CONCLUÍDA COM SUCESSO")
    print("=" * 60)

    # ========================================================
    # PAUSA CONTROLADA
    # ========================================================
    print()
    print("O navegador permanecerá aberto.")
    print("Observe o resultado e a evidência.")
    print()
    input("Pressione ENTER no Terminal para fechar o navegador...")

# ============================================================
# 7. ELEMENTO NÃO ENCONTRADO
# ============================================================
except NoSuchElementException as erro:
    print()
    print("=" * 60)
    print("Elemento não encontrado.")
    print("Verifique o HTML e o localizador utilizado.")
    print()
    print("Detalhes:", erro)
    print("=" * 60)
    input("Pressione ENTER para encerrar...")

# ============================================================
# 8. OUTRA FALHA
# ============================================================
except Exception as erro:
    print()
    print("=" * 60)
    print("Falha inesperada durante a automação.")
    print()
    print("Detalhes:", erro)
    print("=" * 60)
    input("Pressione ENTER para encerrar...")

# ============================================================
# 9. ENCERRAMENTO
# ============================================================
finally:
    if driver is not None:
        print()
        print("Encerrando o navegador...")
        driver.quit()
        print("Navegador encerrado.")
