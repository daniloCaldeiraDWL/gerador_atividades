from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient
import os

app = Flask(__name__)

# --- Configuração Obrigatória ---
HF_API_KEY = os.getenv("HF_API_KEY")  # Chave obtida de variável de ambiente
MODEL_ID = "google/gemma-2-2b-it"
max_new_tokens = 5000
temperature = 0.7
top_p = 0.9

def gerar_texto(api_key, model_id, prompt):
    if not api_key:
        return None, "Erro: Chave de API da Hugging Face não configurada."
    try:
        print(f"Conectando à API com o modelo: {model_id}...")
        client = InferenceClient(token=api_key)
        print(f"Enviando prompt: '{prompt}'")
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(
            messages=messages,
            model=model_id,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p
        )
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip(), None
        else:
            return None, "Erro: A API não retornou uma resposta válida."
    except Exception as e:
        error_msg = f"Erro ao chamar a API da Hugging Face: {e}"
        if "authorization" in str(e).lower():
            error_msg += "\nVerifique se sua chave de API está correta."
        return None, error_msg

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/resultado', methods=['GET'])
def resultado():
    resultado = localStorage.getItem('resultado') if 'localStorage' in globals() else ''
    return render_template('result.html', resultado=resultado)

@app.route('/gerar', methods=['POST'])
def gerar():
    try:
        data = request.get_json()
        num_atividades = int(data['num_atividades'])
        tipo_habilidade = data['tipo_habilidade'].strip()

        if num_atividades <= 0:
            return jsonify({"erro": "O número de atividades deve ser maior que 0."}), 400

        prompt = (f"Monte para mim uma programação de {num_atividades} atividades para uma semana, "
                  f"começando do dia 26/05/2025, para uma criança autista. "
                  f"Essa criança deve desenvolver habilidades de {tipo_habilidade}. "
                  f"As atividades propostas devem especificar qual habilidade está sendo trabalhada.")

        texto_gerado, erro = gerar_texto(HF_API_KEY, MODEL_ID, prompt)
        if texto_gerado:
            return jsonify({"resultado": texto_gerado})
        else:
            return jsonify({"erro": erro or "Não foi possível gerar o texto."}), 500
    except Exception as e:
        return jsonify({"erro": f"Erro ao processar a requisição: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))