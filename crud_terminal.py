import requests
import re

BASE_URL = "http://192.168.0.198:8080"  # Use o endereço local se rodar localmente

def validar_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def validar_telefone(telefone):
    return re.match(r"^\d{8,15}$", telefone.replace(" ", "").replace("-", "").replace("(", "").replace(")", ""))

def input_email():
    while True:
        email = input("Email: ")
        if validar_email(email):
            return email
        print("Email inválido. Tente novamente.")

def formatar_telefone(telefone):
    """Formata o telefone para o padrão (XX) XXXXX-XXXX ou (XX) XXXX-XXXX."""
    numeros = re.sub(r'\D', '', telefone)
    if len(numeros) == 11:
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    elif len(numeros) == 10:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    else:
        return telefone  # Retorna como está se não for 10 ou 11 dígitos

def input_telefone():
    while True:
        telefone = input("Telefone: ")
        if validar_telefone(telefone):
            return formatar_telefone(telefone)
        print("Telefone inválido. Digite apenas números (8 a 15 dígitos).")

def list_items():
    response = requests.get(f"{BASE_URL}/listar")
    if response.ok:
        for item in response.json():
            print(item)
    else:
        print("Falha ao listar cadastros.")

def create_item():
    tipos_validos = ["Morador", "Visitante"]
    while True:
        print("Tipo (Escolha):")
        for idx, tipo in enumerate(tipos_validos, 1):
            print(f"{idx}. {tipo}")
        tipo_input = input("Tipo [1-Morador, 2-Visitante]: ").strip()
        if tipo_input in ["1", "2"]:
            tipo = tipos_validos[int(tipo_input) - 1]
            break
        else:
            print("Opção inválida. Escolha 1 para Morador ou 2 para Visitante.")
    # Bloco: só aceita letras até 'D' e sempre maiúscula
    while True:
        bloco = input("Bloco (A-D): ").strip().upper()
        if bloco in ["A", "B", "C", "D"]:
            break
        else:
            print("Bloco inválido. Digite apenas A, B, C ou D.")
    data = {
        'name': input("Nome: "),
        'phone': input_telefone(),
        'email': input_email(),
        'type': tipo,
        'apartamento': input("Apartamento: "),
        'bloco': bloco
    }
    response = requests.post(f"{BASE_URL}/cadastrar", data=data)
    if response.ok:
        print(response.json())
    else:
        print("Falha ao cadastrar.")

def update_item():
    tipos_validos = ["Morador", "Visitante"]
    nome = input("Nome do cadastro a atualizar: ")
    email = input_email()
    # Consulta antes de atualizar
    params = {'nome': nome, 'email': email}
    response = requests.get(f"{BASE_URL}/consultar", params=params)
    if not (response.ok and response.json()):
        print("Cadastro não encontrado para os dados informados. Verifique o nome e o email.")
        return

    while True:
        print("Novo tipo (escolha uma opção):")
        for idx, tipo in enumerate(tipos_validos, 1):
            print(f"{idx}. {tipo}")
        tipo_input = input("Tipo [1-Morador, 2-Visitante]: ").strip()
        if tipo_input in ["1", "2"]:
            tipo = tipos_validos[int(tipo_input) - 1]
            break
        else:
            print("Opção inválida. Escolha 1 para Morador ou 2 para Visitante.")
    # Bloco: só aceita letras até 'D' e sempre maiúscula
    while True:
        bloco = input("Novo bloco (A-D): ").strip().upper()
        if bloco in ["A", "B", "C", "D"]:
            break
        else:
            print("Bloco inválido. Digite apenas A, B, C ou D.")
    data = {
        'name': input("Novo nome: "),
        'phone': input_telefone(),
        'email': input_email(),
        'type': tipo,
        'apartamento': input("Novo apartamento: "),
        'bloco': bloco
    }
    response = requests.post(f"{BASE_URL}/atualizar", data=data)
    if response.ok:
        print(response.json())
    else:
        print("Falha ao atualizar.")

def delete_item():
    nome = input("Nome do cadastro a deletar: ")
    email = input_email()
    # Consulta antes de deletar
    params = {'nome': nome, 'email': email}
    response = requests.get(f"{BASE_URL}/consultar", params=params)
    if response.ok and response.json():
        print("Cadastro encontrado:")
        print(response.json())
        confirm = input("Tem certeza que deseja deletar este cadastro? (s/n): ").strip().lower()
        if confirm == 's':
            data = {'nome': nome, 'email': email}
            del_response = requests.post(f"{BASE_URL}/deletar", json=data)
            if del_response.ok:
                print(del_response.json())
            else:
                print("Falha ao deletar.")
        else:
            print("Operação de deleção cancelada.")
    else:
        print("Cadastro não encontrado para os dados informados.")

def consultar_item():
    nome = input("Nome para consulta: ")
    email = input("Email (opcional): ")
    if email and not validar_email(email):
        print("Email inválido. Consulta será feita apenas pelo nome.")
        email = ""
    params = {'nome': nome}
    if email:
        params['email'] = email
    response = requests.get(f"{BASE_URL}/consultar", params=params)
    if response.ok:
        print(response.json())
    else:
        print("Falha ao consultar.")

def main():
    while True:
        print("\nMenu CRUD:")
        print("1. Listar cadastros")
        print("2. Cadastrar novo")
        print("3. Atualizar cadastro")
        print("4. Deletar cadastro")
        print("5. Consultar cadastro")
        print("6. Sair")
        choice = input("Escolha uma opção: ")
        if choice == '1':
            list_items()
        elif choice == '2':
            create_item()
        elif choice == '3':
            update_item()
        elif choice == '4':
            delete_item()
        elif choice == '5':
            consultar_item()
        elif choice == '6':
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()