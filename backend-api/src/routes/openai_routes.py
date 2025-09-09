from flask import Blueprint, jsonify, request
import openai
import os

openai_bp = Blueprint('openai', __name__)

@openai_bp.route('/generate-description', methods=['POST'])
def generate_description():
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
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em carreiras e profissões. Escreva descrições profissionais e informativas sobre diferentes profissões, sempre na 1º pessoa."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        description = response.choices[0].message.content.strip()
        
        return jsonify({
            'description': description,
            'profession': profession_clean
        })
        
    except openai.OpenAIError as e:
        return jsonify({'error': f'Erro na API OpenAI: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

