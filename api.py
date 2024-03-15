from flask import Flask, request, jsonify, send_file, make_response
from waitress import serve
from excelToDXF import listToDXF
from verifyDXF.Drawing import Drawing
from datetime import datetime
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

        convertExcelDXF = listToDXF(excelFile)
        return send_file(convertExcelDXF.targetDXFFile, as_attachment=True, download_name= convertExcelDXF.fileName + ".dxf", mimetype='application/dxf')
    else:
        return jsonify({'message': 'Nenhum arquivo enviado.'}), 400

@app.route('/verify', methods=['POST'])
def routeVerifyDrawing():
    file = request.files['file']
    dataIssue = request.form['data']

    if file:
        # Adiciona no começo do arquivo a horário atual na ISO 8601
        currentTime = datetime.now().isoformat()
        fileCurrentTime = currentTime.replace(':', '-')
        fileName = fileCurrentTime + '_' + file.filename

        drawingFile = os.path.join('drawingSaves', fileName)
        file.save(drawingFile)

        verifyDrawing = Drawing(drawingFile, dataIssue)
        return make_response(verifyDrawing.message, 200, {'Content-Type': 'text/plain'})
    else:
        return jsonify({'message': 'Nenhum arquivo enviado.'}), 400

# Erro no Handling
def uncaught_exception_handler(ex):
    print("Uncaught Exception:", ex)

def unhandled_rejection_handler(promise, reason):
    print("[GRAVE] Rejeição possivelmente não tratada em: Promise", promise, "motivo:", reason)

sys.excepthook = uncaught_exception_handler

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.set_exception_handler(unhandled_rejection_handler)

# Opção para testes
if __name__ == '__main__':
    app.run(debug=True)

# Opção para produção
# if __name__ == '__main__':
#     serve(app, host="0.0.0.0", port=8080)