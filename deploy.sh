#!/bin/bash

# Vaultify Deployment Script
echo "🚀 Vaultify Deployment Script"
echo "=============================="

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 1 ]]; then
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Python $python_version is too old. Please use Python 3.8+"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: No .env file found"
    echo "📝 Creating .env template..."
    cat > .env << EOF
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/vaultify

# Encryption Key (generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
ENCRYPTION_KEY=your-encryption-key-here

# Environment
ENVIRONMENT=development
EOF
    echo "✅ Created .env template. Please update it with your actual values."
fi

# Test the application
echo "🧪 Testing application..."
python -c "
from app.main import app
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.get('/health')
print(f'Health check status: {response.status_code}')
if response.status_code == 200:
    print('✅ Application is working correctly!')
else:
    print('❌ Application has issues')
"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run locally:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "To deploy to Render:"
echo "  1. Push your code to GitHub"
echo "  2. Follow the instructions in DEPLOYMENT.md"
echo ""
echo "Happy coding! 🚀" 