from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Buat folder output jika belum ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def clean_up_folder():
    """Hapus semua file di folder jika sudah ada file."""
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in files:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

@app.route('/')
def index():
    # Cek apakah folder output ada dan tidak kosong
    processed_images = os.listdir(app.config['UPLOAD_FOLDER']) if os.path.exists(app.config['UPLOAD_FOLDER']) else []  
    return render_template('index.html', processed_images=processed_images)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        try:
            # Membaca file gambar
            img = Image.open(file.stream).convert('L')  # Mengubah menjadi hitam putih
            
            # Gunakan template nama file
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Panggil fungsi untuk membersihkan folder
            clean_up_folder()

            # Simpan gambar
            img.save(file_path)

            # Kirimkan hasil gambar ke template
            return index()  # Kembali ke index untuk menampilkan semua gambar
        except Exception as e:
            return f'Error saat memproses gambar: {e}'

    return index()

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    files = request.files.getlist('folder[]')
    processed_images = []

    for file in files:
        if file:
            try:
                img = Image.open(file.stream).convert('L')
                filename = file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Panggil fungsi untuk membersihkan folder
                clean_up_folder()

                img.save(file_path)
                processed_images.append(filename)

            except Exception as e:
                return f'Error saat memproses gambar: {e}'

    return index()

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
