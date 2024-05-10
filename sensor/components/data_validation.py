
from sensor.entity import DataValidationConfig
from sensor.entity.artifacts_entity import DataValidationArtifact,DataIngestionArtifact  
from sensor.logger import logging
from sensor.exception import CustomException
import os, sys
import numpy as numpy
import pandas as pd


class DataValidationComponent:
    def __init__(self,data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact
        ):
        try:

            pass
        except Exception as e:
            raise CustomException(e, sys)
    def drop_mising_values_column(self,df:pd.DataFrame,report_key_name:str )->Optional[pd.DataFrame]:
        try:

            pass
        except Exception as e:
            raise CustomException(e, sys)
    
    def is_required_columns_exist(df:pd.DataFrame) ->bool:
            try:
                pass

            except Exception as e:
                raise CustomException(e, sys)
    
    def data_drift(self,base_df:pd.DataFrame,)


