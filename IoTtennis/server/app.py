# server/app.py
import os
import csv
from flask import Flask, jsonify
from flask_cors import CORS  # 如果前端在不同端口，还需要跨域

app = Flask(__name__)
CORS(app)  # 允许所有跨域请求

def read_csv_and_count(file_name):
    # __file__ 是当前 app.py 的绝对路径
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, file_name)
    counts = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            for word in row[0].split():
                counts[word] = counts.get(word, 0) + 1
    return counts

@app.route('/api/player-a/freq')
def player_a_freq():
    freq = read_csv_and_count('player_a.csv')
    # 按出现次数降序
    sorted_freq = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
    return jsonify(sorted_freq)

@app.route('/api/player-b/freq')
def player_b_freq():
    # 直接复用同样的读 CSV 逻辑，但文件名换成 player_b.csv
    freq = read_csv_and_count('player_b.csv')
    sorted_freq = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
    return jsonify(sorted_freq)

if __name__ == '__main__':
    # 指定 host='0.0.0.0' 也能让局域网其他设备访问
    app.run(port=5000, debug=True)
