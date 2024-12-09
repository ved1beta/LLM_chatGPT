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
            <title>AI Text Generation</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                :root {
                    --primary-color: #4a90e2;
                    --secondary-color: #2c3e50;
                    --background-color: #f5f6fa;
                    --text-color: #2c3e50;
                }
                
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 20px;
                    background-color: var(--background-color);
                    color: var(--text-color);
                }
                
                .container {
                    background-color: white;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                
                h1 {
                    color: var(--primary-color);
                    text-align: center;
                    margin-bottom: 1.5rem;
                    font-size: 2.5rem;
                }
                
                textarea { 
                    width: 100%; 
                    height: 120px; 
                    margin: 10px 0;
                    padding: 1rem;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    font-size: 1rem;
                    resize: vertical;
                    transition: border-color 0.3s ease;
                }
                
                textarea:focus {
                    outline: none;
                    border-color: var(--primary-color);
                }
                
                button { 
                    background-color: var(--primary-color);
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 6px;
                    font-size: 1rem;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                    display: block;
                    margin: 1rem auto;
                }
                
                button:hover {
                    background-color: #357abd;
                }
                
                #result { 
                    margin-top: 20px;
                    white-space: pre-wrap;
                    padding: 1rem;
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    border-left: 4px solid var(--primary-color);
                }
                
                .loading {
                    display: none;
                    text-align: center;
                    margin: 1rem 0;
                }
                
                .loading::after {
                    content: "⚡";
                    animation: loading 1s infinite;
                }
                
                @keyframes loading {
                    0% { content: "⚡"; }
                    33% { content: "⚡⚡"; }
                    66% { content: "⚡⚡⚡"; }
                }
                
                .social-links {
                    text-align: center;
                    margin-top: 2rem;
                    padding-top: 1rem;
                    border-top: 1px solid #e0e0e0;
                }
                
                .social-links a {
                    color: var(--secondary-color);
                    font-size: 1.5rem;
                    margin: 0 10px;
                    text-decoration: none;
                    transition: color 0.3s ease;
                }
                
                .social-links a:hover {
                    color: var(--primary-color);
                }
                
                .footer {
                    text-align: center;
                    margin-top: 2rem;
                    color: #666;
                    font-size: 0.9rem;
                }
                
                .layout {
                    display: flex;
                    gap: 2rem;
                    align-items: flex-start;
                }
                
                .main-content {
                    flex: 1;
                }
                
                .sidebar {
                    width: 300px;
                    background: white;
                    padding: 1rem;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                
                .video-container {
                    margin-bottom: 1rem;
                }
                
                .video-thumbnail {
                    width: 100%;
                    border-radius: 8px;
                    transition: transform 0.3s ease;
                }
                
                .video-thumbnail:hover {
                    transform: scale(1.05);
                }
                
                .video-title {
                    font-size: 1rem;
                    color: var(--secondary-color);
                    margin: 0.5rem 0;
                    font-weight: 500;
                }
                
                .video-description {
                    font-size: 0.9rem;
                    color: #666;
                    margin-bottom: 1rem;
                }
                
                @media (max-width: 768px) {
                    .layout {
                        flex-direction: column;
                    }
                    
                    .sidebar {
                        width: 100%;
                    }
                }
            </style>
        </head>
        <body>
            <div class="layout">
                <div class="main-content">
                    <div class="container">
                        <h1>✨ AI Shakesphere</h1>
                        <textarea id="prompt" placeholder="Enter your prompt here and let AI do the magic..."></textarea>
                        <button onclick="generateText()">Generate ✨</button>
                        <div class="loading" id="loading">Generating</div>
                        <div id="result"></div>
                        
                        <div class="social-links">
                            <a href="https://github.com/ved1beta" target="_blank" title="GitHub">
                                <i class="fab fa-github"></i>
                            </a>
                            <a href="https://twitter.com/ant_vedaya" target="_blank" title="Twitter">
                                <i class="fab fa-twitter"></i>
                            </a>
                        </div>
                        
                        <div class="footer">
                            Created with 💙 by ved
                        </div>
                    </div>
                </div>
                
                <div class="sidebar">
                    <div class="video-container">
                        <a href="https://www.youtube.com/watch?v=YOUR_VIDEO_ID" target="_blank">
                            <img 
                                class="video-thumbnail" 
                                src="https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg" 
                                alt="Video thumbnail"
                            >
                        </a>
                        <h3 class="video-title">Your Video Title</h3>
                        <p class="video-description">
                            A brief description of your video content goes here. Make it engaging!
                        </p>
                    </div>
                    
                    <!-- You can add more video containers here -->
                    <div class="video-container">
                        <a href="https://www.youtube.com/watch?v=https://youtu.be/kCc8FmEb1nY?si=XJKYmE_WVHK3zi6i" target="_blank">
                            <img 
                                class="video-thumbnail" 
                                src="https://img.youtube.com/vi/https://youtu.be/kCc8FmEb1nY?si=XJKYmE_WVHK3zi6i/maxresdefault.jpg" 
                                alt="Video thumbnail"
                            >
                        </a>
                        <h3 class="video-title">Another Video Title</h3>
                        <p class="video-description">
                            Description for your second video.
                        </p>
                    </div>
                </div>
            </div>

            <script>
                function generateText() {
                    const prompt = document.getElementById('prompt').value;
                    const loading = document.getElementById('loading');
                    const result = document.getElementById('result');
                    
                    // Show loading animation
                    loading.style.display = 'block';
                    result.textContent = '';
                    
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
                        loading.style.display = 'none';
                        result.textContent = data.generated_text;
                    })
                    .catch((error) => {
                        loading.style.display = 'none';
                        result.textContent = 'Error generating text';
                        console.error('Error:', error);
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