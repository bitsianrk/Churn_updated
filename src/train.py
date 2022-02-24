from pycaret.classification import *

from config import Config
from preprocess_features import FeaturePreprocessor


class ModelTrainer:
    def __init__(self):
        pass

    def train_model(self, final_dataset=FeaturePreprocessor().preprocess_features()):
        data = final_dataset.sample(frac=0.95, random_state=786)
        data_unseen = final_dataset.drop(data.index)
        data.reset_index(inplace=True, drop=True)
        data_unseen.reset_index(inplace=True, drop=True)
        s = setup(data=final_dataset, target="churn_ind", session_id=123, silent=True)
        best_model = compare_models()
        best_model_res = pull()
        best_model_res.to_csv(
            str(Config.TRAIN_MODEL_OUTPUT_PATH) + "/model_comparison.csv", index=False
        )
        model_best = create_model(best_model)
        tuned_model = tune_model(model_best, choose_better=True)
        prediction_score = predict_model(
            tuned_model, data=final_dataset, raw_score=True
        )
        final_model = finalize_model(tuned_model)
        plot_model(final_model, save=True, plot="auc")
        plot_model(final_model, save=True, plot="confusion_matrix")
        interpret_model(final_model, save=True)
        save_model(final_model, "final_model_pipeline")
        Prediction_Score_train_label = prediction_score[["Label", "Score_1"]]
        train_df = pd.read_csv(str(Config.FINAL_TRAIN_DATA_PATH) + "/train_dataset.csv")
        train_data_labels = pd.concat([train_df, Prediction_Score_train_label], axis=1)
        train_data_labels.to_csv(
            str(Config.TRAIN_MODEL_OUTPUT_PATH) + "/train_data_labels.csv", index=None
        )

    def prediction(self, final_pred_dataset):

        print(load_model("final_model_pipeline"))


if __name__ == "__main__":
    model_trainer = ModelTrainer()
    feature_preprocessor = FeaturePreprocessor()
    model_trainer.train_model(feature_preprocessor.preprocess_features())
