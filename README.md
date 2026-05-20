# pageindex-ollama-rag

A simple, minimal vectorless RAG implementation using PageIndex document structure and Ollama for reasoning-based retrieval.

## Overview

This script demonstrates a simple, minimal example of vectorless RAG with PageIndex. You will learn how to:

1. Build a PageIndex tree structure for a document
2. Perform reasoning-based retrieval using tree search
3. Generate answers from the retrieved context

> Note: This is a minimal example intended to illustrate PageIndex's core idea and philosophy, not its full capabilities. More advanced examples will be added soon.

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
git clone https://github.com/jilanikashif375/pageindex-ollama-rag.git
cd pageindex-ollama-rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Step 0: Set up Ollama

1. Install Ollama: https://ollama.ai
2. Pull the model: `ollama pull granite4:latest`

### Step 1: Clone PageIndex repository

```bash
git clone https://github.com/VectifyAI/PageIndex.git
cd PageIndex
```

### Step 2: Generate the PageIndex structure for your PDF

Run the following command to generate the document structure JSON:

```bash
python3 run_pageindex.py --pdf_path /path/to/your/document.pdf
```

Output will be saved in the `results` folder.

### Step 3: Load the generated JSON structure

After the script runs successfully, a JSON file named after your PDF will be created in the `results` folder. Copy it to the `input/` folder of this project.

### Step 4: Run the RAG script

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