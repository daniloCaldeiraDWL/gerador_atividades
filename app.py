from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Configuração Obrigatória ---
HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_ID = "google/gemma-2-2b-it"
max_new_tokens = 5000
temperature = 0.7
top_p = 0.9

def gerar_texto(api_key, model_id, prompt):
    if not api_key:
        logger.error("Chave de API da Hugging Face não configurada.")
        return None, "Erro: Chave de API da Hugging Face não configurada."
    
    try:
        logger.info(f"Conectando à API com o modelo: {model_id}")
        client = InferenceClient(token=api_key, timeout=30)
        logger.info(f"Enviando prompt: '{prompt}'")
        
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(
            messages=messages,
            model=model_id,
            max_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p
        )
        logger.debug(f"Resposta da API: {response}")
        
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip(), None
        else:
            logger.error("A API não retornou uma resposta válida.")
            return None, "Erro: A API não retornou uma resposta válida."
    
    except Exception as e:
        logger.exception(f"Erro ao chamar a API da Hugging Face: {str(e)}")
        if "authorization" in str(e).lower():
            error_msg = "Chave de API inválida ou não autorizada."
        elif "429" in str(e).lower():
            error_msg = "Limite de taxa da API da Hugging Face excedido. Tente novamente mais tarde."
        else:
            error_msg = f"Erro ao chamar a API da Hugging Face: {str(e)}"
        return None, error_msg

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/resultado', methods=['GET'])
def resultado():
    return render_template('result.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    try:
        data = request.get_json()
        logger.debug(f"Dados recebidos: {data}")
        num_atividades = int(data['num_atividades'])
        tipo_habilidade = data['tipo_habilidade'].strip()

        if num_atividades <= 0:
            logger.warning("Número de atividades inválido: %d", num_atividades)
            return jsonify({"erro": "O número de atividades deve ser maior que 0."}), 400

        prompt = (f"Monte para mim uma programação de {num_atividades} atividades para uma semana, "
                  f"começando do dia 26/05/2025, para uma criança autista. "
                  f"Essa criança deve desenvolver habilidades de {tipo_habilidade}. "
                  f"As atividades propostas devem especificar qual habilidade está sendo trabalhada.")

        texto_gerado, erro = gerar_texto(HF_API_KEY, MODEL_ID, prompt)
        if texto_gerado:
            logger.info("Texto gerado com sucesso.")
            return jsonify({"resultado": texto_gerado})
        else:
            logger.error(f"Erro ao gerar texto: {erro}")
            return jsonify({"erro": erro or "Não foi possível gerar o texto."}), 500
    
    except Exception as e:
        logger.exception(f"Erro ao processar a requisição: {str(e)}")
        return jsonify({"erro": f"Erro ao processar a requisição: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))