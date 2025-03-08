# Credit-Card-Clustering-With-Chrome-extension
# Project Overview
  This is a machine learning project that uses credit card customer data to segment customers into meaningful groups. The project combines:
1. Data Science (clustering algorithm)
2. Backend API (FastAPI)
3. Frontend Interface (Chrome Extension)


# Key Features Of The Project
Machine Learning Features
Clustering Algorithm: K-means with 5 clusters
Data Preprocessing:Automatic missing value handling using mean imputation
Feature standardization for better clustering
Features Used:
  1. Balance
  2. Purchase
  3. Credit Limit
   
 #  API Features
 1. RESTful Endpoints:
  - GET  /               # Health check
  - GET  /cluster_info       # Cluster statistics
  - POST /predict_cluster    # New predictions
  - GET  /data_summary      # Dataset statistics
 2. CORS Support: Enables cross-origin requests
 3. Error Handling: Comprehensive error management
 4. Data Validation: Using Pydantic models

# Chrome Extension Features
- User-friendly interface
- Real-time predictions
- Error feedback
- Visual result display
