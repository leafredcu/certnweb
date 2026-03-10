import streamlit as st
from fpdf import FPDF
import math
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO GERAL
# ==============================================================================
st.set_page_config(page_title="Cálculo Valor Venal 2025", layout="wide")

# ==============================================================================
# DADOS EXATOS DO DECRETO Nº 1.849/2025
# ==============================================================================

# ANEXO III - EDIFICAÇÕES
VALORES_EDIFICACAO = {
    # PADRÃO BAIXO
    "R-1 - Residencial unifamiliar - PADRÃO BAIXO - Novo": 2369.59,
    "R-1 - Residencial unifamiliar - PADRÃO BAIXO - Bom": 1895.67,
    "R-1 - Residencial unifamiliar - PADRÃO BAIXO - Regular": 1516.54,
    "R-1 - Residencial unifamiliar - PADRÃO BAIXO - Precário": 1213.23,

    "PP-4 - Residencial multifamiliar popular. Horizontal e vertical até 4 pavimentos - PADRÃO BAIXO - Novo": 1808.05,
    "PP-4 - Residencial multifamiliar popular. Horizontal e vertical até 4 pavimentos - PADRÃO BAIXO - Bom": 1446.44,
    "PP-4 - Residencial multifamiliar popular. Horizontal e vertical até 4 pavimentos - PADRÃO BAIXO - Regular": 1157.15,
    "PP-4 - Residencial multifamiliar popular. Horizontal e vertical até 4 pavimentos - PADRÃO BAIXO - Precário": 925.72,

    "R-8 - Residencial multifamiliar a partir de 5 pavimentos - PADRÃO BAIXO - Novo": 2127.12,
    "R-8 - Residencial multifamiliar a partir de 5 pavimentos - PADRÃO BAIXO - Bom": 1701.70,
    "R-8 - Residencial multifamiliar a partir de 5 pavimentos - PADRÃO BAIXO - Regular": 1361.36,
    "R-8 - Residencial multifamiliar a partir de 5 pavimentos - PADRÃO BAIXO - Precário": 1089.09,

    "PIS - Residencial multifamiliar - Projeto de interesse social: Horizontal ou vertical - Novo": 1638.90,
    "PIS - Residencial multifamiliar - Projeto de interesse social: Horizontal ou vertical - Bom": 1311.12,
    "PIS - Residencial multifamiliar - Projeto de interesse social: Horizontal ou vertical - Regular": 1048.90,
    "PIS - Residencial multifamiliar - Projeto de interesse social: Horizontal ou vertical - Precário": 839.12,

    # PADRÃO NORMAL
    "R-1 - Residencial unifamiliar padrão normal - Novo": 2835.15,
    "R-1 - Residencial unifamiliar padrão normal - Bom": 2268.12,
    "R-1 - Residencial unifamiliar padrão normal - Regular": 1814.50,
    "R-1 - Residencial unifamiliar padrão normal - Precário": 1451.60,

    "R-2 a 7 - Residencial multifamiliar - prédio popular - PADRÃO NORMAL - Novo": 2700.16,
    "R-2 a 7 - Residencial multifamiliar - prédio popular - PADRÃO NORMAL - Bom": 2160.13,
    "R-2 a 7 - Residencial multifamiliar - prédio popular - PADRÃO NORMAL - Regular": 1728.10,
    "R-2 a 7 - Residencial multifamiliar - prédio popular - PADRÃO NORMAL - Precário": 1382.48,

    "R-8 ou mais - Residencial multifamiliar - PADRÃO NORMAL - Novo": 2565.15,
    "R-8 ou mais - Residencial multifamiliar - PADRÃO NORMAL - Bom": 2052.12,
    "R-8 ou mais - Residencial multifamiliar - PADRÃO NORMAL - Regular": 1641.70,
    "R-8 ou mais - Residencial multifamiliar - PADRÃO NORMAL - Precário": 1313.36,

    # PADRÃO ALTO
    "R-1 - Residencial unifamiliar padrão alto - Novo": 3530.93,
    "R-1 - Residencial unifamiliar padrão alto - Bom": 2824.74,
    "R-1 - Residencial unifamiliar padrão alto - Regular": 2259.80,
    "R-1 - Residencial unifamiliar padrão alto - Precário": 1807.84,

    "R-3 ou mais - Residencial multifamiliar, padrão alto - Novo": 2878.94,
    "R-3 ou mais - Residencial multifamiliar, padrão alto - Bom": 2303.15,
    "R-3 ou mais - Residencial multifamiliar, padrão alto - Regular": 1842.52,
    "R-3 ou mais - Residencial multifamiliar, padrão alto - Precário": 1474.02,

    # COMERCIAL
    "CSL-1 - Comercial um pavimento / Comercial loja única - PADRÃO NORMAL - Novo": 1846.54,
    "CSL-1 - Comercial um pavimento / Comercial loja única - PADRÃO NORMAL - Bom": 1477.23,
    "CSL-1 - Comercial um pavimento / Comercial loja única - PADRÃO NORMAL - Regular": 1181.79,
    "CSL-1 - Comercial um pavimento / Comercial loja única - PADRÃO NORMAL - Precário": 945.43,

    "CSL-2 - Comercial até 2 pavimentos - PADRÃO NORMAL - Novo": 2303.15,
    "CSL-2 - Comercial até 2 pavimentos - PADRÃO NORMAL - Bom": 1842.52,
    "CSL-2 - Comercial até 2 pavimentos - PADRÃO NORMAL - Regular": 1474.02,
    "CSL-2 - Comercial até 2 pavimentos - PADRÃO NORMAL - Precário": 1179.21,

    "CSL-4 - Comercial de 4 ou mais pavimentos - PADRÃO NORMAL - Novo": 2829.16,
    "CSL-4 - Comercial de 4 ou mais pavimentos - PADRÃO NORMAL - Bom": 2263.33,
    "CSL-4 - Comercial de 4 ou mais pavimentos - PADRÃO NORMAL - Regular": 1810.66,
    "CSL-4 - Comercial de 4 ou mais pavimentos - PADRÃO NORMAL - Precário": 1448.53,

    "CSL-1 - Comercial um pavimento / Comercial loja única - PADRÃO ALTO - Novo": 2357.63,
    "CSL-1 - Comercial um pavimento / Comercial loja única - PADRÃO ALTO - Bom": 1886.10,
    "CSL-1 - Comercial um pavimento / Comercial loja única - PADRÃO ALTO - Regular": 1508.88,
    "CSL-1 - Comercial um pavimento / Comercial loja única - PADRÃO ALTO - Precário": 1207.11,

    "CSL-2 - Comercial até 2 pavimentos - PADRÃO ALTO - Novo": 2547.27,
    "CSL-2 - Comercial até 2 pavimentos - PADRÃO ALTO - Bom": 2037.82,
    "CSL-2 - Comercial até 2 pavimentos - PADRÃO ALTO - Regular": 1630.25,
    "CSL-2 - Comercial até 2 pavimentos - PADRÃO ALTO - Precário": 1304.20,

    "CSL-4 - Comercial de 4 ou mais pavimentos - PADRÃO ALTO - Novo": 3400.77,
    "CSL-4 - Comercial de 4 ou mais pavimentos - PADRÃO ALTO - Bom": 2720.62,
    "CSL-4 - Comercial de 4 ou mais pavimentos - PADRÃO ALTO - Regular": 2176.49,
    "CSL-4 - Comercial de 4 ou mais pavimentos - PADRÃO ALTO - Precário": 1741.19,

    # INDUSTRIAL
    "GI-1 - Galpão - PADRÃO BAIXO - Novo": 1246.66,
    "GI-1 - Galpão - PADRÃO BAIXO - Bom": 997.33,
    "GI-1 - Galpão - PADRÃO BAIXO - Regular": 797.86,
    "GI-1 - Galpão - PADRÃO BAIXO - Precário": 638.29,

    "GI-2 - Edifício Industrial - estrutura e cobertura metálica - PADRÃO NORMAL - Novo": 1745.32,
    "GI-2 - Edifício Industrial - estrutura e cobertura metálica - PADRÃO NORMAL - Bom": 1396.26,
    "GI-2 - Edifício Industrial - estrutura e cobertura metálica - PADRÃO NORMAL - Regular": 1117.01,
    "GI-2 - Edifício Industrial - estrutura e cobertura metálica - PADRÃO NORMAL - Precário": 893.61,

    "GI-3 - Edifício Industrial - estrutura mista - PADRÃO ALTO - Novo": 2547.27,
    "GI-3 - Edifício Industrial - estrutura mista - PADRÃO ALTO - Bom": 2037.82,
    "GI-3 - Edifício Industrial - estrutura mista - PADRÃO ALTO - Regular": 1630.25,
    "GI-3 - Edifício Industrial - estrutura mista - PADRÃO ALTO - Precário": 1304.20,

    "GI-4 - Edifício industrial - estrutura mista e mezanino - PADRÃO MUITO ALTO - Novo": 3056.72,
    "GI-4 - Edifício industrial - estrutura mista e mezanino - PADRÃO MUITO ALTO - Bom": 2445.38,
    "GI-4 - Edifício industrial - estrutura mista e mezanino - PADRÃO MUITO ALTO - Regular": 1956.30,
    "GI-4 - Edifício industrial - estrutura mista e mezanino - PADRÃO MUITO ALTO - Precário": 1565.04,

    "SEM CONSTRUÇÃO (Lote Vago)": 0.0
}

