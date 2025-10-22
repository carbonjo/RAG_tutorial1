# RAG Tutorial: Retrieval-Augmented Generation with Local Tools

A complete tutorial demonstrating how to build a Retrieval-Augmented Generation (RAG) system using local tools for privacy and efficiency.

## 🚀 What is RAG?

RAG combines the power of:
1. **Retrieval**: Finding relevant information from a knowledge base
2. **Augmentation**: Using that information to enhance a query  
3. **Generation**: Creating a response using a language model

This approach allows LLMs to access up-to-date, domain-specific information that wasn't in their training data.

## 🛠️ Tech Stack

- **PostgreSQL** with pgvector extension for vector storage
- **Ollama** for local LLM and embedding models
- **Python** for the complete pipeline
- **Jupyter Notebook** for interactive learning

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL with pgvector extension
- Ollama installed locally
- Git (for cloning this repository)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd RAG
```

### 2. Set Up PostgreSQL

#### macOS (using Homebrew)
```bash
brew install postgresql pgvector
brew services start postgresql
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
# Install pgvector following their documentation
```

#### Windows
Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/) and install pgvector.

### 3. Create Database and User

```bash
psql postgres
CREATE DATABASE rag_db;
CREATE USER rag_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE rag_db TO rag_user;
\q
```

### 4. Enable pgvector Extension

```bash
psql -U rag_user -d rag_db
CREATE EXTENSION vector;
\q
```

### 5. Set Up Ollama

#### Install Ollama
Visit [ollama.ai](https://ollama.ai/download) and install Ollama.

#### Pull Required Models
```bash
ollama serve  # Start Ollama service (in a separate terminal)
ollama pull gemma3:270m
ollama pull nomic-embed-text
```

### 6. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 7. Run the Tutorial

#### Option A: Jupyter Notebook (Recommended)
```bash
jupyter lab
# Open RAG_Tutorial.ipynb
```

#### Option B: Python Script
```bash
python rag_tutorial.py
```

## 📚 Tutorial Contents

The tutorial covers:

1. **Database Setup**: Creating PostgreSQL tables with vector columns
2. **Document Processing**: Converting text into embeddings
3. **Vector Storage**: Using pgvector for efficient similarity search
4. **Retrieval**: Finding relevant documents for queries
5. **Generation**: Using local LLMs to create responses
6. **Analysis**: Understanding system performance
7. **Visualization**: Creating charts and graphs

## 🔧 Configuration

The system uses these default configurations:

```python
# Database
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "rag_db"
DB_USER = "rag_user"
DB_PASSWORD = "password"

# Ollama
OLLAMA_HOST = "http://localhost:11434"
GENERATION_MODEL = "gemma3:270m"
EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_DIMENSION = 768
```

## 📁 Project Structure

```
RAG/
├── RAG_Tutorial.ipynb    # Interactive Jupyter notebook
├── rag_tutorial.py       # Standalone Python script
├── requirements.txt      # Python dependencies
├── setup_local.sh       # Setup script (if available)
├── README.md            # This file
└── .gitignore          # Git ignore rules
```

## 🎯 Key Features

- **Local Deployment**: Everything runs on your machine
- **Privacy-First**: No data sent to external services
- **Educational**: Step-by-step learning process
- **Interactive**: Jupyter notebook with visualizations
- **Scalable**: Can handle large knowledge bases

## 🚀 Advanced Usage

### Using Different Models

You can experiment with different models:

```python
# Generation models
GENERATION_MODEL = "mistral:latest"  # or "llama3.2:1B", etc.

# Embedding models  
EMBEDDING_MODEL = "nomic-embed-text"  # or other embedding models
```

### Adding More Documents

```python
# Add your own documents
custom_documents = [
    "Your document content here...",
    "Another document...",
    # Add more documents
]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM runtime
- [pgvector](https://github.com/pgvector/pgvector) for PostgreSQL vector operations
- [PostgreSQL](https://www.postgresql.org/) for the database engine

## 📞 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/yourusername/RAG/issues) page
2. Create a new issue with detailed information
3. Make sure all prerequisites are properly installed

## 🔗 Useful Links

- [Ollama Documentation](https://ollama.ai/docs)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Jupyter Documentation](https://jupyter.org/documentation)

---

**Happy Learning! 🎉**
