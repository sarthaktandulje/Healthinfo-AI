#!/bin/bash

set -e

echo "📥 Creating model directory..."
mkdir -p model

echo "⬇️ Downloading X-Ray model..."
wget -O model/xray_model.keras "https://drive.google.com/uc?export=download&id=1wPLKWgWPA5sXBaeKSXJrugnfH-ZVCCfb"

echo "⬇️ Downloading Skin model..."
wget -O model/skin_model_final.keras "https://drive.google.com/uc?export=download&id=1ew3WsO2vYLZypI_rhGuvwRRIWMH9t5ug"

echo "✅ All models downloaded successfully!"
