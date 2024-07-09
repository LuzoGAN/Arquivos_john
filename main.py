from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import os
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def dividir_excel(excel_file, output_dir, linhas_por_arquivo=10000):
    df = pd.read_excel(excel_file)
    os.makedirs(output_dir, exist_ok=True)
    total_linhas = len(df)
    num_files = (total_linhas // linhas_por_arquivo) + int(total_linhas % linhas_por_arquivo != 0)
    output_files = []
    for i in range(num_files):
        start_row = i * linhas_por_arquivo
        end_row = min((i + 1) * linhas_por_arquivo, total_linhas)
        df_chunk = df.iloc[start_row:end_row]
        txt_data = df_chunk.to_csv(index=False, sep="\t")
        output_file = os.path.join(output_dir, f"Arquivo_{i + 1}.txt")
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(txt_data)
        output_files.append(output_file)
    return output_files

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado"
    file = request.files['file']
    if file.filename == '':
        return "Nenhum arquivo selecionado"
    if file and file.filename.endswith('.xlsx'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        output_files = dividir_excel(file_path, RESULT_FOLDER)
        zip_path = os.path.join(RESULT_FOLDER, 'result.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in output_files:
                zipf.write(file, os.path.basename(file))
        return send_from_directory(directory=RESULT_FOLDER, path='result.zip', as_attachment=True)
    else:
        return "Formato de arquivo não suportado"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
