# Deployment Guide

This guide explains how to deploy the TRM Modernization Tool to make it accessible online.

## Option 1: Deploy to Streamlit Sharing (Recommended)

Streamlit Sharing is a free hosting service provided by Streamlit that makes it easy to deploy Streamlit apps.

### Prerequisites

1. A GitHub account
2. A [Streamlit](https://streamlit.io/) account (you can sign up with your GitHub account)

### Steps

1. **Create a GitHub repository**

   - Push your code to a new GitHub repository
   - Ensure your repository includes all necessary files:
     - `app.py`
     - `classification.py`
     - `risk_assessment.py`
     - `data_processor.py`
     - `ui_components.py`
     - `utils.py`
     - `config.py`
     - `requirements.txt`
     - `data/` folder with your datasets

2. **Deploy on Streamlit Sharing**

   - Go to [Streamlit Sharing](https://share.streamlit.io/)
   - Log in with your GitHub account
   - Click "New app"
   - Select your GitHub repository, branch, and main file path (`app.py`)
   - Click "Deploy!"

3. **Add Secrets (for OpenAI API Key)**

   - In your Streamlit app settings, find the "Secrets" section
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY = "your_api_key_here"
     ```

4. **Update Your GitHub Pages Site**

   - In the `docs/index.html` file, update the URLs:
     - Replace `https://yourusername-trm-modernization-tool.streamlit.app` with your actual Streamlit app URL
     - Replace `https://github.com/yourusername/trm-modernization-tool` with your actual GitHub repository URL

5. **Enable GitHub Pages**

   - Go to your GitHub repository settings
   - Scroll down to "GitHub Pages" section
   - Select the "main" branch and "/docs" folder
   - Click "Save"
   - Your site will be available at `https://yourusername.github.io/trm-modernization-tool/`

## Option 2: Self-Hosting

For more control or if you need to host the application internally, you can deploy it on your own server.

### Using Docker

1. **Create a Dockerfile**

   Create a file named `Dockerfile` with the following content:

   ```
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py"]
   ```

2. **Build and Run the Docker Container**

   ```bash
   docker build -t trm-modernization-tool .
   docker run -p 8501:8501 -e OPENAI_API_KEY=your_api_key_here trm-modernization-tool
   ```

3. **Access the Application**

   The application will be available at `http://localhost:8501`

### Using a Cloud Provider

You can deploy your Docker container to any cloud provider that supports Docker, such as:

- AWS Elastic Container Service (ECS)
- Google Cloud Run
- Microsoft Azure Container Instances
- DigitalOcean App Platform

Follow your cloud provider's documentation for deploying Docker containers.

## Troubleshooting

If you encounter any deployment issues:

1. **Streamlit Version Issues**
   - Ensure your `requirements.txt` specifies compatible versions of all packages
   - Try using exact versions (e.g., `streamlit==1.44.1`) instead of ranges

2. **OpenAI API Key Issues**
   - Make sure your API key is correctly set in the Streamlit secrets
   - Check that your OpenAI account has sufficient credits

3. **Memory Issues**
   - If your app crashes due to memory limits, try optimizing your code or consider upgrading to a paid tier for more resources

4. **Import Errors**
   - Ensure all necessary dependencies are listed in your `requirements.txt`
   - Check that your file structure matches what's expected in the imports 