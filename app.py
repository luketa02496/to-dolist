from flask import Flask, jsonify, request
import oracledb

app = Flask(__name__)

def get_connection(): # faz a conexao com o banco
    connection = oracledb.connect('rm557957/300306@oracle.fiap.com.br:1521/orcl')
    return connection

@app.route('/')
def home():
    return "TO DO list"

@app.route('/usuario', methods=['POST'])
def create_user(): #cria um usuario
    try:
        nome = request.json['nome']
        senha = request.json['senha']

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT nome FROM usuario WHERE nome = : nome" ,{'nome' : nome})

        user = cursor.fetchone() 

        if user:
            return jsonify({'message': 'Nome de usuario ja existente'}), 400
        
        cursor.execute("INSERT INTO usuario (nome, senha) VALUES (:nome, :senha) ", {'nome': nome, 'senha': senha})  

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Usuário criado com sucesso!"}), 201
    
    except Exception as e:
     return jsonify({"message": "Erro ao criar usuario", "error": str(e)}), 500
    
@app.route('/usuario/<int:usuario_id>', methods = ['PUT'])
def update_user(usuario_id): #atualiza o usuario
    try:
        data = request.get_json()
        campos = {}

        if 'nome' in data:
            campos['nome'] = data['nome']
        
        if 'senha' in data:
            campos['senha'] = data['senha']

        if not campos:
            return jsonify({"message": "Nenhum campo para atualizar foi informado"}), 400
        
        set_clause = ", ".join([f"{campo} = :{campo}" for campo in campos])

        sql = f"UPDATE usuario set {set_clause} WHERE id = :usuario_id"
        campos["usuario_id"] = usuario_id

        connection= get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, campos)

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Usuario atualizado com sucesso!"}), 200
    
    except Exception as e:
        return jsonify({"message": "Erro ao atualizar usuario", "error": str(e)}),

@app.route('/usuario/<int:id>', methods = ['GET'])
def get_user(id): # lista usuarios
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuario WHERE id =: id", {"id" : id})
    
    user = cursor.fetchone()  

    if user:
        user_data = {
            'id': user[0],
            'nome': user[1],
            'senha': user[2],
        }
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404

    cursor.close()
    connection.close()
    
    return jsonify(user_data)

@app.route('/usuario', methods = ['DELETE'])
def delete_user(): #deleta o usuario pelo ID
    try:
        data = request.get_json()
        id = data['id']

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM usuario WHERE id = :id", {'id': id})

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Usuario excluido com sucesso!"}), 201
        
    except Exception as e:
        return jsonify({"message": "Erro ao excluir usuario", "error": str(e)})
    


@app.route('/usuario', methods = ['GET'])
def get_users(): # lista todos os usuarios
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuario")
    
    tasks = cursor.fetchall()

    task_list = []
    for task in tasks:
        task_list.append({
            'id': task[0],  
            'nome': task[1],
            'senha': task[2],
         })

    cursor.close()
    connection.close()
    
    return jsonify(task_list)
    

#------------------------------------------------------ TAREFAS -------------------------------------------------------------------------
    
@app.route('/tarefas/usuario/<int:usuario_id>', methods=['GET'])
def get_task(usuario_id): #lista as tarefas

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tarefas WHERE usuario_id = :usuario_id", {'usuario_id': usuario_id})
    
    tasks = cursor.fetchall()

    if tasks: 
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task[0],  
                'titulo': task[1], 
                'descricao': task[2],  
                'status': task[3],  
                'usuario_id': task[4]  
            })
    
    else: 
        return jsonify({"message": "Tarefa não encontrada"}), 404
    
    cursor.close()
    connection.close()
    
    return jsonify(task_list)

@app.route('/tarefas', methods=['POST'])
def create_task(): #cria a tarefa
    try:
        data = request.get_json()
        titulo = data['titulo']
        descricao = data['descricao']
        status = data['status']
        usuario_id = data['usuario_id']

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (:titulo, :descricao, :status, :usuario_id)", {'titulo': titulo, 'descricao': descricao, 'status': status, 'usuario_id': usuario_id})
        
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Tarefa adicionada com sucesso!"}), 201
    
    except Exception as e:
        return jsonify({"message": "Erro ao adicionar tarefa", "error": str(e)}), 500
    
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def delete_task(id): #deleta a tarefa
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = :id", {'id': id})

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Tarefa excluida com sucesso!"}), 201
    
    except Exception as e:
        return jsonify({"message": "Erro ao excluir tarefa", "error": str(e)})
    
@app.route('/tarefas/<int:tarefa_id>', methods=['PUT'])
def update_task(tarefa_id): # atualiza a tarefa
    try:
        data = request.get_json()
        campos = {}
        if 'titulo' in data:
            campos['titulo'] = data['titulo']
        
        if 'descricao' in data:
            campos['descricao'] = data['descricao']
        
        if 'status' in data:
            campos['status'] = data['status']

        if not campos:
            return jsonify({"message": "Nenhum campo para atualizar foi informado"}), 400
        
        set_clause = ", ".join([f"{campo} = :{campo}" for campo in campos])

        sql = f"UPDATE tarefas SET {set_clause} WHERE id = :tarefa_id"
        campos["tarefa_id"] = tarefa_id

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, campos)
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Tarefa atualizada com sucesso!"}), 200
    
    except Exception as e:
        return jsonify({"message": "Erro ao atualizar tarefa", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)