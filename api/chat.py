from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
    # api_key="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"
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

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="mistralai/mistral-small-3.2-24b-instruct:free",
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    response = chat_with_gpt(prompt)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="https://www.rintisone.vercel.app/ai-assistant.html", port=5000, debug=True)
