from flask import Flask, request, jsonify, render_template
from inference import load_model, generate_text

app = Flask(__name__)

# Load the model when the server starts
model, vocab, config, device = load_model('gpt_model.pkl')

@app.route('/', methods=['GET'])
def home():
    return '''
    <html>
        <head>
            <title>Text Generation</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                textarea { width: 100%; height: 100px; margin: 10px 0; }
                button { padding: 10px 20px; }
                #result { margin-top: 20px; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>Text Generation</h1>
            <textarea id="prompt" placeholder="Enter your prompt here..."></textarea>
            <br>
            <button onclick="generateText()">Generate</button>
            <div id="result"></div>

            <script>
                function generateText() {
                    const prompt = document.getElementById('prompt').value;
                    fetch('/generate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            prompt: prompt,
                            max_tokens: 500
                        }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('result').textContent = data.generated_text;
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                        document.getElementById('result').textContent = 'Error generating text';
                    });
                }
            </script>
        </body>
    </html>
    '''

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 500)
    
    generated_text = generate_text(prompt, model, vocab, config, device, max_new_tokens=max_tokens)
    
    return jsonify({'generated_text': generated_text})

if __name__ == '__main__':
    app.run(debug=False) 