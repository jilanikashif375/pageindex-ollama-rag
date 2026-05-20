# This script demonstrates a simple, minimal example of vectorless RAG with PageIndex.

# Clone the repository
# git clone https://github.com/VectifyAI/PageIndex.git
# cd PageIndex

# Install dependencies: pip install -r requirements.txt

import ollama
import json
import textwrap

with open("input/successful_file.json", "r", encoding="utf-8") as f:
    doc_structure = json.load(f)

def remove_fields(data, fields=None):
    if isinstance(data, dict):
        return {k: remove_fields(v, fields)
            for k, v in data.items() if k not in fields}
    elif isinstance(data, list):
        return [remove_fields(item, fields) for item in data]
    return data

def call_llm(prompt, model="granite4:latest", temperature=0):
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": temperature}
    )
    return response["message"]["content"].strip()

query = "What are the certificates asked by the provider"

tree_without_text = remove_fields(doc_structure, fields=["text"])

search_prompt = f"""
You are given a question and a tree structure of a document.
Each node contains a node id, node title, and a corresponding summary.
Your task is to find all nodes that are likely to contain the answer to the question.

Question: {query}

Document tree structure:
{json.dumps(tree_without_text, indent=2)}

Please reply in the following JSON format:
{{
    "thinking": "<Your thinking process on which nodes are relevant to the question>",
    "node_list": ["node_id_1", "node_id_2", ..., "node_id_n"]
}}
Directly return the final JSON structure. Do not output anything else.
"""

tree_search_result = call_llm(search_prompt)

def create_node_mapping(tree):
    """Create a flat dict mapping node_id to node for quick lookup."""
    mapping = {}

    def _traverse(nodes):
        for node in nodes:
            if isinstance(node, dict):
                if node.get('node_id'):
                    mapping[node['node_id']] = node
                if node.get('nodes'):
                    _traverse(node['nodes'])

    # If the root is a dict with 'structure', start there
    if isinstance(tree, dict) and 'structure' in tree:
        _traverse(tree['structure'])
    elif isinstance(tree, list):
        _traverse(tree)
    else:
        raise TypeError(f"Unexpected root type: {type(tree)}")

    return mapping

def print_wrapped(text, width=100):
    for line in text.splitlines():
        print(textwrap.fill(line, width=width))

node_map = create_node_mapping(doc_structure)
print(f"Mapped {len(node_map)} nodes")
print(list(node_map.keys())[:10])  # quick peek at first 10 node_ids

try:
    tree_search_result_json = json.loads(tree_search_result)
except json.JSONDecodeError:
    print("LLM output was not valid JSON:")
    print(tree_search_result)
    raise

print('Reasoning Process:')
print_wrapped(tree_search_result_json['thinking'])

print('\nRetrieved Nodes:')
for node_id in tree_search_result_json["node_list"]:
    node = node_map.get(node_id)
    if not node:
        print(f"Warning: node_id '{node_id}' not found in node_map")
        continue

    print(
        f"Node ID: {node['node_id']}\t "
        f"Start: {node.get('start_index')}\t "
        f"End: {node.get('end_index')}\t "
        f"Title: {node['title']}"
    )

node_list = tree_search_result_json["node_list"]

# Use summary instead of text
relevant_content = "\n\n".join(
    node_map[node_id].get("summary") or node_map[node_id].get("text", "")
    for node_id in node_list
    if node_id in node_map
)

print('Retrieved Context:\n')
print_wrapped(relevant_content[:1000] + '...')

answer_prompt = f"""
Answer the question based on the context:

Question: {query}
Context: {relevant_content}

Provide a clear, concise answer based only on the context provided.
"""

print('Generated Answer:\n')
answer = call_llm(answer_prompt)
print_wrapped(answer)
