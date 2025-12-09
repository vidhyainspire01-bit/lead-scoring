import mlflow
from databricks.feature_store import FeatureStoreClient, FeatureLookup
from databricks.feature_store.training_set import TrainingSet
from pyspark.sql import SparkSession, functions as F
from datetime import datetime

def run_batch_scoring():

    spark = SparkSession.builder.getOrCreate()
    fs = FeatureStoreClient()

    print(" Loading new leads for batch scoring...")

    # Load leads not scored yet
    df_new = (
        spark.table("dbw_rakez_ml.rakez_mlops.leads_gold")
        .filter("scored_at IS NULL")
    )

    if df_new.count() == 0:
        print(" No new leads found to score.")
        return "DONE"

    print(f" Found {df_new.count()} new leads.")

    # ------------------------- FEATURES -------------------------
    feature_lookups = [
        FeatureLookup(
            table_name="dbw_rakez_ml.rakez_mlops.fs_lead_features",
            feature_names=[
                "norm_activity",
                "norm_budget",
                "industry_weight",
                "campaign_weight",
                "service_weight",
                "noise"
            ],
            lookup_key="lead_id"
        )
    ]

    ts = fs.create_training_set(
        df=df_new,
        feature_lookups=feature_lookups,
        label=None
    )

    df_features = ts.load_df()
    print(" Features loaded for scoring.")

    # ------------------------- MODEL -------------------------
    model_name = "dbw_rakez_ml.rakez_mlops.lead_scoring_model"

    print(" Loading PRODUCTION model...")
    model_prod = mlflow.pyfunc.load_model(f"models:/{model_name}/Production")

    model_version = mlflow.MlflowClient().get_model_version_by_alias(
        name=model_name, alias="Production"
    ).version

    # Convert to Pandas
    pdf = df_features.toPandas()
    X = pdf.drop(["lead_id"], axis=1)

    print("Generating predictions...")
    preds = model_prod.predict(X)

    # ------------------------- BUILD OUTPUT -------------------------
    now = datetime.utcnow()

    pdf["predicted_segment"] = preds
    pdf["model_version"] = model_version
    pdf["scored_at"] = now

    predictions_df = spark.createDataFrame(pdf)

    # ------------------------- WRITE OUTPUT -------------------------
    output_table = "dbw_rakez_ml.rakez_mlops.leads_predictions_gold"

    print(" Writing predictions to:", output_table)

    (
        predictions_df.write
        .mode("append")
        .option("mergeSchema", "true")
        .saveAsTable(output_table)
    )

    print(" Predictions written successfully.")

    # ------------------------- UPDATE SOURCE TABLE -------------------------
    spark.sql("""
        UPDATE dbw_rakez_ml.rakez_mlops.leads_gold
        SET scored_at = current_timestamp()
        WHERE scored_at IS NULL
    """)

    print(" Updated leads_gold metadata.")
    return "SUCCESS"


# Only runs if executed as script
if __name__ == "__main__":
    run_batch_scoring()