# ANEXO I - TERRENOS
VALORES_BAIRRO = {
    "Aleixa Ferreira: 01; 02; 03; 04; 05; 06; 07; 08; 09; 10; 11; 12; 13 e 14": 550.00,
    "Brasília - Região Antenas: Parte das quadras 15 e 16 com frente para rua Pedro Pinheiro": 200.00,
    "Brasília - Praça - Ponto de Ônibus: Parte das quadras 15 e 16 com frente para rua Maria Carlota; quadras 17; 18; 19; 20; 21; 22; 23; 24; 25; 26; 27; 28; 29; 30 e 31; Parte da quadra 32, 33 e 34; Parte das quadras 35 e 36 com frente para rua Afonso Pena": 390.00,
    "Brasília - Região Central: Parte da quadra 32, 33 e 34, 35 com frente para avenida Israel Pinheiro; Parte da quadra 36; 37; 38; 39; 40; 41; 42; 43; 44; 45; 46; 47; 48; 49; 50; 51; 52; 53; 54": 500.00,
    "Brasília - Região Mineirão Atacado: Parte das quadras 55; 56; 57; 58 60; 61 e 63; Quadras 59; 62; 64 e 65": 550.00,
    "Brasília II: Todas": 400.00,
    "Brasília II: Frente para Avenida São Lucas": 1000.00,
    "Cachoeira: Parte da quadra 01; quadras 02 e 03": 500.00,
    "Cachoeira: Quadras 04 e 05": 340.00,
    "Central Parque: Quadras 01 e 02; parte das quadras 03 e 04; parte da quadra 05": 1500.00,
    "Central Parque: Parte das quadras 03, 04 e 05": 1250.00,
    "Centro: Região próxima à rua Eduardo Cozac": 1250.00,
    "Centro: Região próxima ao Sarzedo Mall e rua José Luiz Rezende": 1000.00,
    "Chácara Satélite: Todas": 550.00,
    "Cinira de Freitas: Quadra 01": 1250.00,
    "Cinira de Freitas: Quadra 02": 1500.00,
    "Cinira de Freitas: Meio e fundo da quadra": 600.00,
    "Vila Eduardo Cozac: Frente para Rua Sabiá": 800.00,
    "São Joaquim: Todas": 500.00,
    "Condomínio Sarzedo I / Condomínio Sarzedo II: Parte interna": 400.00,
    "Distrito Industrial: Todas": 270.00,
    "Estâncias Eliane: Áreas remanescentes; sítios não parcelados": 200.00,
    "Sítio Tabatinga: Áreas remanescentes; sítios não parcelados": 100.00,
    "Fazenda Santa Rosa de Lima: Áreas remanescentes; sítios não parcelados": 340.00,
    "Imaculada Conceição: Parte da quadra 01; lote 01 da quadra 02; Quadra 03, com frente para avenida São Lucas": 1000.00,
    "Imaculada Conceição: Parte das quadras 01, 02 e 03; Quadras 04, 05, 06, 09 e 11": 500.00,
    "Imaculada Conceição: Quadras 07; 08; 10; 12; 13 e 14": 340.00,
    "Jardim Anchieta: Quadras 01; 02; 03; 04; 06; 09; 12; 13; 14; 16": 450.00,
    "Jardim Anchieta: Quadras 05; 07; 08; 10; 11; 15; 17; 18; 19; 20; 21; 22; 23; 24; 25": 300.00,
    "Jardim Das Oliveiras: Quadra 01 e parte da quadra 02 com frente para a MG-040": 700.00,
    "Jardim das Oliveiras: Parte da quadra 02; quadras 03, 04, 05, 06, 07, 08 e 09; área verde e áreas institucionais": 550.00,
    "Jardim Planalto: Todas": 340.00,
    "Jardim Santa Rosa: Parte da quadra 12 e parte da 35 com frente para rua 16; 13; 14; 15; 16; 17; 18; 19; 20; 22; 32; 33; 36; e 41; parte da área institucional 03": 500.00,
    "Jardim Santa Rosa: Parte das quadras 21, 20, 19, 18, parte da área institucional 03; parte das quadras 12, 35 e 36; quadras 05, 06, 07, 08, 09, 10, 11; parte da quadra 04; parte da quadra 33; quadra 24; 32; 44; 37; 38; 39; parte das quadras 40, 45 e 46; parte das quadras 23 e 03; quadras 01 e 02": 700.00,
    "Jardim Santa Rosa: Parte das quadras 40, 45 e 46 com frente para MG-040; parte das quadras 23 e 03 com frente para a MG-040": 1650.00,
    "Jardim Santa Rosa: Parte das quadras 04 e 33; quadra 25, 26 e 43; quadra 27; parte das quadras 28, 29 e 30": 1000.00,
    "Jardim Vera Cruz: Quadras 01; 02; 03; 04; 05; 06; 07; 08; 09; 10; Parte das quadras 11 e 12": 500.00,
    "Jardim Vera Cruz: Quadra 13": 340.00,
    "Jardim Vera Cruz - Fundos e Vila: Parte das quadras 11 e 12; fundos": 200.00,
    "Liberdade: Quadras 01; 02; 03; 04; 05 e 06; Parte das quadras 07 e 08 com frente para rua Ernesto Guevara; Quadras 09; 10; 11; 12; 13; 14 e 15": 600.00,
    "Liberdade: Parte das quadras 07 e 08 com frente para avenida Zumbi dos Palmares": 700.00,
    "Liberdade II: Todas": 200.00,
    "Região do Malongo: Todas": 220.00,
    "Região da Lonax I: Área das indústrias": 270.00,
    "Região da Lonax II: Área remanescente": 200.00,
    "Manoel Pinheiro: Todas": 600.00,
    "Pinheiros: Quadra 08A": 1500.00,
    "Pinheiros: Quadras 7A; 6A; 5A; 4A; 3A; 2A": 1250.00,
    "Pinheiros: Quadra 01A": 550.00,
    "Residencial Masterville: Parte das quadras 10, 06, 03, 04, 16, 17, 02, 37, 38, 40 e 35 com frente para Avenida das Palmeiras": 800.00,
    "Residencial Masterville: Parte das quadras 41, 42, 43, 44, 47, 48, 49, 50, 51, 52, 53, Área Institucional e Área Verde, com frente para a Alameda das Siriemas, Alameda das Andorinhas e Avenida das Palmeiras": 600.00,
    "Residencial Masterville: Quadra 01; parte das quadras 02 e 03; parte das quadras 04 e 06; quadra 05; parte das quadras 07 e 08; parte da quadra 15; quadras 16; 17; 18; 19; parte da quadra 20; parte da quadra 24; quadras 25; 26; 27; parte da quadra 28; parte das quadras 33, 34 e 35; parte das quadras 36; 37; 38 e 39 e 40": 550.00,
    "Residencial Masterville: Quadras 41; 42; 43; 44; 45; 46; 47; 48; 49; 50; 51; 52; 53; 54; áreas institucionais e áreas verdes": 500.00,
    "Residencial Masterville: Parte das quadras 07 e 08 com frente para Alameda das Begônias; parte das quadras 09, 10, 11, 12, 14": 440.00,
    "Residencial Masterville: Parte da quadra 15; parte da quadra 20; parte da quadra 24; parte da quadra 28; parte das quadras 33, 34 e 35 com frente para Alameda dos Flamboyants; quadras 29, 30, 31, 32. Parte das quadras 29, 23, 21; Quadras 22 e 13 e extensão da Avenida das Acácias": 340.00,
    "Riacho Da Mata I: Quadras 20; 21; 22; 23; 24; 25; 26; 27; 28; parte das quadras 29 e 30; quadras 31; 32; 33; 34; 35; 36; 37; 38 e 39; parte da quadra 19 (área verde) com frente para rua Araribá": 500.00,
    "Riacho Da Mata I: Parte da quadra 19 (área verde) frente para rua angelim; parte das quadras 29 e 30 frente para rua angelim": 800.00,
    "Riacho Da Mata II: Quadras 09; 10; 15; 16; 17; 18; Parte da quadra 19 com frente para rua Ipê Roxo": 450.00,
    "Riacho Da Mata III: Quadras 01; 02; 03; 04; 05; 06; 07; 08; 11; 12; 13 e 14": 390.00,
    "Santa Cecília: Parte das quadras 01; 02 e 03 (área institucional)": 600.00,
    "Santa Cecília: Parte das quadras 01; 02 e 03 (área institucional) com frente para avenida Zumbi dos Palmares e MG-040": 700.00,
    "Santa Mônica: Quadras 02; 03; 04; 05 e parte das quadras 01 e 09": 340.00,
    "Santa Mônica: Quadras 06; 07; 08 e 10": 500.00,
    "Santa Mônica: Parte das quadras 09 e 01, frente para rua Elói Cândido de Melo": 550.00,
    "Santa Rita: Quadras 01; 02; 03; 04; 05; 06; 07; 08; 09": 550.00,
    "Anexo ao Santa Rita Pousada Do Rei": 1000.00,
    "MG 040-Galpões": 550.00,
    "Santa Rosa De Lima: Todas": 600.00,
    "Santo Antônio: Quadras 01; 02; 03; 04; 05; 06; 07; 08; 09; 10; 11; 12; 17; 18; 19; 23; 24; 25; parte da quadra 26": 390.00,
    "Santo Antônio: Quadras 04, 08 e 12; Parte das quadras 03; 07; 11; 19; 18 com frente para Avenida Juscelino Dias Magalhães; Região da Vila Vicentina": 500.00,
    "Santo Antônio: 13; 14; 15; 16; 20; 21; 22; parte da quadra 26": 250.00,
    "Olaria: Frente para a avenida São Lucas": 1000.00,
    "Olaria: Meio da quadra": 500.00,
    "Olaria: Fundo da quadra": 340.00,
    "São Cristóvão: Frente para av. São Lucas": 1000.00,
    "São Cristóvão: Meio da quadra": 500.00,
    "São Cristóvão: Fundos": 340.00,
    "São Joaquim: Parte da área verde n° 01 e parte da área verde nº 02; quadras 08; 09; 10; 11; 12; 13; 14; 15; 16 e 17; área institucional 02 e 03; área verde 03 e 04": 500.00,
    "São Joaquim II (Praça): Parte das quadras 01 e 02; parte das quadras 03 e 07; parte da área verde n° 01 e parte da área verde nº 02; quadras 04; 05; 06; área institucional 01": 600.00,
    "São Joaquim: Parte das quadras 01 e 02 e parte das quadras 03 e 07 com frente para Avenida Rouxinol; parte da área verde nº 01 e parte da área verde nº 02": 800.00,
    "São Paulo: Frente para a avenida São Lucas": 1000.00,
    "São Paulo: Meio da quadra": 500.00,
    "São Paulo: Fundos": 340.00,
    "São Pedro: Parte das quadras 03 e 04 com frente para avenida São Lucas": 1000.00,
    "São Pedro: 02; 05; parte das quadras 03 e 04": 550.00,
    "São Pedro: 01; 06 e 07": 340.00,
    "Serra Azul: Parte das quadras 17, 18 e 19 e quadras 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35 e 36": 390.00,
    "Serra Azul: MG-040-Região BH Atacado e Galpões; Parte da área verde": 500.00,
    "Sítio da Lagoa - Fundos do BH Atacado": 1500.00,
    "Sítio da Lagoa: 01; 02; 03; 04; 05; 06; 07; 08; 37": 100.00,
    "Sítio Sarzedo: Todas": 220.00,
    "Perobas - Fundos": 500.00,
    "Perobas: Todas": 60.00,
    "Vila Satélite I: Frente para a Rua Joaquim Pedro de Oliveira": 600.00,
    "Vila Satélite I: Parte das quadras 01, 03, 04, 05, 13 e 14; quadras 07 e 08; quadra 06": 980.00,
    "Vila Satélite I: Parte das quadras 14, 05, 04, 03, e 01; parte das quadras 15 e 16; quadras 11, 10 e 09; quadra 12 e 17": 1250.00,
    "Vila Satélite II: Parte das quadras 02, 03, 04 e 05": 1500.00,
    "Vila Satélite II: Parte das quadras 02, 03, 04 e 05; quadra 06; quadras 07, 08, 09, 10 e 01": 1250.00,
    "Vista da Lagoa: Todas": 260.00,
    "Quintas da Lagoa: Todas": 300.00,
    "Quintas da Jangada: Parte das quadras 01 e 07; Quadras 03; 04; 05; 06; 08 e 09": 300.00,
    "Quintas da Jangada: Quadras 02, 10, 11 e 12 e parte das quadras 01 e 07, com frente para MG-040": 1000.00
}

