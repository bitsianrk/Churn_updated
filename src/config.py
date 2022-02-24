from pathlib import Path


class Config:
    """
    This class shall be used for getting the configuration for the scripts.
    """

    # RANDOM_SEED = 42
    ASSETS_PATH = Path("./assets")
    DATASET_PATH = ASSETS_PATH / "data"
    RAW_TRAIN_DATA_PATH = DATASET_PATH / "train" / "raw"
    RAW_PREDICT_DATA_PATH = DATASET_PATH / "predict" / "raw"
    TRANSFORMED_TRAIN_DATA_PATH = DATASET_PATH / "train" / "transformed"
    TRANSFORMED_PREDICT_DATA_PATH = DATASET_PATH / "predict" / "transformed"
    FINAL_TRAIN_DATA_PATH = DATASET_PATH / "train" / "final"
    FINAL_PREDICT_DATA_PATH = DATASET_PATH / "predict" / "final"
    TRAIN_MODEL_OUTPUT_PATH = DATASET_PATH / "train" / "model_output"
    PREDICT_MODEL_OUTPUT_PATH = DATASET_PATH / "predict" / "model_output"
    # MODELS_PATH = ASSETS_PATH / "models"
    # METRICS_FILE_PATH = ASSETS_PATH / "metrics.json"
    # LOGS_PATH = ASSETS_PATH / "logs"
    # TUNED_HYPERPARAMS_FILE_PATH = ASSETS_PATH / "best_params.json"
    # NOTEBOOKS_PATH = ASSETS_PATH / "notebooks"
    SECRET_FILE_PATH = ASSETS_PATH / "secrets.json"
    MODEL_COMPARISONS_CSV_PATH = ASSETS_PATH / "model_comparisons.csv"
    TRAIN_COLUMNS = [ 'businessid', 'future_state', 'current_state',
       'churn_ind', 'cta_dt_cnt', 'ppv_plv_dt_cnt', 'atc_dt_cnt',
       'distinct_orderdates', 'distinct_promisedates', 'cancellationdt_count',
       'returndt_count', 'quantity_sum', 'cancelled_sum', 'returned_sum',
       'delivered_sum', 'order_items', 'total_discount',
       'total_categories_bought', 'total_jpins_bought', 'gmv_net',
       'net_of_cancellations', 'pct_discount_taken_on_gmv',
       'pct_order_items_taken_on_discount', 'customer_return_pc',
       'cust_imperfect_delivery_pc', 'reattempt_amount_cust', 'total_amount',
       'post_delivery_return_gmv', 'total_trips', 'perfect_delivery_trips',
       'complete_reattempt_trips', 'delivered_amt_pct', 'return_amt_cust_pct',
       'return_amt_jt_pct', 'missing_amt_pct', 'rating_cnt', 'avg_rating',
       'dsat_ind', 'calls', 'total_visits', 'status', 'currentlimit',
       'overalllimit', 'totalbounced', 'totaloutstanding',
       'totaloutstandingbounced', 'totalcreditused', 'totalbouncedcount',
       'totaloutstandingbouncedcount', 'totaloutstandingcount',
       'totalcreditusedcount', 'avg_daily_utilzation', 'credit_user_ind',
       'null_search_cnt', 'target_schemes_count', 'milestones_achieved_count',
       'total_jc_earned', 'sc_points_red', 'sc_rewards_count']
    PREDICT_COLUMNS = ['businessid', 'current_state',
                     'churn_ind', 'cta_dt_cnt', 'ppv_plv_dt_cnt', 'atc_dt_cnt',
                     'distinct_orderdates', 'distinct_promisedates', 'cancellationdt_count',
                     'returndt_count', 'quantity_sum', 'cancelled_sum', 'returned_sum',
                     'delivered_sum', 'order_items', 'total_discount',
                     'total_categories_bought', 'total_jpins_bought', 'gmv_net',
                     'net_of_cancellations', 'pct_discount_taken_on_gmv',
                     'pct_order_items_taken_on_discount', 'customer_return_pc',
                     'cust_imperfect_delivery_pc', 'reattempt_amount_cust', 'total_amount',
                     'post_delivery_return_gmv', 'total_trips', 'perfect_delivery_trips',
                     'complete_reattempt_trips', 'delivered_amt_pct', 'return_amt_cust_pct',
                     'return_amt_jt_pct', 'missing_amt_pct', 'rating_cnt', 'avg_rating',
                     'dsat_ind', 'calls', 'total_visits', 'status', 'currentlimit',
                     'overalllimit', 'totalbounced', 'totaloutstanding',
                     'totaloutstandingbounced', 'totalcreditused', 'totalbouncedcount',
                     'totaloutstandingbouncedcount', 'totaloutstandingcount',
                     'totalcreditusedcount', 'avg_daily_utilzation', 'credit_user_ind',
                     'null_search_cnt', 'target_schemes_count', 'milestones_achieved_count',
                     'total_jc_earned', 'sc_points_red', 'sc_rewards_count']

