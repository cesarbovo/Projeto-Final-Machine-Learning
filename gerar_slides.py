import os
import sys
from fpdf import FPDF

# Forçar encoding padrão no console
sys.stdout.reconfigure(encoding='utf-8')

# Helper para converter strings UTF-8 para Latin-1 e evitar erros na FPDF padrão
def txt_l(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

class PresentationPDF(FPDF):
    def __init__(self):
        # Inicializa em modo paisagem (Landscape A4: 297mm x 210mm)
        super().__init__(orientation='L', unit='mm', format='A4')
        self.set_margins(15, 15, 15)
        self.set_auto_page_break(False)

    def draw_slide_decorations(self, title):
        # 1. Fundo Escuro do Slide (Dark Charcoal #0B0F19)
        self.set_fill_color(11, 15, 25)
        self.rect(0, 0, 297, 210, 'F')
        
        # 2. Barra Lateral de Identidade Visual da GlobalPay (Roxo e Rosa Neon)
        self.set_fill_color(124, 58, 237) # Roxo
        self.rect(0, 0, 6, 210, 'F')
        self.set_fill_color(236, 72, 153) # Rosa
        self.rect(6, 0, 1.5, 210, 'F')
        
        # 3. Título Superior do Slide
        self.set_xy(18, 12)
        self.set_font('Arial', 'B', 20)
        self.set_text_color(255, 255, 255) # Branco Puro
        self.cell(0, 10, txt_l(title), 0, 1, 'L')
        
        # Linha fina roxa abaixo do título
        self.set_fill_color(124, 58, 237)
        self.rect(18, 23, 120, 1, 'F')
        
        # 4. Rodapé do Slide
        self.set_y(195)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(156, 163, 175) # Cinza claro
        self.set_x(18)
        self.cell(100, 10, txt_l("GlobalPay Solutions - Squad 1 Antifraude"), 0, 0, 'L')
        self.set_x(250)
        self.cell(30, 10, txt_l(f"Slide {self.page_no()}"), 0, 0, 'R')

    def draw_stat_callout(self, x, y, value, label, sublabel):
        # Desenha uma caixa de métrica glassmorphism elegante
        self.set_fill_color(17, 24, 39) # Fundo Cinza Escuro
        self.set_draw_color(31, 41, 55) # Borda cinza
        self.rect(x, y, 78, 38, 'DF')
        
        # Linha decorativa roxa na esquerda do card
        self.set_fill_color(124, 58, 237)
        self.rect(x, y, 1.5, 38, 'F')
        
        # Valor principal
        self.set_xy(x + 4, y + 4)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(244, 114, 182) # Rosa Neon
        self.cell(70, 8, txt_l(value), 0, 1, 'L')
        
        # Label
        self.set_x(x + 4)
        self.set_font('Arial', 'B', 8.5)
        self.set_text_color(255, 255, 255) # Branco
        self.cell(70, 5, txt_l(label), 0, 1, 'L')
        
        # Sublabel
        self.set_x(x + 4)
        self.set_font('Arial', '', 7.5)
        self.set_text_color(156, 163, 175) # Cinza claro
        self.multi_cell(70, 4, txt_l(sublabel), 0, 'L')

def gerar_slides():
    pdf = PresentationPDF()
    
    # ==========================================
    # SLIDE 1: CAPA
    # ==========================================
    pdf.add_page()
    # Fundo Escuro
    pdf.set_fill_color(11, 15, 25)
    pdf.rect(0, 0, 297, 210, 'F')
    
    # Barra lateral grossa roxo/rosa
    pdf.set_fill_color(124, 58, 237)
    pdf.rect(0, 0, 12, 210, 'F')
    pdf.set_fill_color(236, 72, 153)
    pdf.rect(12, 0, 3, 210, 'F')
    
    # Conteúdo da capa
    pdf.set_xy(30, 45)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(0, 10, txt_l("BOARD MEETING - APRESENTAÇÃO EXECUTIVA DE RISCO"), 0, 1, 'L')
    
    pdf.set_x(30)
    pdf.set_font('Arial', 'B', 32)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(0, 14, txt_l("GLOBALPAY SOLUTIONS\nDetecção de Fraude Silenciosa"), 0, 'L')
    
    # Linha divisória
    pdf.ln(5)
    pdf.set_fill_color(124, 58, 237)
    pdf.rect(30, pdf.get_y(), 120, 2.5, 'F')
    pdf.ln(10)
    
    pdf.set_x(30)
    pdf.set_font('Arial', 'I', 14)
    pdf.set_text_color(209, 213, 219)
    pdf.cell(0, 8, txt_l("Tradução do Rigor de Machine Learning em Retorno Financeiro Direto (ROI)"), 0, 1, 'L')
    
    # Metadata inferior
    pdf.set_xy(30, 145)
    pdf.set_font('Arial', 'B', 10.5)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 5, txt_l("AUTOR DA CONSULTORIA:"), 0, 1, 'L')
    pdf.set_x(30)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(209, 213, 219)
    pdf.cell(0, 5, txt_l("Squad 1: Detecção de Fraude Silenciosa em Tempo Real (Gateway B2B2C)"), 0, 1, 'L')
    
    pdf.ln(4)
    pdf.set_x(30)
    pdf.set_font('Arial', 'B', 10.5)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 5, txt_l("DIRECIONADO A:"), 0, 1, 'L')
    pdf.set_x(30)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(209, 213, 219)
    pdf.cell(0, 5, txt_l("Diretoria Executiva e Gestão de Risco da GlobalPay Solutions"), 0, 1, 'L')
    
    pdf.ln(4)
    pdf.set_x(30)
    pdf.set_font('Arial', 'B', 10.5)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 5, txt_l("DATA:"), 0, 1, 'L')
    pdf.set_x(30)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(209, 213, 219)
    pdf.cell(0, 5, txt_l("Maio de 2026"), 0, 1, 'L')

    # ==========================================
    # SLIDE 2: A DOR / O PROBLEMA
    # ==========================================
    pdf.add_page()
    pdf.draw_slide_decorations("1. O Custo Invisível da Fraude no Gateway")
    
    # Caixa esquerda para Métricas Gigantes
    pdf.draw_stat_out = pdf.draw_stat_callout(20, 38, "R$ 12.500.000,00", "PERDA ANUAL SILENCIOSA", "Prejuízo projetado com base em fraudes não bloqueadas no gateway.")
    pdf.draw_stat_out = pdf.draw_stat_callout(20, 80, "99.83%", "ALTA ACURÁCIA CEGA", "Falsa segurança gerada pelo brutal desbalanceamento das transações do dia.")
    pdf.draw_stat_out = pdf.draw_stat_callout(20, 122, "R$ 150,00 vs. R$ 10,00", "BALANÇO DE CUSTOS POR OPERAÇÃO", "Prejuízo por chargeback de fraude (FN) contra custo operacional de atrito (FP).")
    
    # Texto à direita explicativo
    pdf.set_xy(110, 38)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 6, txt_l("A Dor de Negócio da GlobalPay Solutions:"), 0, 1, 'L')
    
    pdf.set_x(110)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(229, 231, 235)
    pdf.multi_cell(165, 5, txt_l("* As Duas Feridas Operacionais:\n  A GlobalPay opera com chargebacks devastadores. Cada fraude aprovada incorretamente (Falso Negativo) custa R$ 150,00 de prejuízo direto. Por outro lado, bloquear incorretamente um cliente bom (Falso Positivo) gera fricção de suporte de R$ 10,00 e perda de faturamento.\n\n* A Ilusão da Acurácia:\n  Com apenas 0,172% de fraudes reais no banco de dados, aprovar cega e indiscriminadamente todas as transações resulta em uma 'acurácia' de 99,83%. No entanto, esse comportamento drena R$ 17.250,00 de caixa operacional a cada 12 horas.\n\n* O Desafio Matemático:\n  Os dados são anonimizados via PCA (V1 a V28), impossibilitando intuição básica de comércio. Apenas a modelagem matemática robusta em tempo real pode desmascarar a fraude oculta de forma silenciosa e instantânea no momento exato do checkout."), 0, 'L')

    # ==========================================
    # SLIDE 3: A JORNADA TÉCNICA (SEMMA)
    # ==========================================
    pdf.add_page()
    pdf.draw_slide_decorations("2. Rigor Científico na Jornada SEMMA")
    
    # Três blocos verticais representando as etapas
    # Bloco 1: Sample & Explore
    x1, y1 = 20, 38
    pdf.set_fill_color(17, 24, 39)
    pdf.set_draw_color(31, 41, 55)
    pdf.rect(x1, y1, 80, 140, 'DF')
    pdf.set_fill_color(124, 58, 237)
    pdf.rect(x1, y1, 80, 2, 'F')
    
    pdf.set_xy(x1 + 4, y1 + 6)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(72, 6, txt_l("Amostragem & Análise"), 0, 1, 'L')
    pdf.set_x(x1 + 4)
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(72, 4, txt_l("SAMPLE & EXPLORE"), 0, 1, 'L')
    pdf.ln(4)
    pdf.set_x(x1 + 4)
    pdf.set_font('Arial', '', 9.5)
    pdf.set_text_color(209, 213, 219)
    pdf.multi_cell(72, 5, txt_l("* Divisão Temporal OOT:\n  Isolamento estrito das primeiras 36h para desenvolvimento e as últimas 12h para teste temporal cego do futuro (92.575 transações).\n\n* Desbalanceamento Brutal:\n  Calibração manual focada no PR-AUC por haver apenas 0,172% de fraudes (492 em 284.807 registros).\n\n* Sem Vazamento:\n  Garantia de integridade para simular produção perfeitamente."), 0, 'L')
    
    # Bloco 2: Modify
    x2, y2 = 108, 38
    pdf.set_fill_color(17, 24, 39)
    pdf.rect(x2, y2, 80, 140, 'DF')
    pdf.set_fill_color(124, 58, 237)
    pdf.rect(x2, y2, 80, 2, 'F')
    
    pdf.set_xy(x2 + 4, y2 + 6)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(72, 6, txt_l("Engenharia de Sinais"), 0, 1, 'L')
    pdf.set_x(x2 + 4)
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(72, 4, txt_l("MODIFY"), 0, 1, 'L')
    pdf.ln(4)
    pdf.set_x(x2 + 4)
    pdf.set_font('Arial', '', 9.5)
    pdf.set_text_color(209, 213, 219)
    pdf.multi_cell(72, 5, txt_l("* RobustScaler de Outliers:\n  Neutralização do impacto de transações de valores exorbitantes (outliers até R$ 19k) na coluna 'Amount' e 'Time' usando a mediana.\n\n* Seleção das 3 Melhores PCAs:\n  Mapeamento de features por Random Forest:\n  - V17 (Desvio Transacional Crítico)\n  - V14 (Padrão de Dispersão no Dia)\n  - V12 (Frequência e Limite do Cartão)"), 0, 'L')
    
    # Bloco 3: Model & Assess
    x3, y3 = 196, 38
    pdf.set_fill_color(17, 24, 39)
    pdf.rect(x3, y3, 80, 140, 'DF')
    pdf.set_fill_color(236, 72, 153) # Rosa
    pdf.rect(x3, y3, 80, 2, 'F')
    
    pdf.set_xy(x3 + 4, y3 + 6)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(72, 6, txt_l("Calibração & Performance"), 0, 1, 'L')
    pdf.set_x(x3 + 4)
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(72, 4, txt_l("MODEL & ASSESS TÉCNICO"), 0, 1, 'L')
    pdf.ln(4)
    pdf.set_x(x3 + 4)
    pdf.set_font('Arial', '', 9.5)
    pdf.set_text_color(209, 213, 219)
    pdf.multi_cell(72, 5, txt_l("* RandomForest Classifier:\n  Ajuste fino de árvores de decisão. Escolha de max_depth=10 para regularização perfeita e class_weight='balanced'.\n\n* Curva PR Vencedora:\n  Área Sob a Curva Precision-Recall de 0.8076 no teste cego Out-Of-Time (futuro temporal).\n\n* Alta Precisão:\n  98,8% de precisão a 50%, bloqueando 82 de 83 com quase zero atrito operacional."), 0, 'L')

    # ==========================================
    # SLIDE 4: DEMONSTRAÇÃO DO APLICATIVO
    # ==========================================
    pdf.add_page()
    pdf.draw_slide_decorations("3. Demonstração Executiva do Painel Web")
    
    # Lado esquerdo: Características
    pdf.set_xy(20, 38)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(100, 6, txt_l("A Central Operacional do Gestor de Risco:"), 0, 1, 'L')
    
    pdf.set_x(20)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(229, 231, 235)
    pdf.multi_cell(115, 6, txt_l("* Upload de Lote Simples:\n  Permite ao analista subir arquivos .csv diários e enriquecê-los imediatamente.\n\n* Simulações em Tempo Real:\n  Sliders dinâmicos recalculam o atrito e as perdas financeiras na hora com base na margem de tolerância corporativa.\n\n* Tabela Inteligente Integrada:\n  Ordenação de risco decrescente com indicação visual intuitiva por badges coloridos (🔴 Bloquear, 🟡 Revisar, 🟢 Aprovar).\n\n* Download de Exportação ágil:\n  Botão integrado para exportar as decisões estruturadas em segundos."), 0, 'L')
    
    # Lado direito: Representação gráfica do App (Mockup de Interface)
    xr, yr = 145, 38
    pdf.set_fill_color(17, 24, 39)
    pdf.set_draw_color(31, 41, 55)
    pdf.rect(xr, yr, 132, 140, 'DF')
    
    # Título do Mockup
    pdf.set_xy(xr + 6, yr + 6)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(120, 6, txt_l("Visualização da Interface (Streamlit)"), 0, 1, 'L')
    pdf.set_fill_color(124, 58, 237)
    pdf.rect(xr + 6, yr + 13, 30, 0.8, 'F')
    
    # Cards simulados no Mockup
    pdf.set_fill_color(11, 15, 25)
    pdf.rect(xr + 6, yr + 20, 36, 22, 'DF')
    pdf.rect(xr + 48, yr + 20, 36, 22, 'DF')
    pdf.rect(xr + 90, yr + 20, 36, 22, 'DF')
    
    pdf.set_xy(xr + 8, yr + 22)
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(32, 4, txt_l("📉 CUSTO SEM MODELO"), 0, 1, 'C')
    pdf.set_x(xr + 8)
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(32, 5, txt_l("R$ 17.250,00"), 0, 1, 'C')
    
    pdf.set_xy(xr + 50, yr + 22)
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(32, 4, txt_l("🛡️ CUSTO COM MODELO"), 0, 1, 'C')
    pdf.set_x(xr + 50)
    pdf.set_font('Arial', 'B', 8.5)
    pdf.set_text_color(244, 114, 182) # Rosa Neon
    pdf.cell(32, 5, txt_l("R$ 4.240,00"), 0, 1, 'C')
    
    pdf.set_xy(xr + 92, yr + 22)
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(32, 4, txt_l("💰 ECONOMIA LÍQUIDA"), 0, 1, 'C')
    pdf.set_x(xr + 92)
    pdf.set_font('Arial', 'B', 9.5)
    pdf.set_text_color(52, 211, 153) # Verde Neon
    pdf.cell(32, 5, txt_l("R$ 13.010,00"), 0, 1, 'C')
    
    # Simulação de tabela
    pdf.set_xy(xr + 6, yr + 50)
    pdf.set_font('Arial', 'B', 7.5)
    pdf.set_fill_color(31, 41, 55)
    pdf.cell(20, 5, txt_l("Tempo (s)"), 1, 0, 'C', True)
    pdf.cell(25, 5, txt_l("Valor (R$)"), 1, 0, 'C', True)
    pdf.cell(25, 5, txt_l("Score Risco"), 1, 0, 'C', True)
    pdf.cell(50, 5, txt_l("Ação Recomendada"), 1, 1, 'C', True)
    
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(209, 213, 219)
    # Linha 1
    pdf.set_x(xr + 6)
    pdf.cell(20, 4, txt_l("130182"), 1, 0, 'C')
    pdf.cell(25, 4, txt_l("R$ 956,20"), 1, 0, 'C')
    pdf.cell(25, 4, txt_l("98,40%"), 1, 0, 'C')
    pdf.cell(50, 4, txt_l("Bloquear (Alto Risco)"), 1, 1, 'C')
    
    # Linha 2
    pdf.set_x(xr + 6)
    pdf.cell(20, 4, txt_l("130245"), 1, 0, 'C')
    pdf.cell(25, 4, txt_l("R$ 145,00"), 1, 0, 'C')
    pdf.cell(25, 4, txt_l("32,15%"), 1, 0, 'C')
    pdf.cell(50, 4, txt_l("Revisar (Médio Risco)"), 1, 1, 'C')
    
    # Linha 3
    pdf.set_x(xr + 6)
    pdf.cell(20, 4, txt_l("130291"), 1, 0, 'C')
    pdf.cell(25, 4, txt_l("R$ 12,50"), 1, 0, 'C')
    pdf.cell(25, 4, txt_l("0,02%"), 1, 0, 'C')
    pdf.cell(50, 4, txt_l("Aprovar (Baixo Risco)"), 1, 1, 'C')
    
    # Nota no Mockup
    pdf.set_xy(xr + 6, yr + 85)
    pdf.set_font('Arial', 'I', 8)
    pdf.set_text_color(156, 163, 175)
    pdf.multi_cell(120, 4, txt_l("Interface dinâmica otimizada com acessibilidade total. Textos em alto contraste branco e tons neon sobre o fundo escuro para melhor legibilidade operacional em condições reais de alta pressão."), 0, 'L')

    # ==========================================
    # SLIDE 5: O CLÍMAX FINANCEIRO (ROI)
    # ==========================================
    pdf.add_page()
    pdf.draw_slide_decorations("4. Tradução Executiva: Retorno Financeiro (ROI)")
    
    # Tabela Executiva
    yt = 38
    pdf.set_xy(20, yt)
    pdf.set_font('Arial', 'B', 10.5)
    pdf.set_fill_color(31, 41, 55)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(60, 8, txt_l("Cenário Operacional"), 1, 0, 'C', True)
    pdf.cell(32, 8, txt_l("Taxa de Captura"), 1, 0, 'C', True)
    pdf.cell(35, 8, txt_l("Prejuízo (12h)"), 1, 0, 'C', True)
    pdf.cell(40, 8, txt_l("Economia (12h)"), 1, 0, 'C', True)
    pdf.cell(48, 8, txt_l("Ganho Anualizado"), 1, 1, 'C', True)
    
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(229, 231, 235)
    
    # Linha 1: Baseline
    pdf.set_x(20)
    pdf.cell(60, 8, txt_l("SEM Modelo (Aprovar Tudo)"), 1, 0, 'L')
    pdf.cell(32, 8, txt_l("0.0%"), 1, 0, 'C')
    pdf.cell(35, 8, txt_l("R$ 17.250,00"), 1, 0, 'C')
    pdf.cell(40, 8, txt_l("R$ 0,00"), 1, 0, 'C')
    pdf.cell(48, 8, txt_l("-"), 1, 1, 'C')
    
    # Linha 2: 50%
    pdf.set_x(20)
    pdf.cell(60, 8, txt_l("Modelo (Threshold 50%)"), 1, 0, 'L')
    pdf.cell(32, 8, txt_l("71.30%"), 1, 0, 'C')
    pdf.cell(35, 8, txt_l("R$ 4.960,00"), 1, 0, 'C')
    pdf.cell(40, 8, txt_l("R$ 12.290,00"), 1, 0, 'C')
    pdf.cell(48, 8, txt_l("R$ 8.971.700,00"), 1, 1, 'C')
    
    # Linha 3: 20% (Recomendado)
    pdf.set_x(20)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(52, 211, 153) # Verde Neon
    pdf.cell(60, 8, txt_l("Modelo Otimizado (Threshold 20%)"), 1, 0, 'L')
    pdf.cell(32, 8, txt_l("77.39%"), 1, 0, 'C')
    pdf.cell(35, 8, txt_l("R$ 4.240,00"), 1, 0, 'C')
    pdf.cell(40, 8, txt_l("R$ 13.010,00"), 1, 0, 'C')
    pdf.cell(48, 8, txt_l("R$ 9.497.300,00"), 1, 1, 'C')
    
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(229, 231, 235)
    pdf.ln(5)
    
    # Caixa verde de conclusão/recomendação
    pdf.set_x(20)
    y_alert = pdf.get_y()
    pdf.set_fill_color(20, 83, 45) # Verde floresta escuro
    pdf.set_draw_color(52, 211, 153) # Verde Neon
    pdf.rect(20, y_alert, 215, 38, 'DF')
    pdf.rect(20, y_alert, 2, 38, 'F')
    
    pdf.set_xy(24, y_alert + 3)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(52, 211, 153)
    pdf.cell(200, 6, txt_l("DECISÃO ESTRATÉGICA DE NEGÓCIO: ADOÇÃO DO LIMIAR DE 20%"), 0, 1, 'L')
    
    pdf.set_x(24)
    pdf.set_font('Arial', '', 9.5)
    pdf.set_text_color(229, 231, 235)
    pdf.multi_cell(208, 4.5, txt_l("Recomendamos a ativação do modelo em produção parametrizado com o Threshold de 20%. Isso garante a mitigação de 77,4% de todas as fraudes. Assumimos um aumento controlado de revisões operacionais da equipe (34 falsos alarmes), mas evitamos perdas por chargebacks, resultando em uma economia líquida imediata de R$ 13.010,00 a cada 12 horas. Anualizando essa eficiência, trazemos de volta ao EBITDA da GlobalPay R$ 9.497.300,00 em perdas que simplesmente deixaram de existir."), 0, 'L')
    
    # Próximos passos ao lado direito
    pdf.set_xy(242, yt)
    pdf.set_font('Arial', 'B', 10.5)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(40, 6, txt_l("Rollout da API (3 Semanas):"), 0, 1, 'L')
    pdf.set_fill_color(124, 58, 237)
    pdf.rect(242, yt + 6.5, 30, 0.8, 'F')
    
    pdf.set_xy(242, yt + 11)
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(209, 213, 219)
    pdf.multi_cell(45, 4.5, txt_l("Semana 1:\nIntegração do modelo em ambiente de testes sandbox via API REST.\n\nSemana 2:\nOperação shadow (prevendo sem bloquear) para aferição.\n\nSemana 3:\nRollout completo com threshold de 20%."), 0, 'L')

    # Salvar Slides PDF
    output_slides_path = r"c:\Users\fmsar\OneDrive\Área de Trabalho\FATEC20261\MACHINE LEARNING - JULIO QUINTA\PROJETO_FINAL\slides_pitch.pdf"
    pdf.output(output_slides_path, 'F')
    print("Slides da apresentação em PDF gerados com sucesso em:", output_slides_path)

if __name__ == '__main__':
    gerar_slides()
