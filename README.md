# Análise Preditiva e precificação de Aluguéis em Brasília/DF

## Visão Geral do Projeto
Projeto desenvolvido para coletar, analisar e modelar o preço de aluguel de apartamentos em Brasília/DF. Foram raspados 171 anúncios do portal Wimóveis (https://www.wimoveis.com.br) para identificar os principais fatores que afetam o preço final do imóvel e construir um modelo preditivo.

## Tecnologias Utilizadas
- **Linguagem:** Python
- **Análise & Manipulação:** Pandas, NumPy
- **Visualização de Dados:** Seaborn, Matplotlib
- **Machine Learning:** Scikit-Learn (LinearRegression, Ridge, Lasso)
- **Diagnóstico Estatístico:** Statsmodels (VIF, Análise de Resíduos)

## Principais Insights da Análise Exploratória (EDA)
- **Área Útil vs. Preço:** Forte correlação linear positiva entre metragem (m^2) e preço total do aluguel.
- **Tratamento de Outliers:** Aplicação do método IQR (3x) eliminou registros discrepantes que distorciam os coeficientes do modelo.
- **Variação Regional:** Bairros de alta renda (ex: Asa Sul, Noroeste) apresentam precificação discrepante por $m^2$ quando comparados a outras regiões do DF.

## Resultados do Modelo Preditivo
| Modelo | R² | RMSE | MAE |
| :--- | :---: | :---: | :---: |
| Regressão Linear Múltipla | 0,79 | R$ 1468,14 | R$ 997,39 |
| Regressão Ridge | 0,78 | R$ 1514,72 | R$ 1047,25 |
| Regressão Lasso | 0,79 | R$ 1629,37 | R$ 887,50 |
