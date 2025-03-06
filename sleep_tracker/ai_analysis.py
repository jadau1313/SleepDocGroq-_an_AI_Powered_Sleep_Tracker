

import requests
from groq import Groq
import os

def generate_sleep_insight(insights):
    prompt = f"""
    Based on the following sleep insights, write a friendly summary with 2 to 4 sentences to help the user understand their sleep habits as well as possible improvements. Information should be relevant and backed by modern sleep medicine standards:
    
    Average Sleep Duration: {insights['average_duration']:.2f} hours
    Most common averaged bedtime: {insights['common_bedtime']}
    Average awakenings: {insights['average_awakenings']:.1f}
    Best sleep day: {insights['best_day']} (Quality: {insights['best_quality']})
    Worst sleep day: {insights['worst_day']} (Quality: {insights['worst_quality']})
    Alcohol impact: {insights['alcohol_impact']}
    Cannabis impact: {insights['cannabis_impact']}
    Sleep aid impact: {insights['sleep_aid_impact']}
    
    Be supportive, encouraging, and suggest simple actionable advice.
    
    """
    def draft_message(content, role='user'):
        return {
            "role": role,
            "content": content
         }

    messages = [
        {
        'role': 'system',
        'content': 'You are a sleep doctor and sleep coach who is very friendly and helpful'
        }
    ]
    api_key = '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'
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")

    client = Groq(api_key=api_key)

    messages.append(draft_message(prompt))
    print(messages)

    try:
        chat_completion = client.chat.completions.create(
            temperature=1.0,
            n=1,
            model="mixtral-8x7b-32768",
            max_tokens=1000,
            messages=messages
        )
        print(chat_completion.choices[0].message.content)
        print(chat_completion.usage.total_tokens)
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"AI Sleep Insight could not be generated: {str(e)}"



