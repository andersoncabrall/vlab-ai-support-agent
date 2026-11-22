def _bloco_contexto_cliente(perfil_cliente: dict, ticket: str) -> str:
    return f"""
CONTEXTO DO CLIENTE
- Nome/ID: {perfil_cliente['nome']} ({perfil_cliente['id']})
- Nível técnico: {perfil_cliente['nivel_tecnico']}
- Estilo de comunicação preferido: {perfil_cliente['estilo_comunicacao']}
- Canal de atendimento: {perfil_cliente['canal']}

TICKET DO CLIENTE
\"\"\"{ticket}\"\"\"
""".strip()


def prompt_diagnostico(perfil_cliente: dict, ticket: str, versao: str = "v2") -> str:
    contexto = _bloco_contexto_cliente(perfil_cliente, ticket)

    if versao == "v1":
        return f"""
O cliente {perfil_cliente['nome']} mandou este problema: {ticket}.
Ele tem nível {perfil_cliente['nivel_tecnico']}.
Me dê um diagnóstico com as possíveis causas, o que falta de informação e uma conclusão.
Coloque no formato JSON com hipoteses, dados_faltantes e conclusao_provavel.
""".strip()

    return f"""
Você é um assistente de suporte técnico sênior. Sua responsabilidade é
diagnosticar problemas relatados por clientes com rigor e honestidade sobre
o que ainda é incerto. Você NÃO deve inventar causas sem evidência, e NÃO
deve propor solução nesta etapa — apenas diagnóstico.

{contexto}

TAREFA
Produza um diagnóstico estruturado do problema acima, contendo:
1. Hipóteses: liste de 2 a 4 causas prováveis, ordenadas da mais para a
   menos provável.
2. Evidências disponíveis: o que no ticket sustenta cada hipótese.
3. Dados faltantes: o que seria necessário saber para confirmar a hipótese
   mais provável.
4. Conclusão provável: uma frase objetiva com a causa mais plausível e o
   nível de confiança (baixo, médio, alto).

FORMATO DE SAÍDA
Responda SOMENTE em JSON válido, no formato:
{{
  "hipoteses": [
    {{"causa": "...", "evidencias": "...", "confianca": "baixo|medio|alto"}}
  ],
  "dados_faltantes": ["..."],
  "conclusao_provavel": {{"causa": "...", "confianca": "baixo|medio|alto"}}
}}
Não inclua texto fora do JSON. Não exponha raciocínio interno, apenas o
resultado estruturado.
""".strip()


def prompt_passo_a_passo(perfil_cliente: dict, ticket: str, versao: str = "v2") -> str:
    contexto = _bloco_contexto_cliente(perfil_cliente, ticket)

    return f"""
Você é um assistente de suporte técnico responsável por orientar o cliente
na resolução do problema relatado. Seu público é o cliente descrito abaixo
— adapte vocabulário e profundidade ao nível técnico "{perfil_cliente['nivel_tecnico']}"
e ao estilo "{perfil_cliente['estilo_comunicacao']}". Não assuma conhecimento
prévio além do que o nível técnico indicado permitir.

{contexto}

TAREFA
Produza um passo a passo de resolução para o problema relatado, adequado ao
canal "{perfil_cliente['canal']}" (ex.: respostas mais curtas para chat,
mais formais para e-mail, mais faladas/claras para telefone).

Regras de adaptação:
- leigo: evite jargão técnico, explique cada termo necessário, passos bem
  granulares.
- intermediário: pode usar termos técnicos comuns, passos objetivos.
- avançado: pode ser direto e técnico, sem explicações básicas.

- direto: frases curtas, só o essencial.
- detalhado: explique o porquê de cada passo.
- didático: use analogias ou exemplos quando ajudar a entender.

FORMATO DE SAÍDA
Responda SOMENTE em JSON válido, no formato:
{{
  "passos": [
    {{"ordem": 1, "acao": "...", "observacao": "..."}}
  ],
  "nivel_aplicado": "{perfil_cliente['nivel_tecnico']}",
  "estilo_aplicado": "{perfil_cliente['estilo_comunicacao']}"
}}
""".strip()


def prompt_perguntas_esclarecimento(perfil_cliente: dict, ticket: str, versao: str = "v2") -> str:
    contexto = _bloco_contexto_cliente(perfil_cliente, ticket)

    return f"""
Você é um assistente de triagem de suporte técnico. Sua responsabilidade é
identificar as perguntas mínimas necessárias para avançar no atendimento —
nunca pergunte o que já está respondido no ticket, e nunca peça mais
informação do que o necessário para o próximo passo do atendimento.

{contexto}

TAREFA
Liste de 2 a 5 perguntas de esclarecimento, priorizadas da mais crítica
para a menos crítica, considerando o canal "{perfil_cliente['canal']}"
(pergunte de forma breve se o canal for chat; pode ser mais formal se for
e-mail).

FORMATO DE SAÍDA
Responda SOMENTE em JSON válido, no formato:
{{
  "perguntas": [
    {{"prioridade": 1, "pergunta": "...", "motivo": "..."}}
  ]
}}
""".strip()


def prompt_resumo_visual(perfil_cliente: dict, ticket: str, versao: str = "v2") -> str:
    contexto = _bloco_contexto_cliente(perfil_cliente, ticket)

    return f"""
Você é um assistente que traduz um atendimento técnico em um fluxo visual
simples, para facilitar o entendimento rápido do caso por qualquer pessoa
da equipe de suporte.

{contexto}

TAREFA
Gere um fluxograma em ASCII (usando caixas de texto simples com "+--+",
"|" e setas "-->" ou "v") representando as etapas do atendimento: do
problema relatado até a resolução esperada, passando pelo diagnóstico e
pela decisão principal do caso.

FORMATO DE SAÍDA
Responda SOMENTE em JSON válido, no formato:
{{
  "fluxograma_ascii": "string com o fluxograma, usando \\n para quebras de linha",
  "descricao_estruturada": [
    {{"etapa": "...", "tipo": "entrada|decisao|acao|saida"}}
  ]
}}
""".strip()