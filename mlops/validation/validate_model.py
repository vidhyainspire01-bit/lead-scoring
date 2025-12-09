import mlflow
from databricks.feature_store import FeatureStoreClient
from pyspark.sql import SparkSession
import pandas as pd
from mlflow.tracking import MlflowClient
import sys


MODEL_NAME = "dbw_rakez_ml.rakez_mlops.lead_scoring_model"
ACCURACY_THRESHOLD = 0.75
AUC_THRESHOLD = 0.75


def validate_model():

    spark = SparkSession.builder.getOrCreate()
    fs = FeatureStoreClient()
    client = MlflowClient()

    print(" Fetching latest STAGING model...")

    try:
        latest = client.get_latest_versions(MODEL_NAME, stages=["Staging"])[0]
    except:
        raise Exception(" No model found in STAGING stage.")

    version = latest.version
    run_id = latest.run_id

    print(f"Using version: {version} | run_id: {run_id}")

    # ---------------- METRICS ----------------
    run = client.get_run(run_id)
    acc = float(run.data.metrics["accuracy"])
    auc = float(run.data.metrics["auc"])

    print(f"Accuracy = {acc}")
    print(f"AUC = {auc}")

    if acc < ACCURACY_THRESHOLD:
        print(f" Accuracy below threshold: {acc} < {ACCURACY_THRESHOLD}")
        sys.exit(1)

    if auc < AUC_THRESHOLD:
        print(f" AUC below threshold: {auc} < {AUC_THRESHOLD}")
        sys.exit(1)

    print(" Checking Feature Store Schema...")
    df = fs.read_table("dbw_rakez_ml.rakez_mlops.fs_lead_features")
    sample = df.limit(5).toPandas()

    # ---------------- PREDICTION TEST ----------------
    model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{version}")

    print(" Testing sample prediction...")
    model.predict(sample.drop(["lead_id", "lead_segment"], axis=1))

    print(" Validation PASSED. Model is ready for production.")
    sys.exit(0)


if __name__ == "__main__":
    validate_model()
