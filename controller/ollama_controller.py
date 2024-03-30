import requests
import json

def generate(prompt, temp= 0):
    r = requests.post('http://localhost:11434/api/generate', json={'model': 'mistral:latest', 'prompt': prompt, 'temp': temp}, stream=True)
    for line in r.iter_lines():
        if line:
            body = json.loads(line.decode('utf-8'))
            response = body.get('response', '')
            if response:
                yield response