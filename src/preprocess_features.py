from config import Config
import pandas as pd

class FeaturePreprocessor:
    def __init__(self):
        pass

    def preprocess_features(self):
        train_df = pd.read_csv(str(Config.FINAL_TRAIN_DATA_PATH)+"/train_dataset.csv")
        final_dataset = train_df.iloc[:, 2:]
        final_dataset = pd.get_dummies(data=final_dataset, columns=['current_state', 'status'])
        return final_dataset

# if __name__ == "__main__":
#     FeaturePreprocessor().preprocess_features()