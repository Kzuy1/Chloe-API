from flask import Flask, request, jsonify, send_file, make_response, after_this_request
from waitress import serve
from Excel_To_DXF.ListToDxf import ListToDxf
from Excel_To_DXF_Redecam.ListToDxf import ListToDxf as ListToDxfRedecam
from Verify_Drawing.Drawing import Drawing
from Verify_Drawing_Redecam.Drawing import Drawing as DrawingRedecam
from Importa_Part_Attributes_Excel_To_DXF.importAttributesToDxf import import_attributes_from_xlsx
from utils.file_utils import clear_temp
import os
import asyncio
import sys
import gc

app = Flask(__name__)

@app.route('/')
def pagina_padrao():
    return 'Esta é a página padrão do meu site!'

@app.route('/import-data-to-dxf', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    import_type = request.form.get('import_type')

    if file:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(base_dir, 'Excel_To_DXF', 'temp')
        
        import_data = None
        if import_type == 'redecam':
            temp_dir = os.path.join(base_dir, 'Excel_To_DXF_Redecam', 'temp')
            import_data = ListToDxfRedecam(file)
        else:
            import_data = ListToDxf(file)
    
        @after_this_request
        def cleanup(response):
            clear_temp(temp_dir)
            return response

        return send_file(import_data.target_dxf_path, as_attachment=True, download_name=import_data.file_name + ".dxf", mimetype='application/dxf')
    else:
        return jsonify({'message': 'Nenhum arquivo enviado.'}), 400

@app.route('/verify-drawing', methods=['POST'])
def routeVerifyDrawing():
    file = request.files['file']
    data_issue = request.form['data']
    verification_type = request.form['verification_type']

    if file:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        temp_dir = os.path.join(base_dir, 'Verify_Drawing', 'temp')

        verify_drawing = None
        if verification_type == 'redecam':
            temp_dir = os.path.join(base_dir, 'Verify_Drawing_Redecam', 'temp')
            verify_drawing = DrawingRedecam(file, data_issue)
        else:
            verify_drawing = Drawing(file, data_issue)
        result = verify_drawing.message


        del verify_drawing
        gc.collect()

        @after_this_request
        def cleanup(response):
            clear_temp(temp_dir)
            return response

        return make_response(result, 200, {'Content-Type': 'text/plain'})
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

# Opção para produção   19:46 
if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)

