from flask import Flask, render_template, request, send_file
from PIL import Image
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
import os
import zipfile

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

# Convert Images to PDF
@app.route("/images-to-pdf", methods=["POST"])
def images_to_pdf():
    files = request.files.getlist("images")
    pdf_path = os.path.join(OUTPUT_FOLDER, "converted.pdf")

    image_list = []

    for file in files:
        img_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(img_path)
        image = Image.open(img_path).convert("RGB")
        image_list.append(image)

    if image_list:
        image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])

    return send_file(pdf_path, as_attachment=True)

# Convert PDF to Images
@app.route("/pdf-to-images", methods=["POST"])
def pdf_to_images():
    file = request.files["pdf"]
    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)

    images = convert_from_path(pdf_path)

    zip_path = os.path.join(OUTPUT_FOLDER, "pages.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for i, image in enumerate(images):
            img_path = os.path.join(OUTPUT_FOLDER, f"page_{i+1}.png")
            image.save(img_path, "PNG")
            zipf.write(img_path, f"page_{i+1}.png")

    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    if __name__ == "__main__":

    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
