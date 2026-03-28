from flask import Flask, render_template, request, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)

# فولدر مؤقت للملفات
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return "لم يتم اختيار ملف"
    
    file = request.files['pdf_file']
    if file.filename == '':
        return "اسم الملف فارغ"

    if file:
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        docx_path = pdf_path.replace('.pdf', '.docx')
        
        file.save(pdf_path)
        
        try:
            # عملية التحويل
            cv = Converter(pdf_path)
            cv.convert(docx_path)
            cv.close()
            
            # إرسال الملف وتحميله لليوزر
            return send_file(docx_path, as_attachment=True)
        except Exception as e:
            return f"حدث خطأ: {str(e)}"
        finally:
            # تنظيف الملفات القديمة عشان المساحة
            if os.path.exists(pdf_path): os.remove(pdf_path)

if __name__ == '__main__':
    # بورت 5000 ده اللي بنجرب بيه
    app.run(host='0.0.0.0', port=5000)