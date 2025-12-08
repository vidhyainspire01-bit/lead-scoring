import mlflow
from databricks import feature_store
from databricks.feature_store import FeatureStoreClient
from pyspark.sql import SparkSession
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
import pandas as pd

def run_training():
    spark = SparkSession.builder.getOrCreate()
    fs = FeatureStoreClient()

    print("🟦 Loading Feature Store Table...")
    df = fs.read_table("dbw_rakez_ml.rakez_mlops.fs_lead_features")

    # Convert Spark → Pandas for sklearn model
    pdf = df.toPandas()

    print("🟦 Preparing Training Data...")
    X = pdf.drop(["lead_id", "lead_segment"], axis=1)
    y = pdf["lead_segment"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("🟦 Starting MLflow Run...")
    mlflow.set_experiment("/Shared/lead_scoring_experiments")

    with mlflow.start_run():

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            random_state=42
        )

        print("🟦 Training Model...")
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        auc = roc_auc_score(pd.get_dummies(y_test), pd.get_dummies(preds))
        acc = accuracy_score(y_test, preds)

        print(f"Model Accuracy: {acc}")
        print(f"AUC Score: {auc}")

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("auc", auc)
        mlflow.sklearn.log_model(model, "model")

        print("🟦 Register Model to Unity Catalog...")
        mlflow.register_model(
            "runs:/{}/model".format(mlflow.active_run().info.run_id),
            "dbw_rakez_ml.lead_scoring_model"
        )

    print("Training Completed Successfully ✔")

if __name__ == "__main__":
    run_training()
