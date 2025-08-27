from flask import Flask, request, jsonify, send_file, make_response, after_this_request
from waitress import serve
from excelToDXF import listToDXF
from verifyDXF.Drawing import Drawing
from Importa_Part_Attributes_Excel_To_DXF.importAttributesToDxf import import_attributes_from_xlsx, clear_temp
from datetime import datetime
import os
import time
import asyncio
import sys

app = Flask(__name__)

# Função para deletar arquivos antigos na pasta 'drawingSaves'
def delete_old_files(directory, days_old):
    now = time.time()
    cutoff = now - (days_old * 86400)  # 90 dias em segundos

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_last_modified = os.path.getmtime(file_path)
            if file_last_modified < cutoff:
                os.remove(file_path)

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
    
@app.route('/add-attributes', methods=['POST'])
def routeAddAttributes():
    xlsx_file = request.files.get('xlsx')
    zip_file = request.files.get('zip')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(base_dir, 'Importa_Part_Attributes_Excel_To_DXF', 'temp')

    if xlsx_file and zip_file:
        output_zip_path = import_attributes_from_xlsx(xlsx_file, zip_file)

        @after_this_request
        def cleanup(response):
            clear_temp(temp_dir)
            return response

        return send_file(output_zip_path, as_attachment=True, download_name='resultado.zip', mimetype='application/zip')
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
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=3000, debug=True)

# Opção para produção
if __name__ == '__main__':
    delete_old_files('drawingSaves', 90)
    serve(app, host="0.0.0.0", port=8080)
