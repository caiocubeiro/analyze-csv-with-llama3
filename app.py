from flask import Flask, request, render_template, jsonify, session, redirect, url_for
import pandas as pd
import ollama
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Rota index
@app.route("/")
def index():
    file_path = session.get("file_path")
    file_name = os.path.basename(file_path) if file_path else None
    return render_template("index.html", file_name=file_name)


# Rota para upload do arquivo CSV
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file and file.filename.endswith(".csv"):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        session["file_path"] = file_path
        return redirect(url_for("index"))
    else:
        return "Por favor, envie um arquivo CSV válido.", 400


# Rota para deletar arquivo na session, liberando upload de outros arquivos
@app.route("/delete_session", methods=["POST"])
def delete_session():
    file_path = session.pop("file_path", None)
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for("index"))


# Rota para direcionar pergunta ao LLM
@app.route("/ask", methods=["POST"])
def ask_question():
    file_path = session.get("file_path")
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Upload ou arquivo não identificado."})

    df = pd.read_csv(file_path)
    question = request.json.get("question")
    answer = llama_answer(df, question)
    return jsonify({"answer": answer})


# Função para montar prompt e fazer request ao LLM
def llama_answer(df, question):
    context = df.to_string()
    prompt = f"Contexto: {context}\n Pergunta: {question}\n Sempre responder a pergunta sem informar o código utilizado para analise, somente trazendo o resultado final\nPor favor, responda em português:"
    print("Gerando resposta")
    time_ini = datetime.now()
    response = ollama.chat(
        model="llama3", messages=[{"role": "user", "content": prompt}]
    )
    print(f"Reposta gerada em: {datetime.now() - time_ini}")
    if isinstance(response, dict) and "message" in response:
        content = response["message"].get("content", "Sem conteúdo na resposta")
        return content
    else:
        return "Erro ao processar resposta"


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host="0.0.0.0")
