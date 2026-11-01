import time
import re
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def salvar_acumulando(novos_dados, ficheiro="apartamentos_brasilia.csv"):
    df_novos = pd.DataFrame(novos_dados)
    
    if os.path.exists(ficheiro):
        df_existente = pd.read_csv(ficheiro)
        df_completo = pd.concat([df_existente, df_novos], ignore_index=True)
        df_completo = df_completo.drop_duplicates(subset=["preco", "area_m2", "bairro", "quartos"])
    else:
        df_completo = df_novos.drop_duplicates(subset=["preco", "area_m2", "bairro", "quartos"])
        
    df_completo.to_csv(ficheiro, index=False, encoding="utf-8-sig")
    print(f"\nProgresso: {len(df_completo)} imóveis únicos acumulados no ficheiro '{ficheiro}'.")

def configurar_driver():
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def extrair_bairro(texto):
    bairros = [
        "Asa Norte", "Asa Sul", "Sudoeste", "Noroeste", "Águas Claras",
        "Guará", "Taguatinga", "Lago Norte", "Lago Sul", "Samambaia"
    ]
    for b in bairros:
        if b.lower() in texto.lower():
            return b
    linhas = [l.strip() for l in texto.split("\n") if l.strip()]
    return linhas[-1].split(",")[0] if linhas else "Brasília"

def coletar_apartamentos(max_paginas=12, meta_minima=150):
    # URL aluguel de apartamentos em Brasília
    base_url = "https://www.wimoveis.com.br/apartamentos-aluguel-distrito-federal"
    driver = configurar_driver()
    imoveis = []

    try:
        for pagina in range(1, max_paginas + 1):
            url = f"{base_url}-pagina-{pagina}.html" if pagina > 1 else f"{base_url}.html"
            print(f"\nAcessando página {pagina}: {url}")
            driver.get(url)

            try:
                WebDriverWait(driver, 12).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@data-qa, 'posting')] | //div[contains(@class, 'PostingCard')]"))
                )
            except Exception:
                print("Tempo limite excedido ou página final atingida.")
                break

            # Rolagem para carregar anúncios dinâmicos
            for _ in range(4):
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(0.6)

            cards = driver.find_elements(By.XPATH, "//div[contains(@data-qa, 'posting')] | //div[contains(@class, 'PostingCard')]")
            print(f"Cards detectados na página {pagina}: {len(cards)}")

            for card in cards:
                texto = card.text
                if not texto.strip():
                    continue

                # Preço
                preco_match = re.search(r"R\$\s*([\d\.]+)", texto)
                preco = preco_match.group(0) if preco_match else None

                # Área (m²)
                area_match = re.search(r"(\d+)\s*m²", texto, re.IGNORECASE)
                area = area_match.group(1) if area_match else None

                # Quartos
                quartos_match = re.search(r"(\d+)\s*quarto", texto, re.IGNORECASE)
                quartos = quartos_match.group(1) if quartos_match else 1

                # Vagas
                vagas_match = re.search(r"(\d+)\s*vaga", texto, re.IGNORECASE)
                vagas = vagas_match.group(1) if vagas_match else 0

                # Bairro
                bairro = extrair_bairro(texto)

                if preco and area:
                    imoveis.append({
                        "preco": preco,
                        "area_m2": area,
                        "quartos": quartos,
                        "vagas": vagas,
                        "bairro": bairro,
                        "tipo": "Apartamento"
                    })

            # Remoção de duplicatas em tempo real para controle da contagem
            total_unicos = len(pd.DataFrame(imoveis).drop_duplicates())
            print(f"Total de imóveis únicos coletados: {total_unicos}")

            if total_unicos >= meta_minima:
                print(f"\nMeta de {meta_minima} imóveis atingida com sucesso!")
                break

            time.sleep(2)

    finally:
        driver.quit()

    df = pd.DataFrame(imoveis).drop_duplicates()
    return df

if __name__ == "__main__":
    df_resultado = coletar_apartamentos(max_paginas=12, meta_minima=150)
    salvar_acumulando(df_resultado, "apartamentos_brasilia.csv")