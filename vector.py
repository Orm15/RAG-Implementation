# build_vectorstore.py
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os

# 1. Cargar PDFs desde la carpeta Docs
loader = DirectoryLoader('./Docs', glob="**/*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()
print("Se cargaron los pdfs")

# 2. Dividir en chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
docs_chunks = text_splitter.split_documents(documents)
print("Se dividieron los chunks")

# 3. Embeddings con Ollama (puedes cambiar por sentence-transformers si prefieres velocidad)
embeddings = OllamaEmbeddings(model="nomic-embed-text")


# 4. Inicializar base de datos
db_location = "./chrome_langchain_db"
print("Se iniciliza la base de datos")

vector_store = Chroma(
    persist_directory=db_location,
    embedding_function=embeddings,
    collection_name="Response"
)
print("Se agregan los documentos")

# 5. Agregar documentos
vector_store.add_documents(documents=docs_chunks)

print("Vectorstore creado y persistido en disco.")
print("Cantidad de documentos en la colección:", vector_store._collection.count())
