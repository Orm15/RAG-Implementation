from flask import Flask, request, jsonify
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from geminiClient import *
# Inicializa Flask
app = Flask(__name__)

embedding = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma(
    persist_directory="./chrome_langchain_db",  # Ajusta el path si tu base está en otro lugar
    embedding_function=embedding,
    collection_name="Response"
)
retriever = vector_store.as_retriever(search_kwargs={"k": 8})

final_prompt = PromptTemplate.from_template("""
Tú eres el asistente Botsito y con esta información: {doc}

debes responder esta pregunta: {question} respecto a mi cv, 
si la pregunta no tiene relacion a la respuesta menciona que no puedes 
responder preguntas que no tengan que ver con mi cv
""")

def responder_final(doc_resumido, question):
    prompt = final_prompt.format(doc=doc_resumido, question=question)
    respuesta = clienteLLM(prompt)
    return respuesta.strip()

@app.route("/consultar_base_conocimiento", methods=["POST"])
def consultar_base_conocimiento_endpoint():
    data = request.get_json()
    question = data.get("question", "")
    try:
        docs = retriever.invoke(question)
        if any(docs):
            resumen_concatenado = "\n".join([doc.page_content for doc in docs])
            salida = responder_final(resumen_concatenado, question)
            respuesta = salida
        else:
            respuesta = f"La base de conocimiento no tiene respuesta: {len(docs)}"
        return jsonify({"respuesta": respuesta})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
