from flask import Flask, flash, redirect, render_template, request, send_file
import PyPDF2

app = Flask(__name__)

# Configuration: replace with your actual paths
UPLOAD_FOLDER = 'uploads'
PREDEFINED_PDFS = {
    "Fine PDF": "Fine.pdf",
    "Jay Ganesh PDF": "JAY_ganesh.pdf",
    "Palpasa PDF": "palpasa.pdf",
    "Preina PDF": "preina.pdf"
}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def merge_pdfs(user_pdf, predefined_pdf):
    pdf_merger = PyPDF2.PdfMerger()
    pdf_merger.append(user_pdf)
    pdf_merger.append(predefined_pdf)

    merged_filename = 'merged.pdf'
    merged_filepath = f"{UPLOAD_FOLDER}/{merged_filename}"
    
    with open(merged_filepath, 'wb') as merged_file:
        pdf_merger.write(merged_file)

    return merged_filepath

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'userfile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        userfile = request.files['userfile']
        if userfile.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # Save user's uploaded file
        userfile.save(f"{UPLOAD_FOLDER}/{userfile.filename}")
        
        # Get user's choice of predefined PDF
        predefined_pdf_name = request.form['predefined_pdf']
        predefined_pdf_path = PREDEFINED_PDFS[predefined_pdf_name]
        
        # Merge user's uploaded PDF with the chosen predefined PDF
        user_pdf_path = f"{UPLOAD_FOLDER}/{userfile.filename}"
        merged_pdf_path = merge_pdfs(user_pdf_path, predefined_pdf_path)
        
        return send_file(merged_pdf_path, as_attachment=True)

    return render_template('index.html', predefined_pdfs=PREDEFINED_PDFS)

if __name__ == '__main__':
    app.run(debug=True)
