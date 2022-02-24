from config import Config
import pandas as pd

class DataValidator:
    def __init__(self):
        self.train_data = pd.read_csv(str(Config.FINAL_TRAIN_DATA_PATH)+"/train_dataset.csv")


    def validate_train_data(self):
        for column1, column2 in zip(self.train_data.columns, Config.TRAIN_COLUMNS):
            if column1 != column2:
                print("Columns are not matching: ", column1, column2)
                return False
            else:
                return True

    def validate_predict_data(self):
        pass

if __name__ == "__main__":
    data_validator = DataValidator()
    print(data_validator.validate_train_data())