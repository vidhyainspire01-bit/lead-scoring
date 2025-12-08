# mlops/cicd/promote_model.py
import mlflow
from mlflow.tracking import MlflowClient

MODEL_NAME = "dbw_rakez_ml.rakez_mlops.lead_scoring_model"


def promote_model():
    client = MlflowClient()

    print("🟦 Fetching latest approved model...")
    latest = client.get_latest_versions(MODEL_NAME, stages=["None"])[0]

    version = latest.version
    print("Promoting version:", version)

    # Archive old production versions
    prod_versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
    for pv in prod_versions:
        print("Archiving old version:", pv.version)
        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=pv.version,
            stage="Archived"
        )

    # Promote new model
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=version,
        stage="Production",
        archive_existing_versions=True
    )

    client.update_model_version(
        name=MODEL_NAME,
        version=version,
        description="Auto-promoted via CI/CD pipeline. Production-ready model."
    )

    print("✔ Model promoted to PRODUCTION.")
    print("✔ Version:", version)


if __name__ == "__main__":
    promote_model()
