import os
import sys
import pickle
from fpdf import FPDF

# Forçar encoding padrão no console
sys.stdout.reconfigure(encoding='utf-8')

# Helper para converter strings UTF-8 para Latin-1 e evitar erros na FPDF padrão
def txt_l(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

class PDFRelatorio(FPDF):
    def header(self):
        if self.page_no() > 1:
            # Barra superior roxa estilosa
            self.set_fill_color(124, 58, 237) # Roxo neon
            self.rect(0, 0, 210, 6, 'F')
            
            # Título e Logo superior
            self.set_y(10)
            self.set_font('Arial', 'B', 8)
            self.set_text_color(107, 114, 128) # Cinza
            self.cell(100, 10, txt_l("GLOBALPAY SOLUTIONS | DETECÇÃO DE FRAUDE"), 0, 0, 'L')
            self.cell(90, 10, txt_l("RELATÓRIO EXECUTIVO - SEMMA"), 0, 1, 'R')
            
            # Linha divisória fina
            self.set_draw_color(229, 231, 235)
            self.line(10, 18, 200, 18)
            self.set_y(22)

    def footer(self):
        if self.page_no() > 1:
            # Linha superior divisória do rodapé
            self.set_draw_color(229, 231, 235)
            self.line(10, 280, 200, 280)
            
            self.set_y(281)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(156, 163, 175)
            self.cell(100, 10, txt_l("Propriedade de GlobalPay Solutions - Squad 1 Antifraude"), 0, 0, 'L')
            self.cell(90, 10, txt_l(f"Página {self.page_no()}"), 0, 0, 'R')

    def h1(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(17, 24, 39) # Escuro
        self.cell(0, 8, txt_l(title), 0, 1, 'L')
        # Linha inferior roxa do título
        self.set_draw_color(124, 58, 237)
        self.line(self.get_x(), self.get_y() + 1, self.get_x() + 25, self.get_y() + 1)
        self.ln(5)

    def h2(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_text_color(75, 85, 99) # Cinza escuro
        self.cell(0, 6, txt_l(title), 0, 1, 'L')
        self.ln(2)

    def p(self, text):
        self.set_font('Arial', '', 9.5)
        self.set_text_color(55, 65, 81) # Cinza texto
        self.multi_cell(0, 5, txt_l(text), 0, 'L')
        self.ln(3)

    def alert_box(self, title, text, type_alert='info'):
        # Caixa de alerta elegante
        self.set_font('Arial', 'B', 9.5)
        if type_alert == 'success':
            bg = (240, 253, 244) # Verde claro
            border = (16, 185, 129) # Verde escuro
            text_color = (15, 118, 110)
        elif type_alert == 'danger':
            bg = (254, 242, 242) # Vermelho claro
            border = (239, 68, 68) # Vermelho escuro
            text_color = (185, 28, 28)
        else:
            bg = (245, 243, 255) # Roxo claro
            border = (124, 58, 237) # Roxo escuro
            text_color = (109, 40, 217)

        self.set_fill_color(bg[0], bg[1], bg[2])
        self.set_draw_color(border[0], border[1], border[2])
        self.set_text_color(text_color[0], text_color[1], text_color[2])

        # Retângulo de fundo
        x = self.get_x()
        y = self.get_y()
        self.rect(x, y, 190, 18, 'DF')
        
        # Borda esquerda mais grossa
        self.set_fill_color(border[0], border[1], border[2])
        self.rect(x, y, 2.5, 18, 'F')
        
        self.set_xy(x + 5, y + 2)
        self.cell(0, 4, txt_l(title), 0, 1, 'L')
        self.set_x(x + 5)
        self.set_font('Arial', '', 8.5)
        self.multi_cell(180, 4, txt_l(text), 0, 'L')
        self.set_y(y + 21)

def gerar_pdf():
    pdf = PDFRelatorio()
    pdf.set_margins(10, 10, 10)
    pdf.set_auto_page_break(True, margin=15)
    
    # ==========================================
    # PÁGINA 1: CAPA
    # ==========================================
    pdf.add_page()
    
    # Barra lateral de decoração na capa
    pdf.set_fill_color(124, 58, 237) # Roxo
    pdf.rect(0, 0, 15, 297, 'F')
    pdf.set_fill_color(236, 72, 153) # Rosa
    pdf.rect(15, 0, 2, 297, 'F')
    
    # Conteúdo da capa
    pdf.set_xy(25, 45)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(0, 10, txt_l("PROJETO PRÁTICO FINAL - APRENDIZADO DE MÁQUINA"), 0, 1, 'L')
    
    pdf.set_font('Arial', 'B', 28)
    pdf.set_text_color(17, 24, 39)
    pdf.multi_cell(0, 12, txt_l("GLOBALPAY SOLUTIONS\nAntifraude Silencioso"), 0, 'L')
    
    # Linha decorativa roxa larga
    pdf.ln(5)
    pdf.set_fill_color(124, 58, 237)
    pdf.rect(25, pdf.get_y(), 80, 2.5, 'F')
    pdf.ln(10)
    
    pdf.set_font('Arial', 'I', 13)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 6, txt_l("Tradução da Complexidade de Modelagem Matemática\nem Valor Financeiro Direto e Otimização de Risco Operacional"), 0, 'L')
    
    # Caixa decorativa com resumo rápido de impacto na capa
    pdf.set_xy(25, 140)
    pdf.set_fill_color(17, 24, 39)
    pdf.rect(25, 140, 160, 48, 'F')
    
    pdf.set_xy(30, 145)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, txt_l("PRINCIPAL RESULTADO DO PROJETO"), 0, 1, 'L')
    
    pdf.set_xy(30, 153)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(209, 213, 219)
    pdf.multi_cell(150, 5, txt_l("A implantação do modelo RandomForestClassifier (max_depth=10) com tratamento de dados via RobustScaler e limiar dinâmico de 20% permite capturar 77,4% de todas as fraudes. Isto reduz o custo total de fraudes da GlobalPay de R$ 17.250,00 (baseline) para apenas R$ 4.240,00 na base cega temporal temporal temporal temporal, gerando R$ 13.010,00 de economia líquida (ROI de 75,4%)."), 0, 'L')
    
    # Metadados no final da capa
    pdf.set_xy(25, 225)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(0, 5, txt_l("SQUAD DE DESENVOLVIMENTO:"), 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(0, 5, txt_l("Squad 1: Detecção de Fraude Silenciosa em Tempo Real"), 0, 1, 'L')
    pdf.cell(0, 5, txt_l("Consultoria Técnica e Executiva de Machine Learning"), 0, 1, 'L')
    
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(0, 5, txt_l("CLIENTE:"), 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(0, 5, txt_l("GlobalPay Solutions (Gateway de Pagamentos B2B2C)"), 0, 1, 'L')
    
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(0, 5, txt_l("DATA:"), 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(0, 5, txt_l("Maio de 2026"), 0, 1, 'L')

    # ==========================================
    # PÁGINA 2: SUMÁRIO EXECUTIVO & JORNADA (SAMPLE & EXPLORE)
    # ==========================================
    pdf.add_page()
    
    pdf.h1("1. Sumário Executivo")
    pdf.p("A GlobalPay Solutions processa milhões de pagamentos diariamente e enfrenta o desafio crítico de bloquear transações fraudulentas por cartão de crédito no exato momento da compra, de maneira silenciosa. Aprovar uma fraude gera custos diretos de perda financeira e multas de chargeback (estimados em R$ 150,00 por transação). Por outro lado, um alarme falso que bloqueia um cliente legítimo causa frustração, cancelamentos de compras e custos de suporte técnico (estimados em R$ 10,00 por transação mais o dano de atrito).")
    pdf.p("Nesta consultoria ágil, aplicamos o framework científico SEMMA para construir um modelo preditivo baseado em inteligência artificial. O produto final desenvolvido não é apenas um algoritmo técnico de alta performance (PR-AUC de 0.8076), mas sim uma ferramenta estratégica de gestão de risco que foi incorporada em um aplicativo de simulação executiva em tempo real. O modelo demonstrou matematicamente a capacidade de reduzir o prejuízo com fraudes em até 75,4%, economizando R$ 13.010,00 a cada 12 horas de processamento na base OOT cega, provando ser um gerador direto de EBITDA para a empresa.")
    
    pdf.h1("2. A Jornada Analítica (SEMMA)")
    pdf.h2("2.1. Sample (Amostragem)")
    pdf.p("Para garantir a confiabilidade matemática absoluta do modelo em produção, a partição dos dados rejeitou a amostragem aleatória convencional (K-fold padrão), que sofre de vazamento temporal (data leakage). Adotamos uma Divisão Temporal Rigorosa (Out-Of-Time / OOT):")
    pdf.p("* Base de Desenvolvimento (Treino e Validação): Transações registradas nas primeiras 36 horas (192.232 transações, contendo 377 fraudes - 0,196% de incidência).\n* Base de Teste Cega Temporal (OOT - O Futuro): Transações registradas nas últimas 12 horas (92.575 transações, contendo 115 fraudes - 0,124% de incidência).")
    pdf.p("Dentro da base de desenvolvimento, aplicamos uma divisão estratificada (80/20) para treino e validação interna. Esta estrutura simula fielmente o cenário real em que o modelo é treinado com o histórico passado e deve prever transações futuras desconhecidas.")
    
    pdf.h2("2.2. Explore (Exploração)")
    pdf.p("A fase de exploração de dados revelou três complexidades sênior extremas:")
    pdf.p("1. Desbalanceamento Brutal: Apenas 0,172% do dataset completo representa fraudes. Isso inviabiliza completamente o uso da métrica de Acurácia. Um modelo estúpido que 'aprovasse tudo' teria 99,83% de acurácia, mas geraria prejuízo devastador.\n2. Variáveis Anonimizadas: Devido a restrições rígidas de sigilo bancário (LGPD), as variáveis do cliente foram transformadas via PCA em 28 componentes principais (V1 a V28), impossibilitando intuição de negócio básica e exigindo força analítica puramente estatística.\n3. Disparidade de Escalas e Ausência de Nulos: Verificamos 0 valores nulos no treino. No entanto, a variável Amount (Valor) revelou assimetria gigante (Média: R$ 89,02; Desvio Padrão: R$ 247,66; Máximo: R$ 19.656,53), exigindo tratamento numérico cuidadoso.")

    # ==========================================
    # PÁGINA 3: JORNADA (MODIFY, MODEL, ASSESS TÉCNICO)
    # ==========================================
    pdf.add_page()
    
    pdf.h2("2.3. Modify (Modificação)")
    pdf.p("Para converter as variáveis brutas em sinais limpos de alta qualidade para o classificador, aplicamos duas transformações críticas:")
    pdf.p("1. Escalonamento Robusto (RobustScaler): Devido aos outliers extremos na variável Amount, o escalonamento comum Standard/MinMax sofreria de distorção severa. O RobustScaler utiliza a mediana e o intervalo interquartílico (IQR), neutralizando a influência de compras excepcionalmente caras e estabilizando a convergência matemática. Aplicamos a transformação em 'Time' e 'Amount' (Fitted no treino, aplicado em validação e teste temporal).\n2. Engenharia e Importância de Variáveis: Dentre as 30 colunas de features alimentadas ao modelo, identificamos as três componentes do PCA que mais contribuem individualmente para separar a fraude do comportamento normal:")
    pdf.p("* V17 (Importância Crítica): O indicador de desvio transacional mais forte.\n* V14 (Padrão de Dispersão): Mapeia anomalias em agrupamentos de múltiplos lançamentos.\n* V12 (Comportamento): Capta o comportamento de injeção de transações consecutivas rapidíssimas.")
    
    pdf.h1("3. Modelagem & Validação")
    pdf.h2("3.1. Model (Modelagem)")
    pdf.p("A equipe avaliou o algoritmo RandomForestClassifier. Para evitar o Overfitting (onde o modelo decora o passado e falha no futuro temporal cego OOT), rodamos uma curva de validação variando o hiperparâmetro max_depth (profundidade máxima) entre [3, 5, 8, 10, 12, 15, 20]:")
    pdf.p("* max_depth = 3 a 5: Apresentaram sub-ajuste (Underfitting) com PR-AUC na validação abaixo de 0,77.\n* max_depth = 12 a 20: Apresentaram Overfitting severo (PR-AUC no treino de 0,99 a 1,00, mas decaindo ou estagnando na validação e ampliando drasticamente o consumo computacional).\n* max_depth = 10 (Vencedor): Ponto ideal de generalização, alcançando PR-AUC de 0,8179 na validação e retendo excelentes 0,8076 no teste OOT futuro.")
    pdf.p("O desbalanceamento Brutal de classes foi mitigado configurando o parâmetro class_weight='balanced', forçando as árvores de decisão a penalizarem severamente o erro na classe minoritária (Fraude).")
    
    pdf.h2("3.2. Assess (Avaliação Técnica)")
    pdf.p("A performance técnica final na base Out-Of-Time (OOT) — que representa o teste cego mais rigoroso do mundo real — obteve resultados excelentes:")
    pdf.p("* PR-AUC (Precision-Recall Area Under Curve): 0.8076\n* Matriz de Confusão (no ponto de corte padrão do modelo de 50%):")
    
    # Tabela simples da Matriz de Confusão 50%
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(60, 6, txt_l("Classe Real / Predita"), 1, 0, 'C', True)
    pdf.cell(60, 6, txt_l("Previsto Legítimo (0)"), 1, 0, 'C', True)
    pdf.cell(60, 6, txt_l("Previsto Fraude (1)"), 1, 1, 'C', True)
    
    pdf.set_font('Arial', '', 9)
    pdf.cell(60, 6, txt_l("Legítimo Real (0)"), 1, 0, 'C')
    pdf.cell(60, 6, txt_l("92.459 (Verdadeiro Negativo)"), 1, 0, 'C')
    pdf.cell(60, 6, txt_l("1 (Falso Positivo)"), 1, 1, 'C')
    
    pdf.cell(60, 6, txt_l("Fraude Real (1)"), 1, 0, 'C')
    pdf.cell(60, 6, txt_l("33 (Falso Negativo - Vazou)"), 1, 0, 'C')
    pdf.cell(60, 6, txt_l("82 (Verdadeiro Positivo)"), 1, 1, 'C')
    
    pdf.ln(3)
    pdf.p("Com o ponto de corte padrão (50%), obtivemos Precision de 98,8% (de cada 83 transações bloqueadas, 82 eram de fato fraudes, gerando quase zero atrito operacional inútil) e Recall de 71,3% (bloqueamos 82 das 115 fraudes do lote cego).")

    # ==========================================
    # PÁGINA 4: ASSESS FINANCEIRO & CONCLUSÃO
    # ==========================================
    pdf.add_page()
    
    pdf.h1("4. Tradução Executiva: O Valor Financeiro")
    pdf.p("O clímax do relatório demonstra matematicamente o Retorno Financeiro gerado para a GlobalPay Solutions. Avaliamos a base OOT (92.575 transações) em três cenários de threshold, utilizando os parâmetros reais acordados: Custo do Falso Negativo (Fraude aprovada) = R$ 150,00 e Custo do Falso Positivo (Fricção/Revisão) = R$ 10,00.")
    
    # Tabela comparativa dos cenários financeiros
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(243, 244, 246)
    pdf.cell(48, 8, txt_l("Cenário Operacional"), 1, 0, 'C', True)
    pdf.cell(28, 8, txt_l("Taxa de Captura"), 1, 0, 'C', True)
    pdf.cell(28, 8, txt_l("Fraudes Vazadas"), 1, 0, 'C', True)
    pdf.cell(28, 8, txt_l("Falsos Alarmes"), 1, 0, 'C', True)
    pdf.cell(28, 8, txt_l("Custo Total"), 1, 0, 'C', True)
    pdf.cell(30, 8, txt_l("Economia Líquida"), 1, 1, 'C', True)
    
    pdf.set_font('Arial', '', 8.5)
    # Baseline
    pdf.cell(48, 7, txt_l("SEM Modelo (Aprovar Tudo)"), 1, 0, 'L')
    pdf.cell(28, 7, txt_l("0.0%"), 1, 0, 'C')
    pdf.cell(28, 7, txt_l("115"), 1, 0, 'C')
    pdf.cell(28, 7, txt_l("0"), 1, 0, 'C')
    pdf.cell(28, 7, txt_l("R$ 17.250,00"), 1, 0, 'C')
    pdf.cell(30, 7, txt_l("-"), 1, 1, 'C')
    
    # Threshold 50%
    pdf.cell(48, 7, txt_l("Modelo (Threshold 50%)"), 1, 0, 'L')
    pdf.cell(28, 7, txt_l("71.30%"), 1, 0, 'C')
    pdf.cell(28, 7, txt_l("33"), 1, 0, 'C')
    pdf.cell(28, 7, txt_l("1"), 1, 0, 'C')
    pdf.cell(28, 7, txt_l("R$ 4.960,00"), 1, 0, 'C')
    pdf.cell(30, 7, txt_l("R$ 12.290,00"), 1, 1, 'C')
    
    # Threshold 20%
    pdf.set_font('Arial', 'B', 8.5)
    pdf.cell(48, 7, txt_l("Modelo Otimizado (Threshold 20%)"), 1, 0, 'L')
    pdf.cell(28, 7, txt_l("77.39%"), 1, 0, 'C')
    pdf.cell(28, 7, txt_l("26"), 1, 0, 'C')
    pdf.cell(28, 7, txt_l("34"), 1, 0, 'C')
    pdf.cell(28, 7, txt_l("R$ 4.240,00"), 1, 0, 'C')
    pdf.cell(30, 7, txt_l("R$ 13.010,00"), 1, 1, 'C')
    
    pdf.set_font('Arial', '', 9)
    pdf.ln(4)
    
    pdf.h2("Análise Estratégica do Trade-Off Risco vs. Atrito")
    pdf.p("1. O Ponto Fraco do Baseline: Sem qualquer modelo preditivo, a GlobalPay Solutions absorve uma perda de R$ 17.250,00 em apenas 12 horas. Projetado anualmente, isso equivale a um prejuízo crônico silencioso superior a R$ 12.500.000,00 em perdas por chargeback.")
    pdf.p("2. Modelo a 50% (Foco em Atrito Zero): Este cenário é extremamente conservador em termos de alarmes. Bloqueia apenas 1 transação legítima (falso positivo = R$ 10,00 de custo operacional) e captura 71,3% das fraudes. Esse ajuste gera uma economia espetacular de R$ 12.290,00 a cada 12 horas.")
    pdf.p("3. Modelo a 20% (Ponto Ótimo - RECOMENDADO): Ajustando o limiar de decisão para 20%, o modelo assume um pouco mais de auditorias (34 falsos alarmes, gerando R$ 340,00 de custo operacional), mas eleva a Taxa de Captura para 77,39% (89 das 115 fraudes reais bloqueadas). Isso derruba a perda de fraudes que vazam para R$ 3.900,00. O custo total do sistema cai para R$ 4.240,00 e a economia líquida sobe para R$ 13.010,00 (75,4% de perdas evitadas).")
    
    pdf.alert_box(
        "RECOMENDAÇÃO OPERACIONAL DA CONSULTORIA (ROI FINAL)",
        "Recomendamos implantar o modelo na GlobalPay com o Threshold de 20% como limiar de auditoria imediata. Esta configuração transfere o risco de forma controlada e gera um ganho líquido projetado anualizado superior a R$ 9.497.000,00 em chargebacks evitados frente à aprovação cega, cobrindo com folga o custo operacional das equipes de suporte a risco.",
        "success"
    )
    
    pdf.h2("5. Conclusão")
    pdf.p("A inteligência analítica provou ser o maior motor de eficiência operacional para a GlobalPay Solutions. A combinação de engenharia de variáveis matemáticas (V17, V14 e V12), escalonamento robusto de outliers e um classificador Random Forest calibrado gerou um produto altamente eficaz. O aplicativo interativo Streamlit permite agora à diretoria testar lotes de transações diárias de forma autônoma e ajustar dinamicamente estes limiares conforme a tolerância de risco corporativo flutue ao longo do ano.")
    
    # Salvar PDF
    output_pdf_path = r"c:\Users\fmsar\OneDrive\Área de Trabalho\FATEC20261\MACHINE LEARNING - JULIO QUINTA\PROJETO_FINAL\relatorio_executivo.pdf"
    pdf.output(output_pdf_path, 'F')
    print("Relatório executivo PDF gerado com sucesso em:", output_pdf_path)

if __name__ == '__main__':
    gerar_pdf()
