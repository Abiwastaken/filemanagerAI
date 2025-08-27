import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import os
import hashlib
from jarvis import AI  as brain
from action import actioner as coach

class Trainer():
    def __init__(self, brain):
        """Initialize the AI with binary classification: keep vs archive"""
        # Create the Random Forest model
        self.actioner = coach()
        self.df = pd.DataFrame()
        self.feature_list = []
        self.label_list = []
        # Label encoder for categories
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(self.actioner.categories())  
        self.brain = brain
        
        
        

        
        
    def hash_path(self,path):
        """Hashes a string path to an integer."""
        if pd.isna(path):
            return 0
        ret = int(hashlib.sha256(path.encode('utf-8')).hexdigest(), 16) % (10**8)
        return (ret% 10000) / 10000
        
        
    # extracts features from the CSV file and prepares the DataFrame
    def extract_features(self, path):
        """Extract features from the file list CSV"""
        df = pd.read_csv(path)
        
        df['Parent Folder'] = [os.path.basename(os.path.dirname(p)) for p in df['File Path']]
       
        
        df['Type'] = df['Type'].map({'File': 1, 'Folder': 0})
       
        def days_ago(date_str):
            try:
                if pd.isna(date_str) or date_str == 'N/A':
                    return 0
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                return (datetime.now() - dt).days
            except Exception:
                return 0
        df['Last Modified'] = df['Last Modified'].apply(days_ago)
        df['Creation date'] = df['Creation date'].apply(days_ago)
        print(df.head())
        self.df = df
 # converts a row of the DataFrame into features for the model
    def feature_engineering(self, row):
        """Perform feature engineering on the DataFrame"""
        features = []
        # Example feature engineering steps
        features.append(self.hash_path(row['File Path']))# Hash of file path normalized
        features.append(row['Type'])  # File=1, Folder=0
        features.append(np.log1p(row['Size (bytes)']))  # Log size to reduce skew
        features.append(row['Last Modified']) 
        features.append(row['Creation date'])  
        features.append(self.hash_path(row['Parent Folder']))# Hash of parent folder normalized
        features.append(self.hash_path(row['File Type']))
        features.append(row['Special'])
        return features
        # Add more features as needed   
        
# converts the DataFrame into features and labels for training.    
    def prepare_data_train(self, df):
        """Prepare features and labels for training"""
        feature_list = []
        label_list = []
        if df.empty:
            return np.array(feature_list), np.array(label_list)
        
        if 'WTD' in df.columns:
            for _, row in df.iterrows():
                label_list.append(row['WTD'])
                feature_list.append(self.feature_engineering(row))
        else:
            for _, row in df.iterrows():
                    feature_list.append(self.feature_engineering(row))
                
                
        return np.array(feature_list), self.label_encoder.transform(label_list)

        
        
    
    def train(self, features, label):
        """Train the model with extracted features and label"""
        
        return self.brain.train(features, label)
        
                    
# Usage example
if __name__ == "__main__":
    # Create AI instance
    robo = brain()
    aitrainer = Trainer(robo)
    
    print("\n=== DEMO: Training the AI ===")
    path = ("/Users/abi/Desktop/desktop 2.0/foldermanagerai/filemanagerAI/data/test_list.csv")
      # Extract features from CSV
    aitrainer.extract_features(path)
    aitrainer.prepare_data_train(aitrainer.df)
    features, labels = aitrainer.prepare_data_train(aitrainer.df)
    
    aitrainer.train(features, labels)
    
    print("Training complete.")
    test_samplepath = ("/Users/abi/Desktop/desktop 2.0/foldermanagerai/filemanagerAI/data/te_list.csv")
    test = Trainer(robo)
    test.extract_features(test_samplepath)
    features, labels = test.prepare_data_train(aitrainer.df)
    result = test.brain.predict_batch(features)
  # Assuming 'result' is your list of dictionaries
# Determine the number of iterations based on the smaller list/DataFrame
num_iterations = min(len(result), len(test.df))

for i in range(num_iterations):
    # 'i' is the integer index
    res = result[i]
    
    print(f"File: {test.df.iloc[i]['File Path']}")
    print(f" Predicted Action: {res['action']} with confidence {res['confidence']:.2f}")
    print(f" Probabilities: {res['probabilities']}")
    print("-" * 40)
    i += 1
    print(i)
