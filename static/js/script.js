// =========================
// 🌍 Language System
// =========================
const translateBtn = document.getElementById("translateBtn");
const dropdown = document.getElementById("languageDropdown");
const langInput = document.getElementById("langInput");

if (translateBtn && dropdown) {
  translateBtn.addEventListener("click", () => dropdown.classList.toggle("hidden"));
}

// ---------- Dictionary ----------
const translations = {
  en: {
    title: "🩺 Healthinfo-AI",
    subtitle: "Your Smart Health Diagnosis Assistant 💉",
    uploadLabel: "📁 Upload X-ray or Skin Image",
    scanTypeLabel: "🔍 Select Scan Type",
    analyze: "Analyze",
    scanComplete: "✅ Scanning Complete – Data Processed Successfully",
    back: "← Back to Home",
    cureTitle: "🧾 Suggested Cure / Treatment",
    resultTitle: "🧬 Diagnosis Report",
    resultSubtitle: "Your Healthinfo-AI Scan Results",
    diseases: {
      Pneumonia: "Pneumonia",
      Normal: "Normal",
      akiec: "Actinic Keratoses",
      bcc: "Basal Cell Carcinoma",
      bkl: "Benign Keratosis",
      df: "Dermatofibroma",
      mel: "Melanoma",
      nv: "Melanocytic Nevus",
      vasc: "Vascular Lesion"
    },
    cures: {
      Pneumonia: "Consult a doctor, take rest, drink warm fluids, do steam inhalation, and avoid smoke.",
      Normal: "Healthy lungs! Keep exercising and avoid pollution.",
      akiec: "Use dermatologist-prescribed creams; avoid direct sunlight.",
      bcc: "Usually removed surgically; visit a dermatologist regularly.",
      bkl: "Harmless; keep skin moisturized.",
      df: "Benign; no treatment needed unless cosmetic.",
      mel: "Serious; urgent dermatologist check required.",
      nv: "Monitor moles for changes; avoid long sun exposure.",
      vasc: "Often fades naturally; laser therapy if needed."
    }
  },
  hi: {
    title: "🩺 हेल्थइन्फो-एआई",
    subtitle: "आपका स्मार्ट स्वास्थ्य सहायक 💉",
    uploadLabel: "📁 एक्स-रे या त्वचा की छवि अपलोड करें",
    scanTypeLabel: "🔍 स्कैन प्रकार चुनें",
    analyze: "विश्लेषण करें",
    scanComplete: "✅ स्कैन पूरा – डेटा सफलतापूर्वक प्रोसेस हुआ",
    back: "← होम पर जाएँ",
    cureTitle: "🧾 सुझाया गया इलाज / उपचार",
    resultTitle: "🧬 निदान रिपोर्ट",
    resultSubtitle: "आपके Healthinfo-AI स्कैन परिणाम",
    diseases: {
      Pneumonia: "निमोनिया",
      Normal: "सामान्य",
      akiec: "एक्टिनिक केराटोसिस",
      bcc: "बेसल सेल कार्सिनोमा",
      bkl: "बेनाइन केराटोसिस",
      df: "डर्माटोफाइब्रोमा",
      mel: "मेलानोमा",
      nv: "नेवस (मस्सा)",
      vasc: "वैस्कुलर लीजन"
    },
    cures: {
      Pneumonia: "डॉक्टर से मिलें, आराम करें, गरम तरल पदार्थ लें और प्रदूषण से दूर रहें।",
      Normal: "फेफड़े स्वस्थ हैं! व्यायाम करें और स्वच्छ हवा में रहें।",
      akiec: "डॉक्टर द्वारा सुझाई गई क्रीम लगाएँ और धूप से बचें।",
      bcc: "सर्जरी द्वारा हटाया जा सकता है; नियमित त्वचा जाँच करवाएँ।",
      bkl: "हानिरहित; त्वचा को नम रखें।",
      df: "आम तौर पर इलाज की आवश्यकता नहीं।",
      mel: "गंभीर स्थिति; तुरंत त्वचा विशेषज्ञ से मिलें।",
      nv: "यदि मस्से का रंग या आकार बदले तो डॉक्टर से मिलें।",
      vasc: "अक्सर अपने-आप ठीक हो जाता है; लेज़र उपचार सहायक।"
    }
  },
  ja: {
    title: "🩺 ヘルスインフォAI",
    subtitle: "あなたのスマート健康診断アシスタント 💉",
    uploadLabel: "📁 X線または皮膚の画像をアップロード",
    scanTypeLabel: "🔍 スキャンタイプを選択",
    analyze: "分析する",
    scanComplete: "✅ スキャン完了 – データが正常に処理されました",
    back: "← ホームに戻る",
    cureTitle: "🧾 推奨される治療 / 処置",
    resultTitle: "🧬 診断レポート",
    resultSubtitle: "Healthinfo-AIのスキャン結果",
    diseases: {
      Pneumonia: "肺炎",
      Normal: "正常",
      akiec: "日光角化症",
      bcc: "基底細胞がん",
      bkl: "良性角化症",
      df: "皮膚線維腫",
      mel: "メラノーマ",
      nv: "母斑",
      vasc: "血管性病変"
    },
    cures: {
      Pneumonia: "医師の診察を受け、十分な休息と水分補給を行い、蒸気吸入を試みてください。喫煙や汚染された空気を避けましょう。",
      Normal: "肺は健康です！ 適度な運動をし、清潔な空気を吸いましょう。",
      akiec: "皮膚科で処方された外用薬を使用し、紫外線を避けましょう。",
      bcc: "多くの場合、手術で除去されます。早期発見・早期治療が重要です。",
      bkl: "無害な皮膚変化です。保湿し、気になる場合は医師に相談してください。",
      df: "通常は治療不要ですが、見た目が気になる場合は切除可能です。",
      mel: "悪性腫瘍の可能性があります。できるだけ早く皮膚科を受診してください。",
      nv: "母斑（ホクロ）は通常無害ですが、変化があれば医師へ相談を。",
      vasc: "多くは自然に薄くなります。必要に応じてレーザー治療が有効です。"
    }
  }
};

