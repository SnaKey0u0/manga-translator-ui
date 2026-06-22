import requests

response = requests.post(
    "http://127.0.0.1:8088/v1/chat/completions",
    json={
        "messages": [
            {"role": "system", "content": "你是翻译助手，将日文翻译成中文。"},
            {"role": "user", "content": "将下面的日文文本翻译成中文：こんにちは"}
        ],
        "max_tokens": 50,
        "temperature": 0.3,
    },
    timeout=10
)

print("Status:", response.status_code)
print("Result:", response.json()["choices"][0]["message"]["content"])
