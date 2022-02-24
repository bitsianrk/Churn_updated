from config import Config
import pandas as pd
import numpy as np


class DataTransformer:
    def __init__(self):
        pass

    def transform_train_data(self):
        i = "2022-02-18"
        j = "2021-12-18"

        df1 = pd.read_csv(str(Config.RAW_TRAIN_DATA_PATH) + "/metadata_query_curr.csv")
        df2 = pd.read_csv(str(Config.RAW_TRAIN_DATA_PATH) + "/metadata_query_curr2.csv")

        df1["date_ref"] = i
        df1["date_ref"] = pd.to_datetime(df1["date_ref"], errors="coerce")

        df1["max_order_dt"] = pd.to_datetime(df1["max_order_dt"], errors="coerce")
        df1["days_since_last_order"] = df1["date_ref"] - df1["max_order_dt"]
        df1["days_since_last_order"] = df1.days_since_last_order.apply(lambda x: x.days)

        df1["onboarddate"] = pd.to_datetime(df1["onboarddate"], errors="coerce")
        df1["age_of_biz"] = df1["date_ref"] - df1["onboarddate"]
        df1["age_of_biz"] = df1.age_of_biz.apply(lambda x: x.days)

        conditions = [
            (df1["days_since_last_order"] >= 30) & (df1["days_since_last_order"] < 60),
            (df1["days_since_last_order"] >= 60),
            (df1["days_since_last_order"] < 30),
        ]

        choices = ["lapsed", "churned", "actively_ordering"]
        df1["current_state"] = np.select(conditions, choices)

        conditions1 = [
            (df1["age_of_biz"] <= 60),
            (df1["age_of_biz"] > 60) & (df1["age_of_biz"] <= 90),
            (df1["age_of_biz"] > 90) & (df1["age_of_biz"] <= 120),
            (df1["age_of_biz"] > 120) & (df1["age_of_biz"] <= 150),
            (df1["age_of_biz"] > 150),
        ]

        choices1 = [
            "less than equal to 60",
            "b/w 61 to 90",
            "b/w 91 to 120",
            "b/w 121 to 150",
            "greater than 150",
        ]
        df1["current_business_age"] = np.select(conditions1, choices1)

        df2["prev_date_ref"] = j
        df2["prev_date_ref"] = pd.to_datetime(df2["prev_date_ref"], errors="coerce")

        df2["prev_max_order_dt"] = pd.to_datetime(
            df2["prev_max_order_dt"], errors="coerce"
        )
        df2["prev_days_since_last_order"] = (
            df2["prev_date_ref"] - df2["prev_max_order_dt"]
        )
        df2["prev_days_since_last_order"] = df2.prev_days_since_last_order.apply(
            lambda x: x.days
        )

        #     df6['prev_onboarded_date'] = pd.to_datetime(df6['prev_onboarded_date'], errors='coerce')
        #     df6['prev_age_of_biz'] = df6['prev_date_ref']-df6['prev_onboarded_date']
        #     df6['age_of_biz'] = df6.days_since_last_order.apply(lambda x: x.days)

        conditions2 = [
            (df2["prev_days_since_last_order"] >= 30)
            & (df2["prev_days_since_last_order"] < 60),
            (df2["prev_days_since_last_order"] >= 60),
            (df2["prev_days_since_last_order"] < 30),
        ]

        choices2 = ["lapsed", "churned", "actively_ordering"]
        df2["prev_state"] = np.select(conditions2, choices2)

        # creating the merged dataset

        final = pd.merge(
            df1, df2, how="left", left_on=["businessid"], right_on=["businessid"]
        )

        final["prev_age_of_biz"] = final["age_of_biz"] - 60
        final["l2m_orders"] = final["total_orders"] - final["prev_total_orders"]
        final["l2m_order_dates"] = (
            final["distinct_order_dates"] - final["prev_distinct_order_dates"]
        )

        conditions3 = [
            (final["prev_age_of_biz"] <= 60),
            (final["prev_age_of_biz"] > 60) & (final["prev_age_of_biz"] <= 90),
            (final["prev_age_of_biz"] > 90) & (final["prev_age_of_biz"] <= 120),
            (final["prev_age_of_biz"] > 120) & (final["prev_age_of_biz"] <= 150),
            (final["prev_age_of_biz"] > 150),
        ]

        choices3 = [
            "less than equal to 60",
            "b/w 61 to 90",
            "b/w 91 to 120",
            "b/w 121 to 150",
            "greater than 150",
        ]
        final["prev_business_age"] = np.select(conditions3, choices3)

        final_output = final[
            [
                "businessid",
                "businesstype",
                "onboarddate",
                "max_order_dt",
                "total_orders",
                "days_since_last_order",
                "age_of_biz",
                "current_state",
                "current_business_age",
                "prev_max_order_dt",
                "prev_total_orders",
                "prev_days_since_last_order",
                "prev_age_of_biz",
                "prev_state",
                "l2m_orders",
                "l2m_orders",
                "prev_business_age",
                "date_ref",
                "prev_date_ref",
            ]
        ]

        conditions4 = [
            (final_output.max_order_dt.notnull() == True),
            (final_output.max_order_dt.notnull() == False),
        ]

        choices4 = [1, 0]
        final_output["ETB"] = np.select(conditions4, choices4)

        conditions5 = [
            (final_output.prev_max_order_dt.notnull() == True),
            (final_output.prev_max_order_dt.notnull() == False),
        ]

        choices5 = [1, 0]
        final_output["prev_ETB"] = np.select(conditions5, choices5)
        final_output_metadata = final_output[
            (final_output["ETB"] > 0) & (final_output["prev_ETB"] > 0)
        ]
        final_output_metadata.to_csv(
            str(Config.TRANSFORMED_TRAIN_DATA_PATH) + "/final_output_metadata.csv",
            index=False,
        )

        df21 = pd.read_csv(
            str(Config.RAW_TRAIN_DATA_PATH) + "/metadata_query_master.csv"
        )

        df21["delivered_amt_pct"] = df21["delivered_amount"] / df21["total_amount"]
        df21["return_amt_cust_pct"] = df21["return_amount_cust"] / df21["total_amount"]
        df21["return_amt_jt_pct"] = df21["return_amount_jt"] / df21["total_amount"]
        df21["missing_amt_pct"] = df21["missing_amount"] / df21["total_amount"]

        df21 = df21.drop(columns=["staples_category_bought", "fmcg_category_bought"])

        df21 = df21.drop(
            columns=[
                "fmcg_gmv",
                "staples_gmv",
                "staples_jpin_bought",
                "fmcg_jpin_bought",
                "fmcg_gmv_net",
                "staples_gmv_net",
                "total_shipping",
                "delivered_amount",
                "return_amount_cust",
                "return_amount_jt",
                "missing_amount",
                "complete_rto_trips",
            ]
        )

        df21.to_csv(
            str(Config.TRANSFORMED_TRAIN_DATA_PATH)
            + "/metadata_query_master_transformed.csv",
            index=False,
        )

        df61 = pd.read_csv(str(Config.RAW_TRAIN_DATA_PATH) + "/credit_base_query.csv")
        # df_credit_status = df61[["bz_id", "status"]]
        conditions7 = [
            (df61["status"] == "ACTIVE"),
            (df61["status"] == "BLOCKED"),
            (df61["status"] == "INACTIVE"),
            (df61["status"] == "ON_HOLD"),
        ]
        choices7 = [4, 2, 1, 3]
        df61["status_ind"] = np.select(conditions7, choices7)
        df_credit_status = df61[["bz_id", "status"]]
        conditions8 = [
            (df_credit_status["status"] == "ACTIVE"),
            (df_credit_status["status"] == "BLOCKED"),
            (df_credit_status["status"] == "INACTIVE"),
            (df_credit_status["status"] == "ON_HOLD"),
        ]
        choices8 = [4, 2, 1, 3]
        df_credit_status["status_ind"] = np.select(conditions8, choices8)
        df_credit_statusind = (
            df_credit_status.groupby(["bz_id"]).max("status_ind").reset_index()
        )
        cred_status = pd.merge(
            df_credit_statusind,
            df61,
            how="left",
            left_on=["bz_id", "status_ind"],
            right_on=["bz_id", "status_ind"],
        ).fillna(0)
        df_credit_sum = cred_status[
            [
                "bz_id",
                "status",
                "currentlimit",
                "overalllimit",
                "totalbounced",
                "totaloutstanding",
                "totaloutstandingbounced",
                "totalcreditused",
                "totalbouncedcount",
                "totaloutstandingbouncedcount",
                "totaloutstandingcount",
                "totalcreditusedcount",
            ]
        ]
        df_credit_sum = df_credit_sum.fillna(0)
        df_credit_sum_ag = (
            df_credit_sum.groupby(["bz_id", "status"])
            .agg(
                {
                    "currentlimit": "sum",
                    "overalllimit": "sum",
                    "totalbounced": "sum",
                    "totaloutstanding": "sum",
                    "totaloutstandingbounced": "sum",
                    "totalcreditused": "sum",
                    "totalbouncedcount": "sum",
                    "totaloutstandingbouncedcount": "sum",
                    "totaloutstandingcount": "sum",
                    "totalcreditusedcount": "sum",
                }
            )
            .reset_index()
        )
        df_cred_util = pd.read_csv(
            str(Config.RAW_TRAIN_DATA_PATH) + "/credit_utilization_query.csv"
        )
        cred_final = pd.merge(
            df_credit_sum_ag,
            df_cred_util,
            how="left",
            left_on=["bz_id"],
            right_on=["bz_id"],
        ).fillna(0)
        cred_final.to_csv(
            str(Config.TRANSFORMED_TRAIN_DATA_PATH) + "/credit_final.csv", index=False
        )


    def transform_predict_data(self):
        i = '2022-02-18'

        df1 = pd.read_csv(str(Config.RAW_PREDICT_DATA_PATH) + "/metadata_query_curr_predict.csv")

        df1['date_ref'] = i
        df1['date_ref'] = pd.to_datetime(df1['date_ref'], errors='coerce')

        df1['max_order_dt'] = pd.to_datetime(df1['max_order_dt'], errors='coerce')
        df1['days_since_last_order'] = df1['date_ref'] - df1['max_order_dt']
        df1['days_since_last_order'] = df1.days_since_last_order.apply(lambda x: x.days)

        df1['onboarddate'] = pd.to_datetime(df1['onboarddate'], errors='coerce')
        df1['age_of_biz'] = df1['date_ref'] - df1['onboarddate']
        df1['age_of_biz'] = df1.age_of_biz.apply(lambda x: x.days)

        conditions = [

            (df1['days_since_last_order'] >= 30) & (df1['days_since_last_order'] < 60),
            (df1['days_since_last_order'] >= 60),
            (df1['days_since_last_order'] < 30)

        ]

        choices = ['lapsed', 'churned', 'actively_ordering']
        df1['current_state'] = np.select(conditions, choices)

        conditions1 = [
            (df1['age_of_biz'] <= 60),
            (df1['age_of_biz'] > 60) & (df1['age_of_biz'] <= 90),
            (df1['age_of_biz'] > 90) & (df1['age_of_biz'] <= 120),
            (df1['age_of_biz'] > 120) & (df1['age_of_biz'] <= 150),
            (df1['age_of_biz'] > 150)

        ]

        choices1 = ['less than equal to 60', 'b/w 61 to 90', 'b/w 91 to 120', 'b/w 121 to 150', 'greater than 150']
        df1['current_business_age'] = np.select(conditions1, choices1)

        conditions4 = [
            (df1.max_order_dt.notnull() == True),
            (df1.max_order_dt.notnull() == False)
        ]

        choices4 = [1, 0]
        df1['ETB'] = np.select(conditions4, choices4)

        conditions5 = [
            (df1.prev_max_order_dt.notnull() == True),
            (df1.prev_max_order_dt.notnull() == False)
        ]

        final_output = df1

        final_output_metadata.to_csv(
            str(Config.TRANSFORMED_TRAIN_DATA_PATH) + "/final_output_metadata.csv",
            index=False,
        )

        df21 = pd.read_csv(
            str(Config.RAW_TRAIN_DATA_PATH) + "/metadata_query_master.csv"
        )

        df21["delivered_amt_pct"] = df21["delivered_amount"] / df21["total_amount"]
        df21["return_amt_cust_pct"] = df21["return_amount_cust"] / df21["total_amount"]
        df21["return_amt_jt_pct"] = df21["return_amount_jt"] / df21["total_amount"]
        df21["missing_amt_pct"] = df21["missing_amount"] / df21["total_amount"]

        df21 = df21.drop(columns=["staples_category_bought", "fmcg_category_bought"])

        df21 = df21.drop(
            columns=[
                "fmcg_gmv",
                "staples_gmv",
                "staples_jpin_bought",
                "fmcg_jpin_bought",
                "fmcg_gmv_net",
                "staples_gmv_net",
                "total_shipping",
                "delivered_amount",
                "return_amount_cust",
                "return_amount_jt",
                "missing_amount",
                "complete_rto_trips",
            ]
        )

        df21.to_csv(
            str(Config.TRANSFORMED_TRAIN_DATA_PATH)
            + "/metadata_query_master_transformed.csv",
            index=False,
        )

        df61 = pd.read_csv(str(Config.RAW_TRAIN_DATA_PATH) + "/credit_base_query.csv")
        # df_credit_status = df61[["bz_id", "status"]]
        conditions7 = [
            (df61["status"] == "ACTIVE"),
            (df61["status"] == "BLOCKED"),
            (df61["status"] == "INACTIVE"),
            (df61["status"] == "ON_HOLD"),
        ]
        choices7 = [4, 2, 1, 3]
        df61["status_ind"] = np.select(conditions7, choices7)
        df_credit_status = df61[["bz_id", "status"]]
        conditions8 = [
            (df_credit_status["status"] == "ACTIVE"),
            (df_credit_status["status"] == "BLOCKED"),
            (df_credit_status["status"] == "INACTIVE"),
            (df_credit_status["status"] == "ON_HOLD"),
        ]
        choices8 = [4, 2, 1, 3]
        df_credit_status["status_ind"] = np.select(conditions8, choices8)
        df_credit_statusind = (
            df_credit_status.groupby(["bz_id"]).max("status_ind").reset_index()
        )
        cred_status = pd.merge(
            df_credit_statusind,
            df61,
            how="left",
            left_on=["bz_id", "status_ind"],
            right_on=["bz_id", "status_ind"],
        ).fillna(0)
        df_credit_sum = cred_status[
            [
                "bz_id",
                "status",
                "currentlimit",
                "overalllimit",
                "totalbounced",
                "totaloutstanding",
                "totaloutstandingbounced",
                "totalcreditused",
                "totalbouncedcount",
                "totaloutstandingbouncedcount",
                "totaloutstandingcount",
                "totalcreditusedcount",
            ]
        ]
        df_credit_sum = df_credit_sum.fillna(0)
        df_credit_sum_ag = (
            df_credit_sum.groupby(["bz_id", "status"])
            .agg(
                {
                    "currentlimit": "sum",
                    "overalllimit": "sum",
                    "totalbounced": "sum",
                    "totaloutstanding": "sum",
                    "totaloutstandingbounced": "sum",
                    "totalcreditused": "sum",
                    "totalbouncedcount": "sum",
                    "totaloutstandingbouncedcount": "sum",
                    "totaloutstandingcount": "sum",
                    "totalcreditusedcount": "sum",
                }
            )
            .reset_index()
        )
        df_cred_util = pd.read_csv(
            str(Config.RAW_TRAIN_DATA_PATH) + "/credit_utilization_query.csv"
        )
        cred_final = pd.merge(
            df_credit_sum_ag,
            df_cred_util,
            how="left",
            left_on=["bz_id"],
            right_on=["bz_id"],
        ).fillna(0)
        cred_final.to_csv(
            str(Config.TRANSFORMED_TRAIN_DATA_PATH) + "/credit_final.csv", index=False
        )




if __name__ == "__main__":
    data_transform = DataTransformer()
    data_transform.merge_transformed_train_data()
