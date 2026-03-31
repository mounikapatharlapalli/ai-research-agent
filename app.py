from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"

@app.route('/')
def home():
    return "AI Research Agent Running"

@app.route('/research', methods=['POST'])
def research():
    try:
        data = request.get_json()
        query = data.get("question")

        if not query:
            return jsonify({"error": "Question is required"}), 400

        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"""
        Provide a structured research summary for the topic below:

        Topic: {query}

        Include:
        - Introduction
        - Key Points
        - Conclusion
        """

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        summary = result["choices"][0]["message"]["content"]

        return jsonify({
            "query": query,
            "summary": summary
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
