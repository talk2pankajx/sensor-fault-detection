from sensor.entity.config_entity import BatchPredictionConfig
import os,sys
from sensor.exception import CustomException
from sensor.logger import logging
from sensor.ml.model_resolver import ModelResolver
from sensor.utils import read_yaml_file,write_yaml_file,load_numpy_array,save_object,load_object
from glob import glob
import pandas as pd
from datetime import datetime
import shutil


class BatchPrediction:
    def __init__(self,batch_config:BatchPredictionConfig):
        try:
            self.batch_config = batch_config
        except Exception as e:
            raise CustomException(e, sys)
    def initiate_batch_prediction(self,):
        try:
            input_files = glob(f"{self.batch_config.inbox_dir}/*.csv")

            if len(input_files)==0:
                logging.info("No batch prediction file found")
                return None
            model_resolver = ModelResolver()
            logging.info(f"loading transformers to transform the dataset")
            transformer = load_object(file_path=model_resolver.get_latest_transformer_path())\

            logging.info(f"loading model to predict the dataset")
            model = load_object(file_path=model_resolver.get_latest_model_path())

            logging.info(f"target encoder to predicted colmun into categorical")
            target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_save_path())

            for file_path in input_files:
                logging.info(f"Reading file : {file_path}")
                df=pd.read_csv(file_path)
                df.replace({"na" :np.NAN},inplace = True)
                
                input_feature_names = list(transformer.feature_names_in)
                input_arr = transformer.transform(df[input_feature_names])

                prediction = model.predict(input_arr)
                cat_prediction = target_encoder.inverse_transform(prediction)

                df["prediction"] = prediction
                df["cat_pred"] = cat_prediction

                file_name = os.path.basename(file_path)
                file_name = file_name.replace(".csv", f"_{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
                prediction_file_path = os.path.join(self.batch_config.outbox_dir,file_name)
                df.to_csv(prediction_file_path,index=False,header=True)

                archive_file_path = os.path.join(self.batch_config.archive_dir,file_name)

                shutil.copyfile(src=file_path, dst=archive_file_path)
                logging.info("Copying the file into archive: {archive_file_path}")
                os.remove(file_path)

        except Exception as e:
            raise CustomException(e, sys)



