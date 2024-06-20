from .config import mongo_client
import os,sys
import json
from .exception import CustomException
import logging
import pandas as pd
import yaml
import dill
import numpy as np
def dump_csv_file_to_mongodb_collection(file_path:str,database_name:str,collection_name:str):
    try:
        df = pd.read_csv(file_path)
        logging.info("Reading the csv")
        df.reset_index(drop=True,inplace=True)
        json_records = list(json.loads(df.T.to_json()).values())
        mongo_client[database_name][collection_name].insert_many(json_records)
        
    except Exception as e:
        raise e

def export_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        if "_id" in df.columns.to_list():
            df=df.drop("_id",axis=1)
        return df
    except Exception as e:
        raise CustomException(e, sys)

def write_yaml_file(file_path,data :dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok= True)
        with open(file_path,"w") as file_writer:
            return yaml.dump(data,file_writer)
    except Exception as e:
        raise CustomException(e, sys)

def read_yaml_file(file_path):
    try:
        with open(file_path,"rb") as file_reader:
            return yaml.safe_load(file_reader)
    except Exception as e:
        raise CustomException(e, sys)

def convert_columns_float(df:pd.DataFrame,excude_colummns:list=[])->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in excude_colummns:
                df[column] = df[column].astype('float')
        return df
    except Exception as e:
        raise e

def save_object(file_path:str,obj:object)->None:
    try:
        logging.info("entered the save object in utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj,file_obj)
        logging.info("exited the file save object")
    except Exception as e:
        raise CustomException(e,sys) from e
    
def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"the file: {file_path} does not exist")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e

def save_numpy_array(file_path:str,array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise CustomException(e, sys) from e

def load_numpy_array(file_path:str)->np.array:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys) from e

            