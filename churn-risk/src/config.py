class Configuration:
    """
    Configuration file for Telco Customer Churn
    """
    def __init__(self):
        self.color = '#00A8E0'
        self.total_gauge_color = '#FF0102'
        self.image_path = 'static/churn.png'

        self.training_path = 'data/churnTrain.csv'
        self.testing_path = 'data/churnTest.csv'
        self.default_model = 'telco_churn_model'

        self.y_col = 'Churn'
        self.x_cols = ['Account_Length', 'No_Vmail_Messages', 'Total_Day_minutes', 'Total_Day_Calls',
                       'Total_Day_charge', 'Total_Eve_Minutes', 'Total_Eve_Calls', 'Total_Eve_Charge',
                       'Total_Night_Minutes', 'Total_Night_Calls', 'Total_Night_Charge', 'Total_Intl_Minutes',
                       'Total_Intl_Calls', 'Total_Intl_Charge', 'No_CS_Calls', 'Area_Code', 'International_Plan',
                       'Voice_Mail_Plan', 'State', 'Phone_No']

        self.id_column = "Phone_No"

        self.title = 'Telecom Churn Analytics'
        self.subtitle = 'EDA & Churn Modeling with AutoML & Wave'
        self.icon = 'AddPhone'

        self.model_loaded = False
        self.working_data = self.training_path
        # self.training_data_url = 'https://h2o-internal-release.s3-us-west-2.amazonaws.com/data/Splunk/churn.csv'
        self.training_data_url = 'data/churnTrain.csv'
        # self.testing_data_url = 'https://h2o-internal-release.s3-us-west-2.amazonaws.com/data/Splunk/churn_test.csv'
        self.testing_data_url = 'data/churnTest.csv'

        self.boxes = {
            "banner": "1 1 3 1",
            "content": "1 2 -1 -1",
            "logo": "11 1 -1 1",
            "navbar": "4 1 -1 1",
            "day_stat": "3 2 2 1",
            "eve_stat": "5 2 2 1",
            "night_stat": "3 3 2 1",
            "intl_stat": "5 3 2 1",
            "total_stat": "7 2 1 2",
            "customer": "1 2 2 1",
            "churn_rate": "1 3 2 1",
            "stat_pie": "8 2 -1 2",
            "shap_plot": "1 4 -1 11",
            "top_negative_pd_plot": "1 15 -1 11",
            "top_positive_pd_plot": "1 26 -1 11",
        }

    def load_model(self, predictions_file_path):
        self.model_loaded = True
        self.working_data = predictions_file_path

    def get_column_type(self):
        if self.model_loaded:
            return "Churn Prediction"
        else:
            return "Churn?"

    def get_analysis_type(self):
        if self.model_loaded:
            return "Model Predictions"
        else:
            return "Historical Data"
