from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import CDPChatbot  # Import your chatbot model class

app = Flask(__name__)
CORS(app)

# Initialize the chatbot
chatbot = CDPChatbot()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'Question is required.'}), 400

    # Get response from the chatbot model
    response = chatbot.answer_question(question)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
