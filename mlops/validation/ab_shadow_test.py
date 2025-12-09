# mlops/validation/ab_shadow_test.py

import mlflow
import pandas as pd
from databricks.feature_store import FeatureStoreClient
from sklearn.metrics import accuracy_score, roc_auc_score
from pyspark.sql import SparkSession
from mlflow.tracking import MlflowClient

MODEL_NAME = "dbw_rakez_ml.rakez_mlops.lead_scoring_model"
SHADOW_SAMPLE_SIZE = 500  # sample for A/B testing


def load_models():
    client = MlflowClient()

    print("Loading Champion (Production) model...")
    champion = client.get_latest_versions(MODEL_NAME, stages=["Production"])
    champion_version = champion[0].version if champion else None

    if not champion_version:
        raise Exception("No model in Production. Cannot run A/B test.")

    champion_uri = f"models:/{MODEL_NAME}/Production"
    champion_model = mlflow.pyfunc.load_model(champion_uri)

    print(f"Champion version = {champion_version}")

    print("Loading Challenger (Staging) model...")
    challenger = client.get_latest_versions(MODEL_NAME, stages=["None"])[0]
    challenger_uri = f"models:/{MODEL_NAME}/{challenger.version}"
    challenger_model = mlflow.pyfunc.load_model(challenger_uri)

    print(f"Challenger version = {challenger.version}")

    return champion_model, champion_version, challenger_model, challenger.version


def load_test_data():
    print("Loading Feature Store Table for shadow test...")
    spark = SparkSession.builder.getOrCreate()
    fs = FeatureStoreClient()

    df = fs.read_table("dbw_rakez_ml.rakez_mlops.fs_lead_features")
    pdf = df.toPandas()

    pdf_sample = pdf.sample(SHADOW_SAMPLE_SIZE, random_state=42)

    X = pdf_sample.drop(["lead_id", "lead_segment"], axis=1)
    y = pdf_sample["lead_segment"]

    return X, y


def perform_ab_test():
    champion, champion_version, challenger, challenger_version = load_models()
    X, y = load_test_data()

    print("Running predictions...")

    y_champion = champion.predict(X)
    y_challenger = challenger.predict(X)

    # Convert strings to numbers if needed
    if isinstance(y.iloc[0], str):
        y_true = pd.get_dummies(y)
        y_champion = pd.get_dummies(y_champion)
        y_challenger = pd.get_dummies(y_challenger)
    else:
        y_true = y
        
    print("Calculating Metrics...")

    results = {
        "champion_acc": accuracy_score(y_true, y_champion),
        "challenger_acc": accuracy_score(y_true, y_challenger),
        "champion_auc": roc_auc_score(y_true, y_champion),
        "challenger_auc": roc_auc_score(y_true, y_challenger)
    }

    print("\n===== A/B Shadow Test Results =====")
    print(f"Champion v{champion_version}: acc={results['champion_acc']} auc={results['champion_auc']}")
    print(f"Challenger v{challenger_version}: acc={results['challenger_acc']} auc={results['challenger_auc']}")
    print("=====================================\n")

    # Decision logic
    challenger_win = (
        results["challenger_acc"] >= results["champion_acc"]
        and results["challenger_auc"] >= results["champion_auc"]
    )

    if challenger_win:
        print(" Challenger performs better. Ready for production promotion.")
    else:
        raise Exception("Challenger did NOT outperform champion. Stop promotion.")

    return results


if __name__ == "__main__":
    perform_ab_test()
