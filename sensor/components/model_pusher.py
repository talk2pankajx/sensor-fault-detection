from sensor.entity.config_entity import ModelEvaluationConfig,ModelPusherConfig
from sensor.entity.artifacts_entity import ModelEvaluationArtifact
from sensor.entity.artifacts_entity import DataTransformationArtifact,ModelTrainerArtifact,ModelPusherArtifact
from sensor.logger import logging
from sensor.utils import load_object,save_object,read_yaml_file
from sensor.exception import CustomException
from sensor.ml.model_resolver import ModelResolver
import os, sys

class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
                 data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_artifact:ModelTrainerArtifact):
                try:
                    logging.info(f"{'>>'*20} Model Pusher {'>>'*20}")
                    self.model_pusher_config=model_pusher_config
                    self.data_transformation_artifact=data_transformation_artifact
                    self.model_trainer_artifact=model_trainer_artifact
                    self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.save_model_dir)
                except Exception as e:
                    raise CustomException(e, sys)
                
    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            logging.info(f"Loading Transformer model and target encoder")
            transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model =load_object(file_path=self.model_trainer_artifact.model_path) 
            target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)
            
                        
            #model pusher dir
            logging.info(f"saving the model in the saved model directory")
            save_object(file_path=self.model_pusher_config.pusher_tranformer_path,obj=transformer)
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
            save_object(file_path=self.model_pusher_config.pusher_target_encoder_path,obj=target_encoder)
            
            # save model dir
            
            logging.info("Saving model in the saved model directory")
            transformer_path = self.model_resolver.get_latest_save_transformer_path()
            model_path = self.model_resolver.get_latest_save_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_save_path()
            
            
            save_object(file_path=transformer_path,obj=transformer)
            save_object(file_path=model_path,obj=model)
            save_object(file_path=target_encoder_path, obj=target_encoder)
            
            model_pusher_artifact = ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
                                                        saved_model_dir=self.model_pusher_config.pusher_model_dir,
                                                        )
            saved_model_dir = self.model_pusher_config.pusher_model_dir
            logging.info(f"Model Pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
    
        except Exception as e:
            raise CustomException(e, sys)
