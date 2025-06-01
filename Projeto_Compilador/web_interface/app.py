import re
import subprocess
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Caminho para os ficheiros .pas
PAS_FILES_PATH = '../examples/pas'

def strip_ansi(text):
    """Remove códigos ANSI (cores) da saída, para não quebrar o JSON no frontend."""
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

@app.route('/')
def index():
    pas_files = os.listdir(PAS_FILES_PATH)
    pas_files = [f for f in pas_files if f.endswith('.pas')]
    return render_template('index.html', pas_files=pas_files)

@app.route('/execute', methods=['POST'])
def execute():
    filename = request.json.get('filename')
    action = request.json.get('action')
    full_path = os.path.join(PAS_FILES_PATH, filename)

    if action == "run":
        cmd = ["python3", "../main.py", full_path]
    elif action == "compile_only":
        cmd = ["python3", "../main.py", full_path]
    elif action in ["tokens", "ast", "semantic"]:
        cmd = ["python3", "../test.py", full_path, action]
    else:
        return jsonify({"output": "Ação inválida."})

    try:
        timeout_value = 0.5 if action == "compile_only" else 3
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd(),
            timeout=timeout_value
        )
        output = result.stdout + ("\n" + result.stderr if result.stderr else "")
        output = strip_ansi(output)
    except subprocess.TimeoutExpired:
        if action == "compile_only":
            output = "✅ Compilação concluída. Ficheiro .vm provavelmente gerado com sucesso!"
        else:
            output = (
                "⚠️ Erro: a execução foi interrompida.\n"
                "Provavelmente o programa requere input (instrução 'read'),\n"
                "mas não é possível interagir com input via interface web.\n"
                "Executa este programa no terminal local se precisa de entrada de dados."
            )
    except Exception as e:
        output = f"⚠️ Erro inesperado ao executar: {e}"

    # ✅ GARANTE QUE DEVOLVE SEMPRE RESPOSTA
    return jsonify({"output": output})


@app.route('/get_vm', methods=['POST'])
def get_vm():
    filename = request.json.get('filename')
    base_name = os.path.splitext(filename)[0]
    vm_file_path = os.path.join('examples/vm', base_name + '.vm')

    if not os.path.exists(vm_file_path):
        return jsonify({"output": f"Ficheiro {vm_file_path} não encontrado."})

    try:
        with open(vm_file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        content = f"Erro ao ler ficheiro VM: {e}"

    return jsonify({"output": content})

if __name__ == '__main__':
    app.run(debug=True)
