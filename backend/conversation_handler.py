from memory import get_session, update_session
import re
from datetime import datetime

def extract_flight_info(text):
    """Extract flight information from user message"""
    info = {}
    
    # Extract cities (basic pattern)
    cities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b', text)
    if len(cities) >= 2:
        info['origin'] = cities[0]
        info['destination'] = cities[1]
    
    # Extract dates (basic pattern)
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b'
    ]
    
    for pattern in date_patterns:
        dates = re.findall(pattern, text, re.IGNORECASE)
        if dates:
            info['departure_date'] = dates[0]
            break
    
    return info

async def handle_chat_message(user_id, message):
    """Main conversation handler with context"""
    try:
        session = get_session(user_id)
        
        # Extract any flight information from message
        flight_info = extract_flight_info(message)
        session['context'].update(flight_info)
        
        # Add user message to history
        session['messages'].append({
            'role': 'user',
            'content': message
        })
        
        # Keep only last 10 messages for context
        if len(session['messages']) > 10:
            system_msg = session['messages'][0]
            session['messages'] = [system_msg] + session['messages'][-9:]
        
        # Call DeepSeek API with context
        response = await call_deepseek_api(session['messages'], session['context'])
        
        # Add assistant response
        session['messages'].append({
            'role': 'assistant',
            'content': response
        })
        
        # Update session
        update_session(user_id, session)
        
        return {
            'response': response,
            'context': session['context']
        }
        
    except Exception as e:
        print(f"Error in conversation handler: {e}")
        return {
            'response': "I'm sorry, I encountered an error. Let's try again.",
            'context': {}
        }

async def call_deepseek_api(messages, context):
    """Call DeepSeek API with enhanced context"""
    import openai
    
    # Add context to system message
    context_info = ""
    if context.get('origin') and context.get('destination'):
        context_info = f"\nCurrent booking context: From {context['origin']} to {context['destination']}"
        if context.get('departure_date'):
            context_info += f" on {context['departure_date']}"
    
    if context_info:
        messages[0]['content'] += context_info
    
    try:
        client = openai.OpenAI(
            api_key="your-deepseek-api-key",
            base_url="https://api.deepseek.com"
        )
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"DeepSeek API error: {e}")
        return "I'm having trouble connecting right now. Please try again."
