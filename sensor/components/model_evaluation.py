from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.entity.artifacts_entity import ModelEvaluationArtifact
from sensor.entity.artifacts_entity import DataTransformationArtifact,ModelTrainerArtifact,DataValidationArtifact
from sensor.logger import logging
from sensor.utils import load_object,save_object,read_yaml_file
from sensor.exception import CustomException
from sensor.ml.model_resolver import ModelResolver
import os,sys
import pandas as pd
from sklearn.metrics import f1_score


class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig,
                 data_validation_artifact:DataValidationArtifact,
                 data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_artifact:ModelTrainerArtifact):
                try:
                    logging.info(f"{'>>'*20} Model Evaluation {'<<'*20}")
                    self.model_evaluation_config = model_evaluation_config
                    self.data_validation_artifact = data_validation_artifact
                    self.data_transformation_artifact = data_transformation_artifact
                    self.model_trainer_artifact = model_trainer_artifact
                    self.model_resolver = ModelResolver()
                
                except Exception as e:
                    raise CustomException(e, sys)
    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:            
            logging.info("if saved model folder has model then we will compare "
            "which model is best trained or the model from saved model folder")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
                logging.info(f"Model evaluation artifact :{model_eval_artifact}")
                return model_eval_artifact
            
            logging.info(f"Finding location of transformer, model and target encoder")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()
            
            
            logging.info(f"Previosly trained transformer, model and target encoder")
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            target_encoder = load_object(file_path=target_encoder_path)
            
            
            logging.info(f"Currently trained objects")
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model = load_object(file_path=self.model_trainer_artifact.model_path)
            current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)
            
            test_df = pd.read_csv(self.data_validation_artifact.test_file_path)
            schema_info = read_yaml_file(file_path=self.model_evaluation_config.schema_file_path)
            target_column = schema_info["target_column"]
            
            target_df = test_df[target_column]
            y_true = target_encoder.transform(target_df)
            
            input_feature_name = list(transformer.feature_names_in_)
            input_arr = transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            print(f"Predictions using the previous model:{target_encoder.inverse_transform(y_pred[:5])}")
            previous_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using the previous trained model score: {previous_model_score}")
            
            
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr = current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            y_true =current_target_encoder.transform(target_df)
            current_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using the current trained model score: {current_model_score}")
            print(f"Predictions using the previous model:{current_target_encoder.inverse_transform(y_pred[:5])}")
            
            diff = current_model_score -previous_model_score
            if diff>self.model_evaluation_config.change_threshold:
                logging.info("Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous trained model")
            
            model_eval_artifact = ModelEvaluationArtifact(is_model_accepted=True,improved_accuracy=diff)
            logging.info(f"Model evaluation artifact :{model_eval_artifact}")
            return model_eval_artifact
        
        except Exception as e:
            raise CustomException(e, sys)
