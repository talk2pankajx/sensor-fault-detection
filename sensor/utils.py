from .config import mongo_client
import pandas as pd
import logging
import json
from .exception import CustomException
import os,sys
def dump_csv_file_to_mongodb_collection(file_path:str,database_name:str, collection_name:str)->None:
    try:
         df = pd.read_csv(file_path)
         logging.info(f"Row and columns{df.shape}")

         df.reset_index(drop=True,inplace=True)
         json_record = list(json.loads(df.T.to_json()).values())

         mongo_client[database_name][collection_name].insert_many(json_record)
         
    except Exception as e:
        raise CustomException(e,sys)
        
def export_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        if "_id" in df.columns.to_list():
            df = df.drop("_id",axis =1)
        return df
    except Exception as e:
            raise CustomException(e,sys)