// ---------- Apply Translation ----------
function applyTranslation(lang) {
  const t = translations[lang];
  if (!t) return;

  // Generic labels
  const title = document.querySelector(".title");
  const subtitle = document.querySelector(".subtitle");
  const uploadLabel = document.querySelector(".upload-label");
  const scanTypeLabel = document.querySelector(".scan-type-label");
  const analyzeBtn = document.querySelector(".analyze-btn");
  const backBtn = document.querySelector(".back-btn");
  const cureTitle = document.querySelector(".cure-box h3");
  const scanComplete = document.querySelector(".scan-complete");

  if (title) title.textContent = t.title;
  if (subtitle) subtitle.textContent = t.subtitle;
  if (uploadLabel) uploadLabel.textContent = t.uploadLabel;
  if (scanTypeLabel) scanTypeLabel.textContent = t.scanTypeLabel;
  if (analyzeBtn) analyzeBtn.textContent = t.analyze;
  if (backBtn) backBtn.textContent = t.back;
  if (cureTitle) cureTitle.textContent = t.cureTitle;
  if (scanComplete) scanComplete.textContent = t.scanComplete;

  // --- Translate disease + cure ---
  const diagBox = document.querySelector(".diagnosis-text");
  const cureText = document.querySelector(".cure-box p");
  if (diagBox && cureText) {
    const diseaseKey = diagBox.dataset.disease;
    const translatedDisease = t.diseases[diseaseKey] || diseaseKey;
    const translatedCure = t.cures[diseaseKey] || cureText.textContent;

    const span = diagBox.querySelector("span");
    if (span) span.textContent = translatedDisease;
    cureText.textContent = translatedCure;
  }
}

// ---------- Language Setter ----------
function setLanguage(lang) {
  dropdown.classList.add("hidden");
  translateBtn.innerText =
    lang === "en" ? "🌍 English" :
    lang === "hi" ? "🌍 हिन्दी" :
    lang === "ja" ? "🌍 日本語" : "🌍 English";

  localStorage.setItem("selectedLanguage", lang);
  if (langInput) langInput.value = lang;
  applyTranslation(lang);
}

// ---------- Initialize ----------
window.addEventListener("load", () => {
  const savedLang = localStorage.getItem("selectedLanguage") || "en";
  if (langInput) langInput.value = savedLang;
  setLanguage(savedLang);
});

// ---------- Scanning Overlay ----------
const uploadForm = document.querySelector(".upload-form");
function createLoadingOverlay() {
  if (document.querySelector(".loading-overlay")) return;
  const overlay = document.createElement("div");
  overlay.className = "loading-overlay";
  overlay.innerHTML = `
    <div class="scanner-box"><div class="scanner-line"></div></div>
    <h2>🔍 Scanning in Progress...</h2>`;
  document.body.appendChild(overlay);
}
if (uploadForm) {
  uploadForm.addEventListener("submit", () => {
    const selectedLang = localStorage.getItem("selectedLanguage") || "en";
    if (langInput) langInput.value = selectedLang;
    createLoadingOverlay();
  });
}

// ---------- Back button fade ----------
const backBtn = document.querySelector(".back-btn");
if (backBtn) {
  backBtn.addEventListener("click", (e) => {
    e.preventDefault();
    document.body.style.opacity = "0";
    setTimeout(() => (window.location.href = "/"), 300);
  });
}
