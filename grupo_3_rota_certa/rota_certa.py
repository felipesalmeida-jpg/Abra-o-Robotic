from pathlib import Path
import csv
#import time
from decimal import Decimal, InvalidOperation

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException



PASTA = Path(__file__).resolve().parent
ARQUIVO_HTML = PASTA / 'catalogo.html'
CAMPOS = ['id', 'nome', 'origem', 'destino', 'valor', 'modalidade']


def capturar_html():
    if not ARQUIVO_HTML.exists():
        raise FileNotFoundError(f'Arquivo não encontrado: {ARQUIVO_HTML.name}')

    url = ARQUIVO_HTML.as_uri()

    driver = webdriver.Edge()
    try:
        driver.get(url)
        espera = WebDriverWait(driver, timeout=10)
        espera.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'article.frete')
        ))
        html = driver.page_source
 #      time.sleep(3)          # TEMPORÁRIO: remover depois do teste
    finally:
        driver.quit()

    return html


def extrair_registros(html):
    soup = BeautifulSoup(html, 'html.parser')
    registros = []

    for bloco in soup.select('article.frete'):
        registro = {}

        for campo in CAMPOS:
            tag = bloco.select_one('.' + campo)
            if tag is None:
                registro[campo] = None                    # elemento ausente
            else:
                registro[campo] = tag.get_text(strip=True)  # '' se estiver vazio

        link_tag = bloco.select_one('a.link')
        if link_tag is None:
            registro['link'] = None                       # <a> ausente
        else:
            registro['link'] = link_tag.get('href')       # None se não tiver href

        registros.append(registro)

    return registros


# TODO 3: validar(registro)      -> pendências e status_dado
# TODO 4: converter_valor(texto) -> Decimal ou None
# TODO 5: selecionar(registros)  -> regra do gerente + ordenação
# TODO 6: escrever_csvs(...)     -> todos, selecionados, pendencias
# TODO 7: main()                 -> junta tudo, resumo, tratamento de falhas


if __name__ == '__main__':
    html = capturar_html()
    registros = extrair_registros(html)
    for r in registros:
        print(r)