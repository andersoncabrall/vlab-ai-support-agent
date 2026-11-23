# V-LAB: Assistente de Atendimento com IA

🔗 **Acesse a Demo Online:** [Clique aqui para testar a aplicação](https://vlab-ai-support-agent.onrender.com/)
*(Nota: Por estar hospedado no plano gratuito do Render, o primeiro acesso após inatividade pode levar cerca de 50 segundos para iniciar o servidor).*

Um assistente de suporte técnico via CLI focado na aplicação de técnicas avançadas de **Engenharia de Prompt**, **Injeção de Contexto Dinâmico** e **Adaptação de Persona**. Este projeto foi desenvolvido como parte de um desafio técnico para demonstrar o controle sobre Modelos de Linguagem de Grande Escala (LLMs).

## 🎯 Objetivo do Projeto

O sistema recebe um ticket de suporte e o perfil de um cliente (nível técnico, estilo de comunicação e canal). A partir dessas informações, orquestra a comunicação com a API da Groq para gerar quatro tipos de respostas estruturadas:
1. Diagnóstico do Problema
2. Passo a Passo de Resolução
3. Perguntas de Esclarecimento
4. Resumo Visual (Fluxograma ASCII)

## 🏗️ Arquitetura e Componentes

O projeto segue uma arquitetura modular com separação clara de responsabilidades:
- **`main.py`:** Orquestrador principal (Entrypoint). Gerencia o fluxo de execução, coleta os inputs do usuário e realiza a requisição REST para a API da Groq.
- **`prompts.py`:** O motor de Engenharia de Prompt. Utiliza técnicas de *Persona Prompting*, injeção dinâmica de variáveis e formatação estrita de saída (*Strict Output Formatting* em JSON) para mitigar alucinações.
- **`clientes.json`:** Banco de dados estático simulando os perfis dos clientes (contexto do usuário).
- **`cache.py`:** Camada de persistência. Gera um hash MD5 baseado no input e salva a resposta localmente, evitando requisições redundantes à API e otimizando custos (*Cache Hit*).
- **`PROMPT_ENGINEERING_NOTES.md`:** Relatório técnico contendo a rubrica de comparação entre as versões de prompts (Básico vs. Otimizado).
- **`app.py`:** Interface web interativa construída com Gradio, permitindo testar os diferentes perfis de clientes, ações e versões de prompt diretamente pelo navegador.

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10+
- Chave de API válida da [Groq](https://console.groq.com/)

### Passo a passo (Setup)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/andersoncabrall/vlab-ai-support-agent.git
   cd vlab-ai-support-agent


2. **Crie um ambiente virtual e ative-o (Opcional, mas recomendado):**
```bash
python -m venv venv
source venv/Scripts/activate # No Windows (Git Bash)

```


3. **Instale as dependências:**
```bash
pip install -r requirements.txt

```


4. **Configure as variáveis de ambiente:**
* Faça uma cópia do arquivo `.env.example` e renomeie para `.env`.
* Abra o `.env` e insira sua chave da Groq:
```env
GROQ_API_KEY="sua-chave-aqui-sem-aspas"
GROQ_MODEL="openai/gpt-oss-120b"

```




5. **Rode a aplicação:**
```bash
python main.py

python app.py

```



## 🛠️ Exemplo de Uso

Ao executar o `main.py`, o sistema exibirá um menu interativo no terminal.

1. **ID do cliente:** Digite `cliente_01` (Maria, perfil leigo).
2. **Ticket:** Digite `Minha internet cai toda vez que chove e o roteador fica piscando`.
3. **Opção:** Digite `1` (Diagnóstico).
4. **Versão do Prompt:** Pressione `Enter` para usar o padrão `v2` (otimizado).

O sistema processará a resposta e exibirá um JSON estruturado na tela, salvando uma cópia gerada na pasta `/samples`.

## 🧪 Engenharia de Prompt (V1 vs V2)

Para visualizar as técnicas utilizadas para domar o LLM e mitigar alucinações, leia o arquivo [PROMPT_ENGINEERING_NOTES.md](./PROMPT_ENGINEERING_NOTES.md). Ele contém uma análise detalhada e pontuada (escala de 1 a 5) mostrando por que o prompt V2 supera estruturalmente um prompt ingênuo (V1).

