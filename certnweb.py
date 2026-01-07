import streamlit as st
import math

# Configuração da Página (Título e ícone)
st.set_page_config(
    page_title="Calculadora ITBI/IPTU Sarzedo 2025",
    page_icon="🏙️",
    layout="centered"
)

# ==============================================================================
# DADOS (Copiados do PDF)
# ==============================================================================

VALORES_EDIFICACAO = {
    "--- PADRÃO BAIXO / POPULAR ---": 0,
    "R-1 (Unifamiliar) - Baixo - Novo": 2369.59,
    "R-1 (Unifamiliar) - Baixo - Bom (4-8 anos)": 1895.67,
    "R-1 (Unifamiliar) - Baixo - Regular (9-20 anos)": 1516.54,
    "R-1 (Unifamiliar) - Baixo - Precário (>21 anos)": 1213.23,
    "PP-4 (Multifamiliar) - Baixo - Novo": 1808.05,
    "PP-4 (Multifamiliar) - Baixo - Bom": 1446.44,
    "PP-4 (Multifamiliar) - Baixo - Regular": 1157.15,
    "PP-4 (Multifamiliar) - Baixo - Precário": 925.72,
    "R-8 (Multifamiliar) - Baixo - Novo": 2127.12,
    "R-8 (Multifamiliar) - Baixo - Bom": 1701.70,
    "R-8 (Multifamiliar) - Baixo - Regular": 1361.36,
    "R-8 (Multifamiliar) - Baixo - Precário": 1089.09,
    "PIS (Interesse Social) - Novo": 1638.90,
    "PIS (Interesse Social) - Bom": 1311.12,
    "PIS (Interesse Social) - Regular": 1048.90,
    "PIS (Interesse Social) - Precário": 839.12,
    "--- PADRÃO NORMAL ---": 0,
    "R-1 (Unifamiliar) - Normal - Novo": 2835.15,
    "R-1 (Unifamiliar) - Normal - Bom": 2268.12,
    "R-1 (Unifamiliar) - Normal - Regular": 1814.50,
    "R-1 (Unifamiliar) - Normal - Precário": 1451.60,
    "R-2 a R-7 (Multifamiliar) - Normal - Novo": 2700.16,
    "R-2 a R-7 (Multifamiliar) - Normal - Bom": 2160.13,
    "R-2 a R-7 (Multifamiliar) - Normal - Regular": 1728.10,
    "R-2 a R-7 (Multifamiliar) - Normal - Precário": 1382.48,
    "R-8 ou mais (Multifamiliar) - Normal - Novo": 2565.15,
    "R-8 ou mais (Multifamiliar) - Normal - Bom": 2052.12,
    "R-8 ou mais (Multifamiliar) - Normal - Regular": 1641.70,
    "R-8 ou mais (Multifamiliar) - Normal - Precário": 1313.36,
    "--- PADRÃO ALTO ---": 0,
    "R-1 (Unifamiliar) - Alto - Novo": 3530.93,
    "R-1 (Unifamiliar) - Alto - Bom": 2824.74,
    "R-1 (Unifamiliar) - Alto - Regular": 2259.80,
    "R-1 (Unifamiliar) - Alto - Precário": 1807.84,
    "R-3 ou mais (Multifamiliar) - Alto - Novo": 2878.94,
    "R-3 ou mais (Multifamiliar) - Alto - Bom": 2303.15,
    "R-3 ou mais (Multifamiliar) - Alto - Regular": 1842.52,
    "R-3 ou mais (Multifamiliar) - Alto - Precário": 1474.02,
    "--- COMERCIAL (SALAS E LOJAS) ---": 0,
    "CSL-1 (1 Pav) - Normal - Novo": 1846.54,
    "CSL-1 (1 Pav) - Normal - Bom": 1477.23,
    "CSL-1 (1 Pav) - Normal - Regular": 1181.79,
    "CSL-1 (1 Pav) - Normal - Precário": 945.43,
    "CSL-2 (Até 2 Pav) - Normal - Novo": 2303.15,
    "CSL-2 (Até 2 Pav) - Normal - Bom": 1842.52,
    "CSL-2 (Até 2 Pav) - Normal - Regular": 1474.02,
    "CSL-2 (Até 2 Pav) - Normal - Precário": 1179.21,
    "CSL-4 (4+ Pav) - Normal - Novo": 2829.16,
    "CSL-4 (4+ Pav) - Normal - Bom": 2263.33,
    "CSL-4 (4+ Pav) - Normal - Regular": 1810.66,
    "CSL-4 (4+ Pav) - Normal - Precário": 1448.53,
    "CSL-1 (1 Pav) - Alto - Novo": 2357.63,
    "CSL-1 (1 Pav) - Alto - Bom": 1886.10,
    "CSL-1 (1 Pav) - Alto - Regular": 1508.88,
    "CSL-1 (1 Pav) - Alto - Precário": 1207.11,
    "CSL-2 (Até 2 Pav) - Alto - Novo": 2547.27,
    "CSL-2 (Até 2 Pav) - Alto - Bom": 2037.82,
    "CSL-2 (Até 2 Pav) - Alto - Regular": 1630.25,
    "CSL-2 (Até 2 Pav) - Alto - Precário": 1304.20,
    "CSL-4 (4+ Pav) - Alto - Novo": 3400.77,
    "CSL-4 (4+ Pav) - Alto - Bom": 2720.62,
    "CSL-4 (4+ Pav) - Alto - Regular": 2176.49,
    "CSL-4 (4+ Pav) - Alto - Precário": 1741.19,
    "--- INDÚSTRIA / GALPÃO (GI) ---": 0,
    "GI-1 (Padrão Baixo) - Novo": 1246.66,
    "GI-1 (Padrão Baixo) - Bom": 997.33,
    "GI-1 (Padrão Baixo) - Regular": 797.86,
    "GI-1 (Padrão Baixo) - Precário": 638.29,
    "GI-2 (Padrão Normal) - Novo": 1745.32,
    "GI-2 (Padrão Normal) - Bom": 1396.26,
    "GI-2 (Padrão Normal) - Regular": 1117.01,
    "GI-2 (Padrão Normal) - Precário": 893.61,
    "GI-3 (Padrão Alto) - Novo": 2547.27,
    "GI-3 (Padrão Alto) - Bom": 2037.82,
    "GI-3 (Padrão Alto) - Regular": 1630.25,
    "GI-3 (Padrão Alto) - Precário": 1304.20,
    "GI-4 (Muito Alto) - Novo": 3056.72,
    "GI-4 (Muito Alto) - Bom": 2445.38,
    "GI-4 (Muito Alto) - Regular": 1956.30,
    "GI-4 (Muito Alto) - Precário": 1565.04,
    "SEM CONSTRUÇÃO (Lote Vago)": 0.0
}

