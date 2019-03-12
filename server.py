from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)
@app.route("/users")
def index():
    mysql = connectToMySQL('users')
    users = mysql.query_db('SELECT * FROM users.all_users;')
    # print(users)

    return render_template("index.html", all_users = users)


@app.route("/users/new")
def new_user():


    return render_template("new.html")

@app.route("/users/create", methods=['POST'])
def create_new_user():
    query = "INSERT INTO users.all_users (first_name, last_name, email) VALUES (%(fnm)s, %(lnm)s, %(e)s);"
    
    data = {
        "fnm" : request.form["fname"],
        "lnm" : request.form["lname"],
        "e" : request.form["email"],
    }
    mysql = connectToMySQL('users')
    print(mysql.query_db(query, data))

    return redirect('/users')

@app.route("/users/<id>/update", methods=['POST'])
def update_user(id):
    query = "UPDATE users.all_users SET first_name = %(fnm)s, last_name = %(lnm)s, email = %(e)s WHERE id = "+ id+";"
    print(query)
    data = {
        "fnm" : request.form["fname"],
        "lnm" : request.form["lname"],
        "e" : request.form["email"],
    }
    print(data)
    mysql = connectToMySQL('users')
    mysql.query_db(query, data)

    return redirect('/users/'+id+'/display')

@app.route("/users/<id>/display")
def display_user(id):
    query = "SELECT id, first_name, last_name, email, created_at, edited_at FROM users.all_users WHERE (id = "+id+");"
    mysql = connectToMySQL('users')
    query_result = mysql.query_db(query)
    return render_template("readone.html", user_info = query_result)

@app.route("/users/<id>/edit")
def edit_user(id):
    query = "SELECT id, first_name, last_name, email, created_at, edited_at FROM users.all_users WHERE (id = "+id+");"
    mysql = connectToMySQL('users')
    query_result = mysql.query_db(query)
    print("*"*50, query_result)

    return render_template ("edit_user.html", user_info = query_result)


@app.route("/users/<id>/destroy")
def delete_user(id):
    # print("*"*50,id)
    query = "DELETE FROM users.all_users WHERE (id = "+id+");"
    mysql = connectToMySQL('users')
    mysql.query_db(query)
    return redirect ("/users")









# @app.route("/addpets", methods=['POST'])
# def addpets():
    # query = "INSERT INTO cr_pets.pets (name, type) VALUES (%(nm)s, %(tp)s);"
    
    # data = {
    #     "nm" : request.form["name"],
    #     "tp" : request.form["type"]
    # }
    # mysql = connectToMySQL('users')
    # print(mysql.query_db(query, data))
    # print("*"*50, "\nName: ", data["nm"], " , Type: ", data["tp"])
    # return redirect("/")


            
if __name__ == "__main__":
    app.run(debug=True)
