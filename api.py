from flask import Flask, request, jsonify, send_file
from lista import lista
import os
import asyncio
import sys

app = Flask(__name__)

@app.route('/')
def pagina_padrao():
    return 'Esta é a página padrão do meu site!'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = file.filename
        excelFile = os.path.join('uploads', filename)
        file.save(excelFile)

        blocosFileZip = lista(excelFile)
        return send_file(blocosFileZip, as_attachment=True, download_name="BLOCOS-BRANCOS.zip", mimetype='application/zip')
    else:
        return jsonify({'message': 'Nenhum arquivo enviado.'}), 400
        
# Erro no Handling
def uncaught_exception_handler(ex):
    print("Uncaught Exception:", ex)

def unhandled_rejection_handler(promise, reason):
    print("[GRAVE] Rejeição possivelmente não tratada em: Promise", promise, "motivo:", reason)

sys.excepthook = uncaught_exception_handler

loop = asyncio.get_event_loop()
loop.set_exception_handler(unhandled_rejection_handler)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)