---
name: cadencia-pequenos-passos
description: >-
  Use esta skill em todas as interações de desenvolvimento, análise de dados e modelagem preditiva no TCC.
  Garante o cumprimento estrito do Princípio dos Pequenos Passos: um procedimento por vez, códigos modulares
  e curtos (< 80-100 linhas), explicação prévia da intuição, execução exclusiva pelo pesquisador no terminal,
  e pausa obrigatória para reflexão e validação conjunta antes de qualquer avanço.
---

# Protocolo Operacional: Cadência e Princípio dos Pequenos Passos

Esta skill estabelece a metodologia de colaboração e pair programming entre o assistente de IA e o pesquisador no projeto do TCC. O objetivo central é assegurar que o pesquisador compreenda, acompanhe, valide e aprenda cada decisão metodológica sem sobrecarga cognitiva.

---

## Os 5 Mandamentos da Cadência

### 1. Um Passo de Cada Vez (Single-Step Execution)
- **Proibição de Encadear Tarefas**: Nunca executar ou propor múltiplos procedimentos complexos em uma única resposta (ex: criar script, rodar modelo, gerar gráfico e atualizar relatório tudo de uma vez).
- **Foco Cirúrgico**: Cada interação deve resolver apenas o micro-passo imediatamente acordado.

### 2. Intuição Teórica Prévia e Códigos Enxutos (< 80–100 Linhas)
- **Pedagogia em Primeiro Lugar**: Antes de apresentar o código, explicar em poucas palavras a intuição do método (o que ele faz, por que estamos usando e como funciona matematicamente).
- **Legibilidade e Modularidade**: Evitar scripts monolíticos. Os arquivos devem ser curtos, modulares, ricamente comentados nos pontos estratégicos e fáceis de auditar linha por linha pelo pesquisador.

### 3. Execução Soberana pelo Pesquisador
- **O Agente Escreve, o Pesquisador Executa**: O assistente prepara o script, disponibiliza o link navegável e fornece o comando exato do PowerShell apontando para o ambiente virtual (`.venv`).
- **Autonomia da IDE**: O assistente nunca deve rodar scripts de modelagem ou pipelines em segundo plano sem que o usuário tenha assumido o controle da execução na sua própria máquina.

### 4. Pausa Obrigatória para Reflexão Conjunta
- **Parada Imediata após a Saída**: Assim que o pesquisador cola a saída do terminal, o assistente **deve pausar**.
- **Auditoria Qualitativa**:
  * O que esses números significam na prática?
  * Houve alguma anomalia ou armadilha metodológica (ex: vazamento de ID, overfitting, multicolinearidade)?
  * Como o resultado dialoga com a literatura (Coleman, Bourdieu, Soares & Alves)?
- **Discussão Horizontal**: O assistente e o pesquisador refletem juntos antes de tomar qualquer decisão sobre o passo seguinte.

### 5. Validação Prévia do Próximo Micro-Passo
- Antes de redigir qualquer nova linha de código ou criar o próximo script, o assistente deve:
  1. Explicar a proposta do próximo passo em 2 a 3 linhas;
  2. Aguardar o "de acordo" explícito do pesquisador ("pode ir", "manda bala", "vamos em frente").
