# Churn
Churn Prediction
About 
The product is a Streamlit based web app that looks like the below given snapshot. The Purpose of this application is to run the process automatically on every Friday but at the same time also give the Product Managers the access to a Web Based UI to rerun and check the model results using a UI.
Folder Structure 
I am attaching the folder structure as a screenshot. The following folder structure decides the complete Project.

OVERVIEW
All the Python based files are placed in the “./src “ location. The UI is triggered using the “./src/app.py” file.
The command needed to run this is based out of Streamlit.
Terminal - CLI —-> streamlit run .src/app.py
The above command triggers the application.
PROCESS FLOW WITH UI:

The LEFT Bar has all the options:
Train : Train gives us the ability to train the model again with the existing data in the data folders.
Predict : Predict gives the ability to predict on the existing data in the data folders.
Fetch Data: This gives us the ability to fetch and save the data for train as well as the predict datasets. The same gets saved in the data folder by replacing the existing data. This function is used to update the train and predict dataset and then we can use the Train and Predict buttons to run the model on the new dataset.
Model Comparison: This gives the model comparative analysis for all the different possible models.
Confusion Matrix: This gives the model confusion matrix for the best possible model.
SHAP Values: This gives the SHAP values chart.
Dashboard: This gives out the Shapash Dash Monitor.

DATA PULL:
The data pull that we are doing is all from the redshift tables.
Will need access to create tables in the Redshift database as the final 
