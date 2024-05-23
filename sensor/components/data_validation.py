from sensor.entity.config_entity import DataValidationConfig,TrainingPipelineConfig
from sensor.entity.artifacts_entity import DataValidationArtifact,DataIngestionArtifact  
from sensor.logger import logging
from sensor.exception import CustomException
from typing import Optional
import os, sys
import numpy as numpy
import pandas as pd
from scipy.stats import ks_2samp
from sensor.utils import read_yaml_file,write_yaml_file


class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact
        ):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.vaidation_error = dict()
        except Exception as e:
            raise CustomException(e, sys)

    def drop_mising_values_column(self,df:pd.DataFrame,report_key_name:str )->Optional[pd.DataFrame]:
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = (df.isna().sum())*100/df.shape[0]
            logging.info(f"dropping the columns according to the schema above to {threshold}")
            drop_column_names = null_report[null_report>threshold].index
            logging.info(f"columns to drop={list(drop_column_names)}")
            self.vaidation_error[report_key_name] = list(drop_column_names)
            df.drop(list(drop_column_names),axis=1,inplace=True)

            if len(df.columns)==0:
                None
            return df
        except Exception as e:
            raise CustomException(e, sys)
    
    def is_required_columns_exist(self,df:pd.DataFrame,report_key_name) ->bool:
            try:
                schema_info = read_yaml_file(file_path = self.data_validation_config.schema_file_path)
                required_columns = schema_info['required_columns']
                logging.info(f"required columns: {required_columns}")
                missing_required_columns = []
                for column in required_columns:
                    if column not in df.columns:
                        missing_required_columns.append(column)
                if len(missing_required_columns) ==0:
                    return True
                logging.info(f"missing requiured columns are {missing_required_columns} ")                
                self.vaidation_error[report_key_name] = missing_required_columns
                return False   


            except Exception as e:
                raise CustomException(e, sys)
    
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name)->None:
            try:
                drift_report = dict()
                base_columns = base_df.columns
                current_columns=current_df.columns
                for base_column in base_columns:
                    base_data,current_data = base_df[base_column],current_df[base_column]
                    logging.info(f"Hypothesis {base_column}:{base_data.dtype},{current_data.dtype}")
                    same_distribution = ks2samp(base_data,current_data)
                    if same_distribution.pvalue>0.05:
                        drift_report[base_column] = {
                            "pvalues":float({same_distribution.pvalue}),
                            "same_distribution":True
                        }
                    if same_distribution.pvalue<0.05:
                        drift_report[base_column] = {
                            "pvalues":float({same_distribution.pvalue}),
                            "same_distribution":False
                        }
                self.validation_error[report_key_name] = drift_report       

            except Exception as e:
                raise CustomException(e, sys)

    def drop_columns(self,df:pd.DataFrame)->pd.DataFrame:
        try:
            schema_info = read_yaml_file(file_path = self.data_validation_config.schema_file_path)
            drop_columns = schema_info['drop_columns']
            df.drop(drop_columns,axis=1,inplace=True)
            logging.info(f"Dropping column based on schema provided {drop_columns}")
        except Exception as e:
            raise e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            self.drop_columns(df=train_df)
            self.drop_columns(df =test_df)
            train_df = self.drop_mising_values_column(df=train_df, report_key_name= "train_missing_values_columns")
            testself.drop_mising_values_column(df=test_df, report_key_name= "test_missing_values_columns")
            if train_df is None:
                logging.info(f"No column left in train_df hence stopping the pipeline")
                raise Exception("No column left in train_df hence stopping the pipeline")
            if test_df is None:
                logging.info(f"No column left in test_df hence stopping the pipeline")
                raise Exception("No column left in test_df hence stopping the pipeline")

            exist = self.is_required_columns_exist(df=train_df, report_key_name="train_required_columns")
            if not exist:
                raise Exception("required columns are not available in train_df")
                        
            exist = self.is_required_columns_exist(df=test_df, report_key_name="test_required_columns")
            if not exist:
                raise Exception("required columns are not available in test_df")
            if len( train_df.columns) !=len(test_df.columns):
                raise Exception("Train and test df have not equal columns")
            self.data_drift(base_df=train_df, current_df=test_df, report_key_name="tran_test_drift")
            os.makedirs(self.data_validation_config.valid_dir, exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path,header=True, index=False)            
            test_df.to_csv(self.data_validation_config.valid_test_file_path,header=True, index=False)

            write_yaml_file(file_path=data_validation_config.report_file_name, data=self.vaidation_error)
            DataValidationArtifact(report_file_path=data_validation_config.report_file_name,
             train_file_path=data_validation_config.valid_train_file_path,
             test_file_path=data_validation_config.valid_test_file_path,
             status = True)           

        except Exception as e:
            raise CustomException(e, sys)




