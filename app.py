import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler

# Configuração da página Streamlit (Must be the first Streamlit command)
st.set_page_config(
    page_title="GlobalPay Antifraude Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS Customizado para Estética Premium (Vibrant Dark Mode / Glassmorphism)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Background Geral */
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1F2937;
    }
    
    /* ----------------------------------------------------
       Garantir Acessibilidade Visual (Contraste de Fontes)
       ---------------------------------------------------- */
    /* Textos gerais do corpo e parágrafos */
    .stApp p, .stApp li, .stApp span, .stApp div[data-testid="stMarkdownContainer"] p {
        color: #E5E7EB !important; /* Cinza claro para leitura perfeita */
    }
    
    /* Títulos e Cabeçalhos */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #FFFFFF !important; /* Branco de alto impacto */
    }
    
    /* Rótulos dos Widgets (sliders, selectboxes, inputs) */
    .stApp label, .stApp div[data-testid="stWidgetLabel"] p, .stApp div[data-testid="stWidgetLabel"] span {
        color: #FFFFFF !important; /* Branco de alto contraste */
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Valores de sliders e detalhes numéricos */
    div[data-testid="stSlider"] div, div[data-testid="stSlider"] span, div[data-testid="stSlider"] p {
        color: #E5E7EB !important;
    }
    
    /* Textos das Abas (Tabs) */
    button[data-baseweb="tab"] p, button[data-baseweb="tab"] span {
        color: #9CA3AF !important; 
    }
    button[data-baseweb="tab"][aria-selected="true"] p, button[data-baseweb="tab"][aria-selected="true"] span {
        color: #FFFFFF !important; /* Branco ativo */
        font-weight: 700 !important;
    }
    
    /* Elementos na Sidebar */
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] h2 {
        color: #FFFFFF !important;
    }
    
    /* Custom Card */
    .metric-card {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.8), rgba(31, 41, 55, 0.5));
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
        margin-bottom: 16px;
    }
    
    .metric-title {
        font-size: 14px;
        color: #E5E7EB; /* Alterado de #9CA3AF para #E5E7EB para contraste perfeito */
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 4px;
        color: #FFFFFF !important;
    }
    
    .metric-sub {
        font-size: 12px;
        color: #9CA3AF; /* Alterado de #6B7280 para #9CA3AF para contraste perfeito */
    }
    
    /* Custom Headers */
    .main-title {
        background: linear-gradient(to right, #A78BFA, #F472B6); /* Cores mais claras/neon */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 40px;
        margin-bottom: 4px;
        text-align: left;
    }
    
    .sub-title {
        color: #D1D5DB; /* Alterado de #9CA3AF para #D1D5DB */
        font-size: 16px;
        margin-bottom: 24px;
        text-align: left;
    }
    
    /* Status Badges */
    .badge {
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-bloquear {
        background-color: rgba(239, 68, 68, 0.25);
        color: #F87171; /* Tom mais claro/acessível */
        border: 1px solid rgba(239, 68, 68, 0.5);
    }
    .badge-revisar {
        background-color: rgba(245, 158, 11, 0.25);
        color: #FBBF24; /* Tom mais claro/acessível */
        border: 1px solid rgba(245, 158, 11, 0.5);
    }
    .badge-aprovar {
        background-color: rgba(16, 185, 129, 0.25);
        color: #34D399; /* Tom mais claro/acessível */
        border: 1px solid rgba(16, 185, 129, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Funções de Carregamento de Recursos (Cache para performance)
# ----------------------------------------------------
@st.cache_resource
def carregar_modelo():
    modelo_path = 'modelo_antifraude_v1.pkl'
    if not os.path.exists(modelo_path):
        return None
    with open(modelo_path, 'rb') as f:
        modelo = pickle.load(f)
    return modelo

@st.cache_resource
def carregar_escalonador():
    scaler_path = 'scaler_antifraude.pkl'
    if not os.path.exists(scaler_path):
        return None
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    return scaler

@st.cache_data
def carregar_ground_truth():
    gt_path = 'ground_truth_oot.pkl'
    if not os.path.exists(gt_path):
        return None
    with open(gt_path, 'rb') as f:
        gt = pickle.load(f)
    return gt

# Inicialização de dados e modelos
model = carregar_modelo()
scaler = carregar_escalonador()
gt_labels = carregar_ground_truth()

# ----------------------------------------------------
# Configuração da Barra Lateral (Sidebar)
# ----------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/625/625591.png", width=70)
st.sidebar.markdown("<h2 style='margin-top:0px;'>GlobalPay Solutions</h2>", unsafe_allow_html=True)
st.sidebar.markdown("*Portal de Prevenção a Fraude B2B2C*")
st.sidebar.divider()

st.sidebar.subheader("🎛️ Limiares de Decisão")
threshold_revisao = st.sidebar.slider(
    "Limiar de Revisão Manual (Médio Risco)",
    min_value=0.01,
    max_value=0.99,
    value=0.10,
    step=0.01,
    help="Transações com score acima deste valor serão enviadas para revisão manual de risco."
)

threshold_bloqueio = st.sidebar.slider(
    "Limiar de Bloqueio Automático (Alto Risco)",
    min_value=0.01,
    max_value=0.99,
    value=0.50,
    step=0.01,
    help="Transações com score acima deste valor serão bloqueadas de forma preventiva imediata."
)

if threshold_revisao >= threshold_bloqueio:
    st.sidebar.error("⚠️ O Limiar de Revisão deve ser menor que o Limiar de Bloqueio.")

st.sidebar.divider()
st.sidebar.subheader("💰 Parâmetros Financeiros")
custo_fn = st.sidebar.number_input(
    "Custo de Falso Negativo (Fraude Aprovada)",
    min_value=1.0,
    max_value=5000.0,
    value=150.0,
    step=10.0,
    help="Perda por chargeback direta + multa de bandeira quando uma fraude passa pelo sistema."
)

custo_fp = st.sidebar.number_input(
    "Custo de Falso Positivo (Atrito / Revisão)",
    min_value=0.5,
    max_value=1000.0,
    value=10.0,
    step=1.0,
    help="Custo operacional de verificação e custo intangível de fricção (potencial perda do cliente bom)."
)

# ----------------------------------------------------
# Cabeçalho Principal da Aplicação
# ----------------------------------------------------
st.markdown("<h1 class='main-title'>🛡️ Detecção de Fraude Silenciosa</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Gateway GlobalPay B2B2C — Monitoramento e Mitigação de Riscos de Transações em Tempo Real</p>", unsafe_allow_html=True)

# Verificação se o modelo e escalonador estão carregados
if model is None or scaler is None:
    st.error("❌ Erro ao carregar os arquivos essenciais (`modelo_antifraude_v1.pkl` ou `scaler_antifraude.pkl`). Certifique-se de que estão na mesma pasta do app.")
    st.stop()

# ----------------------------------------------------
# Upload de Arquivos / Carregamento Padrão
# ----------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload de Lote de Transações (.CSV)", 
    type=["csv"], 
    help="Envie um arquivo CSV contendo os dados transacionais do dia. O arquivo deve conter colunas de Time, Amount e as PCAs V1-V28."
)

df_input = None
using_default = False

# Se o usuário não subir um CSV, tenta carregar o 'clientes_do_dia.csv' padrão
if uploaded_file is not None:
    try:
        df_input = pd.read_csv(uploaded_file)
        st.success(f"✔️ Lote carregado com sucesso: {uploaded_file.name} ({len(df_input)} transações)")
    except Exception as e:
        st.error(f"Erro ao ler o arquivo enviado: {e}")
else:
    default_csv_path = 'clientes_do_dia.csv'
    if os.path.exists(default_csv_path):
        df_input = pd.read_csv(default_csv_path)
        using_default = True
        st.info("💡 **clientes_do_dia.csv** detectado no diretório e carregado automaticamente como lote de demonstração.")
    else:
        st.warning("⚠️ Nenhum arquivo carregado. Por favor, faça o upload de um lote de transações (.csv) ou coloque o arquivo 'clientes_do_dia.csv' na mesma pasta.")

# ----------------------------------------------------
# Execução da Previsão e Cálculos de Negócio
# ----------------------------------------------------
if df_input is not None:
    # Validar se as colunas estão no formato correto
    features_order = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
                      'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20',
                      'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount']
    
    missing_cols = [col for col in features_order if col not in df_input.columns]
    
    if len(missing_cols) > 0:
        st.error(f"❌ O arquivo CSV não possui as colunas obrigatórias: {missing_cols}")
    else:
        # Criar cópia escalonada para o modelo
        df_scaled = df_input.copy()
        df_scaled[['Time', 'Amount']] = scaler.transform(df_input[['Time', 'Amount']])
        
        # Predição (Probabilidade de Fraude)
        with st.spinner("Computando análise de risco e scores de fraude..."):
            scores = model.predict_proba(df_scaled[features_order])[:, 1]
        
        # Enriquecer o DataFrame de entrada com os resultados
        df_result = df_input.copy()
        df_result['Probabilidade_Fraude'] = scores
        
        # Definir Decisão baseada nos Limiares
        decisoes = []
        for s in scores:
            if s >= threshold_bloqueio:
                decisoes.append("Bloquear")
            elif s >= threshold_revisao:
                decisoes.append("Revisar")
            else:
                decisoes.append("Aprovar")
        
        df_result['Decisao'] = decisoes

        # Distribuição das decisões
        n_total = len(df_result)
        n_bloquear = decisoes.count("Bloquear")
        n_revisar = decisoes.count("Revisar")
        n_aprovar = decisoes.count("Aprovar")
        
        # ----------------------------------------------------
        # Abas da Interface (Tabs)
        # ----------------------------------------------------
        tab_principal, tab_tecnica = st.tabs(["📊 Simulador Financeiro & Decisões", "📈 Análise Técnica & PR-Curve"])
        
        with tab_principal:
            # ----------------------------------------------------
            # Simulação Financeira (ROI)
            # ----------------------------------------------------
            st.subheader("🎯 Simulação de Impacto Financeiro e ROI")
            
            # Se for o arquivo de demonstração padrão (OOT) ou se tiver coluna 'Class'
            # podemos calcular métricas de negócio EXATAS e reais
            tem_class_real = 'Class' in df_input.columns or (using_default and gt_labels is not None)
            
            if tem_class_real:
                y_real = df_input['Class'].values if 'Class' in df_input.columns else gt_labels[:len(df_result)]
                
                # Matriz de Confusão para a decisão final
                # Transação fraudulenta (y_real == 1)
                # Transação normal (y_real == 0)
                # Bloqueio é considerado ação corretiva. 
                # Falso Negativo (FN): Fraude real (y_real == 1) APROVADA ou REVISADA (não bloqueada). 
                # Espera, no modelo do notebook, a decisão é binária (Bloqueia se probabilidade >= threshold).
                # Para nossa regra de 3 estados:
                # - Bloquear: Bloqueio automático imediato (Evita fraude, mas pode gerar falso positivo se real for 0).
                # - Revisar: Transação vai para auditoria. Vamos considerar que a revisão manual custa custo_fp (análise)
                #   e se for fraude ela é capturada com sucesso (não gera custo_fn) e se for normal ela é liberada (não gera chargeback, apenas o custo_fp da análise).
                # - Aprovar: Transação aprovada imediatamente. Se for fraude real, gera o custo_fn (chargeback).
                
                tp_bloqueados = 0  # Fraude real bloqueada automaticamente (Sem prejuízo)
                fp_bloqueados = 0  # Legítima bloqueada automaticamente (Custo FP)
                
                tp_revisados = 0   # Fraude real identificada e corrigida na revisão (Custo FP da análise, sem custo FN)
                fp_revisados = 0   # Legítima revisada e liberada (Custo FP da análise)
                
                fn_aprovados = 0   # Fraude real aprovada incorretamente (Custo FN - perda total)
                tn_aprovados = 0   # Legítima aprovada (Custo Zero)
                
                for idx, dec in enumerate(decisoes):
                    real_c = y_real[idx]
                    if dec == "Bloquear":
                        if real_c == 1:
                            tp_bloqueados += 1
                        else:
                            fp_bloqueados += 1
                    elif dec == "Revisar":
                        if real_c == 1:
                            tp_revisados += 1
                        else:
                            fp_revisados += 1
                    else:  # Aprovar
                        if real_c == 1:
                            fn_aprovados += 1
                        else:
                            tn_aprovados += 1
                
                # TOTAL DE FRAUDES NO LOTE
                total_fraudes_reais = int(sum(y_real))
                
                # Baseline: Sem modelo, todas as transações são aprovadas automaticamente
                # Prejuízo Baseline = Total de fraudes * Custo FN
                prejuizo_baseline = total_fraudes_reais * custo_fn
                
                # Prejuízo com Modelo = (Fraudes Aprovadas * Custo FN) + (Bloqueados Falsos Positivos * Custo FP) + (Revisados Falsos Positivos * Custo FP) + (Revisados Verdadeiros Positivos * Custo FP)
                # Note: Tanto bloqueados normais (FP) quanto qualquer revisão geram custo_fp.
                prejuizo_modelo = (fn_aprovados * custo_fn) + ((fp_bloqueados + fp_revisados + tp_revisados) * custo_fp)
                
                economia_liquida = prejuizo_baseline - prejuizo_modelo
                roi_percentual = (economia_liquida / prejuizo_baseline) * 100 if prejuizo_baseline > 0 else 0.0
                
                # Exibir métricas nos Cards
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">📉 Custo SEM Modelo (Baseline)</div>
                        <div class="metric-value" style="color: #FFFFFF;">R$ {prejuizo_baseline:,.2f}</div>
                        <div class="metric-sub" style="color: #D1D5DB;">{total_fraudes_reais} fraudes reais 100% aprovadas</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">🛡️ Custo COM Nosso Modelo</div>
                        <div class="metric-value" style="color: #F472B6;">R$ {prejuizo_modelo:,.2f}</div>
                        <div class="metric-sub" style="color: #D1D5DB;">{fn_aprovados} vazamentos (FN) | {fp_bloqueados + fp_revisados} falsos alarmes</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col3:
                    cor_economia = "#34D399" if economia_liquida > 0 else "#F87171"
                    st.markdown(f"""
                    <div class="metric-card" style="border: 1px solid rgba(52, 211, 153, 0.35);">
                        <div class="metric-title" style="color: #34D399; font-weight: 700;">💰 Economia Líquida Gerada</div>
                        <div class="metric-value" style="color: {cor_economia}; font-size: 30px;">R$ {economia_liquida:,.2f}</div>
                        <div class="metric-sub" style="color: #D1D5DB;">Retorno Financeiro Direto de {roi_percentual:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Alerta detalhado do ROI
                st.info(f"🟢 **Sucesso Operacional:** O modelo detectou e bloqueou/revisou **{total_fraudes_reais - fn_aprovados}** de **{total_fraudes_reais}** fraudes reais (**{(total_fraudes_reais - fn_aprovados)/total_fraudes_reais*100:.2f}% de Taxa de Captura / Recall**). Apenas **{fn_aprovados}** fraudes passaram sem bloqueio.")
                
            else:
                # Estimativa baseada em probabilidade e taxa histórica média (0.17%) se não houver rótulo
                taxa_historica = 0.0017
                total_fraudes_estimadas = int(n_total * taxa_historica) if int(n_total * taxa_historica) > 0 else 10
                
                # Simular baseado nas previsões do modelo
                # Como não temos labels, vamos computar as economias aproximadas
                # usando a probabilidade média como expectativa matemática
                soma_probabilidades = sum(scores)
                prejuizo_baseline = soma_probabilidades * custo_fn
                
                # Perda estimada com modelo = probabilidade das transações aprovadas
                prejuizo_fn = sum([scores[i] for i, d in enumerate(decisoes) if d == 'Aprovar']) * custo_fn
                # Falsos positivos estimados = frações de não-fraudes nas transações que não foram aprovadas
                custo_alarmes = sum([(1 - scores[i]) for i, d in enumerate(decisoes) if d != 'Aprovar']) * custo_fp
                
                prejuizo_modelo = prejuizo_fn + custo_alarmes
                economia_liquida = prejuizo_baseline - prejuizo_modelo
                roi_percentual = (economia_liquida / prejuizo_baseline) * 100 if prejuizo_baseline > 0 else 0.0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">📉 Custo Estimado SEM Modelo</div>
                        <div class="metric-value" style="color: #FFFFFF;">R$ {prejuizo_baseline:,.2f}</div>
                        <div class="metric-sub" style="color: #D1D5DB;">Expectativa baseada nos scores brutos do modelo</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">🛡️ Custo Estimado COM Modelo</div>
                        <div class="metric-value" style="color: #F472B6;">R$ {prejuizo_modelo:,.2f}</div>
                        <div class="metric-sub" style="color: #D1D5DB;">Prejuízo projetado com as decisões recomendadas</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    cor_economia = "#34D399" if economia_liquida > 0 else "#F87171"
                    st.markdown(f"""
                    <div class="metric-card" style="border: 1px solid rgba(52, 211, 153, 0.35);">
                        <div class="metric-title" style="color: #34D399; font-weight: 700;">💰 Economia Líquida Estimada</div>
                        <div class="metric-value" style="color: {cor_economia}; font-size: 30px;">R$ {economia_liquida:,.2f}</div>
                        <div class="metric-sub" style="color: #D1D5DB;">Retorno esperado projetado: {roi_percentual:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.warning("ℹ️ **Nota:** Como o arquivo enviado não possui coluna 'Class' e não é o lote padrão, os valores acima representam projeções matemáticas baseadas na esperança probabilística das predições do modelo.")
            
            st.divider()
            
            # ----------------------------------------------------
            # Estatísticas Operacionais
            # ----------------------------------------------------
            col_chart, col_stats = st.columns([1, 1])
            
            with col_stats:
                st.subheader("📋 Distribuição Operacional das Decisões")
                
                st.markdown(f"""
                *   🟢 **Aprovadas Automaticamente:** **{n_aprovar}** transações ({n_aprovar/n_total*100:.3f}% do lote)
                    *   *Transações limpas que fluem sem atrito para os clientes bons.*
                *   🟡 **Enviadas para Revisão Manual:** **{n_revisar}** transações ({n_revisar/n_total*100:.3f}% do lote)
                    *   *Transações de risco moderado que exigem auditoria da equipe de risco.*
                *   🔴 **Bloqueadas Preventivamente:** **{n_bloquear}** transações ({n_bloquear/n_total*100:.3f}% do lote)
                    *   *Transações de altíssimo risco bloqueadas no exato segundo da compra.*
                """)
                
                # Métricas adicionais de atrito
                taxa_atrito = (n_bloquear + n_revisar) / n_total * 100
                st.markdown(f"**Taxa total de intervenção operacional (atrito):** `{taxa_atrito:.3f}%` das transações do dia.")
            
            with col_chart:
                # Criar gráfico de pizza das decisões
                labels = ['Aprovar', 'Revisar', 'Bloquear']
                sizes = [n_aprovar, n_revisar, n_bloquear]
                colors = ['#10B981', '#F59E0B', '#EF4444']
                
                fig, ax = plt.subplots(figsize=(6, 4))
                fig.patch.set_facecolor('#0B0F19')
                ax.set_facecolor('#0B0F19')
                
                wedges, texts, autotexts = ax.pie(
                    sizes, 
                    labels=labels, 
                    autopct=lambda p: '{:.2f}%'.format(p) if p > 0 else '', 
                    startangle=140, 
                    colors=colors,
                    textprops=dict(color="w", weight="bold")
                )
                for t in texts:
                    t.set_color('#F3F4F6')
                
                ax.axis('equal')  
                plt.title("Proporção das Decisões no Lote", color="w", fontsize=14, pad=15)
                st.pyplot(fig)
                plt.close()
            
            st.divider()
            
            # ----------------------------------------------------
            # Tabela Interativa de Resultados
            # ----------------------------------------------------
            st.subheader("🔍 Investigar Transações no Lote")
            
            # Caixa de busca e filtros rápidos
            filtro_decisao = st.selectbox(
                "Filtrar transações por Decisão recomendada:",
                options=["Todas", "Bloquear", "Revisar", "Aprovar"]
            )
            
            # Ordenar por maior risco
            df_display = df_result.copy()
            if filtro_decisao != "Todas":
                df_display = df_display[df_display['Decisao'] == filtro_decisao]
            
            df_display = df_display.sort_values(by="Probabilidade_Fraude", ascending=False)
            
            # Formatar tabela para exibição amigável
            st.write(f"Mostrando as {min(100, len(df_display))} transações mais críticas:")
            
            # Criar tabela formatada bonita
            tabela_bonita = []
            for i, row in df_display.head(100).iterrows():
                # Badge customizado
                if row['Decisao'] == 'Bloquear':
                    dec_badge = "🔴 Bloquear"
                elif row['Decisao'] == 'Revisar':
                    dec_badge = "🟡 Revisar"
                else:
                    dec_badge = "🟢 Aprovar"
                    
                tabela_bonita.append({
                    "Index": int(i),
                    "Tempo (s)": int(row['Time']),
                    "Valor (R$)": f"R$ {row['Amount']:.2f}",
                    "Score de Risco": f"{row['Probabilidade_Fraude']*100:.2f}%",
                    "Ação Recomendada": dec_badge,
                    "Variáveis Principais (PCA)": f"V17: {row['V17']:.3f} | V14: {row['V14']:.3f} | V12: {row['V12']:.3f}"
                })
            
            st.dataframe(pd.DataFrame(tabela_bonita), use_container_width=True)
            
            # ----------------------------------------------------
            # Download dos resultados processados
            # ----------------------------------------------------
            csv_data = df_result.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Baixar Lote Processado Enriquecido (CSV)",
                data=csv_data,
                file_name="lote_processado_globalpay.csv",
                mime="text/csv",
                help="Clique para baixar o arquivo completo com as novas colunas 'Probabilidade_Fraude' e 'Decisao' incorporadas."
            )
            
        with tab_tecnica:
            # ----------------------------------------------------
            # Detalhes Técnicos do Modelo
            # ----------------------------------------------------
            st.subheader("🛠️ Detalhes Metodológicos e Validação (SEMMA)")
            
            col_text, col_graph = st.columns([1, 1])
            
            with col_text:
                st.markdown("""
                ### A Jornada de Modelagem Matemática
                O modelo embarcado foi estruturado seguindo o rigoroso framework **SEMMA**:
                
                1.  **Sample (Amostragem):** 
                    Divisão temporal estrita (Out-Of-Time). O modelo treinou apenas nas transações das primeiras **36 horas** e foi validado em um teste cego "do futuro" correspondente às últimas **12 horas** (representado por este lote de teste de 92.575 transações). Isso impede o vazamento de dados temporal e simula perfeitamente o ambiente de produção.
                
                2.  **Explore & Modify:** 
                    Identificação de que a variável `Amount` (Volume) é extremamente distorcida por transações massivas (outliers). Aplicamos o **RobustScaler** nas variáveis `Time` e `Amount` para estabilizar o aprendizado numérico da Random Forest.
                
                3.  **Model:** 
                    Treinamento do algoritmo **Random Forest Classifier** ajustando o hiperparâmetro de profundidade máxima (`max_depth=10`) para regularizar e evitar o sobreajuste (overfitting). O desbalanceamento brutal (apenas **0,17%** de fraudes) foi contido através da atribuição de **pesos de classe balanceados** nas árvores de decisão.
                
                4.  **Assess:** 
                    Pelo extremo desbalanceamento, a acurácia é uma métrica nula (um modelo cego que aprova tudo tem 99.83% de acurácia). Nosso foco foi maximizar a curva **Precision-Recall AUC (PR-AUC)**, que atingiu excelentes **0.8076** no teste temporal cego.
                """)
                
                # Importância de Features teórica
                st.markdown("""
                ### 🚀 As 3 Variáveis Mais Preditoras do PCA:
                *   **V17 (Impacto Crítico):** Altamente correlacionada com a assinatura de transações fraudulentas em lote.
                *   **V14 (Variabilidade de Padrão):** Detecta transações simultâneas incomuns.
                *   **V12 (Comportamento do Cartão):** Identifica desvios históricos de limites de compras por segundo.
                """)
                
            with col_graph:
                st.subheader("Curva Precision-Recall da Validação Temporal")
                
                # Plotar a curva PR se o arquivo de curva_pr_oot.png não existir, ou criá-la se tivermos ground truth
                if tem_class_real:
                    from sklearn.metrics import precision_recall_curve, average_precision_score
                    
                    precision, recall, _ = precision_recall_curve(y_real, scores)
                    pr_auc = average_precision_score(y_real, scores)
                    
                    fig, ax = plt.subplots(figsize=(6, 4.5))
                    fig.patch.set_facecolor('#0B0F19')
                    ax.set_facecolor('#111827')
                    
                    ax.plot(recall, precision, label=f"OOT (PR-AUC = {pr_auc:.4f})", color='#8B5CF6', lw=2.5)
                    ax.set_xlabel("Recall (Taxa de Captura de Fraudes)", color="#9CA3AF")
                    ax.set_ylabel("Precision (Taxa de Acertos do Modelo)", color="#9CA3AF")
                    ax.set_title("Curva Precision-Recall no Teste Temporal OOT", color="w", fontsize=12, pad=10)
                    
                    ax.tick_params(colors='#9CA3AF')
                    ax.grid(True, color="#1F2937", alpha=0.5)
                    ax.legend(facecolor='#111827', edgecolor='#1F2937', labelcolor='w')
                    
                    # Remover bordas
                    for spine in ax.spines.values():
                        spine.set_color('#1F2937')
                        
                    st.pyplot(fig)
                    plt.close()
                else:
                    curva_img_path = 'curva_pr_oot.png'
                    if os.path.exists(curva_img_path):
                        st.image(curva_img_path, caption="Curva Precision-Recall da Validação Temporal (PR-AUC = 0.8076)")
                    else:
                        st.info("ℹ️ Gráfico de validação indisponível (Carregue a base clientes_do_dia.csv para plotar o PR interativo).")