VALORES_BAIRRO = {
    "Aleixa Ferreira (Todas as quadras)": 550.00,
    "Brasília - Região Antenas (Frente p/ Rua Pedro Pinheiro)": 200.00,
    "Brasília - Praça/Ponto de Ônibus (Frente p/ Maria Carlota/Afonso Pena/Outros)": 390.00,
    "Brasília - Região Central (Av. Israel Pinheiro/Outras)": 500.00,
    "Brasília - Região Mineirão Atacado (Qds 55 a 65)": 550.00,
    "Brasília II (Geral - Quadras internas)": 400.00,
    "Brasília II (Comercial / Av. Israel Pinheiro)": 1000.00,
    "Cachoeira (Q 01 parcial, 02 e 03)": 500.00,
    "Cachoeira (Q 04 e 05)": 340.00,
    "Central Parque (Quadras 01, 02 e partes nobres)": 1500.00,
    "Central Parque (Quadras 03, 04, 05 - partes)": 1250.00,
    "Centro (Região R. Eduardo Cozac)": 1250.00,
    "Centro (Sarzedo Mall / R. José Luiz Rezende)": 1000.00,
    "Chácara Satélite (Todas)": 550.00,
    "Cinira de Freitas (Quadra 01)": 1250.00,
    "Cinira de Freitas (Quadra 02)": 1500.00,
    "Cinira de Freitas (Meio e fundo da quadra)": 600.00,
    "Vila Eduardo Cozac (Frente R. Sabiá)": 800.00,
    "São Joaquim (Todas)": 500.00,
    "Condomínio Sarzedo I e II (Parte interna)": 400.00,
    "Distrito Industrial (Todas)": 270.00,
    "Estâncias Eliane / Sítio Tabatinga (Remanescentes)": 200.00,
    "Fazenda Santa Rosa de Lima (Remanescentes)": 100.00,
    "Imaculada Conceição (Remanescentes/Sítios)": 340.00,
    "Imaculada Conceição (Frente Av. São Lucas)": 1000.00,
    "Imaculada Conceição (Quadras 01 a 06, 09, 11)": 500.00,
    "Imaculada Conceição (Quadras 07, 08, 10, 12 a 14)": 340.00,
    "Jardim Anchieta (Q 01 a 04, 06, 09, 12 a 14, 16)": 450.00,
    "Jardim Anchieta (Q 05, 07, 08, 10, 11, 15, 17 a 25)": 300.00,
    "Jardim Das Oliveiras (Frente MG-040)": 700.00,
    "Jardim Das Oliveiras (Quadras internas e áreas verdes)": 550.00,
    "Jardim Planalto (Todas)": 340.00,
    "Jardim Santa Rosa (Q 12 a 22, 32, 33, 36, 41...)": 500.00,
    "Jardim Santa Rosa (Intermediário - Q 21, 20, 19, 05 a 11...)": 700.00,
    "Jardim Santa Rosa (Nobre - Frente MG-040 / Av. São Lucas)": 1650.00,
    "Jardim Santa Rosa (Comercial Padrão)": 1000.00,
    "Jardim Vera Cruz (Q 01 a 10 e partes)": 500.00,
    "Jardim Vera Cruz (Q 13)": 340.00,
    "Jardim Vera Cruz (Fundos e Vila)": 200.00,
    "Liberdade (Frente R. Ernesto Guevara e Q 09 a 15)": 600.00,
    "Liberdade (Frente Av. Zumbi dos Palmares)": 700.00,
    "Liberdade II (Todas)": 200.00,
    "Região do Malongo": 220.00,
    "Região da Lonax I (Indústrias)": 270.00,
    "Região da Lonax II (Remanescente)": 200.00,
    "Manoel Pinheiro (Todas)": 600.00,
    "Pinheiros (Quadra 08A)": 1500.00,
    "Pinheiros (Quadras 2A a 7A)": 1250.00,
    "Pinheiros (Quadra 01A)": 550.00,
    "Residencial Masterville (Av. das Palmeiras)": 800.00,
    "Residencial Masterville (Alamedas Siriemas, Andorinhas...)": 600.00,
    "Residencial Masterville (Geral - Quadras internas)": 550.00,
    "Residencial Masterville (Q 41 a 54 e áreas verdes)": 500.00,
    "Residencial Masterville (Alameda das Begônias)": 440.00,
    "Residencial Masterville (Alameda Flamboyants e outras)": 340.00,
    "Riacho Da Mata I (Q 20 a 39 e outras)": 500.00,
    "Riacho Da Mata I (Frente R. Araribá/Angelim)": 800.00,
    "Riacho Da Mata II (Q 09, 10, 15 a 19)": 450.00,
    "Riacho Da Mata III (Q 01 a 08, 11 a 14)": 390.00,
    "Santa Cecília (Q 01 a 03)": 600.00,
    "Santa Cecília (Frente Av. Zumbi/MG-040)": 700.00,
    "Santa Mônica (Q 01 a 05 e 09)": 340.00,
    "Santa Mônica (Q 06, 07, 08, 10)": 500.00,
    "Santa Mônica (Frente R. Elói Cândido de Melo)": 550.00,
    "Santa Rita (Q 01 a 09)": 550.00,
    "Santa Rita (Anexo Pousada do Rei)": 1000.00,
    "Santa Rita (MG-040 Galpões)": 550.00,
    "Santa Rosa De Lima (Todas)": 600.00,
    "Santo Antônio (Geral - Q 01 a 12, 17 a 19...)": 390.00,
    "Santo Antônio (Av. Juscelino / Vila Vicentina)": 500.00,
    "Santo Antônio (Fundos - Q 13 a 16, 20 a 22...)": 250.00,
    "Olaria (Frente Av. São Lucas)": 1000.00,
    "Olaria (Meio da quadra)": 500.00,
    "Olaria (Fundo da quadra)": 340.00,
    "São Cristóvão (Frente Av. São Lucas)": 1000.00,
    "São Cristóvão (Meio da quadra)": 500.00,
    "São Cristóvão (Fundos)": 340.00,
    "São Joaquim (Áreas verdes, Q 08 a 17...)": 500.00,
    "São Joaquim II (Praça - Q 01 a 07 partes)": 600.00,
    "São Joaquim (Av. Rouxinol)": 800.00,
    "São Paulo (Frente Av. São Lucas)": 1000.00,
    "São Paulo (Meio da quadra)": 500.00,
    "São Paulo (Fundos)": 340.00,
    "São Pedro (Av. São Lucas)": 1000.00,
    "São Pedro (Q 02, 05, partes 03 e 04)": 550.00,
    "São Pedro (Q 01, 06, 07)": 340.00,
    "Serra Azul (Q 17 a 36 e outras)": 390.00,
    "Serra Azul (MG-040 / BH Atacado / Galpões)": 500.00,
    "Sítio da Lagoa (Fundos BH Atacado)": 1500.00,
    "Sítio da Lagoa (Outros / Sítios)": 100.00,
    "Sítio Sarzedo": 220.00,
    "Perobas (Fundos)": 500.00,
    "Perobas (Geral)": 60.00,
    "Vila Satélite I (R. Joaquim Pedro de Oliveira)": 600.00,
    "Vila Satélite I (Q 01, 03 a 08, 13, 14)": 980.00,
    "Vila Satélite I (Nobre - Frente MG-040 e Q 09 a 17)": 1250.00,
    "Vila Satélite II (Q 02 a 05 - partes)": 1500.00,
    "Vila Satélite II (Q 01 e 06 a 10 - partes)": 1250.00,
    "Vista da Lagoa (Todas)": 260.00,
    "Quintas da Lagoa (Todas)": 300.00,
    "Quintas da Jangada (Q 01 a 09 - partes)": 300.00,
    "Quintas da Jangada (Frente MG-040 - Q 01, 02, 07, 10 a 12)": 1000.00,
}

