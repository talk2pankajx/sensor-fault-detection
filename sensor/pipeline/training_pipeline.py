from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig,DataValidationConfig
from sensor.entity.artifacts_entity import DataIngestionArtifact,DataValidationArtifact
from sensor.logger import logging
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.exception import CustomException
import os, sys

class TrainingPipeline:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.training_pipeline_config = training_pipeline_config
        except Exception as  e:
            raise CustomException(e,sys)
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_validation_config=data_validation_config, 
                data_ingestion_artifact = data_ingestion_artifact)
            return data_validation.initiate_data_validation()

        except Exception as e:
            raise CustomException(e, sys)

    def start(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact) 


        except Exception as e:
            raise CustomException(e,sys)
            


