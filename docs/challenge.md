
## Metric Formula Correction

Initially, the formula for calculating a specific metric in the notebook was incorrect. It was corrected to reflect a more accurate calculation. This was crucial for properly evaluating the model's effectiveness.

## Model Selection

After reviewing various candidate models, the XGBoost model with class balancing and feature selection was chosen. The justification for this selection was based on a trade-off between the model's performance and generalization. This particular model showed solid metrics during testing and validation.

## Features of api.py

Health Endpoint
A health endpoint (/health) was implemented for quickly checking the API's status.

# Prediction Endpoint

A prediction endpoint (/predict) was implemented that uses the chosen model to make predictions based on real-time data sent.

# Model Trained Verification

Before making any predictions, the API checks whether the model has been trained. If not, it returns an HTTP 400 error with the message "Model not trained".