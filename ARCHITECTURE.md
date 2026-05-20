# PageIndex RAG - Architecture Documentation

## Overview

This project implements a simple, minimal example of vectorless RAG (Retrieval-Augmented Generation) with PageIndex. It uses reasoning-based retrieval to find relevant document sections using an LLM (Ollama).

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Input Layer                              │
│  ┌─────────────────┐    ┌─────────────────────────────┐   │
│  │  JSON Structure │    │   input/successful_file.json │   │
│  │    (from PDF)   │───▶│   (document tree with node   │   │
│  └─────────────────┘    │    id, title, summary, text) │   │
│                        └───────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  Processing Layer                            │
│                                                              │
│  ┌──────────────────┐    ┌─────────────────────────────┐   │
│  │ remove_fields()  │───▶│ Remove 'text' field from    │   │
│  │                  │    │ tree to reduce prompt size  │   │
│  └──────────────────┘    └─────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────┐    ┌─────────────────────────────┐   │
│  │create_node_map() │───▶│ Flatten tree into dict for  │   │
│  │                  │    │ quick node_id lookup        │   │
│  └──────────────────┘    └─────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────┐    ┌─────────────────────────────┐   │
│  │   call_llm()    │───▶│  Ollama API wrapper (LLM     │   │
│  │                  │    │  granite4:latest)           │   │
│  └──────────────────┘    └─────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  Retrieval Flow                              │
│                                                              │
│   ┌─────────────┐                                           │
│   │   Query     │──────────────┐                             │
│   └─────────────┘              ▼                             │
│                      ┌─────────────────────┐                 │
│                      │  Tree Search (LLM)  │                 │
│                      │  - Analyze tree     │                 │
│                      │  - Find relevant    │                 │
│                      │    nodes            │                 │
│                      │  - Return node_ids  │                 │
│                      └─────────┬───────────┘                 │
│                                │                             │
│                                ▼                             │
│                      ┌─────────────────────┐                 │
│                      │  Response Parsing   │                 │
│                      │  - JSON with        │                 │
│                      │    thinking +       │                 │
│                      │    node_list        │                 │
│                      └─────────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  Generation Flow                             │
│                                                              │
│   ┌──────────────────┐   ┌─────────────────────────────┐    │
│   │ Retrieved Nodes │──▶│ Extract summaries/text      │    │
│   └──────────────────┘   └──────────────┬──────────────┘    │
│                                         │                   │
│                                         ▼                   │
│                              ┌─────────────────────┐         │
│                              │ Answer Generation   │         │
│                              │ (LLM)               │         │
│                              │ - Context + Query   │         │
│                              │ - Final answer      │         │
│                              └─────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## File Structure

```
pageIndex/
├── ARCHITECTURE.md          # This documentation
├── pageindex_rag.py         # Main RAG script
├── requirements.txt         # Python dependencies
├── input/                   # Input JSON files
│   └── successful_file.json # Sample document structure
└── venv/                   # Virtual environment
```

## Core Components

### 1. `call_llm(prompt, model, temperature)`
- Wraps Ollama chat API
- Default model: `granite4:latest`
- Returns stripped response content

### 2. `remove_fields(data, fields)`
- Recursively removes specified fields from JSON
- Used to strip `text` field, keeping only structure, titles, summaries

### 3. `create_node_mapping(tree)`
- Converts nested tree to flat dictionary: `node_id -> node`
- Enables O(1) lookup for retrieved node_ids

### 4. `print_wrapped(text, width)`
- Utility for readable console output

## Data Flow

1. **Load**: Read JSON file from `input/` folder
2. **Prepare**: Remove `text` field from tree structure
3. **Search Prompt**: Build prompt with query + tree structure
4. **LLM Search**: Call Ollama to find relevant nodes
5. **Parse**: Extract `thinking` and `node_list` from JSON response
6. **Retrieve**: Get node content using node_id mapping
7. **Generate**: Build answer prompt with context + query
8. **LLM Answer**: Generate final answer

## Dependencies

- `ollama` - Local LLM interface

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Pull required model
ollama pull granite4:latest

# Run
python pageindex_rag.py
```

## JSON Input Format

Expected structure:
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