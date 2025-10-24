from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA

# 1️⃣ Load PDF
loader = PyPDFLoader("data/document1.pdf")
pages = loader.load()

# 2️⃣ Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = splitter.split_documents(pages)

# 3️⃣ Create embeddings using Ollama
embeddings = OllamaEmbeddings(model="llama3")  # or "mistral"

# 4️⃣ Build FAISS vector store
vectorstore = FAISS.from_documents(docs, embeddings)

# 5️⃣ Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 6️⃣ Create LLM (local Ollama model)
llm = OllamaLLM(model="llama3")

# 7️⃣ Build RAG chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 8️⃣ Chat loop
while True:
    query = input("\nAsk a question about the PDF (or type 'exit'): ")
    if query.lower() == "exit":
        break
    result = qa_chain.invoke({"query": query})
    print("\n📘 Answer:\n", result["result"])
