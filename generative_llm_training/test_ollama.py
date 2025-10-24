from ollama import embeddings

output = embeddings(model='llama3', prompt='FastAPI is a modern web framework for Python.')
print(output)
