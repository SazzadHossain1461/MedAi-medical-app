#!/bin/bash

echo "======================================"
echo "Medical Prediction System Setup"
echo "======================================"

# Create necessary directories
echo "Creating directories..."
mkdir -p models logs datasets database

# Create Python virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo "======================================"
echo "Setup completed successfully!"
echo "======================================"
echo ""
echo "To activate the virtual environment, run:"
echo "source venv/bin/activate"
echo ""
echo "To train models, run:"
echo "python main.py train-all"
echo ""
echo "To start API server, run:"
echo "python main.py api"
echo ""
echo "To test API endpoints, run:"
echo "python test_api.py"