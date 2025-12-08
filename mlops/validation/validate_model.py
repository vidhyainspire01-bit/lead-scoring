# mlops/validation/validate_model.py
import mlflow
from databricks.feature_store import FeatureStoreClient
from pyspark.sql import SparkSession
import pandas as pd
from mlflow.tracking import MlflowClient


MODEL_NAME = "dbw_rakez_ml.rakez_mlops.lead_scoring_model"
ACCURACY_THRESHOLD = 0.75
AUC_THRESHOLD = 0.75


def validate_model():
    spark = SparkSession.builder.getOrCreate()
    fs = FeatureStoreClient()
    client = MlflowClient()

    print("🟦 Fetching latest staging model...")
    latest = client.get_latest_versions(MODEL_NAME, stages=["None"])[0]  # freshest version
    version = latest.version
    run_id = latest.run_id

    print(f"Using model version: {version}, run_id: {run_id}")

    # Load metrics from run
    run = client.get_run(run_id)
    acc = float(run.data.metrics["accuracy"])
    auc = float(run.data.metrics["auc"])

    print(f"Accuracy = {acc}")
    print(f"AUC = {auc}")

    if acc < ACCURACY_THRESHOLD:
        raise Exception(f"❌ Accuracy below threshold: {acc} < {ACCURACY_THRESHOLD}")

    if auc < AUC_THRESHOLD:
        raise Exception(f"❌ AUC below threshold: {auc} < {AUC_THRESHOLD}")

    print("🟦 Checking Feature Store Schema...")
    df = fs.read_table("dbw_rakez_ml.rakez_mlops.fs_lead_features")
    pdf = df.limit(100).toPandas()

    # Load model with pyfunc
    model_uri = f"models:/{MODEL_NAME}/{version}"
    model = mlflow.pyfunc.load_model(model_uri)

    print("🟦 Testing single prediction...")
    model.predict(pdf.drop(["lead_id", "lead_segment"], axis=1).head(1))

    print("✔ Model validation PASSED. Ready for promotion.")


if __name__ == "__main__":
    validate_model()
