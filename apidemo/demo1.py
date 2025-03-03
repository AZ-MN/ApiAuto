from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/user', methods=['GET'])
def get_user():
    data = {
        "code": "ok",
        "message": "成功",
        "data": [{
            "id": "001",
            "name": "Jack",
            "age": 18
        }]
    }
    return jsonify(data)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, port=3000)  # flask默认使用 5000 端口，可添加 port 参数改为 3000 端口
