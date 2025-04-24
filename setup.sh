#!/bin/bash

# TRM Modernization Tool Setup Script

echo "Setting up TRM Modernization Tool..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "Activating virtual environment (Windows)..."
    source venv/Scripts/activate
else
    # Unix/macOS
    echo "Activating virtual environment (Unix/macOS)..."
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "# Add your OpenAI API key here for LLM-based classification" > .env
    echo "# OPENAI_API_KEY=your_api_key_here" >> .env
    echo "# OPENAI_MODEL=gpt-3.5-turbo" >> .env
    echo "# OPENAI_TEMPERATURE=0" >> .env
fi

echo "Setup complete! You can now run the application with:"
echo ""
echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "  streamlit run app.py"
echo ""
echo "The application will be available at http://localhost:8501" 