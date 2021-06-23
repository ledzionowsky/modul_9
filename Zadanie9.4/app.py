from flask import Flask, request, render_template, redirect, url_for, jsonify, abort
from forms import TodoForm
from models import todos

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/todos/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            todos.create(form.data)
            todos.save_all()
        return redirect(url_for("todos_list"))

    return render_template("todos.html", form=form, todos=todos.all(), error=error)

@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():

    return jsonify(todos.all())

@app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    if not request.json or not 'Marka' in request.json:
        abort(400)
    todo = {
        'id': todos.all()[-1]['id'] + 1,
        'Marka': request.json['Marka'],
        'Model': request.json['Model'],
        'Rocznik': request.json['Rocznik'],
        'Kolor': request.json['Kolor'],
        'Moc': request.json['Moc'],
        'Czy bezwypadkowy?': False
    }
    todos.create(todo)
    return jsonify({'todo': todo}), 201

@app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    result = todos.delete(todo_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    print(str(todo_id))
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})

@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'Marka' in data and not isinstance(data.get('Marka'), str),
        'Model' in data and not isinstance(data.get('Model'), str),
        'Rocznik' in data and not isinstance(data.get('Rocznik'), int),
        'Kolor' in data and not isinstance(data.get('Kolor'), str),
        'Moc' in data and not isinstance(data.get('Moc'), int),
        'Czy bezwypadkowy?' in data and not isinstance(data.get('Czy bezwypadkowy'), bool)
    ]):
        abort(400)
    todo = {
        'Marka': data.get('Marka', todo['Marka']),
        'Model': data.get('Model', todo['Model']),
        'Rocznik': data.get('Rocznik', todo['Rocznik']),
        'Kolor': data.get('Kolor', todo['Kolor']),
        'Moc': data.get('Moc', todo['Moc']),
        'Czy bezwypadkowy?': data.get('Czy bezwypadkowy?', todo['Czy bezwypadkowy?'])
    }
    todos.update(todo_id, todo)
    return jsonify({'todo': todo})


@app.route("/todo_id/<int:todo_id>/", methods=["GET", "POST"])
def todo_details(todo_id):
    todo = todos.get(todo_id - 1)
    form = TodoForm(data=todo)

    if request.method == "POST":
        if form.validate_on_submit():
            todos.update(todo_id - 1, form.data)
        return redirect(url_for("todos_list"))
    return render_template("todos.html", form=form, todo_id=todo_id)


if __name__ == "__main__":
    app.run(debug=True)
