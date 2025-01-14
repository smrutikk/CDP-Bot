
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
## Deployment Link
https://cdp-chat-bot.netlify.app/

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
   cd backend
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
   python scraper.py
   python app.py
   ```

5. Access the app in your browser at `http://localhost:5000`.

6. Start React server:
   ```bash
   npm start
   ```
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







