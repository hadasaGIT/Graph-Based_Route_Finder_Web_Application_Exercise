import ast
import json
from flask import Flask, render_template, request, jsonify
from helpers import shortest_path, generate_kml

with open('../graph_example.json', 'r') as file:
    graph_data = json.load(file)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/find_route', methods=['POST'])
def find_route():
    start_point = request.form.get('start_point')
    end_point = request.form.get('end_point')

    if not start_point or not end_point:
        return jsonify({'error': 'נקודת ההתחלה ונקודת הסיום הינן שדות חובה'}), 400

    short_path = shortest_path(ast.literal_eval(start_point), ast.literal_eval(end_point), graph_data)
    print("Shortest distance:", short_path)

    response = {
        'shortest_path': short_path
    }
    kml_file_path = generate_kml(short_path)
    print("KML file generated:", kml_file_path)
    return render_template('result.html', shortest_route=response,kml_file_path=kml_file_path)


if __name__ == '__main__':
    app.run(debug=True)
