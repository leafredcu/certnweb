import streamlit as st
import math

# ==============================================================================
# CONFIGURAÇÃO VISUAL E CSS (UI DESIGN)
# ==============================================================================
st.set_page_config(
    page_title="Tributos Sarzedo 2025",
    page_icon="🏛️",
    layout="centered"
)

# CSS para melhorar o visual (Espaçamento e Fontes)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.4rem;
        color: #2e7bcf;
    }
    .result-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        margin-top: 20px;
    }
    .extenso {
        font-style: italic;
        color: #555;
        font-size: 0.95rem;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# FUNÇÕES AUXILIARES (Extenso e Formatação)
# ==============================================================================

def formatar_moeda(valor):
    s = "{:,.2f}".format(valor)
    return f"R$ {s.replace(',', '_').replace('.', ',').replace('_', '.')}"

def numero_por_extenso(n):
    """Converte número para extenso (Padrão Monetário Brasileiro) - Sem dependências"""
    if n == 0: return "zero reais"
    
    unidades = ["", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
    dezespeciais = ["dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"]
    dezenas = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
    centenas = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"]

    def convert_group(num):
        if num == 100: return "cem"
        s = ""
        c, d, u = (num // 100), (num % 100 // 10), (num % 10)
        
        if c > 0:
            s += centenas[c]
            if d > 0 or u > 0: s += " e "
        
        if d == 1:
            s += dezespeciais[u]
        elif d > 1:
            s += dezenas[d]
            if u > 0: s += " e " + unidades[u]
        elif u > 0:
            if c == 0: s += unidades[u] # Evita "cento e zero" ou coisa assim
            else: s += unidades[u] # Caso normal (ex: 105 -> cento e cinco)
        return s

    inteiro = int(n)
    centavos = int(round((n - inteiro) * 100))
    parts = []
    
    # Bilhões
    bilhao = (inteiro // 1000000000) % 1000
    if bilhao > 0:
        term = "bilhão" if bilhao == 1 else "bilhões"
        parts.append(f"{convert_group(bilhao)} {term}")
    
    # Milhões
    milhao = (inteiro // 1000000) % 1000
    if milhao > 0:
        term = "milhão" if milhao == 1 else "milhões"
        parts.append(f"{convert_group(milhao)} {term}")
    
    # Milhares
    mil = (inteiro // 1000) % 1000
    if mil > 0:
        term = "mil" # Invariável
        if mil == 1: parts.append(term)
        else: parts.append(f"{convert_group(mil)} {term}")
    
    # Unidades
    resto = inteiro % 1000
    if resto > 0:
        conector = " e " if parts else ""
        # Regra do "e": se for múltiplo de 100 ou menor que 100
        parts.append(f"{convert_group(resto)}")
    
    # Montagem Reais
    texto_reais = ", ".join(parts).replace(", ", " e " if len(parts)==2 else ", ", 1)
    if not texto_reais: texto_reais = "zero"
    texto_reais += " real" if inteiro == 1 else " reais"
    
    # Montagem Centavos
    texto_centavos = ""
    if centavos > 0:
        texto_centavos = f" e {convert_group(centavos)}"
        texto_centavos += " centavo" if centavos == 1 else " centavos"
        
    return (texto_reais + texto_centavos).upper()

# ==============================================================================
# DADOS (Simplificados para leitura)
# ==============================================================================
# ... (Mantendo os mesmos dicionários para não ocupar espaço, mas eles estão aqui na lógica)
VALORES_EDIFICACAO = {
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
    "R-1 (Unifamiliar) - Alto - Novo": 3530.93,
    "R-1 (Unifamiliar) - Alto - Bom": 2824.74,
    "R-1 (Unifamiliar) - Alto - Regular": 2259.80,
    "R-1 (Unifamiliar) - Alto - Precário": 1807.84,
    "R-3 ou mais (Multifamiliar) - Alto - Novo": 2878.94,
    "R-3 ou mais (Multifamiliar) - Alto - Bom": 2303.15,
    "R-3 ou mais (Multifamiliar) - Alto - Regular": 1842.52,
    "R-3 ou mais (Multifamiliar) - Alto - Precário": 1474.02,
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

# ==============================================================================
# INTERFACE PRINCIPAL
# ==============================================================================

st.title("🏙️ Sistema Tributário Sarzedo 2025")
st.markdown("**Decreto Municipal N° 1.849/2025**")

# Uso de Abas para limpar a interface (UI Melhorada)
tab1, tab2 = st.tabs([" Passo 1: Imóveis", " Passo 2: Resultado"])

with tab1:
    # --- CARD TERRENO ---
    with st.container(border=True):
        st.subheader("🏡 Dados do Terreno")
        
        col1, col2 = st.columns(2)
        
        with col1:
            bairros_lista = sorted(VALORES_BAIRRO.keys())
            bairro_selecionado = st.selectbox("📍 Bairro / Região:", bairros_lista, help="Selecione conforme o Anexo I")
            valor_m2_terreno = VALORES_BAIRRO[bairro_selecionado]
            st.caption(f"Valor Base: **{formatar_moeda(valor_m2_terreno)} / m²**")
        
        with col2:
            area_lote = st.number_input("📐 Área do Lote (m²):", min_value=0.0, format="%.2f", value=0.0)
            fracao_ideal = st.number_input("🍰 Fração Ideal:", min_value=0.0, value=1.0, format="%.4f", help="1.0 para lote inteiro, 0.5 para metade, etc.")

    st.write("") # Espaçamento

    # --- CARD CONSTRUÇÃO ---
    with st.container(border=True):
        st.subheader("🏗️ Dados da Construção")
        
        # Estado da aplicação para itens
        if 'imoveis' not in st.session_state:
            st.session_state.imoveis = []

        # Botões de controle
        c_btn1, c_btn2, c_space = st.columns([1, 1, 3])
        if c_btn1.button("➕ Adicionar"):
            st.session_state.imoveis.append({"area": 0.0, "tipo": list(VALORES_EDIFICACAO.keys())[0]})
        
        if c_btn2.button("🧹 Limpar Lista"):
            st.session_state.imoveis = []

        # Renderização dinâmica dos campos com "respiro"
        opcoes_construcao = [k for k in VALORES_EDIFICACAO.keys() if VALORES_EDIFICACAO[k] > 0 or "SEM CONSTRUÇÃO" in k]
        
        if not st.session_state.imoveis:
            st.info("Nenhuma construção adicionada. Clique em '➕ Adicionar' se houver edificação.")
        
        for i, item in enumerate(st.session_state.imoveis):
            st.markdown(f"**Edificação #{i+1}**")
            c_input1, c_input2 = st.columns([1, 2])
            
            # Atualiza os valores direto na sessão
            new_area = c_input1.number_input(f"Área (m²)", min_value=0.0, format="%.2f", key=f"area_{i}", value=item['area'])
            new_tipo = c_input2.selectbox(f"Padrão Construtivo", options=opcoes_construcao, key=f"tipo_{i}", index=opcoes_construcao.index(item['tipo']) if item['tipo'] in opcoes_construcao else 0)
            
            st.session_state.imoveis[i]['area'] = new_area
            st.session_state.imoveis[i]['tipo'] = new_tipo
            st.divider()

    st.write("")
    
    # Botão de Ação Principal
    if st.button("CALCULAR TRIBUTO 🚀", type="primary"):
        st.session_state.calcular = True
        # Força pular para a aba de resultado (gambiarra visual, mas o usuário clica na aba manual se precisar)
        st.toast("Cálculo realizado! Veja a aba 'Resultado'.")

with tab2:
    if st.session_state.get('calcular'):
        # CÁLCULOS
        val_terreno_total = area_lote * fracao_ideal * valor_m2_terreno
        
        val_construcao_total = 0
        detalhes = []
        
        for item in st.session_state.imoveis:
            if item['area'] > 0:
                v_m2 = VALORES_EDIFICACAO[item['tipo']]
                v_total = item['area'] * v_m2
                val_construcao_total += v_total
                detalhes.append((item['tipo'], item['area'], v_m2, v_total))
        
        valor_final = val_terreno_total + val_construcao_total
        
        # APRESENTAÇÃO (Visual Card)
        st.markdown(f"""
        <div class="result-card">
            <h3 style="text-align: center; color: #444;">CERTIDÃO DE LANÇAMENTO</h3>
            <hr>
            <h4 style="color: #2e7bcf;">1. TERRENO</h4>
            <p><strong>Bairro:</strong> {bairro_selecionado}<br>
            <strong>Área Tributável:</strong> {area_lote * fracao_ideal:.2f} m²<br>
            <strong>Valor Venal:</strong> {formatar_moeda(val_terreno_total)}</p>
            
            <h4 style="color: #2e7bcf;">2. CONSTRUÇÕES</h4>
            <p><strong>Total Construído:</strong> {sum(d[1] for d in detalhes):.2f} m²<br>
            <strong>Valor Venal:</strong> {formatar_moeda(val_construcao_total)}</p>
            
            <hr>
            <h2 style="text-align: center; color: #2e7bcf;">TOTAL: {formatar_moeda(valor_final)}</h2>
            <p style="text-align: center; font-style: italic; color: #666;">({numero_por_extenso(valor_final)})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detalhes técnicos (Expander para não poluir)
        with st.expander("🔎 Ver Memória de Cálculo Detalhada"):
            st.write("--- Detalhamento das Edificações ---")
            for d in detalhes:
                st.write(f"- {d[0]}: {d[1]}m² x {formatar_moeda(d[2])} = **{formatar_moeda(d[3])}**")
    else:
        st.info("Preencha os dados na aba 'Passo 1' e clique em Calcular.")
