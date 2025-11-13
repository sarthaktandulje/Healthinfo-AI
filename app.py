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
MODEL_XRAY_PATH = "xray_model.keras"
MODEL_SKIN_PATH = "model/skin_model_final.keras"
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
# Cure translations (EN / HI / JA)
# ------------------------------
CURES = {
    'en': {
        'xray': {
            'Pneumonia': (
                "🩺 **Recommended Care for Pneumonia:**\n\n"
                "🔹 **Medical Treatment:**\n"
                "   - Visit a pulmonologist or physician immediately.\n"
                "   - Take prescribed antibiotics or antivirals (as per doctor’s diagnosis — bacterial or viral pneumonia differ).\n"
                "   - In some cases, hospitalization may be required for oxygen therapy.\n\n"
                "🔹 **Home Remedies & Supportive Care:**\n"
                "   - Get plenty of rest — avoid overexertion.\n"
                "   - Drink warm fluids to loosen mucus.\n"
                "   - Steam inhalation can help clear airways.\n"
                "   - Avoid smoking or polluted air.\n"
                "   - Maintain proper nutrition — vitamin C, zinc, and protein-rich foods aid recovery.\n\n"
                "🔹 **Prevention:**\n"
                "   - Get vaccinated against influenza and pneumococcal infections.\n"
                "   - Wash hands regularly and avoid close contact with sick people."
            ),
            'Normal': (
                "💪 **Healthy Lung Tips:**\n\n"
                "✅ Maintain clean air in your environment.\n"
                "✅ Stay active — light cardio and breathing exercises boost lung capacity.\n"
                "✅ Keep hydrated and avoid dust/smoke.\n"
                "✅ Get routine health check-ups once every 6–12 months."
            )
        },
        'skin': {
            'akiec': (
                "☀️ **Actinic Keratoses (Precancerous Lesion):**\n\n"
                "🔹 **Treatment:**\n"
                "   - Topical creams like 5-fluorouracil or imiquimod prescribed by a dermatologist.\n"
                "   - Cryotherapy (freezing) may be done to remove lesions.\n"
                "   - Laser therapy or photodynamic therapy for multiple lesions.\n\n"
                "🔹 **Lifestyle:**\n"
                "   - Avoid direct sunlight; use SPF 50+ sunscreen and protective clothing.\n"
                "   - Regular dermatological checkups are essential."
            ),
            'bcc': (
                "💊 **Basal Cell Carcinoma (Skin Cancer):**\n\n"
                "🔹 **Treatment:**\n"
                "   - Surgical excision is the primary treatment (high cure rates when treated early).\n"
                "   - Non-surgical options: radiation, topical immunotherapy for specific cases.\n\n"
                "🔹 **Follow-up:**\n"
                "   - Regular monitoring to prevent recurrence and early detection of new lesions."
            ),
            'bkl': (
                "🧴 **Benign Keratosis (Non-cancerous):**\n\n"
                "🔹 **Treatment:**\n"
                "   - Usually harmless; removal is cosmetic.\n"
                "   - Cryotherapy or laser removal if symptomatic or cosmetically unwanted.\n\n"
                "🔹 **Skin Care:**\n"
                "   - Regular moisturizing and avoid picking at lesions."
            ),
            'df': (
                "🌿 **Dermatofibroma:**\n\n"
                "🔹 **Treatment:**\n"
                "   - Usually no treatment required — benign.\n"
                "   - Surgical excision if irritating or for cosmetic reasons.\n\n"
                "🔹 **Advice:**\n"
                "   - Avoid friction and keep area moisturized."
            ),
            'mel': (
                "⚠️ **Melanoma (Serious Skin Cancer):**\n\n"
                "🔹 **Treatment:**\n"
                "   - Urgent dermatologist visit and biopsy.\n"
                "   - Early stage: surgical removal with margins.\n"
                "   - Advanced: immunotherapy, targeted therapy, or chemotherapy may be needed.\n\n"
                "🔹 **Prevention:**\n"
                "   - Regular skin checks, ABCDE monitoring for moles, and strict sun protection."
            ),
            'nv': (
                "💧 **Melanocytic Nevus (Mole):**\n\n"
                "🔹 **Treatment:**\n"
                "   - Usually benign — observe for changes.\n"
                "   - If it changes shape/color/bleeds, consult a dermatologist immediately.\n\n"
                "🔹 **Advice:**\n"
                "   - Avoid prolonged sun exposure and monitor regularly."
            ),
            'vasc': (
                "🩸 **Vascular Lesions (e.g., Hemangioma):**\n\n"
                "🔹 **Treatment:**\n"
                "   - Many fade spontaneously; laser therapy reduces redness.\n"
                "   - Surgical removal if persistent or symptomatic.\n\n"
                "🔹 **Care:**\n"
                "   - Avoid trauma and keep area clean."
            )
        }
    },
    # ------------------------------
    # Hindi Translations (concise but meaningful)
    # ------------------------------
    'hi': {
        'xray': {
            'Pneumonia': (
                "🩺 **निमोनिया के लिए सुझाव:**\n\n"
                "🔹 **चिकित्सकीय उपचार:**\n"
                "   - तुरंत डॉक्टर से संपर्क करें।\n"
                "   - डॉक्टर द्वारा निर्धारित एंटीबायोटिक/एंटिवायरल लें (बैक्टीरियल वाइरल अलग होते हैं)।\n"
                "   - ज़रूरत पड़ने पर ऑक्सीजन या अस्पतालीन देखभाल आवश्यक हो सकती है।\n\n"
                "🔹 **घर पर देखभाल:**\n"
                "   - पूरा आराम करें और अधिक मेहनत से बचें।\n"
                "   - गरम तरल पदार्थ पिएं और स्टीम लें।\n"
                "   - धूम्रपान और प्रदूषित हवा से बचें。\n"
            ),
            'Normal': (
                "💪 **स्वस्थ फेफड़े के सुझाव:**\n\n"
                "✅ स्वच्छ वायु रखें, हल्का व्यायाम और साँसों के अभ्यास करें, पानी पिएं।"
            )
        },
        'skin': {
            'akiec': "☀️ **एक्टिनिक केराटोसिस:** डॉक्टर द्वारा क्रीम या क्रायोथेरेपी; धूप से बचें और एसपीएफ लगाएं।",
            'bcc': "💊 **बेसल सेल कार्सिनोमा:** आमतौर पर सर्जिकल हटाना आवश्यक; जल्द निदान जरूरी।",
            'bkl': "🧴 **बेनाइन केराटोसिस:** सामान्यतः हानिरहित; मॉइस्चराइज़ और जरूरत पर हटवाया जा सकता है।",
            'df': "🌿 **डर्माटोफाइब्रोमा:** आमतौर पर उपचार नहीं चाहिए; कॉस्मेटिक कारणों से हटवाया जा सकता है।",
            'mel': "⚠️ **मेलैनोमा:** तुरंत त्वचा विशेषज्ञ से मिलें; बायोप्सी और जल्दी सर्जिकल हटाना जरूरी हो सकता है।",
            'nv': "💧 **नैवस (मोल):** बदलने पर डॉक्टर को दिखाएं; आमतौर पर निगरानी पर्याप्त।",
            'vasc': "🩸 **वैस्कुलर Lesion:** अक्सर लेज़र थेरेपी से सुधरता है; चोट से बचें।"
        }
    },
    # ------------------------------
    # Japanese Translations (concise)
    # ------------------------------
    'ja': {
        'xray': {
            'Pneumonia': (
                "🩺 **肺炎の推奨ケア:**\n\n"
                "🔹 **医療的処置:**\n"
                "   - すぐに医師（呼吸器内科）を受診してください。\n"
                "   - 医師の診断に応じた抗生物質や抗ウイルス薬を服用。\n"
                "   - 必要なら酸素療法や入院が必要になることがあります。\n\n"
                "🔹 **自宅でのケア:**\n"
                "   - 十分な休息をとる。\n"
                "   - 温かい飲み物を摂り、蒸気吸入が有効。\n"
                "   - 喫煙や汚れた空気を避ける。"
            ),
            'Normal': (
                "💪 **肺の健康アドバイス:**\n\n"
                "✅ 定期的な運動と呼吸エクササイズ、清潔な空気を保つこと。"
            )
        },
        'skin': {
            'akiec': "☀️ **日光角化症（前癌病変）:** 皮膚科で外用薬や凍結療法。日焼け対策を徹底してください。",
            'bcc': "💊 **基底細胞がん:** 早期なら手術での切除が主な治療です。皮膚科受診を。",
            'bkl': "🧴 **良性角化症:** 基本的に害は少なく、必要なら除去可能です。",
            'df': "🌿 **皮膚線維腫:** 通常治療不要。美容目的で手術的除去可能。",
            'mel': "⚠️ **メラノーマ（悪性）:** 緊急の皮膚科受診、生検と早期切除が重要です。",
            'nv': "💧 **母斑（ホクロ）:** 変化があれば専門医へ。通常は経過観察でOK。",
            'vasc': "🩸 **血管性病変:** 多くは自然軽快、レーザー治療が有効。"
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
        # preprocess
        img = image.load_img(file_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        if scan_type == "xray":
            if xray_model is None:
                return jsonify({"error": "X-ray model not loaded!"})
            pred = xray_model.predict(img_array)[0][0]
            confidence = pred if pred > 0.5 else 1 - pred
            predicted_class = xray_labels[1] if pred > 0.5 else xray_labels[0]
            label_icon = "😷" if predicted_class == "Pneumonia" else "😊"
            color = "red" if predicted_class == "Pneumonia" else "green"
            cure = CURES[lang]['xray'].get(predicted_class, CURES[lang]['xray'].get('Normal'))

        elif scan_type == "skin":
            if skin_model is None:
                return jsonify({"error": "Skin model not loaded!"})
            preds = skin_model.predict(img_array)[0]
            class_idx = int(np.argmax(preds))
            confidence = float(np.max(preds))
            predicted_class = skin_labels[class_idx]
            label_icon = "🩺"
            color = "#38bdf8"
            cure = CURES[lang]['skin'].get(predicted_class, "Consult a dermatologist for a detailed diagnosis.")

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
    app.run
