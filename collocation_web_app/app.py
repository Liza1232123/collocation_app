from flask import Flask, render_template, request, jsonify
from collocation_finder import CollocationFinder
import json
import os

app = Flask(__name__)
finder = CollocationFinder()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    min_freq = data.get('min_freq', 1)

    print(f"Получен запрос: text='{text[:50]}...', min_freq={min_freq}")
    
    if not text:
        return jsonify({'error': 'Текст не введен'})
    
    results = finder.find_collocations(text, min_freq)

    print(f"Результат: {len(results.get('collocations', []))} коллокаций")
    return jsonify(results)

@app.route('/save', methods=['POST'])
def save_results():
    data = request.get_json()
    results = data.get('results', {})
    filename = data.get('filename', 'results.json')
    
    os.makedirs('results', exist_ok=True)
    with open(f'results/{filename}', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return jsonify({'message': f'Результаты сохранены в {filename}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)