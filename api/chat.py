# api/chat.py
import json
import urllib.request
import urllib.parse
import os

def handler(request):
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    # Only allow POST requests
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse request body
        if hasattr(request, 'body'):
            body = request.body
        else:
            body = request.get_body()
            
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        elif body is None:
            body = '{}'
            
        data = json.loads(body)
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': 'No prompt provided'})
            }
        
        # System instructions
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

        # Prepare API request
        api_url = "https://openrouter.ai/api/v1"
        
        # Get API key from environment variable (recommended) or fallback to hardcoded
        api_key = os.environ.get('OPENROUTER_API_KEY', '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')
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://rintisone.vercel.app',
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
        
        # Make API request using urllib (more compatible with Vercel)
        req_data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(api_url, data=req_data)
        
        for key, value in headers.items():
            req.add_header(key, value)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                
                if 'error' in response_data:
                    return {
                        'statusCode': 500,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                        },
                        'body': json.dumps({'error': f'AI API Error: {response_data["error"]}'})
                    }
                
                ai_response = response_data['choices'][0]['message']['content'].strip()
                
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                    },
                    'body': json.dumps({'response': ai_response})
                }
                
        except urllib.error.HTTPError as e:
            error_msg = f'HTTP Error {e.code}: {e.reason}'
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': error_msg})
            }
        except urllib.error.URLError as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': f'Network error: {str(e.reason)}'})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'error': f'API request failed: {str(e)}'})
            }
            
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'error': f'Server error: {str(e)}'})
        }
