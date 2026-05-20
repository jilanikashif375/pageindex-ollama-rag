# pageindex-ollama-rag

A simple, minimal vectorless RAG implementation using PageIndex document structure and Ollama for reasoning-based retrieval.

## Description

This project demonstrates a vectorless RAG approach where instead of using semantic search with embeddings, an LLM analyzes the document tree structure to identify relevant sections based on the query. The document is represented as a tree with node IDs, titles, and summaries - the LLM reasons over this structure to find the most relevant nodes.

## Features

- Reasoning-based retrieval using document tree structure
- No vector embeddings required
- Uses Ollama for local LLM inference
- Default model: granite4:latest

## Requirements

- Python 3.x
- Ollama installed with a model pulled

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pageindex-ollama-rag.git
cd pageindex-ollama-rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull required Ollama model
ollama pull granite4:latest
```

## Usage

Place your document structure JSON file in the `input/` folder as `successful_file.json`, then run:

```bash
python pageindex_rag.py
```

## Input Format

The JSON file should contain a document structure with nodes:

```json
{
  "structure": [
    {
      "node_id": "0001",
      "title": "Section Title",
      "summary": "Brief summary of content",
      "start_index": 1,
      "end_index": 5,
      "nodes": [...]
    }
  ]
}
```

## Project Structure

```
pageindex-ollama-rag/
├── README.md           # This file
├── ARCHITECTURE.md     # Architecture documentation
├── pageindex_rag.py    # Main RAG script
├── requirements.txt    # Python dependencies
└── input/              # Input JSON files
    └── successful_file.json
```

## How It Works

1. **Load Document**: Reads JSON structure from input folder
2. **Tree Search**: LLM analyzes the tree structure to find relevant nodes
3. **Context Retrieval**: Extracts content from retrieved nodes
4. **Answer Generation**: LLM generates answer based on retrieved context

## License

MIT