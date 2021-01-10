import json

from flask import Flask, request, jsonify
from urllib.parse import urlparse, parse_qs

from main import Graph

app = Flask(__name__)

graph = Graph()


def create_command(command, data):
    try:
        if data[1].strip() != 'content-type : application/json':
            return jsonify({"msg": "Invalid command syntax"}), 400

        if command[1].strip() == '/devices':
            request_data = json.loads(data[2])
            status_code, msg = graph.add_node(request_data["name"], request_data["type"])
            return jsonify({"msg": msg}), status_code

        elif command[1].strip() == '/connections':
            request_data = json.loads(data[2])
            status_code, msg = graph.add_connection(request_data["source"], request_data["targets"])
            return jsonify({"msg": msg}), status_code
    except Exception as e:
        return jsonify({"msg": "Invalid command syntax"}), 400


def modify_command(command, data):
    if data[1].strip() != 'content-type : application/json':
        return jsonify({"msg": "Invalid command syntax"}), 400

    node = command[1].split('/')[2]

    value = json.loads(data[2])['value']
    status_code, msg = graph.change_strength(node, value)
    return jsonify({"msg": msg}), status_code


def fetch_command(command):
    try:
        parse_result = urlparse(command[1])
        if parse_result.path == '/devices':
            data = graph.fetch_devices()
            return jsonify({"devices": data}), 200

        elif parse_result.path == '/info-routes':
            query = parse_qs(urlparse(command[1]).query)
            to = query['to'][0]
            frm = query['from'][0]

            status_code, msg = graph.find_path(frm, to)

            return jsonify({"msg": msg}), status_code

        return jsonify({"msg": "Invalid Command."}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Invalid Request"}), 400


@app.route('/ajiranet/process/', methods=['GET', 'POST'])
def hello():
    try:
        data = request.get_data().decode('utf-8').split("\n")
        data = [i for i in data if i != '']
        command = data[0].split()

        if command[0].strip() == 'CREATE':
            return create_command(command, data)

        if command[0] == 'FETCH':
            return fetch_command(command)

        if command[0] == 'MODIFY' and data[1].strip() == 'content-type : application/json':
            return modify_command(command, data)

        return jsonify({"msg": "Invalid Command."}), 400
    except Exception:
        return jsonify({"msg": "Invalid Command."}), 400


if __name__ == '__main__':
    app.run(port=8080)
