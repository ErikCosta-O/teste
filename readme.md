# Sistema de Cadastro de Moradores e Visitantes

## Visão Geral

Este projeto é um sistema web completo para cadastro, consulta, atualização e exclusão de moradores e visitantes, voltado para controle de acesso em condomínios ou edifícios residenciais. Ele utiliza Python (Flask) no backend, SQLite como banco de dados, e HTML/CSS/JavaScript no frontend. O sistema é modular, fácil de instalar e expandir, e inclui scripts para backup e restauração do banco de dados.

---

## Funcionalidades

- **Cadastro de Moradores e Visitantes:** Insere novos registros com nome, telefone (com máscara), email, tipo (morador ou visitante), apartamento e bloco. O formulário é dinâmico: campos de apartamento e bloco só aparecem se o tipo for "morador".
- **Atualização de Cadastro:** Permite atualizar qualquer campo de um cadastro existente, identificado pelo email. O sistema verifica se o cadastro existe antes de atualizar.
- **Listagem de Cadastros:** Exibe todos os cadastros em uma tabela dinâmica na interface, atualizada automaticamente após operações.
- **Consulta de Cadastro:** Busca por nome (e opcionalmente email) para localizar cadastros específicos.
- **Exclusão de Cadastro:** Deleta um cadastro por nome e email, com confirmação para evitar exclusões acidentais.
- **Backup e Restauração:** Scripts Python para exportar (backup) e importar (restauração) o banco de dados SQLite.

---

## Estrutura dos Arquivos e Explicação Detalhada

### `servidor.py`

Arquivo principal do backend, responsável por toda a lógica de negócio e integração com o banco de dados.

- **Framework:** Utiliza Flask para criar uma API RESTful.
- **Banco de Dados:** Conecta-se a um banco SQLite, criando a tabela `tb_cadastro` com os campos ID, NOME, TELEFONE, EMAIL, TIPO, APARTAMENTO e BLOCO.
- **Rotas Implementadas:**
  - `/` : Renderiza a página principal.
  - `/cadastrar` : Recebe dados via POST para inserir um novo cadastro. Valida se o email já existe antes de inserir.
  - `/listar` : Retorna todos os cadastros em formato JSON.
  - `/consultar` : Permite buscar um cadastro por nome (e opcionalmente email), retornando os dados em JSON.
  - `/atualizar` : Recebe dados via POST para atualizar um cadastro existente, identificado pelo email.
  - `/deletar` : Recebe dados via POST para excluir um cadastro, identificado por nome e email.
- **Validação:** Todas as operações verificam a existência do cadastro antes de inserir, atualizar ou deletar, garantindo integridade dos dados.
- **Resposta:** Todas as respostas das rotas são em JSON, exceto a rota principal que retorna HTML.

### `static/crud.js`

Arquivo JavaScript responsável por toda a lógica do frontend e comunicação com o backend.

- **Funções Principais:**
  - `listarCadastros()`: Realiza requisição GET para `/listar` e popula a tabela de cadastros na interface.
  - `criarCadastro()`: Coleta dados do formulário, faz validação básica e envia via POST para `/cadastrar`.
  - `atualizarCadastro()`: Envia dados atualizados via POST para `/atualizar`.
  - `consultarCadastro()`: Realiza requisição GET para `/consultar` com parâmetros de busca.
  - `deletarCadastro()` e `confirmarDelecao()`: Envia requisição POST para `/deletar` após confirmação do usuário.
  - `toggleMoradorFields()`: Mostra ou oculta campos de apartamento e bloco conforme o tipo selecionado.
  - `formatarTelefone()`: Aplica máscara de telefone ao campo correspondente.
- **Integração:** Utiliza `fetch` para comunicação assíncrona com o backend, atualizando a interface conforme as respostas recebidas.
- **Manipulação de DOM:** Atualiza tabelas, mensagens de feedback e visibilidade de campos dinamicamente.

### `templates/homepage.html`

Arquivo HTML que define a interface principal do sistema.

- **Componentes:**
  - Formulário de cadastro e atualização, com campos dinâmicos.
  - Tabela para listagem de todos os cadastros.
  - Painel para consulta de cadastro específico.
  - Seção para exclusão de cadastro, com confirmação.
  - Área "Sobre" explicando o funcionamento do sistema.
- **Integração:** Inclui o arquivo `crud.js` para adicionar interatividade e comunicação com o backend.
- **Acessibilidade:** Estrutura semântica para facilitar navegação e compreensão.

### `static/styles/estilo.css`

Arquivo de estilos CSS responsável pela aparência visual do sistema.

- **Layout:** Define espaçamentos, alinhamentos e responsividade para diferentes tamanhos de tela.
- **Cores e Tipografia:** Aplica paleta de cores, fontes e estilos de botões e inputs.
- **Feedback Visual:** Destaca mensagens de sucesso, erro e campos obrigatórios.
- **Responsividade:** Garante boa experiência em dispositivos móveis e desktops.

### `atualizar_banco.py`

Script Python para restauração do banco de dados a partir de um arquivo `.sql`.

- **Leitura de Arquivo:** Lê comandos SQL de um arquivo de backup.
- **Execução:** Executa cada comando no banco SQLite, recriando a estrutura e os dados.
- **Tratamento de Colunas:** Adiciona valores padrão para colunas ausentes, caso o backup seja de uma versão anterior do banco.
- **Uso:** Fundamental para recuperação de dados ou migração entre ambientes.

### `backup_banco.py`

Script Python para exportação (backup) do banco de dados SQLite.

- **Exportação:** Utiliza o método `con.iterdump()` para gerar todos os comandos SQL necessários para recriar a estrutura e os dados do banco.
- **Saída:** Salva o conteúdo em um arquivo `.sql`, que pode ser utilizado posteriormente para restauração.
- **Importância:** Garante segurança dos dados e facilita a portabilidade do sistema.

### `backup_cadastro.sql`

Arquivo SQL gerado pelo backup do banco de dados.

- **Conteúdo:** Inclui comandos para criação da tabela `tb_cadastro` e inserção de todos os registros existentes no momento do backup.
- **Utilização:** Pode ser usado pelo script `atualizar_banco.py` para restaurar o banco de dados em outro ambiente ou após perda de dados.

### `requirements.txt`

Arquivo de dependências do projeto.

- **Conteúdo:** Lista os pacotes necessários para execução do sistema, como Flask e Gunicorn.
- **Instalação:** Permite instalação rápida do ambiente com o comando `pip install -r requirements.txt`.

---

## Detalhamento da Parte de Rede

- **Protocolo:** HTTP/HTTPS
- **Formato de Dados:** JSON (para APIs), FormData (para formulários)
- **Endpoints:**
  - `GET /listar`: Retorna todos os cadastros em JSON.
  - `POST /cadastrar`: Cria cadastro.
  - `POST /atualizar`: Atualiza cadastro.
  - `GET /consultar?nome=...&email=...`: Consulta cadastro específico.
  - `POST /deletar`: Deleta cadastro.

### Fluxo de Requisição

1. O usuário interage com a interface (por exemplo, cria um cadastro).
2. O JavaScript coleta os dados e faz um `fetch` para o endpoint correspondente.
3. O Flask processa a requisição, interage com o banco de dados e retorna resposta em JSON.
4. O frontend exibe feedback e atualiza a interface conforme necessário.

### Segurança e Validação

- **Frontend:** Validação de campos obrigatórios, formato de email, máscara de telefone.
- **Backend:** Verificação de existência de cadastro, validação de dados recebidos.
- **Observação:** Não há autenticação ou criptografia implementada (pode ser adicionado para produção).

---