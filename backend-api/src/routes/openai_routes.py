from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import openai
import os

openai_bp = Blueprint('openai', __name__)

@openai_bp.route('/generate-description', methods=['POST', 'OPTIONS'])
@cross_origin(origins='*', methods=['POST', 'OPTIONS'], allow_headers=['Content-Type', 'Authorization'])
def generate_description():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    
    try:
        data = request.json
        profession = data.get('profession')
        
        if not profession:
            return jsonify({'error': 'Profissão é obrigatória'}), 400
        
        # Remover emojis da profissão se houver
        profession_clean = profession.split(' ', 1)[-1] if ' ' in profession else profession
        
        # Configurar OpenAI (a chave já está nas variáveis de ambiente)
        client = openai.OpenAI()
        
        # Prompt para gerar descrição da profissão
        prompt = f"Escreva uma descrição detalhada da profissão {profession_clean}, incluindo responsabilidades, áreas de atuação e características principais. A descrição deve ser profissional, informativa e ter entre 100-200 palavras."
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em carreiras e profissões. Escreva descrições profissionais e informativas sobre diferentes profissões."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        description = response.choices[0].message.content.strip()
        
        result = jsonify({
            'description': description,
            'profession': profession_clean
        })
        
        # Add CORS headers to the response
        result.headers.add('Access-Control-Allow-Origin', '*')
        return result
        
    except openai.OpenAIError as e:
        error_response = jsonify({'error': f'Erro na API OpenAI: {str(e)}'})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500
    except Exception as e:
        error_response = jsonify({'error': f'Erro interno: {str(e)}'})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500

