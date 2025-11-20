#!/bin/bash

echo "⬇️ Downloading REAL MODEL FILES..."

mkdir -p model

curl -L -o model/xray_model.keras "https://drive.google.com/uc?export=download&id=1wPLKWgWPA5sXBaeKSXJrugnfH-ZVCCfb"
curl -L -o model/skin_model_final.keras "https://drive.google.com/uc?export=download&id=1ew3WsO2vYLZypI_rhGuvwRRIWMH9t5ug"

echo "✅ Models downloaded successfully!"