def formatar_moeda(valor):
    s = "{:,.2f}".format(valor)
    return f"R$ {s.replace(',', '_').replace('.', ',').replace('_', '.')}"

# ==============================================================================
# INTERFACE
# ==============================================================================

st.title("🏙️ Sistema de Cálculo Tributário - Sarzedo 2025")
st.markdown("### Decreto Municipal N° 1.849/2025")

# --- SEÇÃO 1: TERRENO ---
st.divider()
st.header("1. Dados do Terreno")
col1, col2 = st.columns(2)

with col1:
    bairros_lista = sorted(VALORES_BAIRRO.keys())
    bairro_selecionado = st.selectbox("Selecione o Bairro / Região:", bairros_lista)
    valor_m2_terreno = VALORES_BAIRRO[bairro_selecionado]
    st.info(f"Valor Planta: {formatar_moeda(valor_m2_terreno)} / m²")

with col2:
    area_lote = st.number_input("Área do Lote (m²):", min_value=0.0, format="%.2f")
    fracao_ideal = st.number_input("Fração Ideal (1.0 = 100%):", min_value=0.0, value=1.0, format="%.4f")

# --- SEÇÃO 2: EDIFICAÇÕES ---
st.divider()
st.header("2. Edificações")

# Controle de sessão para quantidade de edificações
if 'qtd_imoveis' not in st.session_state:
    st.session_state.qtd_imoveis = 1

