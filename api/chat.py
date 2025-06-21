# api/chat.py
from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse
import urllib.error
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

Selalu jawab dalam Bahasa Indonesia yang ramah dan profesional. Berikan jawaban yang singkat namun informatif."""
                
                # Get API key from environment variable
                api_key = os.environ.get('OPENROUTER_API_KEY')
                if not api_key:
                    # Fallback to hardcoded key
                    api_key = "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"
                
                # Prepare the payload for DeepSeek model
                payload = {
                    "model": "deepseek/deepseek-r1-0528:free",
                    "messages": [
                        {"role": "system", "content": INSTRUCTIONS},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 800,
                    "temperature": 0.7,
                    "stream": False
                }
                
                # Convert payload to JSON
                json_data = json.dumps(payload).encode('utf-8')
                
                # Create request
                req = urllib.request.Request(
                    "https://openrouter.ai/api/v1/chat/completions",
                    data=json_data,
                    headers={
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json',
                        'HTTP-Referer': 'https://rintisone.vercel.app',
                        'X-Title': 'RintisOne AI Assistant'
                    }
                )
                
                # Make the request with timeout
                try:
                    with urllib.request.urlopen(req, timeout=30) as response:
                        response_data = json.loads(response.read().decode())
                        
                        if 'error' in response_data:
                            raise Exception(f"API Error: {response_data['error']}")
                        
                        if 'choices' not in response_data or len(response_data['choices']) == 0:
                            raise Exception("No response from AI model")
                        
                        ai_response = response_data['choices'][0]['message']['content'].strip()
                        result = {'response': ai_response}
                        
                        self.wfile.write(json.dumps(result).encode())
                        return
                        
                except urllib.error.HTTPError as e:
                    error_code = e.code
                    if error_code == 401:
                        fallback_response = {
                            'response': 'Halo! Saya Rintis dari RintisOne. Saat ini sistem autentikasi sedang bermasalah. RintisOne adalah platform yang menghubungkan perusahaan dengan ekosistem kampus. Tim kami dari 7 universitas siap membantu strategi ekspansi bisnis Anda. Ada yang ingin ditanyakan tentang layanan kami?'
                        }
                    elif error_code == 429:
                        fallback_response = {
                            'response': 'Halo! Saya Rintis, asisten RintisOne. Sistem sedang sibuk saat ini. RintisOne menyediakan survei kampus terstruktur, analisis riset berbasis AI, stakeholder mapping, dan promosi komunitas untuk membantu ekspansi bisnis Anda di ekosistem kampus. Ada yang bisa saya bantu?'
                        }
                    else:
                        fallback_response = {
                            'response': 'Halo! Saya Rintis dari RintisOne. Meskipun sistem AI sedang mengalami gangguan, saya tetap siap membantu. RintisOne adalah inisiatif mahasiswa yang menghubungkan bisnis dengan kampus melalui riset, AI, dan blockchain. Ada informasi yang Anda butuhkan?'
                        }
                    
                    self.wfile.write(json.dumps(fallback_response).encode())
                    return
                
                except urllib.error.URLError:
                    fallback_response = {
                        'response': 'Halo! Saya Rintis, asisten RintisOne. Koneksi sedang bermasalah, tapi saya tetap di sini. RintisOne membantu perusahaan mengekspansi bisnis melalui ekosistem kampus dengan riset terstruktur dan teknologi AI. Ada yang ingin Anda ketahui tentang layanan kami?'
                    }
                    self.wfile.write(json.dumps(fallback_response).encode())
                    return
                
                except Exception as api_error:
                    fallback_response = {
                        'response': 'Halo! Saya Rintis dari RintisOne. Sedang ada masalah teknis, tapi saya masih bisa membantu dengan informasi dasar. RintisOne menyediakan layanan ekspansi bisnis melalui kampus dengan pendekatan riset dan teknologi. Tim kami tersebar di berbagai universitas di Pulau Jawa. Apakah ada yang bisa dibantu?'
                    }
                    self.wfile.write(json.dumps(fallback_response).encode())
                    return
            
            except Exception as e:
                fallback_response = {
                    'response': 'Halo! Saya Rintis dari RintisOne. Maaf ada gangguan sistem, tapi saya tetap di sini untuk membantu. RintisOne adalah platform yang menghubungkan perusahaan dengan ekosistem kampus melalui survei terstruktur, analisis AI, dan strategi berkelanjutan. Ada pertanyaan tentang layanan kami?'
                }
                self.wfile.write(json.dumps(fallback_response).encode())
            
        except json.JSONDecodeError:
            error_response = {
                'response': 'Halo! Saya Rintis dari RintisOne. Format permintaan tidak valid, tapi saya tetap siap membantu. RintisOne menyediakan layanan ekspansi bisnis melalui ekosistem kampus. Ada yang bisa saya bantu?'
            }
            self.wfile.write(json.dumps(error_response).encode())
        except Exception as e:
            fallback_response = {
                'response': 'Halo! Saya Rintis dari RintisOne. Terjadi kesalahan sistem, tapi saya tetap di sini untuk membantu. RintisOne adalah inisiatif kolaboratif mahasiswa yang menghubungkan perusahaan dengan kampus. Ada informasi yang Anda butuhkan?'
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
