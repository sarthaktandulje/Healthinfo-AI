// =========================
// 🌍 Language System
// =========================
const translateBtn = document.getElementById("translateBtn");
const dropdown = document.getElementById("languageDropdown");
const langInput = document.getElementById("langInput");

// Toggle language dropdown
if (translateBtn && dropdown) {
  translateBtn.addEventListener("click", () => dropdown.classList.toggle("hidden"));
}

// Close dropdown when clicking outside
document.addEventListener("click", (e) => {
  if (dropdown && !dropdown.contains(e.target) && e.target !== translateBtn) {
    dropdown.classList.add("hidden");
  }
});

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
    loading: "🔍 Scanning in Progress...",
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
    loading: "🔍 स्कैन जारी है...",
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
    loading: "🔍 スキャン中...",
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
      Pneumonia: "医師の診察を受け、十分な休息と水分補給を行いましょう。",
      Normal: "肺は健康です！ 適度な運動をし、清潔な空気を吸いましょう。",
      akiec: "皮膚科で処方された外用薬を使用し、紫外線を避けてください。",
      bcc: "多くの場合、手術で除去されます。",
      bkl: "無害な皮膚変化です。保湿を心掛けてください。",
      df: "治療は不要ですが、気になる場合は除去可能です。",
      mel: "悪性腫瘍の可能性があります。早急に検査を受けてください。",
      nv: "通常無害ですが、変化があれば医師の診察を。",
      vasc: "自然に薄くなる場合があります。必要ならレーザー治療が有効です。"
    }
  }
};

// Apply translation to elements
function applyTranslation(lang) {
  const t = translations[lang];
  if (!t) return;

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

  // Translate diagnosis + cure on result page
  const diagBox = document.querySelector(".diagnosis-text");
  const cureText = document.querySelector(".cure-box p");

  if (diagBox && cureText) {
    const disease = diagBox.dataset.disease;
    const translatedDisease = t.diseases[disease] || disease;
    const translatedCure = t.cures[disease] || cureText.textContent;

    const span = diagBox.querySelector("span");
    if (span) span.textContent = translatedDisease;
    cureText.textContent = translatedCure;
  }
}

// Set language manually
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

// Initialize language on page load
window.addEventListener("load", () => {
  const savedLang = localStorage.getItem("selectedLanguage") || "en";
  if (langInput) langInput.value = savedLang;
  setLanguage(savedLang);
});

// =========================
// 🔄 Scanning Overlay
// =========================
const uploadForm = document.querySelector(".upload-form");

function createLoadingOverlay() {
  if (document.querySelector(".loading-overlay")) return;

  const overlay = document.createElement("div");
  overlay.className = "loading-overlay";

  const selectedLang = localStorage.getItem("selectedLanguage") || "en";

  overlay.innerHTML = `
    <div class="scanner-box"><div class="scanner-line"></div></div>
    <h2 id="loadingText">${translations[selectedLang].loading}</h2>
  `;

  document.body.appendChild(overlay);
}

if (uploadForm) {
  uploadForm.addEventListener("submit", (e) => {
    const fileInput = document.querySelector("input[type='file']");
    const selectedLang = localStorage.getItem("selectedLanguage") || "en";

    // File validation
    if (!fileInput.files.length) {
      e.preventDefault();
      alert("⚠️ Please upload an image first!");
      return;
    }

    // Prevent double submission
    uploadForm.querySelector("button[type='submit']").disabled = true;

    if (langInput) langInput.value = selectedLang;

    createLoadingOverlay();
  });
}

// =========================
// ↩️ Back button smooth fade
// =========================
const backBtnFade = document.querySelector(".back-btn");

if (backBtnFade) {
  backBtnFade.addEventListener("click", (e) => {
    e.preventDefault();

    document.body.style.transition = "opacity 0.5s ease";
    document.body.style.opacity = 0;

    setTimeout(() => {
      window.location.href = "/";
    }, 450);
  });
}
