from dataclasses import dataclass
@dataclass
class DataIngestionArtifact:
    train_file_path :str
    test_file_path : str
@dataclass
class DataValidationArtifact:
    train_file_path :str
    test_file_path:str
    report_file_path:str
    status :bool
    #decidimg status based on the status varible boolean