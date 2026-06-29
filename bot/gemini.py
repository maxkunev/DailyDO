from google import genai
import os
import prompts as pt
from datetime import date

from string import Template

import asyncio


client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

async def get_tasks(tasks):
    
    prompt = Template(pt.EXTRACT_DATA_PROMPT).substitute(
    current_date=date.today().isoformat(),
    text_from_user=tasks,
    )
    
    interaction = await asyncio.to_thread(
        client.interactions.create,
        model="gemma-4-31b-it",
        input=prompt
    )
    
    return interaction.output_text