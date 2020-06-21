"""Env dataclass to load and hold all environment variables
"""
from dataclasses import dataclass
import os
from typing import Optional

from dotenv import load_dotenv

@dataclass(frozen=True)
class Env:
    """Loads all environment variables into a predefined set of properties
    """
    # to load .env file into environment variables for local execution
    load_dotenv()
    resource_group = os.environ.get("RESOURCE_GROUP")
    subscription_id = os.environ.get("SUBSCRIPTION_ID")
    la_workspace_id = os.environ.get("LOG_ANALYTICS_WORKSPACE_ID")
    la_workspace_name = os.environ.get("WORKSPACE_NAME")
    la_secret_key = os.environ.get("LOG_ANALYTICS_SECRET_KEY")
