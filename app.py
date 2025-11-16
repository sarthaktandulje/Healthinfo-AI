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
# Configuration
# ------------------------------
MODEL_XRAY_PATH = "model/xray_model.keras"         # FIXED PATH
MODEL_SKIN_PATH = "model/skin_model_final.keras"   # FIXED PATH
UPLOAD_FOLDER = "static/uploaded"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------------------
# Load Both Models
# ------------------------------
xray_model, skin_model = None, None

try:
    xray_model = tf.keras.models.load_model(MODEL_XRAY_PATH)
    print("✅ X-ray Model loaded successfully!")
except Exception as e:
    print(f"⚠️ X-ray model not loaded: {e}")

try:
    skin_model = tf.keras.models.load_model(MODEL_SKIN_PATH)
    print("✅ Skin Model loaded successfully!")
except Exception as e:
    print(f"⚠️ Skin model not loaded: {e}")

# ------------------------------
# Labels
# ------------------------------
xray_labels = ["Normal", "Pneumonia"]
skin_labels = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

# ------------------------------
# Cure Translations (EN / HI / JA)
# ------------------------------

CURES = {
    'en': {
        'xray': {
            'Pneumonia': (
                "🩺 **Recommended Care for Pneumonia:**\n\n"
                "🔹 Visit a pulmonologist.\n"
                "🔹 Take prescribed antibiotics.\n"
                "🔹 Warm fluids + steam inhalation.\n"
                "🔹 Avoid smoking/polluted air."
            ),
            'Normal': (
                "💪 **Healthy Lung Tips:**\n"
                "Stay active, hydrated, and avoid dust/smoke."
            )
        },
        'skin': {
            'akiec': "☀️ Precancerous lesion. Dermatologist creams / cryotherapy recommended.",
            'bcc': "💊 Basal Cell Carcinoma. Needs dermatologist visit + possible removal.",
            'bkl': "🧴 Benign lesion. Removal optional.",
            'df': "🌿 Harmless. Surgery optional.",
            'mel': "⚠️ Dangerous melanoma. Urgent doctor visit required.",
            'nv': "💧 Normal mole. Monitor for changes.",
            'vasc': "🩸 Vascular lesion. Laser treatment may help."
        }
    },
    'hi': {
        'xray': {
            'Pneumonia': "🩺 निमोनिया: डॉक्टर से तुरंत मिलें, दवा लें, स्टीम लें।",
            'Normal': "💪 फेफड़े स्वस्थ: साफ हवा रखें और व्यायाम करें।"
        },
        'skin': {
            'akiec': "☀️ एक्टिनिक केराटोसिस: डॉक्टर उपचार आवश्यक।",
            'bcc': "💊 बेसल सेल कार्सिनोमा: सर्जरी सम्भव।",
            'bkl': "🧴 बेनाइन केराटोसिस: हानिरहित।",
            'df': "🌿 डर्माटोफाइब्रोमा: सामान्यतः सुरक्षित।",
            'mel': "⚠️ मेलैनोमा: तुरंत डॉक्टर को दिखाएं।",
            'nv': "💧 तिल: सामान्य, बदलाव पर डॉक्टर से मिलें।",
            'vasc': "🩸 वैस्कुलर लेशन: लेज़र उपचार सम्भव।"
        }
    },
    'ja': {
        'xray': {
            'Pneumonia': "🩺 肺炎：医師の診察が必要です。",
            'Normal': "💪 健康な肺：運動と清潔な空気を保つ。"
        },
        'skin': {
            'akiec': "☀️ 皮膚科で治療を受けてください。",
            'bcc': "💊 基底細胞がん：早期治療が必要。",
            'bkl': "🧴 良性病変：問題なし。",
            'df': "🌿 良性の線維腫。",
            'mel': "⚠️ メラノーマ：緊急検査が必要。",
            'nv': "💧 ほくろ：変化があれば病院へ。",
            'vasc': "🩸 血管病変：レーザー治療可能。"
        }
    }
}

# ------------------------------
# Routes
# ------------------------------
@app.route('/')
def home():
    return render_template('index.html', lang='en')

@app.route('/predict', methods=['POST'])
def predict():
    scan_type = request.form.get("scan_type", "xray")
    lang = request.form.get("lang", "en")

    if lang not in CURES:
        lang = "en"

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded!"})

    file = request.files['file']
    if file.filename == "":
        return jsonify({"error": "Empty filename!"})

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        img = image.load_img(file_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # --------------------------
        # X-RAY Prediction
        # --------------------------
        if scan_type == "xray":
            if xray_model is None:
                return jsonify({"error": "X-ray model not loaded!"})

            pred = xray_model.predict(img_array)[0][0]
            confidence = pred if pred > 0.5 else 1 - pred
            predicted_class = xray_labels[1] if pred > 0.5 else xray_labels[0]
            label_icon = "😷" if predicted_class == "Pneumonia" else "😊"
            color = "red" if predicted_class == "Pneumonia" else "green"
            cure = CURES[lang]['xray'].get(predicted_class)

        # --------------------------
        # SKIN Prediction
        # --------------------------
        elif scan_type == "skin":
            if skin_model is None:
                return jsonify({"error": "Skin model not loaded!"})

            preds = skin_model.predict(img_array)[0]
            class_idx = int(np.argmax(preds))
            confidence = float(np.max(preds))
            predicted_class = skin_labels[class_idx]
            label_icon = "🩺"
            color = "#38bdf8"
            cure = CURES[lang]['skin'].get(predicted_class)

        else:
            return jsonify({"error": "Invalid scan type!"})

        return render_template(
            "result.html",
            result=f"{predicted_class} {label_icon}",
            confidence=f"{confidence*100:.2f}%",
            color=color,
            image_file=filename,
            scan_type=scan_type,
            cure=cure
        )

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": f"Prediction failed: {e}"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
