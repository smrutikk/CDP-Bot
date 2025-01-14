from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from scraper import scrape_documentation, find_relevant_docs, generate_step_by_step
import os

app = Flask(__name__, static_folder='frontend/build')  # Serving React build folder
CORS(app)  # Enable CORS for all routes

# Route to serve the React app
@app.route('/')
def home():
    return send_from_directory(os.path.join(app.static_folder), 'index.html')

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    platform = data.get("platform")
    query = data.get("query")

    # Try embeddings first, fall back to scraping if no results
    response = find_relevant_docs(query) or scrape_documentation(platform, query)

    return jsonify({"response": response})

@app.route('/ask', methods=['POST'])
def ask():
    # Get user input and platform
    user_input = request.form.get('query')  # 'query' is sent via form data
    platform = request.form.get('platform')  # Get platform (Segment, mParticle, etc.)

    try:
        if platform not in DOCS_URLS:
            return jsonify({"error": "Platform not recognized."}), 400

        # Get the response from scraping documentation, finding relevant docs, or generating steps
        scraped_docs = scrape_documentation(platform, user_input)
        relevant_docs = find_relevant_docs(user_input)
        step_by_step_guide = generate_step_by_step(platform, user_input)

        # Return a JSON response with the relevant data
        return jsonify({
            "scraped_docs": scraped_docs,
            "relevant_docs": relevant_docs,
            "step_by_step_guide": step_by_step_guide
        })
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port, debug=True)

