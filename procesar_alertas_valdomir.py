#!/usr/bin/env python3
"""
Procesa alertas de Google sobre Sebastián Valdomir
Guarda en Airtable automáticamente
"""

import re
import json
from html.parser import HTMLParser
import urllib.request
import urllib.error

# Configuración
AIRTABLE_BASE_ID = 'appEUSIW4bXqh38M6'
AIRTABLE_TABLE_ID = 'tblH4rH9vZQr4Jy6l'
AIRTABLE_TOKEN = 'patdRWnurwsIu3Odd'

class HTMLLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_link = None
        self.current_text = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.current_link = value
    
    def handle_data(self, data):
        if self.current_link:
            self.current_text.append(data)
    
    def handle_endtag(self, tag):
        if tag == 'a' and self.current_link:
            text = ''.join(self.current_text).strip()
            if text:
                self.links.append({'url': self.current_link, 'text': text})
            self.current_link = None
            self.current_text = []

def extract_title_and_url(html_content):
    parser = HTMLLinkParser()
    try:
        parser.feed(html_content)
        if parser.links:
            first = parser.links[0]
            return first['text'], first['url']
    except:
        pass
    return None, None

def extract_media(text):
    lines = text.split('\n')
    for line in lines[:10]:
        line = line.strip()
        match = re.search(r'\*\*([^*]+)\*\*', line)
        if match:
            media = match.group(1).strip()
            if 2 < len(media) < 100:
                return media
    return 'Google Alerts'

def save_to_airtable(titulo, url, medio, fecha):
    api_url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}'
    
    payload = {
        'records': [{
            'fields': {
                'Título': titulo,
                'Link': url,
                'Medio': medio,
                'Fecha': fecha,
                'Tipo de aparición': 'Mención',
            }
        }]
    }
    
    json_data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        api_url,
        data=json_data,
        headers={
            'Authorization': f'Bearer {AIRTABLE_TOKEN}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return 'records' in result
    except Exception as e:
        print(f'Error: {str(e)}')
        return False

def process_alert(html_content, text_content, email_date):
    titulo, url = extract_title_and_url(html_content)
    medio = extract_media(text_content)
    
    if not titulo:
        lines = text_content.split('\n')
        for line in lines[:5]:
            if line.strip() and len(line) > 10:
                titulo = line.strip()
                break
    
    return {
        'titulo': titulo or 'Sin título',
        'url': url or '',
        'medio': medio,
        'fecha': email_date,
    }

if __name__ == '__main__':
    print('✓ Procesador de alertas de Valdomir listo')
