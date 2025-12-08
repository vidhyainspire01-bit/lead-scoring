# mlops/scoring/batch_scoring.py

import mlflow
from databricks.feature_store import FeatureStoreClient
from databricks.feature_store import FeatureLookup
from pyspark.sql import functions as F

spark = spark
fs = FeatureStoreClient()

# ------------------------------------------------------------
# STEP 1 — Load NEW leads from silver or gold table
# ------------------------------------------------------------
print("🟦 Loading new leads for batch scoring...")

df_new = spark.table("dbw_rakez_ml.rakez_mlops.leads_gold") \
              .filter(F.col("scored_at").isNull())

if df_new.count() == 0:
    print("🟨 No new leads found to score.")
    dbutils.notebook.exit("DONE")

print(f"🟦 Found {df_new.count()} new leads.")


# ------------------------------------------------------------
# STEP 2 — Use Feature Store Lookups
# ------------------------------------------------------------
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

# Build training set (no label)
from databricks.feature_store.training_set import TrainingSet

ts = fs.create_training_set(
    df=df_new,
    feature_lookups=feature_lookups,
    label=None
)

df_features = ts.load_df()

print("🟦 Features loaded for scoring.")
df_features.display()


# ------------------------------------------------------------
# STEP 3 — Load PRODUCTION MODEL
# ------------------------------------------------------------
model_name = "dbw_rakez_ml.rakez_mlops.lead_scoring_model"

print("🟦 Loading Production model...")

model_prod = mlflow.pyfunc.load_model(f"models:/{model_name}/Production")

model_version = mlflow.pyfunc.get_model_info(f"models:/{model_name}/Production").version


# ------------------------------------------------------------
# STEP 4 — Apply Model Predictions
# ------------------------------------------------------------
print("🟦 Generating predictions...")

pdf = df_features.toPandas()
X = pdf.drop(["lead_id"], axis=1)

preds = model_prod.predict(X)

# Build dataframe for writing back to Delta
predictions_df = spark.createDataFrame(
    pdf.assign(
        predicted_segment=preds,
        model_version=model_version,
        scored_at=F.current_timestamp().cast("string")
    )
)


# ------------------------------------------------------------
# STEP 5 — Write results to GOLD predictions table
# ------------------------------------------------------------
output_table = "dbw_rakez_ml.rakez_mlops.leads_predictions_gold"

print("🟦 Writing predictions to table:", output_table)

(
    predictions_df
    .write
    .mode("append")
    .option("mergeSchema", "true")
    .saveAsTable(output_table)
)

print("🟩 Batch scoring completed successfully.")


# ------------------------------------------------------------
# STEP 6 — Update original leads scored_at column
# ------------------------------------------------------------
spark.sql("""
UPDATE dbw_rakez_ml.rakez_mlops.leads_gold
SET scored_at = current_timestamp()
WHERE scored_at IS NULL
""")

print("🟩 Updated leads_gold with scoring metadata.")


dbutils.notebook.exit("SUCCESS")
