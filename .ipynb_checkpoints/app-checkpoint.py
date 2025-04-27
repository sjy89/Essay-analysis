from flask import Flask, request, render_template, jsonify
import apis  # 使用上传的 apis.py 文件


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    content = request.form.get('content', '')
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    try:
        rounds_result = apis.analyze_essay(content)
        return jsonify({'rounds_result': rounds_result})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to analyze essay'}), 500

if __name__ == '__main__':
    app.run(debug=True)
