# api/chat.py
from http.server import BaseHTTPRequestHandler
import json
import requests
import os

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
            
            try:
                INSTRUCTIONS = """Nama kamu Rintis. Kamu adalah asisten virtual yang ramah, responsif, dan solutif, siap membantu pelanggan RintisOne dalam memahami layanan, menyelesaikan kendala teknis, menjawab pertanyaan umum, serta memberikan panduan penggunaan platform.

RintisOne adalah inisiatif kolaboratif mahasiswa dari berbagai universitas di Pulau Jawa yang bertujuan menjembatani perusahaan dengan ekosistem kampus. Kami memadukan riset lapangan, edukasi komunitas, dan teknologi seperti AI & Blockchain untuk menghasilkan strategi ekspansi yang akurat, transparan, dan berkelanjutan.

Layanan kami:
- Survei Kampus Terstruktur: Pemetaan menyeluruh terhadap ekosistem universitas, UMKM, dan stakeholder kampus
- Analisis Riset Berbasis AI: Insight strategis dari data real-time yang diproses cepat dan akurat
- Stakeholder Mapping & Edukasi Pasar: Menemukan titik implementasi terbaik dan membangun pemahaman yang menyeluruh
- Promosi Komunitas & Onboarding Mahasiswa: Meningkatkan adopsi produk melalui komunikasi yang tepat sasaran

Tim RintisOne:
- Pandu Bagus Witjaksono Athallah (Founder), mahasiswa Universitas Padjajaran
- Sabdo Dwiyantoro Aji, mahasiswa Universitas Brawijaya
- Fawwaz Absyar Rifai, mahasiswa Universitas Sebelas Maret
- Sultan Alexander Muhammad Rasyid, mahasiswa Institut Pertanian Bogor
- Fadhli Luthfanhadi, mahasiswa Universitas Diponegoro
- Lalu Muhammad Zidan Alfinly, mahasiswa Universitas Indonesia
- Silvan Nando Himawan, mahasiswa Universitas Pembangunan Nasional "Veteran" Yogyakarta

Selalu jawab dalam Bahasa Indonesia yang ramah dan profesional."""
                
                # Get API key from environment variable (more secure)
                api_key = os.environ.get('OPENROUTER_API_KEY')
                if not api_key:
                    # Fallback to hardcoded key (less secure, but for testing)
                    api_key = "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"
                
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://rintisone.vercel.app',  # Update with your actual domain
                    'X-Title': 'RintisOne AI Assistant'
                }
                
                payload = {
                    "model": "deepseek/deepseek-r1-0528:free",  # More reliable model
                    "messages": [
                        {"role": "system", "content": INSTRUCTIONS},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 800,
                    "temperature": 0.7,
                    "stream": False
                }
                
                # Add timeout and better error handling
                response = requests.post(
                    "https://openrouter.ai/api/v1",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                # Debug logging
                print(f"API Response Status: {response.status_code}")
                print(f"API Response Headers: {dict(response.headers)}")
                
                if response.status_code == 401:
                    self.wfile.write(json.dumps({
                        'error': 'Authentication failed. Please check API key configuration.'
                    }).encode())
                    return
                elif response.status_code == 429:
                    # Fallback response for rate limiting
                    fallback_response = {
                        'response': 'Maaf, sistem sedang sibuk. Sebagai asisten RintisOne, saya siap membantu Anda dengan informasi tentang layanan kami. RintisOne menyediakan survei kampus terstruktur, analisis riset berbasis AI, stakeholder mapping, dan promosi komunitas untuk membantu ekspansi bisnis Anda di ekosistem kampus. Ada yang bisa saya bantu?'
                    }
                    self.wfile.write(json.dumps(fallback_response).encode())
                    return
                elif response.status_code != 200:
                    # Try fallback response
                    fallback_response = {
                        'response': f'Halo! Saya Rintis, asisten virtual RintisOne. Maaf sedang mengalami gangguan teknis. RintisOne adalah platform yang menghubungkan perusahaan dengan ekosistem kampus melalui riset, AI, dan blockchain. Tim kami tersebar di berbagai universitas di Pulau Jawa. Ada yang bisa saya bantu terkait layanan kami?'
                    }
                    self.wfile.write(json.dumps(fallback_response).encode())
                    return
                
                response_data = response.json()
                
                if 'error' in response_data:
                    # Provide fallback response
                    fallback_response = {
                        'response': 'Halo! Saya Rintis dari RintisOne. Saat ini sistem AI sedang maintenance, namun saya tetap bisa membantu Anda dengan informasi dasar tentang layanan kami. RintisOne menyediakan layanan survei kampus, analisis AI, dan strategi ekspansi bisnis. Ada pertanyaan spesifik yang bisa saya jawab?'
                    }
                    self.wfile.write(json.dumps(fallback_response).encode())
                    return
                
                ai_response = response_data['choices'][0]['message']['content'].strip()
                result = {'response': ai_response}
                
                self.wfile.write(json.dumps(result).encode())
                
            except requests.exceptions.Timeout:
                fallback_response = {
                    'response': 'Halo! Saya Rintis, asisten RintisOne. Koneksi sedikit lambat, tapi saya tetap di sini. RintisOne membantu perusahaan mengekspansi bisnis melalui ekosistem kampus dengan riset terstruktur dan teknologi AI. Ada yang ingin Anda ketahui tentang layanan kami?'
                }
                self.wfile.write(json.dumps(fallback_response).encode())
            except requests.exceptions.RequestException as req_error:
                fallback_response = {
                    'response': 'Halo! Saya Rintis dari RintisOne. Sedang ada masalah jaringan, tapi saya masih bisa membantu dengan informasi dasar. RintisOne adalah inisiatif mahasiswa yang menghubungkan bisnis dengan kampus melalui survei, AI, dan blockchain. Tim kami ada di 7 universitas di Pulau Jawa. Ada yang bisa dibantu?'
                }
                self.wfile.write(json.dumps(fallback_response).encode())
            except Exception as api_error:
                fallback_response = {
                    'response': 'Halo! Saya Rintis, asisten virtual RintisOne. Meskipun sistem AI sedang bermasalah, saya tetap siap membantu. RintisOne menyediakan layanan ekspansi bisnis melalui kampus dengan pendekatan riset dan teknologi. Apakah ada informasi khusus yang Anda butuhkan?'
                }
                self.wfile.write(json.dumps(fallback_response).encode())
            
        except json.JSONDecodeError:
            error_response = {'error': 'Format data tidak valid'}
            self.wfile.write(json.dumps(error_response).encode())
        except Exception as e:
            fallback_response = {
                'response': 'Halo! Saya Rintis dari RintisOne. Maaf ada gangguan sistem, tapi saya tetap di sini untuk membantu. RintisOne adalah platform yang menghubungkan perusahaan dengan ekosistem kampus. Ada pertanyaan tentang layanan kami?'
            }
            self.wfile.write(json.dumps(fallback_response).encode())
    
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
