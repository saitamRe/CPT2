
from enum import StrEnum


class PipelineSteps(StrEnum):
    INGESTION = "ingestion" 
    CLEAN = "clean_assets" 
    SILVER = "silver_assets" 
    GOLD = "gold_assets"
