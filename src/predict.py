from pycaret.classification import *

from config import Config
from preprocess_features import FeaturePreprocessor


class ModelPredictor:
    def __init__(self):
        pass

    def prediction_model(self, final_pred_dataset):
        model_prediction = load_model("final_model_pipeline")
        model_prediction.predict(final_pred_dataset).to_csv(
            str(Config.PREDICT_MODEL_OUTPUT_PATH) + "/predictions.csv", index=False
        )


if __name__ == "__main__":
    # model_trainer = ModelTrainer()
    # feature_preprocessor = FeaturePreprocessor()
    # model_trainer.train_model(feature_preprocessor.preprocess_features())
    ModelPredictor().prediction_model()
