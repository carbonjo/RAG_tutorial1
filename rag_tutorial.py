"""
RAG Tutorial with Ollama, PostgreSQL, and Python

This script provides a complete, self-contained tutorial for building a Retrieval-Augmented Generation (RAG) system.
It uses local installations of PostgreSQL and Ollama for a private and efficient setup.

Components:
- Python: The core programming language.
- PostgreSQL: A powerful relational database with pgvector extension.
- Ollama: A local runtime for large language models.
- Gemma 3:270M: A compact, high-performing language model from Google.
- nomic-embed-text: A local embedding model from Ollama.

How to Use This Tutorial:

Step 0: Prerequisites
- Install PostgreSQL with pgvector extension:
  - macOS: `brew install postgresql pgvector`
  - Ubuntu/Debian: `sudo apt install postgresql postgresql-contrib` then install pgvector
  - Windows: Download from https://www.postgresql.org/download/
- Install Ollama: https://ollama.ai/download
- Ensure you have Python 3.9+ and pip installed.

Step 1: Set up PostgreSQL
- Start PostgreSQL service:
  - macOS: `brew services start postgresql`
  - Ubuntu/Debian: `sudo systemctl start postgresql`
  - Windows: Start PostgreSQL service from Services
- Create a database and user:
  ```bash
  psql postgres
  CREATE DATABASE rag_db;
  CREATE USER rag_user WITH PASSWORD 'password';
  GRANT ALL PRIVILEGES ON DATABASE rag_db TO rag_user;
  \q
  ```
- Connect to the new database and enable pgvector:
  ```bash
  psql -U rag_user -d rag_db
  CREATE EXTENSION vector;
  \q
  ```

Step 2: Set up Ollama
- Start Ollama service:
  - macOS: `ollama serve` (in a separate terminal)
  - Ubuntu/Debian: `ollama serve` (in a separate terminal)
  - Windows: Run Ollama application
- Pull the required models:
  ```bash
  ollama pull gemma3:270m
  ollama pull nomic-embed-text
  ```

Step 3: Install Python Libraries
- Make sure you are in a Python virtual environment (recommended).
- Run: `pip install -r requirements.txt`

Step 4: Run This Script
- Execute: `python rag_tutorial.py`
- Follow the output in the console as the script guides you through the RAG process.
"""

import os
import psycopg
import ollama
import time

# Configuration
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "rag_db"
DB_USER = "rag_user"
DB_PASSWORD = "password"
OLLAMA_HOST = "http://localhost:11434"
GENERATION_MODEL = "gemma3:270m"
EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_DIMENSION = 768  # nomic-embed-text model dimension

# --- Step 1: Connect to the database and ensure the table exists ---
def setup_database():
    """
    Connects to the PostgreSQL database, creates the vector extension,
    and sets up the 'documents' table if it doesn't exist.
    """
    conn = None
    try:
        print("\n--- Connecting to PostgreSQL database ---")
        conn = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            autocommit=True,
            gssencmode="disable"
        )
        print("Connection successful!")
        
        with conn.cursor() as cur:
            # Check if the 'vector' extension is installed
            cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector';")
            if cur.fetchone() is None:
                print("pgvector extension not found. Please ensure your Docker image supports it.")
                print("This script uses the 'ankane/pgvector' Docker image which has it pre-installed.")
                print("If you're running a different PostgreSQL image, you may need to install it manually.")
                return None
            else:
                print("pgvector extension is installed.")

            # Drop the table if it already exists to start fresh
            cur.execute("DROP TABLE IF EXISTS documents;")
            
            # Create the documents table with a vector column
            cur.execute(f"""
                CREATE TABLE documents (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    embedding VECTOR({VECTOR_DIMENSION})
                );
            """)
            print(f"Table 'documents' created successfully with a VECTOR({VECTOR_DIMENSION}) column.")
        
        return conn

    except psycopg.OperationalError as e:
        print(f"\nError: Could not connect to PostgreSQL. Please ensure the Docker container is running and accessible.")
        print(f"Details: {e}")
        return None

