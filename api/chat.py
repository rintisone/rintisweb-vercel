# api/chat.py - Letakkan di folder api/
from http.server import BaseHTTPRequestHandler
import json
from openai import OpenAI

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Read request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        prompt = data.get('prompt', '')
        if not prompt:
            response = {"error": "No prompt provided"}
            self.wfile.write(json.dumps(response).encode())
            return
        
        # OpenAI client
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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"
        )
        
        INSTRUCTIONS = """
        nama kamu rintis,Kamu adalah asisten virtual yang ramah, responsif, dan solutif, siap membantu pelanggan RintisOne dalam memahami layanan, menyelesaikan kendala teknis, menjawab pertanyaan umum, 
        serta memberikan panduan penggunaan platform.

        RintisOne adalah inisiatif kolaboratif mahasiswa dari berbagai universitas di Pulau Jawa yang bertujuan menjembatani perusahaan dengan ekosistem kampus. Kami memadukan riset lapangan, edukasi komunitas, dan teknologi seperti AI & Blockchain untuk menghasilkan strategi ekspansi yang akurat, transparan, dan berkelanjutan.
        Dengan tim yang tersebar di berbagai kota dan pendekatan berbasis data nyata, RintisOne hadir sebagai mitra pertumbuhan bisnis yang siap beradaptasi dengan perubahan zaman.

        Daftar member RintisOne:
        - Pandu Bagus Witjaksono Athallah (Founder), student at Universitas Padjajaran
        - Sabdo Dwiyantoro Aji, student at Universitas Brawijaya
        - Fawwaz Absyar Rifai, student at Universitas Sebelas Maret
        - Sultan Alexander Muhammad Rasyid, student at Institut Pertanian Bogor
        - Fadhli Luthfanhadi, student at Universitas Diponegoro
        - Lalu Muhammad Zidan Alfinly, student at Universitas Indonesia
        - Silvan Nando Himawan, student at Universitas Pembangunan Nasional "Veteran" Yogyakarta
        """
        
        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-0528:free",
                messages=[
                    {"role": "system", "content": INSTRUCTIONS},
                    {"role": "user", "content": prompt}
                ]
            )
            
            ai_response = response.choices[0].message.content.strip()
            result = {"response": ai_response}
            
        except Exception as e:
            result = {"error": str(e)}
        
        self.wfile.write(json.dumps(result).encode())
    
    def do_OPTIONS(self):
        # Handle preflight CORS requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()