#!/bin/bash
set -e

echo "📥 Creating model directory..."
mkdir -p model

echo "⬇️ Downloading X-Ray model..."
curl -L "https://drive.google.com/uc?export=download&id=1wPLKWgWPA5sXBaeKSXJrugnfH-ZVCCfb" -o model/xray_model.keras

echo "⬇️ Downloading Skin model..."
curl -L "https://drive.google.com/uc?export=download&id=1ew3WsO2vYLZypI_rhGuvwRRIWMH9t5ug" -o model/skin_model_final.keras

echo "✅ All models downloaded successfully!"
