import os
import requests
import re
from openai import OpenAI
from langdetect import detect
    
def evaluate_resume(resume_text):

    content=""

    lang = detect(resume_text)
    
    if lang.startswith("zh"):
        lang_instruction = "请用中文回答以下内容："
    else:
        lang_instruction = "Please respond in English to the following resume content:"

    
    if lang.startswith("zh"):
        api_key = os.environ.get("DASHSCOPE_API_KEY")
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        if not api_key:
            return 60, "⚠️ 未检测到 API Key，无法连接通义千问接口"
        prompt = f"""{lang_instruction}你是一名资深HR专家。请根据以下简历内容，先用一段简短文字先总体评价下简历，然后从内容完整性、逻辑清晰性、突出优势三个维度进行评分（0-100），最后给出具体的优化建议：简历内容如下：{resume_text}"""
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


    else:
        prompt = f"""You are a professional recruiter at a U.S.-based company. Please review the following resume and provide a structured evaluation based on U.S. industry hiring standards.Follow this format in your response:
1. **Overall Summary**: In 2–3 sentences, summarize the overall impression of the resume, including strengths or weaknesses.
2. **Score the Resume** (scale 0–100 for each category):
   - Content Completeness (e.g., key sections present: experience, education, skills)
   - Clarity and Structure (e.g., formatting, bullet points, reverse chronology)
   - Relevance and Keyword Match (e.g., alignment with typical job descriptions)
3. **Strengths**: List 2–3 things the candidate did well (e.g., metrics, clarity, relevance).
4. **Areas for Improvement**: Provide 2–3 specific suggestions to improve the resume and increase job-matchability.Resume content:{resume_text}"""
    
        client=OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        # 调用 ChatGPT
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                {"role": "system", "content": "You are a helpful and professional HR advisor."},
                {"role": "user", "content": prompt}
            ],
                temperature=0.7
            )
            content=response.choices[0].message.content
        except Exception as e:
            content= f"❌ GPT 调用失败：{str(e)}"     
    

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


    

