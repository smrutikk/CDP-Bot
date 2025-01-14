
# CDP Bot

A powerful Customer Data Platform (CDP) assistant bot designed to streamline platform documentation queries and guide generation. This project integrates a Flask backend with a React frontend to deliver a seamless experience for developers.

## Features

- **Documentation Querying:** Search for relevant documentation based on your query and platform.
- **Step-by-Step Guides:** Automatically generate step-by-step instructions for various platforms.
- **Scraping & Embeddings:** Combines scraping and embeddings for robust results.
- **React Integration:** Serves a React-based frontend for a modern UI experience.
- **CORS Support:** Enabled for secure cross-origin communication.

---

## Tech Stack

- **Backend:** Flask, Flask-CORS
- **Frontend:** React
- **Additional Libraries:** 
  - `requests` 
  - `beautifulsoup4` (for web scraping)
  - `openai` (for AI-powered responses)
  - `pinecone-client` (for embedding-based queries)

---

## Installation

### Prerequisites

- Python 3.8+
- Node.js (for React frontend)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cdp-bot.git
   cd cdp-bot
   ```

2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```

5. Access the app in your browser at `http://localhost:5000`.

---

## API Endpoints

### 1. `GET /`
Serves the React frontend.

### 2. `POST /query`
Accepts JSON payload:
```json
{
  "platform": "platform_name",
  "query": "your_query"
}
```
Returns:
```json
{
  "response": "relevant_documentation_or_scraped_data"
}
```

### 3. `POST /ask`
Accepts form data:
- `query`: User's query.
- `platform`: Platform name.

Returns:
```json
{
  "scraped_docs": "scraped_results",
  "relevant_docs": "relevant_documents",
  "step_by_step_guide": "generated_steps"
}
```

---

## How It Works

1. **Query Handling:**
   - Embeddings are used to find relevant documentation.
   - Falls back to scraping if embeddings yield no results.

2. **Documentation Scraping:**
   - Uses BeautifulSoup to extract useful data from the platform's official documentation.

3. **Step-by-Step Guide Generation:**
   - Leverages OpenAI to generate actionable guides based on the query.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- Flask for backend support.
- React for frontend development.
- OpenAI for natural language processing.
- Pinecone for embeddings.
- BeautifulSoup for web scraping.
