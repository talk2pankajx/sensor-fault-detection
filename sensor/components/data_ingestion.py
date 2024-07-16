from sensor.entity.artifacts_entity import DataIngestionArtifact
from sensor.entity.config_entity import DataIngestionConfig
from sensor.exception import CustomException
from sensor.logger import logging
from sensor.utils import export_collection_as_dataframe
import os, sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("exporting collection as dataframe")            
            df = export_collection_as_dataframe(
                database_name = self.data_ingestion_config.database_name,
                collection_name = self.data_ingestion_config.collection_name)
            logging.info("removing NAN values")
            df.replace({"na":np.nan},inplace=True)

            logging.info("Splitting the data in train and test data")
            train_df,test_df = train_test_split(df,test_size = self.data_ingestion_config.test_size,train_size=self.data_ingestion_config.train_size)

            logging.info("creating dataset directory")
            os.makedirs(self.data_ingestion_config.dataset_dir,exist_ok=True)
            logging.info("saving test and train file")
            train_df.to_csv(self.data_ingestion_config.train_data_path,index=False,header=True)
            test_df.to_csv(self.data_ingestion_config.test_data_path,index=False,header=True)
            logging.info("preparing data artifact")
            data_ingestion_artifact = DataIngestionArtifact(train_file_path =self.data_ingestion_config.train_data_path,
            test_file_path = self.data_ingestion_config.test_data_path)
            logging.info(f"data Ingestion artifact :{data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys)
