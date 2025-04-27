from flask import Flask, request, render_template, jsonify, redirect, url_for
import apis
import json
import os
from openai import OpenAI
import os
import base64
import mimetypes

import logging

logging.disable(logging.DEBUG)  # 关闭DEBUG日志的打印
#logging.disable(logging.WARNING)  # 关闭WARNING日志的打印

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于session安全

HISTORY_FILE = 'history.json'

# 保持原有的历史记录处理函数不变
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


@app.route('/')
def login():
    return render_template('login.html')

# 修改后的路由配置
@app.route('/index')
def index():
    """主入口页面"""
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    """分析结果展示页面"""
    return render_template('analysis.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """分析请求处理（保持原有逻辑）"""
    content = request.form.get('content', '').strip()
    if not content:
        return jsonify({'error': 'No content provided'}), 400

    try:
        final_result, scores = apis.analyze_essay(content)
        
        # 保存历史记录
        history = load_history()
        history_entry = {
            'essay': content,
            'result': final_result,
            'scores': scores
        }
        history.append(history_entry)
        save_history(history)

        return jsonify({
            'rounds_result': final_result,
            'scores': scores
        })
    except Exception as e:
        print(f"分析错误: {str(e)}")
        return jsonify({'error': 'Failed to analyze essay'}), 500


@app.route('/history')
def history_page():
    """独立历史页入口"""
    return render_template('history.html')

@app.route('/api/history')
def get_history():
    """纯数据接口"""
    try:
        with open(HISTORY_FILE, 'r') as f:
            return jsonify({'data': json.load(f)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#  读取本地文件，并编码为 BASE64 格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key="sk-fd29d704f45e4675bf9df4a70034654d",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
@app.route('/upload_image', methods=['POST'])
def upload_image():
    """上传图片并提取文字进行分析"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # 将文件读取为字节流并进行 BASE64 编码
        content_type, _ = mimetypes.guess_type(image_file.filename)
        
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        image_url_str = f"data:{content_type};base64,{base64_image}"

        # 构造请求消息
        completion = client.chat.completions.create(
            model="qwen-vl-ocr",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url_str},
                            "min_pixels": 28 * 28 * 4,
                            "max_pixels": 28 * 28 * 1280
                        },
                        {"type": "text", "text": "Read all the text in the image."}
                    ],
                }
            ],
        )

        # 提取识别结果
        extracted_text = completion.choices[0].message.content

        # 调用作文分析函数
        final_result, scores = apis.analyze_essay(extracted_text)

        # 保存历史记录
        history = load_history()
        history_entry = {
            'essay': extracted_text,
            'result': final_result,
            'scores': scores
        }
        history.append(history_entry)
        save_history(history)

        return jsonify({
            'rounds_result': final_result,  
            'scores': scores
        })

    except Exception as e:
        print(f"图片处理错误: {str(e)}")
        return jsonify({'error': 'Failed to process image'}), 500


if __name__ == '__main__':
    app.run(debug=True)