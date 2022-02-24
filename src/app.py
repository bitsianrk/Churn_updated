import pandas as pd
import streamlit as st
from pycaret import *
from preprocess_features import FeaturePreprocessor
from predict import *
from save_data import *
from train import *
from explainerdashboard import ClassifierExplainer, ExplainerDashboard




def run_app():
    st.title("Churn Prediction")
    # st.markdown(
    #     "Welcome to this simple web application that classifies shops. The shops are classified into two different classes namely: open and closed."
    # )
    ui = st.sidebar.radio(
        "Choose an option",
        ("Train", "Predict", "Fetch Data", "Model Comparisons", "Confusion Matrix", "SHAP Values", "Dashboard"),
    )
    if ui == "Train":
        st.subheader("Train the model")
        st.markdown("This section is used to train the model.")
        if st.button("Start Training"):
            with st.spinner("Training started..."):
                ModelTrainer().train_model()
                st.success("Training completed")
    if ui == "Predict":
        st.subheader("Predict the churn")
        st.markdown("This section is used to predict the churn.")
        if st.button("Start Prediction"):
            with st.spinner("Prediction started..."):
                ModelPredictor().prediction_model()
                st.success("Prediction completed")
    if ui == "Fetch Data":
        st.subheader("Fetch Data")
        st.markdown("This section is used to fetch data from the database.")
        if st.button("Start Data Fetching"):
            with st.spinner("Fetching data..."):
                SaveData().save_data()
                st.success("Data Fetching completed")
    if ui == "Model Comparisons":
        st.subheader("Model Comparisons")
        st.markdown("This section is used to compare the models.")
        df = pd.read_csv(str(Config.TRAIN_MODEL_OUTPUT_PATH) + "/model_comparison.csv")
        st.dataframe(df.style.highlight_max(axis=0))
        # st.success("Model comparisons loaded")
    if ui == "Confusion Matrix":
        st.subheader("Confusion Matrix")
        st.markdown("This section is used to view the confusion matrix.")
        st.write("0 : No churn | 1 : Churn")
        st.write("X Axis : Predicted Class | Y Axis : Actual Class")
        st.image("Confusion Matrix.png", caption="Confusion Matrix")
        # st.success("Model results loaded")
    if ui == "SHAP Values":
        st.subheader("SHAP Values")
        st.markdown("This section is used to view the SHAP values.")
        # model = load_model("final_model_pipeline")
        # interpret_model(model, display_format="streamlit")
        # st.image("SHAP Values.png", caption="SHAP Values")
        # st.success("Model results loaded")
    if ui == "Dashboard":
        st.subheader("Dashboard")
        st.markdown("This section is used to view the dashboard.")
        #explainer = ClassifierExplainer(model, X_test, y_test)
        # predict_data = FeaturePreprocessor().preprocess_features()
        # unseen_data_shapash = pd.get_dummies(data=predict_data, columns=['dsat_ind', 'credit_user_ind'])
        # predictions_label_final = pd.read_csv(str(Config.TRAIN_MODEL_OUTPUT_PATH) + "/train_data_labels.csv").loc[:, "Label"]
        # xpl.compile(x=unseen_data_shapash, model=load_model("final_model_pipeline"), y_pred=predictions_label_final)
        # app = xpl.run_app(host='localhost')
        # st.write("0 : No churn | 1 : Churn")
        # st.write("X Axis : Predicted Class | Y Axis : Actual Class")
        # st.image("Dashboard.png", caption="Dashboard")
        # st.success("Model results loaded")
    # with st.expander("Fetch and Save Data"):
    #     if st.button("Start fetching data"):
    #         with st.spinner("Fetching and saving data...."):
    #             SaveData().save_data()
    #             st.success("Data fetched and saved successfully.")
    #
    # with st.expander("Train"):
    #     if st.button("Start Training"):
    #         with st.spinner("Model training...."):
    #             ModelTrainer().train_model()
    #             st.success("Model training completed")
    #     # c1, c2, c3, c4 = st.columns(4)
    #     # with c1:
    #     #     if st.button("Dashboard"):
    #     #         with st.spinner("Starting dashboard..."):
    #     #             # xpl = SmartExplainer()
    #     #             # xpl.compile(x=unseen_data_shapash, model=load_model("final_model_pipeline"), y_pred=predictions_label_final)
    #     #             st.success("Training results loaded")
    #     # with c2:
    #     #     if st.button("Data Profiling"):
    #     #         with st.spinner("Generating report...."):
    #     #             df = pd.read_csv(str(Config.FINAL_TRAIN_DATA_PATH)+"/train_dataset.csv")
    #     #             profile = ProfileReport(df, title="Churn Report")
    #     #             profile.to_file(str(Config.ASSETS_PATH)+"/report.html")
    #     #             st.success("Report generated successfully")
    #     if st.button("Model Comparison"):
    #         with st.spinner("Loading training results...."):
    #             df = pd.read_csv(str(Config.TRAIN_MODEL_OUTPUT_PATH)+"/model_comparison.csv")
    #             st.dataframe(df)
    #             st.success("Model comparisons loaded")
    #     if st.button("Model Results"):
    #         with st.spinner("Loading training results...."):
    #             # model = load_model("final_model_pipeline")
    #             # plot_model(model,use_train_data = True,  save=True) #to_file=str(Config.ASSETS_PATH)+"/auc.png")
    #             # plot_model(model,use_train_data = True, plot='confusion_matrix', save=True) #to_file=str(Config.ASSETS_PATH)+"/cm.png")
    #             # st.image("AUC.png", caption='Area Under Curve')
    #             st.write(f"0 : No churn | 1 : Churn")
    #             # st.write("")
    #             st.write(f"X Axis : Predicted Class | Y Axis : Actual Class")
    #             # st.write("")
    #             st.image("Confusion Matrix.png", caption='Confusion Matrix')
    #             st.success("Model results loaded")
    #
    # with st.expander("Predict"):
    #     if st.button("Start Prediction"):
    #         with st.spinner("Model predicting...."):
    #             ModelPredictor().prediction_model()
    #             st.success("Prediction completed")


if __name__ == "__main__":
    run_app()