# --- Step 2: Ingest Sample Data and Create Embeddings ---
def ingest_data(conn):
    """
    Loads a sample text, splits it into chunks, generates embeddings for each chunk,
    and inserts the data into the PostgreSQL table.
    """
    print("\n--- Ingesting sample data and creating embeddings ---")
    
    # Sample long document text
    document = """
    A llama is a domesticated South American camelid, widely used as a meat and pack animal by Andean cultures since the pre-Columbian era.
    Llamas are social animals and live in herds. The largest are the guanacos, which can weigh up to 300 pounds.
    Llamas can be quite calm and cooperative if they are raised correctly, which makes them great companions for people in the mountains.
    A female llama gives birth standing up. The gestation period for a llama is about 11.5 months.
    The llamas have long, thick necks, a small head with a cleft upper lip, and long ears.
    """
    
    # Split the document into chunks for the RAG system.
    # A simple split by sentence or a fixed number of words works well for a tutorial.
    chunks = document.split('.')
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    
    # Create the Ollama client
    client = ollama.Client(host=OLLAMA_HOST)
    
    with conn.cursor() as cur:
        for chunk in chunks:
            print(f"Processing chunk: '{chunk[:50]}...'")
            try:
                # Generate embedding for the chunk using the local embedding model
                embedding_response = client.embeddings(
                    model=EMBEDDING_MODEL,
                    prompt=chunk
                )
                embedding = embedding_response['embedding']
                
                # Insert the chunk and its embedding into the database
                cur.execute(
                    "INSERT INTO documents (content, embedding) VALUES (%s, %s);",
                    (chunk, embedding)
                )
                print(f"Inserted chunk into database. Vector dimension: {len(embedding)}")
                
            except (ollama.RequestError, ollama.ResponseError) as e:
                print(f"\nError: Could not connect to Ollama. Please ensure the Docker container is running and the model is pulled.")
                print(f"Details: {e}")
                return False
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return False
    
    print("\nData ingestion complete.")
    return True

# --- Step 3: Perform a Retrieval-Augmented Generation Query ---
def run_rag_query(conn, user_query):
    """
    Performs the full RAG process:
    1. Generates an embedding for the user's query.
    2. Retrieves the most relevant documents from the database.
    3. Feeds the retrieved documents and the query to Gemma to generate a final answer.
    """
    print(f"\n--- Processing user query: '{user_query}' ---")
    
    client = ollama.Client(host=OLLAMA_HOST)
    
    try:
        # Generate embedding for the user query
        query_embedding_response = client.embeddings(
            model=EMBEDDING_MODEL,
            prompt=user_query
        )
        query_embedding = query_embedding_response['embedding']
        
        # Use psycopg to query the database for the most similar documents
        # The `<=>` operator performs cosine distance search on vectors.
        with conn.cursor() as cur:
            # Convert the embedding list to a PostgreSQL vector string
            vector_str = '[' + ','.join(map(str, query_embedding)) + ']'
            cur.execute(f"""
                SELECT
                    content
                FROM
                    documents
                ORDER BY
                    embedding <=> %s::vector
                LIMIT 3;
            """, (vector_str,))
            
            # Fetch the results
            retrieved_docs = [row[0] for row in cur.fetchall()]
            
        print("\n--- Retrieved the following relevant chunks from the database ---")
        for i, doc in enumerate(retrieved_docs):
            print(f"Chunk {i+1}: {doc}")
            
        # Create a context string from the retrieved documents
        context = " ".join(retrieved_docs)
        
        # Construct the final prompt for the LLM
        prompt = f"Based on the provided context, answer the question clearly and helpfully. Use only information from the context.\n\nContext: {context}\n\nQuestion: {user_query}\n\nAnswer:"
        
        # Generate the final response using the Gemma model
        print("\n--- Generating response with Gemma 3:270M ---")
        stream = client.generate(
            model=GENERATION_MODEL,
            prompt=prompt,
            stream=True
        )
        
        full_response = ""
        print("Response:")
        for chunk in stream:
            response_text = chunk['response']
            full_response += response_text
            print(response_text, end='', flush=True)
            
        print("\n\n--- RAG process complete ---")
        return full_response
        
    except (ollama.RequestError, ollama.ResponseError) as e:
        print(f"\nError: Could not connect to Ollama. Please ensure the Docker container is running and the model is pulled.")
        print(f"Details: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during the RAG process: {e}")
        return None

# Main function to orchestrate the tutorial
def main():
    print("Welcome to the Interactive RAG Tutorial!")
    print("This script will demonstrate how to build a RAG system using local tools.")
    
    # 1. Database Setup
    conn = setup_database()
    if conn is None:
        return
        
    # 2. Data Ingestion
    ingestion_success = ingest_data(conn)
    if not ingestion_success:
        conn.close()
        return

    # Give the user a moment to see the output
    time.sleep(2)
    
    # 3. RAG Query
    user_question = "What makes a llama a good companion?"
    run_rag_query(conn, user_question)
    
    conn.close()
    
if __name__ == "__main__":
    main()
