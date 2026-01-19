#!/usr/bin/env bash
set -e

echo "🔧 Setting up environment..."
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install --with-deps

echo "✅ Setup complete."
echo "🚀 Starting dashboard at port 8000..."
uvicorn webui.app:app --host 0.0.0.0 --port 8000
