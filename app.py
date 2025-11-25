from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf

# ------------------------------
# Initialize Flask App
# ------------------------------
app = Flask(__name__, static_folder='static', template_folder='templates')

# ------------------------------
# Model Paths (FINAL & CORRECT)
# ------------------------------
MODEL_XRAY_PATH = "healthinfo_models/xray_model.keras"
MODEL_SKIN_PATH = "healthinfo_models/skin_model_final.keras"
UPLOAD_FOLDER = "static/uploaded"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------------------
# Diagnostics
# ------------------------------
print("\n====== DEBUG START ======")
print("📂 ROOT DIR:", os.listdir("."))

if os.path.exists("healthinfo_models"):
    print("📁 MODEL FOLDER FOUND:", os.listdir("healthinfo_models"))
else:
    print("❌ MODEL FOLDER NOT FOUND")

def safe_size(path):
    try:
        return f"{os.path.getsize(path)} bytes"
    except:
        return "Not Found"

print("🔍 X-RAY MODEL SIZE:", safe_size(MODEL_XRAY_PATH))
print("🔍 SKIN MODEL SIZE:", safe_size(MODEL_SKIN_PATH))

# ------------------------------
# Load Models (Safe Loading)
# ------------------------------
xray_model = None
skin_model = None

try:
    xray_model = tf.keras.models.load_model(MODEL_XRAY_PATH)
    print("✅ X-RAY MODEL LOADED")
except Exception as e:
    print("❌ Failed to load X-Ray model:", e)

try:
    skin_model = tf.keras.models.load_model(MODEL_SKIN_PATH)
    print("✅ SKIN MODEL LOADED")
except Exception as e:
    print("❌ Failed to load Skin model:", e)

print("====== DEBUG END ======\n")

# ------------------------------
# Class Labels
# ------------------------------
xray_labels = ["Normal", "Pneumonia"]
skin_labels = ["akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"]

# ------------------------------
# Cure Translations
# ------------------------------
CURES = {
    "en": {
        "xray": {
            "Pneumonia": "🩺 Visit a pulmonologist + antibiotics + steam.",
            "Normal": "💪 Maintain clean air & healthy habits."
        },
        "skin": {
            "akiec": "☀️ Precancerous lesion. Dermatologist recommended.",
            "bcc": "💊 Cancerous lesion. Needs doctor.",
            "bkl": "🧴 Benign lesion.",
            "df": "🌿 Harmless.",
            "mel": "⚠️ Dangerous melanoma. Urgent attention needed.",
            "nv": "💧 Normal mole.",
            "vasc": "🩸 Vascular lesion. Laser possible."
        }
    }
}

# ------------------------------
# Routes
# ------------------------------
@app.route("/")
def home():
    return render_template("index.html", lang="en")

@app.route("/predict", methods=["POST"])
def predict():
    scan_type = request.form.get("scan_type", "xray")
    lang = request.form.get("lang", "en")

    if lang not in CURES:
        lang = "en"

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"})

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        img = image.load_img(file_path, target_size=(224, 224))
        img_array = np.expand_dims(image.img_to_array(img), axis=0) / 255.0

        # X-ray branch
        if scan_type == "xray":
            if xray_model is None:
                return jsonify({"error": "X-ray model not loaded"})

            pred = xray_model.predict(img_array)[0][0]
            confidence = max(pred, 1 - pred)
            predicted_class = xray_labels[1] if pred > 0.5 else xray_labels[0]
            icon = "😷" if predicted_class == "Pneumonia" else "😊"
            color = "red" if predicted_class == "Pneumonia" else "green"
            cure = CURES[lang]["xray"][predicted_class]

        # Skin branch
        elif scan_type == "skin":
            if skin_model is None:
                return jsonify({"error": "Skin model not loaded"})

            preds = skin_model.predict(img_array)[0]
            class_idx = int(np.argmax(preds))
            confidence = float(np.max(preds))
            predicted_class = skin_labels[class_idx]
            icon = "🩺"
            color = "#38bdf8"
            cure = CURES[lang]["skin"][predicted_class]

        else:
            return jsonify({"error": "Invalid scan type"})

        return render_template(
            "result.html",
            result=f"{predicted_class} {icon}",
            confidence=f"{confidence * 100:.2f}%",
            color=color,
            image_file=filename,
            scan_type=scan_type,
            cure=cure,
        )

    except Exception as e:
        print("❌ Prediction error:", e)
        return jsonify({"error": "Prediction failed", "details": str(e)})

# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
