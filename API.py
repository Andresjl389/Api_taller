import os
import mysql.connector 
from functools import wraps
from flask import Flask, jsonify, request
from pymongo import MongoClient


app = Flask(__name__)
app.config['SECRET_KEY'] = "mytoken"

try:
    client = MongoClient("mongodb+srv://Andreses:qO0eRncJlMS4f78t@cluster0.eydrwxt.mongodb.net/")
    db = client["Generador_Recetas"]
    collection = db["recetas"]
    collection2 = db["comments"]
    client.server_info()
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print("Error al conectar la base de datos: ", str(e))

    
@app.route('/obtener_receta', methods=['POST'])
def obtener_receta():
    ingrediente_digitado = request.form['ingrediente_receta']
    
    resultados = collection.find({'ingrediente_principal':ingrediente_digitado})
    
    recetas = [dict(recetas) for recetas in resultados]

    
    return jsonify({"Receta": recetas})

    
@app.route('/create_receipe', methods=['POST'])

def create_Post():
    Id = request.form['id']
    NomReceta = request.form['Nombre_receta']
    Description = request.form['Descripcion']
    Ingredients = request.form['Ingredientes']
    Ingre_Principal = request.form['Ingrediente_principal']
    
    nueva_receta = {
        "_id": Id,
        "nombre": NomReceta,
        "description": Description,
        "ingrediente_principal": Ingre_Principal,
        "ingredienntes": Ingredients
    }
    
    insert = collection.insert_one(nueva_receta)
    
    print("Id de la receta insertada: ", insert.inserted_id)
    
    return jsonify({"Id de la receta insertadad": nueva_receta})
    
    
@app.route('/recipes/<recipe_id>/comment', methods=['GET','POST'])
def recipes_comments(recipe_id):
    if request.method == 'POST':
        comment_text = request.form['Comment']
        
        comments = {
            "recipe_id": recipe_id,
            "comment_text": comment_text
        }
        
        insert = collection2.insert_one(comments)
        
        print(comments)
        
        
        
        return jsonify({"mesage": "comentario agregado"})
    elif request.method == 'GET':
        resultado_comment = collection2.find({'recipe_id': recipe_id})
        comentarios = [dict(comentario) for comentario in resultado_comment]
        
        for comentario in comentarios:
            comentario["_id"] = str(comentario["_id"])
        return jsonify({"comments": comentarios})

    
    
@app.route('/prueba', methods=['GET'])
def prueba():
    return jsonify({"mesage": "comentarios"})
    
    
"""
MAIN ...........................................................................
"""
if __name__ == '__main__':
    # app.run()
    app.run(debug=True, port=os.getenv("PORT", default=5000))
