from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS

from werkzeug.utils import secure_filename
import os




from utils.parser import extract_text_from_file
from utils.gpt_evaluator import evaluate_resume

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_resume():
	
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    print(f"✅ 上传成功：{file.filename}")

    # 模拟提取简历内容
    try:
        text = extract_text_from_file(filepath)
        print("📄 实际提取结果：", repr(text[:500]))
        print("📄 提取内容：", text[:200])  # 打印前 200 字
        score, feedback = evaluate_resume(text)
        print("🤖 AI 分析：", feedback[:200])  # 打印前 200 字
        return jsonify({
            "score": score,
            "feedback": feedback,
            "resume_text": text
        })
    except Exception as e:
        print("❌ 发生错误：", str(e))  # ✅ 打印错误内容
        return jsonify({
            "error": str(e),
            "score": 0,
            "feedback": "AI 分析失败",
            "resume_text": ""
        }), 500
    # score, feedback = evaluate_resume(text)
    print(f"✅ 分析完成：score={score}")
    return jsonify({
    'score': score,
    'feedback': feedback,
    'resume_text': text  # ✅ 添加这个字段
    })


    

    return jsonify({
        "score": 80,
        "suggestions": [response.choices[0].message.content]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

