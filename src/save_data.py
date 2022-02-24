from query import Queries
from config import Config
from fetch_data import DataFetcher


class SaveData:
    def __init__(self):
        self.queries_dict = Queries().get_train_queries()
        self.pred_queries_dict = Queries().get_predict_queries()

    def save_data(self):
        for query_name, query in self.queries_dict.items():
            data_fetcher = DataFetcher()
            data_fetcher.fetch_data(query).to_csv(
                str(Config.RAW_TRAIN_DATA_PATH) + "/" + query_name + ".csv", index=False
            )
        for query_name, query in self.pred_queries_dict.items():
            data_fetcher = DataFetcher()
            data_fetcher.fetch_data(query).to_csv(
                str(Config.RAW_PREDICT_DATA_PATH) + "/" + query_name + "_predict.csv", index=False
            )


if __name__ == "__main__":
    save_data = SaveData()
    save_data.save_data()
