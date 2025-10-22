# RAG Tutorial - Local Setup

This tutorial demonstrates how to build a Retrieval-Augmented Generation (RAG) system using local tools.

## Quick Start

### Option 1: Automated Setup (macOS/Linux)
```bash
./setup_local.sh
```

### Option 2: Manual Setup

#### 1. Install PostgreSQL with pgvector

**macOS:**
```bash
brew install postgresql pgvector
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
# Install pgvector manually - see https://github.com/pgvector/pgvector#installation
```

**Windows:**
- Download PostgreSQL from https://www.postgresql.org/download/
- Install pgvector extension

#### 2. Set up Database
```bash
# Create database and user (as superuser)
psql postgres
CREATE DATABASE rag_db;
CREATE USER rag_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE rag_db TO rag_user;
\q

# Enable pgvector extension (as superuser)
psql postgres -c "\c rag_db" -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Grant necessary permissions to rag_user
psql postgres -c "\c rag_db" -c "GRANT USAGE ON SCHEMA public TO rag_user;"
psql postgres -c "\c rag_db" -c "GRANT CREATE ON SCHEMA public TO rag_user;"
```

#### 3. Install Ollama
- Download from https://ollama.ai/download
- Start Ollama: `ollama serve`
- Pull models:
  ```bash
  ollama pull gemma3:270m
  ollama pull nomic-embed-text
  ```

#### 4. Set up Python Environment
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

#### 5. Run the Tutorial
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start Ollama in the background (if not already running)
ollama serve &

# Verify Ollama is working
ollama list

# Run the tutorial
python rag_tutorial.py
```

## Configuration

The tutorial uses these default settings (in `rag_tutorial.py`):

- **Database**: `rag_db` on localhost:5432
- **User**: `rag_user` with password `password`
- **Ollama**: http://localhost:11434
- **Models**: `gemma3:270m` and `nomic-embed-text`

## Troubleshooting

### PostgreSQL Connection Issues
- Ensure PostgreSQL is running: `brew services list` (macOS) or `sudo systemctl status postgresql` (Linux)
- Check if pgvector extension is installed: `psql -U rag_user -d rag_db -c "SELECT * FROM pg_extension WHERE extname = 'vector';"`

### Ollama Issues
- Ensure Ollama is running: `ollama list`
- Check if models are available: `ollama list`
- If you get "'Client' object has no attribute 'embed'" error:
  - Make sure Ollama is running: `ollama serve &`
  - Verify models are installed: `ollama list`
  - Check if nomic-embed-text model is available: `ollama show nomic-embed-text`

### Python Issues
- Ensure you're in a virtual environment: `which python` should show your venv path
- Activate venv if needed: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
- Check if all dependencies are installed: `pip list`
- Reinstall dependencies if needed: `pip install -r requirements.txt`

## What This Tutorial Does

1. **Document Processing**: Loads and chunks text documents
2. **Embedding Generation**: Creates vector embeddings using nomic-embed-text
3. **Vector Storage**: Stores embeddings in PostgreSQL with pgvector
4. **Similarity Search**: Finds relevant documents using vector similarity
5. **RAG Generation**: Uses Gemma 3 to generate responses based on retrieved context

## Files

- `rag_tutorial.py` - Main tutorial script
- `requirements.txt` - Python dependencies
- `setup_local.sh` - Automated setup script
- `Pride_and_Prejudice.txt` - Sample document for the tutorial
