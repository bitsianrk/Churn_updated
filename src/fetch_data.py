import json
from read_json import JSON_Reader
import requests
from config import Config
import psycopg2
import pandas as pd
import numpy as np
import datetime
from datetime import date
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.metrics import (
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    classification_report,
    precision_recall_curve,
)
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    StratifiedKFold,
    GridSearchCV,
    RandomizedSearchCV,
)
from collections import Counter
import time
from psycopg2.extras import NamedTupleCursor

# from Query_for_data import *


class DataFetcher:
    def __init__(self):
        self.json_reader_object = JSON_Reader()
        self.secrets_dict = self.json_reader_object.read_json_file(
            file_path=Config.SECRET_FILE_PATH
        )

    def fetch_data(self, query):

        output = []
        redshiftdata = {}
        list1 = []

        try:
            con = psycopg2.connect(
                host=self.secrets_dict["red_host"],
                user=self.secrets_dict["name"],
                password=self.secrets_dict["password"],
                database=self.secrets_dict["db_name"],
                port=self.secrets_dict["port"],
            )
            cur = con.cursor(cursor_factory=NamedTupleCursor)
            cur.execute(query)
            output = cur.fetchall()
            output = pd.DataFrame(output)
            return output

        except psycopg2.Error as e:

            print("Error Occurred -> ", e)
            return []


if __name__ == "__main__":
    # read_secrets_file(Config.SECRET_FILE_PATH)
    # fetch_data(queryString_input)
    # df = DataFetcher(queryString_input)
    # df.read_secrets_file(Config.SECRET_FILE_PATH)
    # df.fetch_data(queryString_input)
    dfo = DataFetcher()
    dfo.fetch_data()
