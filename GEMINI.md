# Diretrizes de Trabalho e Governança do Projeto (TCC Desempenho Escolar)

Este documento estabelece o protocolo de colaboração e desenvolvimento entre o pesquisador (usuário) e o assistente de IA.

---

## 1. Princípio dos Pequenos Passos (Pacing & Cadência)
- **Um passo de cada vez**: Nunca executar múltiplos procedimentos complexos em sequência sem pausa.
- **Pausa obrigatória para reflexão**: Após cada etapa ou descoberta de dados, deve haver uma parada explícita para reflexão, discussão teórica e alinhamento antes de propor ou executar o passo seguinte.
- **Validação prévia**: Antes de rodar ou criar códigos novos, alinhar a proposta em poucas linhas e aguardar a validação do pesquisador.

---

## 2. Código Modular, Enxuto e Fácil de Revisar
- **Tamanho gerenciável**: Evitar scripts longos e monolíticos que dificultem a leitura e a revisão por parte do pesquisador.
- **Divisão por responsabilidade**: Se uma tarefa envolver mais de uma etapa analítica, dividi-la em funções claras ou passos independentes.
- **Transparência**: Priorizar clareza pedagógica e legibilidade do código sobre soluções excessivamente densas.

---

## 3. Construção Colaborativa do Relatório Metodológico
- Os resultados e conclusões de cada etapa devem ser revisados e discutidos com o pesquisador antes ou durante a incorporação no relatório (`reports/relatorio_metodologico_tcc.md`).
- O texto do relatório deve refletir fielmente a fundamentação teórica de Eficácia Escolar (Coleman, Bourdieu, Soares & Alves, Franco) e as decisões metodológicas pactuadas.

---

## 4. Rigor Econométrico e Epistemológico
- **Sem vazamento de alvo (*Target Leakage*)**: Manter variáveis correlatas contemporâneas (como Língua Portuguesa) estritamente no âmbito exploratório/epistemológico, sem inseri-las como preditoras no modelo de Machine Learning, para preservar a mensuração de fatores de gestão e políticas públicas.
- **Visão Sistêmica de 360º**: Reconhecer limites das variáveis observadas e contextualizar os achados como contribuições pontuais dentro de um ecossistema educacional complexo.
