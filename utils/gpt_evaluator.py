import os
import requests
import re


def evaluate_resume(resume_text):
    
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        return 60, "⚠️ 未检测到 API Key，无法连接通义千问接口"
		url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    prompt = f"""
你是一名资深HR专家。请根据以下简历内容，先用一段简短文字先总体评价下简历，然后从内容完整性、逻辑清晰性、突出优势三个维度进行评分（0-100），最后给出具体的优化建议：
简历内容如下：
{resume_text}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen-turbo",
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "result_format": "message"
        }
    }

    response = requests.post(url, json=data, headers=headers)
    result = response.json()

    try:
        content = result['output']['choices'][0]['message']['content']
    except Exception:
        content = "【解析失败】" + str(result)
    print("🤖 通义千问返回：", result)



    # 简单提取分数（你也可以优化匹配规则）
    import re

    def extract_score(content):
    # 尝试提取“综合评分：85/100” 或 “最终评分：85/100”
        match = re.search(r'(综合|最终)?评分[:：]?\s*(\d{1,3})\s*/\s*100', content)
        if match:
            return int(match.group(2))

        # 否则提取所有 (xx/100)，并计算平均
        scores = re.findall(r'\b(\d{1,3})/100\b', content)
        if scores:
            avg_score = round(sum(map(int, scores)) / len(scores))
            return avg_score

        # 如果以上都失败，则默认75
        return 75

    score = extract_score(content)  # ✅ 推荐调用
    return score, content

