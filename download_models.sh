#!/bin/bash

echo "⬇️ Downloading REAL MODEL FILES..."

mkdir -p model

curl -L -o model/xray_model.keras "https://drive.google.com/uc?export=download&id=YOUR_XRAY_FILE_ID"
curl -L -o model/skin_model_final.keras "https://drive.google.com/uc?export=download&id=YOUR_SKIN_FILE_ID"

echo "✅ Models downloaded successfully!"
