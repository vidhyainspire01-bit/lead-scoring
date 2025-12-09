import mlflow
import pandas as pd
from databricks.feature_store import FeatureStoreClient
from pyspark.sql import functions as F, SparkSession

class LeadScoringModel:

    def __init__(self, context):
        self.model_name = "dbw_rakez_ml.rakez_mlops.lead_scoring_model"
        self.model = mlflow.pyfunc.load_model(f"models:/{self.model_name}/Production")

        self.fs = FeatureStoreClient()
        self.spark = SparkSession.builder.getOrCreate()

    def predict(self, data):

        lead_ids = [d["lead_id"] for d in data]

        # Pull only required rows
        features_df = (
            self.fs.read_table("dbw_rakez_ml.rakez_mlops.fs_lead_features")
            .filter(F.col("lead_id").isin(lead_ids))
        )

        pdf = features_df.toPandas()
        X = pdf.drop(["lead_id", "lead_segment"], axis=1)

        preds = self.model.predict(X)

        response = []
        for idx, lid in enumerate(pdf["lead_id"]):
            response.append({
                "lead_id": int(lid),
                "predicted_segment": preds[idx],
                "confidence": 1.0  # optional placeholder
            })

        return response
