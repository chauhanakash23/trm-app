# TRM Modernization Tool

A tool for classifying software products into Technical Reference Model (TRM) domains and subdomains, assessing risk factors, and providing visualization tools for analysis.

## Features

- **Software Classification**: Classify software products into TRM domains and subdomains using either rule-based or LLM-based methods
- **Risk Assessment**: Automatically assess risk levels based on lifecycle status, vendor information, and classification
- **Data Visualization**: View classification results and risk metrics through interactive dashboards
- **CSV File Upload**: Upload your own software inventory for classification
- **Export Options**: Export classification results as CSV or JSON

## Demo

![TRM Modernization Tool Demo](docs/demo.gif)

## GCP Deployment Instructions

### Prerequisites

1. Have a Google Cloud account
2. Enable billing for your GCP project
3. Install Google Cloud SDK (not required for web console deployment)

### Deployment Steps Using GCP Web Console

1. **Sign in to Google Cloud Console**
   - Go to [https://console.cloud.google.com/](https://console.cloud.google.com/)
   - Sign in with your Google account

2. **Create a new project (if needed)**
   - Click on the project selector at the top of the page
   - Click on "New Project"
   - Enter a project name and select a billing account
   - Click "Create"

3. **Enable APIs**
   - Go to "APIs & Services" > "Library"
   - Search for "App Engine Admin API" and enable it
   - Search for "Cloud Build API" and enable it

4. **Deploy to App Engine**
   - Go to "App Engine" in the left navigation
   - Click "Create Application"
   - Select a region close to your target users
   - Select "Python" as the language
   - Click "Next"
   - Select "Standard" environment
   - Click "Next"

5. **Upload and Deploy Your Code**
   - In the App Engine dashboard, click "Deploy"
   - Click "Browse" and select this project folder as a ZIP file
   - Alternatively, you can use Cloud Shell to deploy directly from GitHub
   
6. **Monitor Deployment**
   - Wait for the deployment to complete
   - You can monitor the progress in the "Versions" page

7. **Access Your App**
   - Once deployed, your app will be available at:
     `https://[PROJECT_ID].appspot.com`

8. **Set Up Custom Domain (Optional)**
   - Go to "Settings" in App Engine
   - Click on "Custom Domains"
   - Follow the instructions to map your domain

### Environment Variables

You may need to set the following environment variables in the App Engine console:

- `OPENAI_API_KEY`: Your OpenAI API key (if using GPT for classification)

## Local Development

1. Create a virtual environment: `python -m venv trm_env`
2. Activate it: `source trm_env/bin/activate` (Unix) or `trm_env\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `streamlit run app.py`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/trm-modernization-tool.git
cd trm-modernization-tool
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. (Optional) Set up OpenAI API key for LLM-based classification:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Upload a CSV file with the following columns:
   - Product Name
   - Description
   - Category Hint
   - Vendor
   - Lifecycle Status

4. Choose a classification method:
   - Rule-based: Uses keyword matching (faster, less accurate)
   - LLM-based: Uses AI to understand context (slower, more accurate)

5. Click "Run Classification" to process the data

6. View the results in the dashboard and explore using the filters

## Try It Online

For a quick demo, you can try the application online using Streamlit Sharing:

[Open TRM Modernization Tool Demo](https://yourusername-trm-modernization-tool.streamlit.app)

## Project Structure

- `app.py`: Main application entry point
- `classification.py`: Classification logic (rule-based and LLM-based)
- `risk_assessment.py`: Risk assessment logic
- `data_processor.py`: Data loading and processing functions
- `ui_components.py`: UI rendering functions
- `utils.py`: Utility functions
- `config.py`: Application configuration
- `data/`: Sample datasets
  - `software_list.csv`: Default dataset
  - `complex_software_list.csv`: More complex dataset to test LLM vs rule-based classification

## Development

### Testing Different Classification Methods

The repository includes two datasets for testing:
- `data/software_list.csv`: Basic dataset with clear keywords
- `data/complex_software_list.csv`: More ambiguous descriptions that benefit from LLM classification

To test these different datasets:
1. Rename the dataset you want to use to `software_list.csv`
2. Run the application and use the "Use default dataset" option

### Adding Custom Domains

To add custom TRM domains and subdomains, edit the `config.py` file:

```python
TRM_DOMAINS_SUBDOMAINS = {
    "Your New Domain": ["Subdomain 1", "Subdomain 2"],
    # ...existing domains...
}

CLASSIFICATION_KEYWORDS = {
    "Your New Domain": ["keyword1", "keyword2", "keyword3"],
    # ...existing keywords...
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [OpenAI](https://openai.com/) API for LLM-based classification