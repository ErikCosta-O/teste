import logging
from flask import Flask, request, jsonify, render_template, send_file, g
import sqlite3

app = Flask(__name__, template_folder='templates')

# Caminho do banco de dados
caminho_banco = 'cadastro.db'

# Configuração do logging
logging.basicConfig(filename='flask.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

@app.before_request
def log_request_info():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'N/A')
    logging.info(f"IP: {ip} - Método: {request.method} - Rota: {request.path} - User-Agent: {user_agent}")

# Rota para exibir a página HTML
@app.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')  # Certifique-se de que o arquivo HTML está na pasta "templates"

# Rota para criar ou atualizar um cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    type_ = request.form.get('type')
    apartamento = request.form.get('apartamento')  # Novo campo
    bloco = request.form.get('bloco')  # Novo campo
    try:
        con = sqlite3.connect(caminho_banco)
        cur = con.cursor()
        # Verificar se o cadastro já existe
        cur.execute("SELECT * FROM tb_cadastro WHERE EMAIL = ?", (email,))
        resultado = cur.fetchone()
        if resultado:
            return jsonify({"error": f"Cadastro com email {email} já existe!"}), 400
        else:
            # Inserir novo cadastro
            cur.execute(
                "INSERT INTO tb_cadastro (NOME, TELEFONE, EMAIL, TIPO, APARTAMENTO, BLOCO) VALUES (?, ?, ?, ?, ?, ?)",
                (name, phone, email, type_, apartamento, bloco)
            )
            con.commit()
            return jsonify({"message": f"Cadastro de {name} inserido com sucesso!"})
    except sqlite3.Error as ex:
        return jsonify({"error": f"Erro ao acessar o banco de dados: {ex}"})
    finally:
        if 'con' in locals() and con:
            con.close()

# Rota para listar todos os cadastros
@app.route('/listar', methods=['GET'])
def listar():
    try:
        con = sqlite3.connect(caminho_banco)
        cur = con.cursor()
        cur.execute("SELECT NOME, TELEFONE, EMAIL, TIPO, APARTAMENTO, BLOCO FROM tb_cadastro")
        registros = cur.fetchall()
        return jsonify(registros)
    except sqlite3.Error as ex:
        return jsonify({"error": f"Erro ao acessar o banco de dados: {ex}"})
    finally:
        if 'con' in locals() and con:
            con.close()

# Rota para deletar um cadastro
@app.route('/deletar', methods=['POST'])
def deletar():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    # Verifica se o nome e email foram fornecidos
    # Se não, retorna um erro
    if not nome or not email:
        return jsonify({"error": "Nome e email são obrigatórios para deletar um cadastro."}), 400
    try:
        con = sqlite3.connect(caminho_banco)
        cur = con.cursor()
        # Deleta o cadastro com base no nome e email
        cur.execute("DELETE FROM tb_cadastro WHERE NOME = ? AND EMAIL = ?", (nome, email))
        con.commit()

        if cur.rowcount > 0:
            return jsonify({"message": f"Cadastro de {nome} com email {email} deletado com sucesso!"})
        else:
            return jsonify({"message": "Cadastro não encontrado."}), 404
    except sqlite3.Error as ex:
        return jsonify({"error": f"Erro ao acessar o banco de dados: {ex}"}), 500
    finally:
        if 'con' in locals() and con:
            con.close()

# Rota para consultar um cadastro específico
@app.route('/consultar', methods=['GET'])
def consultar():
    nome = request.args.get('nome')  # Nome será obrigatório
    email = request.args.get('email')  # Email será opcional

    if not nome:
        return jsonify({"message": "Por favor, insira um nome para consultar."}), 400

    try:
        con = sqlite3.connect(caminho_banco)
        cur = con.cursor()

        # Converte o nome para minúsculas e usa o operador LIKE para busca parcial
        nome = f"%{nome.lower()}%"
        if email:
            # Consulta por nome e email, insensível a maiúsculas/minúsculas
            cur.execute("SELECT * FROM tb_cadastro WHERE LOWER(NOME) LIKE ? AND LOWER(EMAIL) = ?", (nome, email.lower()))
        else:
            # Consulta apenas por nome, insensível a maiúsculas/minúsculas
            cur.execute("SELECT * FROM tb_cadastro WHERE LOWER(NOME) LIKE ?", (nome,))

        registro = cur.fetchone()
        if registro:
            colunas = [desc[0] for desc in cur.description]
            registro_dict = dict(zip(colunas, registro))
            return jsonify(registro_dict)
        else:
            return jsonify({"message": "Registro não encontrado."}), 404
    except sqlite3.Error as ex:
        return jsonify({"error": f"Erro ao acessar o banco de dados: {ex}"})
    finally:
        if 'con' in locals() and con:
            con.close()

# Rota para atualizar um cadastro existente
@app.route('/atualizar', methods=['POST'])
def atualizar():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    type_ = request.form.get('type')
    apartamento = request.form.get('apartamento')  # Novo campo
    bloco = request.form.get('bloco')  # Novo campo

    try:
        con = sqlite3.connect(caminho_banco)
        cur = con.cursor()

        # Atualizar cadastro existente
        cur.execute(
            "UPDATE tb_cadastro SET NOME = ?, TELEFONE = ?, TIPO = ?, APARTAMENTO = ?, BLOCO = ? WHERE EMAIL = ?",
            (name, phone, type_, apartamento, bloco, email)
        )
        con.commit()
        return jsonify({"message": f"Cadastro de {name} atualizado com sucesso!"})
    except sqlite3.Error as ex:
        return jsonify({"error": f"Erro ao acessar o banco de dados: {ex}"})
    finally:
        if 'con' in locals() and con:
            con.close()

# Exemplo de uso do log em uma rota
@app.route('/exemplo_log')
def exemplo_log():
    app.logger.info('Acessou a rota /exemplo_log')
    return 'Log registrado!'

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/logs_data')
def logs_data():
    try:
        try:
            with open('flask.log', 'r', encoding='utf-8') as f:
                conteudo = f.read()
        except UnicodeDecodeError:
            with open('flask.log', 'r', encoding='latin-1') as f:
                conteudo = f.read()
        return conteudo
    except Exception as e:
        return f"Erro ao ler o arquivo de log: {e}"

@app.route('/sql', methods=['GET', 'POST'])
def sql_interface():
    resultado = None
    colunas = None
    erro = ""
    if request.method == 'POST':
        comando = request.form.get('comando_sql', '').strip()
        if not comando.lower().startswith("select"):
            erro = "Só é permitido comandos SELECT!"
        else:
            try:
                con = sqlite3.connect(caminho_banco)
                cur = con.cursor()
                cur.execute(comando)
                colunas = [desc[0] for desc in cur.description]
                resultado = cur.fetchall()
            except Exception as ex:
                erro = str(ex)
            finally:
                if 'con' in locals() and con:
                    con.close()
    return render_template('sql_interface.html', resultado=resultado, colunas=colunas, erro=erro)

if __name__ == '__main__':
    import os
    import socket

    # Descobre o IP local automaticamente
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Não precisa estar acessível, só para pegar o IP local
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()

    port = int(os.environ.get('PORT', 8080))  # Pega a porta do ambiente ou usa 8080 como padrão
    print(f"Servidor rodando em http://{local_ip}:{port}")
    app.run(host=local_ip, port=port, debug=True)