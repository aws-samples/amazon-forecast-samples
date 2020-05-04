import logging
from boto3 import client

class Loader: 
    def __init__(self): 
        self.forecast_cli = client('forecast') 
        self.logger = logging.getLogger() 
        self.logger.setLevel(logging.INFO) 