# ==============================================================================
# FUNÇÕES DO SISTEMA
# ==============================================================================

def formatar_moeda(valor):
    s = "{:,.2f}".format(valor)
    return f"R$ {s.replace(',', '_').replace('.', ',').replace('_', '.')}"

def numero_por_extenso(n):
    if n == 0: return "ZERO REAIS"
    
    unidades = ["", "UM", "DOIS", "TRÊS", "QUATRO", "CINCO", "SEIS", "SETE", "OITO", "NOVE"]
    dezespeciais = ["DEZ", "ONZE", "DOZE", "TREZE", "QUATORZE", "QUINZE", "DEZESSEIS", "DEZESSETE", "DEZOITO", "DEZENOVE"]
    dezenas = ["", "", "VINTE", "TRINTA", "QUARENTA", "CINQUENTA", "SESSENTA", "SETENTA", "OITENTA", "NOVENTA"]
    centenas = ["", "CENTO", "DUZENTOS", "TREZENTOS", "QUATROCENTOS", "QUINHENTOS", "SEISCENTOS", "SETECENTOS", "OITOCENTOS", "NOVECENTOS"]

    def convert_group(num):
        if num == 100: return "CEM"
        s = ""
        c, d, u = (num // 100), (num % 100 // 10), (num % 10)
        
        if c > 0:
            s += centenas[c]
            if d > 0 or u > 0: s += " E "
        
        if d == 1:
            s += dezespeciais[u]
        elif d > 1:
            s += dezenas[d]
            if u > 0: s += " E " + unidades[u]
        elif u > 0:
            if c == 0: s += unidades[u]
            else: s += unidades[u]
        return s

    inteiro = int(n)
    centavos = int(round((n - inteiro) * 100))
    parts = []
    
    bilhao = (inteiro // 1000000000) % 1000
    if bilhao > 0: parts.append(f"{convert_group(bilhao)} {'BILHÃO' if bilhao == 1 else 'BILHÕES'}")
    
    milhao = (inteiro // 1000000) % 1000
    if milhao > 0: parts.append(f"{convert_group(milhao)} {'MILHÃO' if milhao == 1 else 'MILHÕES'}")
    
    mil = (inteiro // 1000) % 1000
    if mil > 0:
        if mil == 1: parts.append("MIL")
        else: parts.append(f"{convert_group(mil)} MIL")
    
    resto = inteiro % 1000
    if resto > 0: parts.append(f"{convert_group(resto)}")
    
    texto_reais = ", ".join(parts).replace(", ", " E " if len(parts)==2 else ", ", 1)
    if not texto_reais: texto_reais = "ZERO"
    texto_reais += " REAL" if inteiro == 1 else " REAIS"
    
    texto_centavos = ""
    if centavos > 0:
        texto_centavos = f" E {convert_group(centavos)}"
        texto_centavos += " CENTAVO" if centavos == 1 else " CENTAVOS"
        
    return (texto_reais + texto_centavos).upper()

# ==============================================================================
# CLASSE PARA GERAR PDF (ESTILO TABELA ALINHADA)
# ==============================================================================
class PDF(FPDF):
    def rounded_rect(self, x, y, w, h, r, style=''):
        k = self.k
        self._out('%.2F %.2F m' % ((x + r) * k, (self.h - y) * k))
        self._out('%.2F %.2F l' % ((x + w - r) * k, (self.h - y) * k))
        self._out('%.2F %.2F %.2F %.2F %.2F %.2F c' % 
            ((x + w) * k, (self.h - y) * k, (x + w) * k, (self.h - (y + r)) * k, (x + w) * k, (self.h - (y + r)) * k))
        self._out('%.2F %.2F l' % ((x + w) * k, (self.h - (y + h - r)) * k))
        self._out('%.2F %.2F %.2F %.2F %.2F %.2F c' % 
            ((x + w) * k, (self.h - (y + h)) * k, (x + w - r) * k, (self.h - (y + h)) * k, (x + w - r) * k, (self.h - (y + h)) * k))
        self._out('%.2F %.2F l' % ((x + r) * k, (self.h - (y + h)) * k))
        self._out('%.2F %.2F %.2F %.2F %.2F %.2F c' % 
            ((x) * k, (self.h - (y + h)) * k, (x) * k, (self.h - (y + h - r)) * k, (x) * k, (self.h - (y + h - r)) * k))
        self._out('%.2F %.2F l' % ((x) * k, (self.h - (y + r)) * k))
        self._out('%.2F %.2F %.2F %.2F %.2F %.2F c' % 
            ((x) * k, (self.h - y) * k, (x + r) * k, (self.h - y) * k, (x + r) * k, (self.h - y) * k))
        if style == 'F':
            op = 'f'
        elif style == 'FD' or style == 'DF':
            op = 'B'
        else:
            op = 'S'
        self._out(op)

def create_pdf(area_lote, valor_m2_lote, total_lote, lista_construcoes, total_final, extenso, bairro, fracao_ideal):
    pdf = PDF(orientation='L', unit='mm', format='A4') # Paisagem
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.set_line_width(0.5)
    
    # Filtra construções zeradas (CORREÇÃO DO ITEM VAZIO)
    construcoes_validas = [c for c in lista_construcoes if c['area'] > 0]
    
    col_width = 80
    gap = 2
    start_x = 20
    
    def draw_headers(y_pos):
        pdf.set_xy(start_x, y_pos)
        pdf.cell(col_width, 10, "ÁREA CONSTRUÍDA", border=1, align='C')
        pdf.set_xy(start_x + col_width + gap, y_pos)
        pdf.cell(col_width, 10, "VALOR P/ M2 CONSTRUÇÃO", border=1, align='C')
        pdf.set_xy(start_x + (col_width + gap)*2, y_pos)
        pdf.cell(col_width, 10, "TOTAL", border=1, align='C')
        return y_pos + 10

    # DATA
    pdf.set_xy(start_x, 10)
    pdf.cell(0, 10, datetime.now().strftime("%d/%m/%Y"), align='C')

    # ===============================================
    # 1. LINHA 1 - LOTE
    # ===============================================
    y = 20
    pdf.set_font("Arial", 'B', 12)
    pdf.set_xy(start_x, y)
    pdf.cell(col_width, 10, "ÁREA LOTE", border=1, align='C')
    pdf.set_xy(start_x + col_width + gap, y)
    pdf.cell(col_width, 10, "VALOR P/ M2 TERRENO", border=1, align='C')
    pdf.set_xy(start_x + (col_width + gap)*2, y)
    pdf.cell(col_width, 10, "TOTAL", border=1, align='C')
    
    y += 12
    pdf.set_font("Arial", 'B', 14)
    
    # Lote + FI
    pdf.set_xy(start_x, y)
    area_lote_fmt = f"{area_lote:,.4f} M2".replace(',', '_').replace('.', ',').replace('_', '.')
    fi_fmt = f"F.I: {fracao_ideal:.4f}".replace(',', '_').replace('.', ',').replace('_', '.')
    # Usa MultiCell aqui porque são 2 linhas
    pdf.multi_cell(col_width, 10, f"{area_lote_fmt}\n{fi_fmt}", border=1, align='C')
    
    y_fixed = y 
    
    # Valor M2
    pdf.set_xy(start_x + col_width + gap, y_fixed)
    pdf.cell(col_width, 20, f"{valor_m2_lote:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'), border=1, align='C')
    
    # Total
    pdf.set_xy(start_x + (col_width + gap)*2, y_fixed)
    pdf.cell(col_width, 20, f"{total_lote:,.4f}".replace(',', '_').replace('.', ',').replace('_', '.'), border=1, align='C')

    # ===============================================
    # 2. CONSTRUÇÃO (CORREÇÃO DE ALINHAMENTO E PAGINAÇÃO)
    # ===============================================
    y = y_fixed + 25
    pdf.set_font("Arial", 'B', 12)
    y = draw_headers(y) # Desenha cabeçalho
    
    pdf.set_font("Arial", 'B', 12)
    
    if not construcoes_validas:
        pdf.set_xy(start_x, y)
        pdf.cell(col_width, 10, "0,0000 M2", border=1, align='C')
        pdf.set_xy(start_x + col_width + gap, y)
        pdf.cell(col_width, 10, "R$ 0,00", border=1, align='C')
        pdf.set_xy(start_x + (col_width + gap)*2, y)
        pdf.cell(col_width, 10, "R$ 0,00", border=1, align='C')
        y += 10
    else:
        for i, item in enumerate(construcoes_validas):
            # Se não couber na página, cria nova
            if y > 160: 
                pdf.add_page()
                y = 20
                y = draw_headers(y)
            
            # Formata dados
            txt_area = f"Edif. {i+1}: {item['area']:,.4f} M2".replace(',', '_').replace('.', ',').replace('_', '.')
            txt_val = f"R$ {item['valor_m2']:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            txt_total = f"R$ {item['total']:,.4f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            # Desenha células ALINHADAS (usando cell, não multi_cell)
            pdf.set_xy(start_x, y)
            pdf.cell(col_width, 10, txt_area, border=1, align='C')
            
            pdf.set_xy(start_x + col_width + gap, y)
            pdf.cell(col_width, 10, txt_val, border=1, align='C')
            
            pdf.set_xy(start_x + (col_width + gap)*2, y)
            pdf.cell(col_width, 10, txt_total, border=1, align='C')
            
            y += 10

    # ===============================================
    # 3. RODAPÉ
    # ===============================================
    if y > 140:
        pdf.add_page()
        y = 20
        
    y += 5
    pdf.set_font("Arial", '', 8)
    pdf.set_xy(start_x, y)
    
    # Legenda detalhada
    lista_descricoes = ""
    for i, c in enumerate(construcoes_validas):
        desc_curta = (c['tipo'][:90] + '...') if len(c['tipo']) > 90 else c['tipo']
        lista_descricoes += f"Edif. {i+1} = {desc_curta}\n"
    
    bairro_resumo = (bairro[:90] + '...') if len(bairro) > 90 else bairro
    info_text = f"Bairro: {bairro_resumo}\nLegenda Edificações:\n{lista_descricoes}"
    
    pdf.multi_cell(col_width * 3, 4, info_text, align='L')
    
    # Total Extenso
    y = pdf.get_y() + 5
    if y > 170:
        pdf.add_page()
        y = 20
        
    pdf.set_font("Arial", 'B', 10)
    pdf.set_xy(start_x, y)
    texto_final = f"TOTAL DA AVALIAÇÃO: R$ {total_final:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.') + f" ({extenso})"
    pdf.multi_cell(250, 6, texto_final, align='L')
    
    y = pdf.get_y() + 10
    pdf.set_xy(start_x + 100, y)
    pdf.cell(100, 10, "VALORES CONFORME DECRETO Nº 1.849/2025", align='R')
    
    # PROTEÇÃO CONTRA ERRO DE CARACTERE (Codificação segura)
    return pdf.output(dest='S').encode('latin-1', 'replace')

# ==============================================================================
# CSS
# ==============================================================================
st.markdown("""
    <style>
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    input[type=number] { -moz-appearance: textfield; }
    .stApp { background-color: white; color: black; }
    h1, h2, h3, label { color: black !important; font-family: Arial, sans-serif; }
    .stSelectbox div[data-baseweb="select"] > div { white-space: normal; height: auto; min-height: 38px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# INTERFACE
# ==============================================================================

st.title("Cálculo Valor Venal 2025")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Terreno")
    bairros_lista = sorted(VALORES_BAIRRO.keys())
    bairro_selecionado = st.selectbox("Bairro / Região", bairros_lista)
    valor_m2_terreno = VALORES_BAIRRO[bairro_selecionado]
    st.caption(f"Valor Base: {formatar_moeda(valor_m2_terreno)} / m²")
    
    area_lote = st.number_input("Área do Lote (m²)", min_value=0.0, format="%.4f", step=0.0001)
    fracao_ideal = st.number_input("Fração Ideal", min_value=0.0, value=1.0, format="%.4f", step=0.0001)

    st.write("")
    st.write("")

    st.subheader("2. Edificações")
    
    if 'imoveis' not in st.session_state:
        st.session_state.imoveis = [{"area": 0.0, "tipo": list(VALORES_EDIFICACAO.keys())[0]}]

    opcoes_construcao = sorted(list(VALORES_EDIFICACAO.keys()))
    
    for i, item in enumerate(st.session_state.imoveis):
        st.markdown(f"**Item {i+1}**")
        
        idx_tipo = 0
        if item['tipo'] in opcoes_construcao:
            idx_tipo = opcoes_construcao.index(item['tipo'])
            
        new_tipo = st.selectbox(f"Tipo - Item {i+1}", options=opcoes_construcao, key=f"tipo_{i}", index=idx_tipo)
        v_base = VALORES_EDIFICACAO[new_tipo]
        st.caption(f"Valor Base: {formatar_moeda(v_base)} / m²")

        new_area = st.number_input(f"Área (m²) - Item {i+1}", min_value=0.0, format="%.4f", step=0.0001, key=f"area_{i}", value=item['area'])
        
        st.session_state.imoveis[i]['tipo'] = new_tipo
        st.session_state.imoveis[i]['area'] = new_area
        st.markdown("---")

    cb1, cb2 = st.columns(2)
    if cb1.button("➕ Adicionar Edificação", use_container_width=True):
        st.session_state.imoveis.append({"area": 0.0, "tipo": opcoes_construcao[0]})
        st.rerun()
        
    if cb2.button("🧹 Limpar Lista", type="primary", use_container_width=True):
        st.session_state.imoveis = [{"area": 0.0, "tipo": opcoes_construcao[0]}]
        st.rerun()

with col2:
    st.subheader("Resultado")
    
    total_terreno = area_lote * fracao_ideal * valor_m2_terreno
    
    lista_final_construcoes = []
    total_constr_geral = 0.0
    
    for item in st.session_state.imoveis:
        v_m2 = VALORES_EDIFICACAO[item['tipo']]
        total_item = item['area'] * v_m2
        total_constr_geral += total_item
        
        lista_final_construcoes.append({
            "tipo": item['tipo'],
            "area": item['area'],
            "valor_m2": v_m2,
            "total": total_item
        })
    
    total_final = total_terreno + total_constr_geral
    total_final_rounded = round(total_final, 2)
    extenso = numero_por_extenso(total_final_rounded)
    
    st.markdown(f"**Valor Terreno:** {formatar_moeda(total_terreno)}")
    st.markdown("**Detalhamento Construções:**")
    for c in lista_final_construcoes:
        if c['area'] > 0:
            st.text(f"- {c['area']:.4f}m² x {formatar_moeda(c['valor_m2'])} = {formatar_moeda(c['total'])}")
            
    st.markdown(f"**Total Construção:** {formatar_moeda(total_constr_geral)}")
    st.divider()
    st.markdown(f"### TOTAL: {formatar_moeda(total_final_rounded)}")
    st.caption(f"({extenso})")
    
    st.write("")
    
    if total_final > 0:
        pdf_bytes = create_pdf(
            area_lote, 
            valor_m2_terreno, 
            total_terreno,
            lista_final_construcoes, 
            total_final_rounded,
            extenso,
            bairro_selecionado,
            fracao_ideal
        )
        
        nome_arquivo = f"calculo_venal_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.pdf"
        
        st.download_button(
            label="📄 BAIXAR PDF (TABELA OFICIAL)",
            data=pdf_bytes,
            file_name=nome_arquivo,
            mime="application/pdf",
            type="primary"
        )
