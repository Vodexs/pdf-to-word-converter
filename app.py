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

    # استخدام tempfile.gettempdir() عشان نضمن المسار الصح في Vercel
    base_temp = tempfile.gettempdir()
    pdf_path = os.path.join(base_temp, "input.pdf")
    docx_path = os.path.join(base_temp, "output.docx")

    try:
        # حفظ الملف
        file.save(pdf_path)

        # التأكد إن الملف اتسيف فعلاً قبل البدء
        if not os.path.exists(pdf_path):
            return "فشل في حفظ الملف مؤقتاً", 500

        # عملية التحويل
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

        # دالة التنظيف بعد الإرسال
        @after_this_request
        def cleanup(response):
            try:
                if os.path.exists(pdf_path): os.remove(pdf_path)
                if os.path.exists(docx_path): os.remove(docx_path)
            except:
                pass
            return response

        return send_file(
            docx_path,
            as_attachment=True,
            download_name=file.filename.replace('.pdf', '.docx')
        )

    except Exception as e:
        return f"حدث خطأ: {str(e)}", 500

app = app
