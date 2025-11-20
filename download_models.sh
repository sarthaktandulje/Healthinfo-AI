#!/bin/bash

echo "⬇️ Downloading REAL MODEL FILES..."

mkdir -p model

curl -L "https://drive.google.com/uc?export=download&id=1DtShDIR56OC0miur1lGTupjeBCPmqZ" -o model/xray_model.keras
curl -L "https://drive.google.com/uc?export=download&id=1ew3WsO2vYLZypI_rhGuvwRRIWMH9t5ug" -o model/skin_model_final.keras

echo "✅ Models downloaded successfully!"