col_btn1, col_btn2 = st.columns([1, 4])
if col_btn1.button("➕ Adicionar"):
    st.session_state.qtd_imoveis += 1
if col_btn2.button("➖ Remover"):
    if st.session_state.qtd_imoveis > 1:
        st.session_state.qtd_imoveis -= 1

# Listas para guardar os dados inputados
areas_construidas = []
tipos_construidos = []

# Opções de construção (filtrando os títulos)
opcoes_construcao = [k for k in VALORES_EDIFICACAO.keys() if VALORES_EDIFICACAO[k] > 0 or "SEM CONSTRUÇÃO" in k]

for i in range(st.session_state.qtd_imoveis):
    st.markdown(f"**Edificação {i+1}**")
    c1, c2 = st.columns([1, 3])
    with c1:
        a = st.number_input(f"Área (m²) - Edif. {i+1}", min_value=0.0, format="%.2f", key=f"area_{i}")
    with c2:
        t = st.selectbox(f"Tipo - Edif. {i+1}", options=opcoes_construcao, key=f"tipo_{i}")
    
    areas_construidas.append(a)
    tipos_construidos.append(t)
    st.markdown("---")

# --- BOTÃO CALCULAR ---
if st.button("🖩 CALCULAR VALOR VENAL", type="primary", use_container_width=True):
    
    # Cálculos
    valor_total_terreno = area_lote * fracao_ideal * valor_m2_terreno
    
    total_construcao = 0
    detalhes_constr = []
    
    for area, tipo in zip(areas_construidas, tipos_construidos):
        if area > 0:
            val_m2 = VALORES_EDIFICACAO[tipo]
            val_total_item = area * val_m2
            total_construcao += val_total_item
            detalhes_constr.append((tipo, area, val_m2, val_total_item))
            
    valor_final = valor_total_terreno + total_construcao
    
    # Exibição do Resultado
    st.success("Cálculo Realizado com Sucesso!")
    
    st.markdown("### 📋 Memória de Cálculo")
    
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.markdown("#### Terreno")
        st.write(f"**Bairro:** {bairro_selecionado}")
        st.write(f"**Área Efetiva:** {area_lote * fracao_ideal:.2f} m²")
        st.metric(label="Valor Venal do Terreno", value=formatar_moeda(valor_total_terreno))
        
    with col_res2:
        st.markdown("#### Construções")
        st.write(f"**Qtd Edificações:** {len(detalhes_constr)}")
        st.metric(label="Valor Venal das Construções", value=formatar_moeda(total_construcao))

    # Detalhamento das construções (se houver)
    if detalhes_constr:
        with st.expander("Ver detalhes das edificações"):
            for d in detalhes_constr:
                st.write(f"• **{d[0]}**: {d[1]}m² x {formatar_moeda(d[2])} = **{formatar_moeda(d[3])}**")

    st.divider()
    st.markdown(f"<h2 style='text-align: center; color: #2e7bcf;'>VALOR TOTAL: {formatar_moeda(valor_final)}</h2>", unsafe_allow_html=True)