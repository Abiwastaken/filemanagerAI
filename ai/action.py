import pandas as pd
import numpy as np
from datetime import datetime
import os
import hashlib


from sklearn.preprocessing import LabelEncoder
import pickle

class actioner():
    def __init__(self):
        """Initialize the AI with binary classification: keep vs archive"""
       
        
        
    def categories(self):
        
        # Categories (keep it simple)
        self.categories = ["MOVE.APPLICATION","MOVE.SCRIPT", "ARCHIVE.0", "MOVE.PICTURE", "DELETE.0", "MOVE.DOCUMENTS", "MOVE.SONG", "KEEP.0"]
        self.feature_list = []
        self.label_list = []
        # Label encoder for categories
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(self.categories)  
        return self.categories