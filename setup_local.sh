#!/bin/bash

# RAG Tutorial Local Setup Script
# This script helps set up the local environment for the RAG tutorial

echo "🚀 Setting up RAG Tutorial Local Environment"
echo "=============================================="

# Check if we're on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📱 Detected macOS"
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    echo "🍺 Installing PostgreSQL and pgvector via Homebrew..."
    brew install postgresql pgvector
    
    echo "🔧 Starting PostgreSQL service..."
    brew services start postgresql
    
    echo "📦 Installing Ollama..."
    if ! command -v ollama &> /dev/null; then
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo "✅ Ollama already installed"
    fi
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Detected Linux"
    
    # Check if we're on Ubuntu/Debian
    if command -v apt &> /dev/null; then
        echo "📦 Installing PostgreSQL..."
        sudo apt update
        sudo apt install -y postgresql postgresql-contrib
        
        echo "📦 Installing pgvector..."
        # Note: pgvector installation varies by distribution
        # This is a simplified version - check pgvector docs for your specific distro
        echo "⚠️  Please install pgvector manually for your distribution"
        echo "   See: https://github.com/pgvector/pgvector#installation"
        
        echo "🔧 Starting PostgreSQL service..."
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
        
        echo "📦 Installing Ollama..."
        if ! command -v ollama &> /dev/null; then
            curl -fsSL https://ollama.ai/install.sh | sh
        else
            echo "✅ Ollama already installed"
        fi
    else
        echo "❌ This script supports Ubuntu/Debian. Please install PostgreSQL and pgvector manually."
        exit 1
    fi
    
else
    echo "❌ Unsupported operating system: $OSTYPE"
    echo "Please install PostgreSQL with pgvector and Ollama manually."
    exit 1
fi

echo ""
echo "🗄️  Setting up database..."
echo "Creating database and user..."

# Create database and user
sudo -u postgres psql -c "CREATE DATABASE rag_db;" 2>/dev/null || echo "Database might already exist"
sudo -u postgres psql -c "CREATE USER rag_user WITH PASSWORD 'password';" 2>/dev/null || echo "User might already exist"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE rag_db TO rag_user;"

# Enable pgvector extension
sudo -u postgres psql -d rag_db -c "CREATE EXTENSION IF NOT EXISTS vector;"

echo ""
echo "🤖 Setting up Ollama models..."
echo "Pulling required models (this may take a few minutes)..."

# Start Ollama in background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to start
sleep 5

# Pull models
ollama pull gemma3:270m
ollama pull nomic-embed-text

# Stop background Ollama
kill $OLLAMA_PID 2>/dev/null

echo ""
echo "🐍 Setting up Python environment..."
echo "Installing Python dependencies..."

pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the tutorial:"
echo "1. Start Ollama: ollama serve"
echo "2. In another terminal, run: python rag_tutorial.py"
echo ""
echo "Note: Keep Ollama running in the background while using the tutorial."
