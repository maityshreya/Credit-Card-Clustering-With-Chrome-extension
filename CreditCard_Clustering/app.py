from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from typing import List, Dict
import uvicorn
import requests

app = FastAPI(title="Credit Card Clustering API",
             description="API for credit card customer segmentation using KMeans clustering")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Global variables to store our models and data
df = None
kmeans_model = None
scaler = None
imputer = None

class CustomerData(BaseModel):
    BALANCE: float
    PURCHASES: float
    CREDIT_LIMIT: float

class ClusterResponse(BaseModel):
    cluster_id: int
    cluster_description: str

@app.on_event("startup")
async def load_model():
    global df, kmeans_model, scaler, imputer
    try:
        # Load the data
        df = pd.read_csv('CC GENERAL.csv')
        
        # Initialize the models
        clustering_data = df[["BALANCE", "PURCHASES", "CREDIT_LIMIT"]]
        
        # Setup imputer
        imputer = SimpleImputer(strategy='mean')
        imputed_data = imputer.fit_transform(clustering_data)
        
        # Setup scaler
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(imputed_data)
        
        # Train KMeans
        kmeans_model = KMeans(n_clusters=5, random_state=42)
        kmeans_model.fit(scaled_data)
        
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        raise HTTPException(status_code=500, detail="Error loading model and data")

@app.get("/")
async def root():
    return {"message": "Credit Card Clustering API is running"}

@app.get("/cluster_info")
async def get_cluster_info():
    if kmeans_model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Get cluster centers and sizes
    cluster_centers = kmeans_model.cluster_centers_
    cluster_labels = kmeans_model.labels_
    
    cluster_info = {}
    for i in range(len(cluster_centers)):
        size = np.sum(cluster_labels == i)
        center = cluster_centers[i]
        cluster_info[f"Cluster {i}"] = {
            "size": int(size),
            "center_balance": float(center[0]),
            "center_purchases": float(center[1]),
            "center_credit_limit": float(center[2])
        }
    
    return cluster_info

@app.post("/predict_cluster")
async def predict_cluster(customer: CustomerData):
    if kmeans_model is None or scaler is None or imputer is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    try:
        # Prepare the data
        data = np.array([[customer.BALANCE, customer.PURCHASES, customer.CREDIT_LIMIT]])
        
        # Impute if there are any missing values
        data = imputer.transform(data)
        
        # Scale the data
        data = scaler.transform(data)
        
        # Predict cluster
        cluster = int(kmeans_model.predict(data)[0])
        
        # Get cluster description based on the center
        center = kmeans_model.cluster_centers_[cluster]
        if center[0] > 0.5 and center[1] > 0.5:
            description = "High Balance & High Purchase"
        elif center[0] > 0.5:
            description = "High Balance & Low Purchase"
        elif center[1] > 0.5:
            description = "Low Balance & High Purchase"
        else:
            description = "Low Balance & Low Purchase"
        
        return ClusterResponse(
            cluster_id=cluster,
            cluster_description=description
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/data_summary")
async def get_data_summary():
    if df is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    summary = {
        "total_customers": len(df),
        "average_balance": float(df["BALANCE"].mean()),
        "average_purchases": float(df["PURCHASES"].mean()),
        "average_credit_limit": float(df["CREDIT_LIMIT"].mean()),
        "missing_values": {
            "balance": int(df["BALANCE"].isnull().sum()),
            "purchases": int(df["PURCHASES"].isnull().sum()),
            "credit_limit": int(df["CREDIT_LIMIT"].isnull().sum())
        }
    }
    
    return summary

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True) 