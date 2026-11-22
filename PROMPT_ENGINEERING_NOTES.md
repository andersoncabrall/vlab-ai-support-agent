# Notas de Engenharia de Prompt

## Comparação de Desempenho (Diagnóstico)
**Ticket testado:** "Minha internet cai toda vez que chove e o roteador fica com a luz vermelha piscando"
**Cliente:** cliente_01 (Maria Silva | Nível: leigo | Estilo: didático | Canal: chat)

### Versão 1 (Prompt Básico)
- **Clareza (3/5):** A IA conseguiu devolver o JSON corretamente, mas as descrições foram genéricas.
- **Adequação ao nível do cliente (2/5):** O prompt não forçou a IA a considerar o contexto, resultando em uma análise padrão que ignora o perfil do usuário.
- **Acionabilidade (2/5):** A IA "alucinou" um nível de confiança "alto" para uma queda de energia sem evidências suficientes, o que poderia levar o suporte a um caminho errado.

### Versão 2 (Prompt Otimizado)
- **Clareza (5/5):** Estrutura impecável. As hipóteses e evidências foram cruzadas de forma lógica e direta.
- **Adequação ao nível do cliente (5/5):** A adoção da persona de "suporte técnico sênior" garantiu um diagnóstico técnico rigoroso internamente, perfeito para basear o próximo passo do atendimento.
- **Acionabilidade (5/5):** A IA manteve o rigor ("confiança: médio/baixo") e gerou uma lista de dados faltantes precisos (ex: "Localização do roteador", "Tipo de conexão"), mostrando exatamente o que o atendente precisa perguntar.

## Estratégias Utilizadas no V2 (Prompt Engineering)
1. **Persona e Contexto:** Defini claramente o papel ("assistente de suporte técnico sênior") e injetei variáveis dinâmicas (`nivel_tecnico`, `estilo_comunicacao`, `canal`) via f-strings para guiar o comportamento.
2. **Restrições de Alucinação:** Adicionei regras explícitas ("NÃO deve inventar causas sem evidência") que impediram a IA de dar certezas irreais, como ocorreu no V1.
3. **Output Formatting:** O uso de delimitadores e a exigência de "Responda SOMENTE em JSON válido" garantiu a integração perfeita com o sistema e evitou textos conversacionais indesejados.