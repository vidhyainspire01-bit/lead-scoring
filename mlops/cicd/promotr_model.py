import mlflow
from mlflow.tracking import MlflowClient

MODEL_NAME = "dbw_rakez_ml.rakez_mlops.lead_scoring_model"


def promote_model():

    client = MlflowClient()

    print(" Fetching latest STAGING model...")

    staging = client.get_latest_versions(MODEL_NAME, stages=["Staging"])
    if len(staging) == 0:
        raise Exception(" No model in STAGING to promote.")

    model_version = staging[0].version

    print(f"Promoting version {model_version} → PRODUCTION")

    # Archive existing PROD models
    prod_versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
    for pv in prod_versions:
        print(f"Archiving old prod version: {pv.version}")
        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=pv.version,
            stage="Archived"
        )

    # Promote new one
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=model_version,
        stage="Production",
        archive_existing_versions=True
    )

    # Add metadata
    client.update_model_version(
        name=MODEL_NAME,
        version=model_version,
        description="Promoted via GitHub CI/CD — validated + approved."
    )

    # Add alias for serving
    client.set_model_version_tag(
        name=MODEL_NAME,
        version=model_version,
        key="env",
        value="production"
    )

    print("✔ Model successfully promoted to Production.")
    print(f"✔ Production Version: {model_version}")


if __name__ == "__main__":
    promote_model()
