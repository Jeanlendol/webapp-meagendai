from flask import Blueprint, jsonify, request
import openai
import os

openai_bp = Blueprint('openai', __name__)

@openai_bp.route('/generate-description', methods=['POST', 'OPTIONS'])
def generate_description():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
            
        profession = data.get('profession')
        
        if not profession:
            return jsonify({'error': 'Profissão é obrigatória'}), 400
        
        # Remover emojis da profissão se houver
        profession_clean = profession.split(' ', 1)[-1] if ' ' in profession else profession
        
        # Verificar se a chave da OpenAI está configurada
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return jsonify({'error': 'Chave da OpenAI não configurada'}), 500
        
        # Configurar OpenAI
        client = openai.OpenAI(api_key=api_key)
        
        # Prompt para gerar descrição da profissão
        prompt = f"Escreva uma descrição detalhada da profissão {profession_clean}, incluindo responsabilidades, áreas de atuação e características principais. A descrição deve ser profissional, informativa e ter entre 100-200 palavras."
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Modelo correto
            messages=[
                {"role": "system", "content": "Você é um especialista em carreiras e profissões. Escreva descrições profissionais e informativas sobre diferentes profissões."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        description = response.choices[0].message.content.strip()
        
        return jsonify({
            'success': True,
            'description': description,
            'profession': profession_clean
        })
        
    except openai.APIError as e:
        print(f"Erro OpenAI API: {str(e)}")
        return jsonify({'error': f'Erro na API OpenAI: {str(e)}'}), 500
    except openai.RateLimitError as e:
        print(f"Limite de taxa OpenAI: {str(e)}")
        return jsonify({'error': 'Limite de requisições excedido. Tente novamente mais tarde.'}), 429
    except Exception as e:
        print(f"Erro interno: {str(e)}")
        return jsonify({'error': f'Erro interno do servidor'}), 500
