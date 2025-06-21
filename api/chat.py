# api/chat.py
from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):# api/chat.py - Fallback version
from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.wfile.write(json.dumps({'error': 'No data received'}).encode())
                return
                
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            prompt = data.get('prompt', '').strip()
            if not prompt:
                self.wfile.write(json.dumps({'error': 'No prompt provided'}).encode())
                return
            
            # Prepare response context
            context = """Saya adalah Rintis, asisten virtual RintisOne yang membantu dengan layanan ekspansi bisnis ke ekosistem kampus. 
            RintisOne adalah kolaborasi mahasiswa dari berbagai universitas di Pulau Jawa untuk menjembatani perusahaan dengan kampus melalui riset, AI, dan blockchain."""
            
            # Simple response generation based on keywords
            response_text = self.generate_response(prompt, context)
            
            result = {'response': response_text}
            self.wfile.write(json.dumps(result).encode())
            
        except json.JSONDecodeError:
            error_response = {'error': 'Invalid JSON in request body'}
            self.wfile.write(json.dumps(error_response).encode())
        except Exception as e:
            error_response = {'error': f'Server error: {str(e)}'}
            self.wfile.write(json.dumps(error_response).encode())
    
    def generate_response(self, prompt, context):
        prompt_lower = prompt.lower()
        
        # Define response patterns
        if any(word in prompt_lower for word in ['halo', 'hai', 'hello', 'hi']):
            return "Halo! Saya Rintis, asisten virtual RintisOne. Bagaimana saya bisa membantu Anda hari ini? Saya dapat memberikan informasi tentang layanan ekspansi bisnis kami ke ekosistem kampus."
        
        elif any(word in prompt_lower for word in ['layanan', 'service', 'offer']):
            return """RintisOne menawarkan:
            
**Survei Kampus Terstruktur**: Pemetaan menyeluruh ekosistem universitas dan UMKM
**Analisis Riset Berbasis AI**: Insight strategis dari data real-time
**Stakeholder Mapping**: Identifikasi titik implementasi terbaik  
**Promosi Komunitas**: Meningkatkan adopsi produk melalui komunikasi tepat sasaran

Apakah ada layanan spesifik yang ingin Anda ketahui lebih lanjut?"""
        
        elif any(word in prompt_lower for word in ['tim', 'team', 'member']):
            return """Tim RintisOne terdiri dari mahasiswa berbagai universitas:
            
- **Pandu Bagus Witjaksono Athallah** (Founder) - Universitas Padjajaran
- **Sabdo Dwiyantoro Aji** - Universitas Brawijaya  
- **Fawwaz Absyar Rifai** - Universitas Sebelas Maret
- **Sultan Alexander Muhammad Rasyid** - Institut Pertanian Bogor
- **Fadhli Luthfanhadi** - Universitas Diponegoro
- **Lalu Muhammad Zidan Alfinly** - Universitas Indonesia
- **Silvan Nando Himawan** - UPN "Veteran" Yogyakarta"""
        
        elif any(word in prompt_lower for word in ['kontak', 'contact', 'hubungi']):
            return "Untuk menghubungi RintisOne, Anda dapat menggunakan form kontak di website kami atau mengirim pesan melalui platform ini. Tim kami siap membantu menjawab pertanyaan tentang layanan ekspansi bisnis ke ekosistem kampus."
        
        elif any(word in prompt_lower for word in ['ai', 'artificial intelligence', 'teknologi']):
            return "RintisOne menggunakan teknologi AI untuk analisis riset berbasis data real-time, memberikan insight strategis untuk ekspansi bisnis. Kami juga mengintegrasikan blockchain untuk transparansi dan akurasi dalam proses bisnis."
        
        elif any(word in prompt_lower for word in ['kampus', 'universitas', 'mahasiswa']):
            return "RintisOne fokus menjembatani perusahaan dengan ekosistem kampus di Pulau Jawa. Kami memahami dinamika mahasiswa, UMKM kampus, dan stakeholder universitas untuk membantu ekspansi bisnis yang efektif dan berkelanjutan."
        
        else:
            return f"Terima kasih atas pertanyaan Anda tentang '{prompt}'. Sebagai asisten RintisOne, saya dapat membantu dengan informasi tentang layanan ekspansi bisnis, tim kami, teknologi yang kami gunakan, atau cara menghubungi kami. Apakah ada hal spesifik yang ingin Anda ketahui?"
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'RintisOne AI API is running', 'status': 'ok'}).encode())
    def do_POST(self):
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.wfile.write(json.dumps({'error': 'No data received'}).encode())
                return
                
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            prompt = data.get('prompt', '').strip()
            if not prompt:
                self.wfile.write(json.dumps({'error': 'No prompt provided'}).encode())
                return
            
            # Use requests instead of OpenAI client to avoid compatibility issues
            try:
                INSTRUCTIONS = """nama kamu rintis,Kamu adalah asisten virtual yang ramah, responsif, dan solutif, siap membantu pelanggan RintisOne dalam memahami layanan, menyelesaikan kendala teknis, menjawab pertanyaan umum, serta memberikan panduan penggunaan platform.

RintisOne adalah inisiatif kolaboratif mahasiswa dari berbagai universitas di Pulau Jawa yang bertujuan menjembatani perusahaan dengan ekosistem kampus. Kami memadukan riset lapangan, edukasi komunitas, dan teknologi seperti AI & Blockchain untuk menghasilkan strategi ekspansi yang akurat, transparan, dan berkelanjutan.

Daftar member RintisOne:
- Pandu Bagus Witjaksono Athallah (Founder), student at Universitas Padjajaran
- Sabdo Dwiyantoro Aji, student at Universitas Brawijaya
- Fawwaz Absyar Rifai, student at Universitas Sebelas Maret
- Sultan Alexander Muhammad Rasyid, student at Institut Pertanian Bogor
- Fadhli Luthfanhadi, student at Universitas Diponegoro
- Lalu Muhammad Zidan Alfinly, student at Universitas Indonesia
- Silvan Nando Himawan, student at Universitas Pembangunan Nasional "Veteran" Yogyakarta"""
                
                # Direct API call using requests
                headers = {
                    'Authorization': 'Bearer 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',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://your-vercel-app.vercel.app',
                    'X-Title': 'RintisOne AI Assistant'
                }
                
                payload = {
                    "model": "deepseek/deepseek-r1-0528:free",
                    "messages": [
                        {"role": "system", "content": INSTRUCTIONS},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
                
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code != 200:
                    error_detail = response.text
                    self.wfile.write(json.dumps({
                        'error': f'API Error {response.status_code}: {error_detail}'
                    }).encode())
                    return
                
                response_data = response.json()
                
                if 'error' in response_data:
                    self.wfile.write(json.dumps({
                        'error': f'AI API Error: {response_data["error"]}'
                    }).encode())
                    return
                
                ai_response = response_data['choices'][0]['message']['content'].strip()
                result = {'response': ai_response}
                
                self.wfile.write(json.dumps(result).encode())
                
            except requests.exceptions.Timeout:
                error_response = {'error': 'AI service timeout. Please try again.'}
                self.wfile.write(json.dumps(error_response).encode())
            except requests.exceptions.RequestException as req_error:
                error_response = {'error': f'Network error: {str(req_error)}'}
                self.wfile.write(json.dumps(error_response).encode())
            except Exception as api_error:
                error_response = {'error': f'AI service error: {str(api_error)}'}
                self.wfile.write(json.dumps(error_response).encode())
            
        except json.JSONDecodeError:
            error_response = {'error': 'Invalid JSON in request body'}
            self.wfile.write(json.dumps(error_response).encode())
        except Exception as e:
            error_response = {'error': f'Server error: {str(e)}'}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle preflight CORS requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
    def do_GET(self):
        # Handle GET requests (for testing)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'RintisOne AI API is running', 'status': 'ok'}).encode())
