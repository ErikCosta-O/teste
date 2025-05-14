from flask import Flask, request, jsonify, render_template
import sqlite3
import re  # Importa o módulo para expressões regulares

app = Flask(__name__, template_folder='templates')

# Caminho do banco de dados
caminho_banco = 'cadastro.db'

def validar_campos(name, phone, email, type_, apartamento, bloco):
    """
    Valida os campos para garantir que não contenham caracteres inválidos.
    :param name: Nome do usuário.
    :param phone: Telefone no formato (XX) XXXXX-XXXX.
    :param email: Email do usuário.
    :param type_: Tipo do cadastro.
    :param apartamento: Apartamento.
    :param bloco: Bloco.
    :return: True se todos os campos forem válidos, False caso contrário.
    """
    # Validação de caracteres especiais para os campos de texto
    regex_texto = r'^[a-zA-Z0-9\s]+$'  # Permite apenas letras, números e espaços
    if not re.match(regex_texto, name) or not re.match(regex_texto, type_):
        return False

    # Validação do telefone no formato (XX) XXXXX-XXXX
    regex_telefone = r'^\(\d{2}\)\s\d{4,5}-\d{4}$'
    if not re.match(regex_telefone, phone):
        return False

    # Validação de email (formato básico)
    regex_email = r'^[^@]+@[^@]+\.[^@]+$'
    if not re.match(regex_email, email):
        return False

    # Validação de apartamento e bloco (se fornecidos)
    if apartamento and not re.match(regex_texto, apartamento):
        return False
    if bloco and not re.match(regex_texto, bloco):
        return False

    return True

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

    # Valida os campos
    if not validar_campos(name, phone, email, type_, apartamento, bloco):
        return jsonify({"error": "Os campos contêm valores inválidos. Verifique o formato do telefone e evite caracteres especiais."}), 400

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
    nome = data.get('nome', '').strip().lower()  # Normaliza o nome
    email = data.get('email', '').strip().lower()  # Normaliza o email

    if not nome or not email:
        return jsonify({"error": "Nome e email são obrigatórios para deletar um cadastro."}), 400

    try:
        con = sqlite3.connect(caminho_banco)
        cur = con.cursor()

        # Deleta o cadastro com base no nome e email (insensível a maiúsculas/minúsculas)
        cur.execute(
            "DELETE FROM tb_cadastro WHERE LOWER(NOME) = ? AND LOWER(EMAIL) = ?",
            (nome, email)
        )
        con.commit()

        if cur.rowcount > 0:
            return jsonify({"message": f"Cadastro de {nome} com email {email} deletado com sucesso!"})
        else:
            return jsonify({"error": "Cadastro não encontrado."}), 404
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

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Use a porta fornecida pelo Render
    app.run(host='0.0.0.0', port=port, debug=True)