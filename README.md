# TRM Modernization Tool

A tool for classifying software products into Technical Reference Model (TRM) domains and subdomains, assessing risk factors, and providing visualization tools for analysis.

## Features

- **Software Classification**: Classify software products into TRM domains and subdomains using either rule-based or LLM-based methods
- **Risk Assessment**: Automatically assess risk levels based on lifecycle status, vendor information, and classification
- **Data Visualization**: View classification results and risk metrics through interactive dashboards
- **CSV File Upload**: Upload your own software inventory for classification
- **Export Options**: Export classification results as CSV or JSON


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

https://trm-modernization-app.el.r.appspot.com/

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


### Testing Different Classification Methods

The repository includes two datasets for testing:
- `data/software_list.csv`: Basic dataset with clear keywords
- `data/complex_software_list.csv`: More ambiguous descriptions that benefit from LLM classification


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [OpenAI](https://openai.com/) API for LLM-based classification
