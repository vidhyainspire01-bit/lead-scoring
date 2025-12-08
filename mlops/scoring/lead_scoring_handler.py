# mlops/serving/lead_scoring_handler.py

import mlflow
import pandas as pd
from databricks.feature_store import FeatureStoreClient

class LeadScoringModel:

    def __init__(self, context):
        """
        Called once when the endpoint starts.
        Loads the Production model and Feature Store reference.
        """
        self.model_name = "dbw_rakez_ml.rakez_mlops.lead_scoring_model"
        self.model = mlflow.pyfunc.load_model(f"models:/{self.model_name}/Production")
        self.fs = FeatureStoreClient()

    def predict(self, data):
        """
        Called for every API request.
        data = list of dictionaries [{lead_id: 123}, ...]
        """

        lead_ids = [d["lead_id"] for d in data]

        # Load required features from FS
        features_df = self.fs.read_table("dbw_rakez_ml.rakez_mlops.fs_lead_features")
        features_pdf = features_df.toPandas()

        batch = features_pdf[features_pdf["lead_id"].isin(lead_ids)]

        # Drop non-feature columns
        X = batch.drop(["lead_id", "lead_segment"], axis=1)

        preds = self.model.predict(X)

        # Build response
        response = []
        for i, lid in enumerate(lead_ids):
            response.append({
                "lead_id": lid,
                "predicted_segment": preds[i],
                "score": float(i) / len(lead_ids),   # optional scoring
            })

        return response
