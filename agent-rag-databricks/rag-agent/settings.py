import os
from dotenv import load_dotenv

class Settings:
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
    DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

    # DATABRICKS_ACCOUNT_ID = os.getenv("DATABRICKS_ACCOUNT_ID")
    MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI")
    EXPERIMENT_ID = os.getenv("EXPERIMENT_ID")

    VS_ENDPOINT = os.getenv("VS_ENDPOINT")
    INDEX_NAME = os.getenv("INDEX_NAME")
    LLM_ENDPOINT = os.getenv("LLM_ENDPOINT")
    MODEL_NAME = os.getenv("MODEL_NAME")
    DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")

settings = Settings()