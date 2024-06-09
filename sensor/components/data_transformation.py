from sensor.entity.config_entity import DataTransformationConfig
from sensor.entity.artifacts_entity import DataValidationArtifact,DataTransformationArtifact  
from sensor.logger import logging
from sensor.exception import CustomException
from typing import Optional
import os, sys
import numpy as np
import pandas as pd
from sensor.utils import read_yaml_file,write_yaml_file,save_object,save_numpy_array
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from imblearn.combine import SMOTETomek
from sklearn.preprocessing import RobustScaler,LabelEncoder

class DataTransformation:
    def __init__(self,data_transformation_config: DataTransformationConfig,
        data_validation_artifact : DataValidationArtifact):
        try:
            logging.info("starting data transformation")
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact =  data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)
            robust_scaler = RobustScaler()
            pipeline = Pipeline(steps=[
                ('SimpleImputer',simple_imputer),
                ('RobustScaler',robust_scaler)
            ]) 
            return pipeline     
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_tranformation(self)->DataTransformationArtifact:
        try:
            schema_info = read_yaml_file(file_path = self.data_transformation_config.schema_file_path)
            target_column = schema_info["target_column"]
            #reading the the training and test file
            logging.info(f"reading the train and test data file")
            train_df = pd.read_csv(self.data_validation_artifact.train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.test_file_path)
            logging.info("Selecting the input feature for test and train data")
            input_feature_train_df = train_df.drop(target_column,axis=1)
            input_feature_test_df = test_df.drop(target_column,axis=1)
            logging.info("Selecting the target feature for train and test dataframe")
            target_feature_train_df = train_df[target_column]
            target_feature_test_df = test_df[target_column]
            logging.info("Label Encoding the cat target colmun into numerical ")
            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            #transform the colmuns
            logging.info("tranformation of target columns")
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)

            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            logging.info("transforming input features")

            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            logging.info("Balancing the imbalanced dataset")
            smt = SMOTETomek(random_state = 42)

            logging.info(f"Before resampling the training set input:{input_feature_train_arr.shape} Target :{target_feature_train_arr.shape}")
            input_feature_train_arr,target_feature_train_arr = smt.fit_resample(input_feature_train_arr,target_feature_train_arr)
            logging.info(f"After resampling the training set input:{input_feature_train_arr.shape} Target :{target_feature_train_arr.shape}")

            logging.info(f"Before resampling the testing set input:{input_feature_test_arr.shape} Target :{target_feature_test_arr.shape}")
            input_feature_test_arr,target_feature_test_arr = smt.fit_resample(input_feature_test_arr,target_feature_test_arr)
            logging.info(f"After resampling the testing set input:{input_feature_test_arr.shape} Target :{target_feature_test_arr.shape}")

            train_arr = np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr,target_feature_test_arr]

            logging.info(f"Saving the data")
            save_numpy_array(file_path=self.data_transformation_config.transform_train_path,array=train_arr)
            save_numpy_array(file_path=self.data_transformation_config.transform_test_path,array=test_arr)

            logging.info(f"Save label encoder")
            save_object(file_path =self.data_transformation_config.target_encoder_path,obj=label_encoder )

            logging.info("Save transformation pipeline")
            save_object(file_path=self.data_transformation_config.transform_object_path,obj=transformation_pipeline)
            data_transformation_artifact = DataTransformationArtifact(
                transform_object_path = self.data_transformation_config.transform_object_path,
                transform_train_path = self.data_transformation_config.transform_train_path,
                transform_test_path = self.data_transformation_config.transform_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path
            )
            logging.info(f"Data transformation artifact : {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e,sys)