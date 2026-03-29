import os
import tempfile
import shutil
from flask import Flask, render_template, request, send_file, after_this_request
from pdf2docx import Converter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return "فين الملف؟", 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return "اختار ملف PDF الأول", 400

    temp_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(temp_dir, "input.pdf")
    docx_path = os.path.join(temp_dir, "output.docx")

    try:
        file.save(pdf_path)
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

        @after_this_request
        def cleanup(response):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            return response

        return send_file(
            docx_path,
            as_attachment=True,
            download_name=file.filename.replace('.pdf', '.docx')
        )
    except Exception as e:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return f"Error: {str(e)}", 500

# ده السطر المهم لـ Vercel
app = app
