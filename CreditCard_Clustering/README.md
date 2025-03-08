# Credit Card Customer Segmentation Project

This project implements a machine learning system that segments credit card customers into distinct clusters based on their spending behavior and credit characteristics. It includes a FastAPI backend service and a Chrome extension for easy interaction with the clustering model.

## Project Structure

```
credit-card-clustering/
├── app.py                 # FastAPI application
├── requirements.txt       # Python dependencies
├── CC GENERAL.csv        # Dataset file
├── README.md             # This file
└── extension/            # Chrome extension files
    ├── manifest.json
    ├── popup.html
    ├── popup.js
    └── images/
        ├── icon16.png
        ├── icon48.png
        └── icon128.png
```

## Features

- Customer segmentation using K-means clustering
- RESTful API endpoints for:
  - Predicting customer segments
  - Getting cluster information
  - Retrieving data summaries
- Chrome extension for easy interaction with the API
- Automatic handling of missing values
- Data standardization
- CORS support for cross-origin requests

## Installation

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>(e.g. https://github.com/maityshreya/Credit-Card-Clustering-With-Chrome-extension)
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Chrome Extension Setup

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked"
4. Select the `extension` folder from the project directory

## Usage

### Starting the Backend Server

1. Make sure you have the dataset file `CC GENERAL.csv` in the project root directory
2. Run the FastAPI server:
```bash
python app.py
```
3. The server will start at `http://127.0.0.1:8000`
4. Access the API documentation at `http://127.0.0.1:8000/docs`

### API Endpoints

- `GET /`: Check if the API is running
- `GET /cluster_info`: Get information about all clusters
- `POST /predict_cluster`: Predict cluster for new customer data
- `GET /data_summary`: Get summary statistics of the dataset

### Using the Chrome Extension

1. Click the extension icon in Chrome's toolbar
2. Enter customer data:
   - Balance
   - Purchases
   - Credit Limit
3. Click "Predict Cluster"
4. View the prediction result and cluster description

### Example API Usage

```python
import requests

# Predict cluster for a customer
response = requests.post(
    "http://127.0.0.1:8000/predict_cluster",
    json={
        "BALANCE": 1000.0,
        "PURCHASES": 500.0,
        "CREDIT_LIMIT": 2000.0
    }
)
print(response.json())
```

## Technical Details

### Machine Learning Pipeline

1. Data Preprocessing:
   - Missing value imputation using mean strategy
   - Feature standardization using StandardScaler

2. Clustering:
   - Algorithm: K-means
   - Number of clusters: 5
   - Features used:
     - Balance
     - Purchases
     - Credit Limit

### API Implementation

- Framework: FastAPI
- CORS enabled for cross-origin requests
- Pydantic models for request/response validation
- Automatic API documentation with Swagger UI

## Requirements

- Python 3.7+
- FastAPI
- pandas
- scikit-learn
- numpy
- uvicorn
- Google Chrome (for extension)

## Error Handling

The application includes comprehensive error handling for:
- Missing data
- Invalid input values
- Server connection issues
- API request failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Dataset source: [Add source information]
- FastAPI framework
- scikit-learn library 
