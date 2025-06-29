import requests

class DeepSeekKnowledgeTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # 请根据DeepSeek官方文档修改endpoint
        self.endpoint = "https://api.deepseek.ai/v1/search"

    def query(self, question: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": question,
            "top_k": 3
        }
        response = requests.post(self.endpoint, json=payload, headers=headers)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if not results:
                return "抱歉，知识库中未找到相关内容。"
            answer = "\n".join([f"- {item['text']}" for item in results])
            return f"根据知识库查询到以下内容：\n{answer}"
        else:
            return f"查询知识库失败，错误代码：{response.status_code}"
