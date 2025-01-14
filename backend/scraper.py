import requests
from bs4 import BeautifulSoup
import openai
from pinecone import Pinecone, ServerlessSpec

# Configuration
DOCS_URLS = {
    "segment": "https://segment.com/docs/",
    "mparticle": "https://docs.mparticle.com/",
    "lytics": "https://docs.lytics.com/",
    "zeotap": "https://docs.zeotap.com/home/en-us/"
}

OPENAI_API_KEY = "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"
PINECONE_API_KEY = "pcsk_4X8Cgk_HG2dtDKAEF1Jx13nCt7Hb1zEAsPVaeza15E2psXwkQECWvkxzQ3tf4Lomge8RoN"

pc = Pinecone(api_key=PINECONE_API_KEY)

# Index setup
index_name = "cdp-documentation"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="euclidean",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")  # Ensure correct region
    )

index = pc.Index(index_name)

def scrape_documentation(platform, query):
    """Scrapes the documentation based on the platform and the query."""
    url = DOCS_URLS.get(platform.lower())
    if not url:
        return "Documentation URL not found for this platform."

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Fetch the documentation page
        response = requests.get(url, headers=headers)
        print(f"Fetched URL: {url}, Status Code: {response.status_code}")
        if response.status_code != 200:
            return f"Unable to fetch documentation for {platform}. Status code: {response.status_code}"

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for sections that are more specific to the query
        relevant_text = []
        for section in soup.find_all(['section', 'div']):
            header = section.find(['h2', 'h3'])
            if header and query.lower() in header.text.lower():
                content = section.get_text(strip=True)
                if content:
                    relevant_text.append(content)

        # Remove duplicates and return top 5 results
        unique_results = list(dict.fromkeys(relevant_text))[:5]
        if unique_results:
            return "\n\n".join(unique_results)
        else:
            return f"No relevant information found for query: {query}."

    except Exception as e:
        return f"An error occurred: {str(e)}"

def find_relevant_docs(query, top_k=3):
    """Search for relevant docs using Pinecone and OpenAI embeddings."""
    openai.api_key = OPENAI_API_KEY
    try:
        query_embedding = openai.Embedding.create(input=query, model="text-embedding-ada-002")['data'][0]['embedding']

        # Query Pinecone for the most relevant documents
        results = index.query(query_embedding, top_k=top_k, include_metadata=True)
        if 'matches' in results:
            return [result['metadata']['text'] for result in results['matches']]
        else:
            return "No relevant matches found in Pinecone."

    except Exception as e:
        return f"Error querying Pinecone: {str(e)}"

def generate_step_by_step(platform, query):
    """Generates a step-by-step guide using OpenAI for a given platform and query."""
    openai.api_key = OPENAI_API_KEY
    prompt = f"Provide a step-by-step guide for {query} in {platform}."

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating response from OpenAI: {str(e)}"