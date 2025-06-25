import mysql.connector
from tabulate import tabulate

# Configurações de conexão
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="4182Joaogabryel",
        database="Projeto"
    )

# Funções auxiliares
def verificar_id(tabela, id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM {tabela} WHERE id = %s", (id,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Erro ao verificar ID em {tabela}:", e)
        return False
    finally:
        if conn.is_connected():
            conn.close()

# Funções de listagem
def listar_animais():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.nome, a.sexo, a.idade, 
            e.nome_comum, h.nome, t.nome 
            FROM animais a
            JOIN especies e ON a.especie_id = e.id
            JOIN habitats h ON a.habitat_id = h.id
            JOIN tratadores t ON a.tratador_id = t.id
            ORDER BY a.id
        """)

        dados = cursor.fetchall()
        print("\n=== Lista de Animais ===")
        print(tabulate(dados, headers=["ID", "Nome", "Sexo", "Idade", "Espécie", "Habitat", "Tratador"], tablefmt="fancy_grid"))
    except Exception as e:
        print("Erro ao listar animais:")
        print("Tipo do erro:", type(e).__name__)
        print("Mensagem:", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def listar_especies():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome_comum, nome_cientifico, classificacao, origem FROM especies ORDER BY id")
        dados = cursor.fetchall()
        print("\n=== Lista de Espécies ===")
        print(tabulate(dados, headers=["ID", "Nome Comum", "Nome Científico", "Classificação", "Origem"], tablefmt="fancy_grid"))
    except Exception as e:
        print("Erro ao listar espécies:")
        print("Tipo do erro:", type(e).__name__)
        print("Mensagem:", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def listar_habitats():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, tipo, temperatura_media, umidade_media FROM habitats ORDER BY id")
        dados = cursor.fetchall()
        print("\n=== Lista de Habitats ===")
        print(tabulate(dados, headers=["ID", "Nome", "Tipo", "Temp. Média", "Umidade Média"], tablefmt="fancy_grid"))
    except Exception as e:
        print("Erro ao listar habitats:")
        print("Tipo do erro:", type(e).__name__)
        print("Mensagem:", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def listar_tratadores():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, especialidade, telefone FROM tratadores ORDER BY id")
        dados = cursor.fetchall()
        print("\n=== Lista de Tratadores ===")
        print(tabulate(dados, headers=["ID", "Nome", "Especialidade", "Telefone"], tablefmt="fancy_grid"))
    except Exception as e:
        print("Erro ao listar tratadores:")
        print("Tipo do erro:", type(e).__name__)
        print("Mensagem:", str(e))
    finally:
        if conn.is_connected():
            conn.close()

# Funções CRUD
def adicionar_animal():
    print("\n=== Adicionar Animal ===")
    
    # Listar opções disponíveis primeiro
    print("\nEspécies disponíveis:")
    listar_especies()
    
    print("\nHabitats disponíveis:")
    listar_habitats()
    
    print("\nTratadores disponíveis:")
    listar_tratadores()
    
    # Pedir os dados
    nome = input("\nNome do animal: ")
    sexo = input("Sexo (Macho/Fêmea): ")
    idade = int(input("Idade: "))
    especie_id = int(input("ID da Espécie: "))
    habitat_id = int(input("ID do Habitat: "))
    tratador_id = int(input("ID do Tratador: "))
    
    # Verificar IDs
    if not verificar_id("especies", especie_id):
        print("Erro: ID de espécie inválido!")
        return
    if not verificar_id("habitats", habitat_id):
        print("Erro: ID de habitat inválido!")
        return
    if not verificar_id("tratadores", tratador_id):
        print("Erro: ID de tratador inválido!")
        return
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO animais (nome, sexo, idade, especie_id, habitat_id, tratador_id) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (nome, sexo, idade, especie_id, habitat_id, tratador_id)
        cursor.execute(sql, valores)
        conn.commit()
        print("\nAnimal adicionado com sucesso!")
    except Exception as e:
        print("\nErro ao adicionar animal:")
        print("Tipo do erro:", type(e).__name__)
        print("Mensagem:", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def excluir_animal():
    listar_animais()
    id_animal = int(input("\nID do animal a excluir: "))
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM animais WHERE id = %s", (id_animal,))
        conn.commit()
        print("\nAnimal excluído com sucesso!")
    except Exception as e:
        print("\nErro ao excluir animal:")
        print("Tipo do erro:", type(e).__name__)
        print("Mensagem:", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def atualizar_animal():
    listar_animais()
    id_animal = int(input("\nID do animal a atualizar: "))
    novo_nome = input("Novo nome (deixe em branco para não alterar): ")
    novo_sexo = input("Novo sexo (Macho/Fêmea, deixe em branco para não alterar): ")
    nova_idade = input("Nova idade (deixe em branco para não alterar): ")
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Construir a query dinamicamente com base nos campos preenchidos
        campos = []
        valores = []
        
        if novo_nome:
            campos.append("nome = %s")
            valores.append(novo_nome)
        if novo_sexo:
            campos.append("sexo = %s")
            valores.append(novo_sexo)
        if nova_idade:
            campos.append("idade = %s")
            valores.append(int(nova_idade))
            
        if not campos:
            print("Nenhum campo para atualizar!")
            return
            
        valores.append(id_animal)
        sql = f"UPDATE animais SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, valores)
        conn.commit()
        print("\nAnimal atualizado com sucesso!")
    except Exception as e:
        print("\nErro ao atualizar animal:")
        print("Tipo do erro:", type(e).__name__)
        print("Mensagem:", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def listar_animais_por_habitat():
    print("\n=== Habitats disponíveis ===")
    listar_habitats()

    try:
        habitat_id = int(input("\nDigite o ID do habitat desejado: "))

        if not verificar_id("habitats", habitat_id):
            print("ID de habitat inválido!")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.nome, a.sexo, a.idade, e.nome_comum, t.nome
            FROM animais a
            JOIN especies e ON a.especie_id = e.id
            JOIN tratadores t ON a.tratador_id = t.id
            WHERE a.habitat_id = %s
            ORDER BY a.id
        """, (habitat_id,))
        dados = cursor.fetchall()

        print(f"\n=== Animais no Habitat ID {habitat_id} ===")
        if dados:
            print(tabulate(dados, headers=["ID", "Nome", "Sexo", "Idade", "Espécie", "Tratador"], tablefmt="fancy_grid"))
        else:
            print("Nenhum animal encontrado nesse habitat.")
    except Exception as e:
        print("Erro ao listar animais por habitat:")
        print("Tipo do erro:", type(e).__name__)
        print("Mensagem:", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def listar_visitas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT vv.id, a.nome, vv.data_visita, vv.observacoes
            FROM visitas_veterinarias vv
            JOIN animais a ON vv.animal_id = a.id
            ORDER BY vv.id
        """)
        dados = cursor.fetchall()
        print("\n=== Lista de Visitas Veterinárias ===")
        print(tabulate(dados, headers=["ID", "Animal", "Data da Visita", "Observações"], tablefmt="fancy_grid"))
    except Exception as e:
        print("Erro ao listar visitas veterinárias:")
        print("Tipo do erro:", type(e).__name__)
        print("Mensagem:", str(e))
    finally:
        if conn.is_connected():
            conn.close()

def listar_dieta_animal():
    listar_animais()
    id_animal = int(input("\nID do animal para ver a dieta: "))

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.nome, al.tipo_racao, al.quantidade_kg, al.horario
            FROM alimentacoes al
            JOIN animais a ON al.animal_id = a.id
            WHERE a.id = %s
            ORDER BY al.horario
        """, (id_animal,))
        dados = cursor.fetchall()
        print(f"\n=== Dieta do animal ID {id_animal} ===")
        print(tabulate(dados, headers=["Animal", "Ração", "Quantidade (kg)", "Horário"], tablefmt="fancy_grid"))
    except Exception as e:
        print("Erro ao listar dieta:")
        print("Tipo do erro:", type(e).__name__)
        print("Mensagem:", str(e))
    finally:
        if conn.is_connected():
            conn.close()


    


# Menu principal
def menu():
    while True:
        print("\n=== MENU DO ZOOLÓGICO ===")
        print("1. Listar animais")
        print("2. Adicionar animal")
        print("3. Atualizar animal")
        print("4. Excluir animal")
        print("5. Listar espécies")
        print("6. Listar habitats")
        print("7. Listar tratadores")
        print("8. Listar animais por habitat")  
        print("9. Ver dieta de um animal")  
        print("10. Listar visitas veterinárias")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_animais()
        elif opcao == "2":
            adicionar_animal()
        elif opcao == "3":
            atualizar_animal()
        elif opcao == "4":
            excluir_animal()
        elif opcao == "5":
            listar_especies()
        elif opcao == "6":
            listar_habitats()
        elif opcao == "7":
            listar_tratadores()
        elif opcao == "8":
            listar_animais_por_habitat()
        elif opcao == "9":
            listar_dieta_animal()
        elif opcao == "10":
            listar_visitas()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
