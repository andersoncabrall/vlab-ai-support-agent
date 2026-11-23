import gradio as gr
import os
from main import carregar_configuracao, carregar_clientes, TIPOS_CONTEUDO

config = carregar_configuracao()
clientes = carregar_clientes()

opcoes_clientes = {f"[{c['id']}] {c['nome']}": c for c in clientes}
nomes_clientes = list(opcoes_clientes.keys())

opcoes_tarefa = {nome: num for num, (nome, _) in TIPOS_CONTEUDO.items()}
nomes_tarefas = list(opcoes_tarefa.keys())

def processar_atendimento(cliente_selecionado, ticket, tarefa_selecionada, versao):
    if not ticket.strip():
        return {"erro": "O ticket não pode estar vazio."}

    cliente = opcoes_clientes[cliente_selecionado]
    num_tarefa = opcoes_tarefa[tarefa_selecionada]
    _, funcao_geradora = TIPOS_CONTEUDO[num_tarefa]

    resultado = funcao_geradora(cliente, ticket, config, versao_prompt=versao)
    return resultado

with gr.Blocks(title="V-LAB: Assistente de Suporte AI", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🤖 V-LAB: Assistente de Atendimento com IA")
    gr.Markdown("Selecione o perfil do cliente, descreva o problema e escolha a ação desejada para gerar o retorno via LLM.")

    with gr.Row():
        with gr.Column(scale=1):
            cliente_dropdown = gr.Dropdown(choices=nomes_clientes, label="1. Perfil do Cliente", value=nomes_clientes[0])
            tarefa_dropdown = gr.Dropdown(choices=nomes_tarefas, label="2. Tipo de Ação", value=nomes_tarefas[0])
            versao_radio = gr.Radio(choices=["v1", "v2"], label="3. Versão do Prompt", value="v2")

        with gr.Column(scale=2):
            ticket_input = gr.Textbox(lines=5, label="Descrição do Problema (Ticket)", placeholder="Ex: Minha internet cai toda vez que chove e o roteador fica piscando...")

    btn_gerar = gr.Button("Gerar Resposta", variant="primary")
    
    gr.Markdown("### Resultado Gerado")
    saida_json = gr.JSON(label="JSON de Saída")

    btn_gerar.click(
        fn=processar_atendimento,
        inputs=[cliente_dropdown, ticket_input, tarefa_dropdown, versao_radio],
        outputs=[saida_json]
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0")