import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os
from action import actioner as slaver

class AI:
    def __init__(self):
        """The brain that predicts actions for files/folders"""
        # Create the Random Forest model with trial parameters (30 files/folders)
        self.forest = RandomForestClassifier(
            n_estimators=50,        # 50 trees as specified
            max_depth=6,           # Maximum depth of 6  
            min_samples_split=4,   # Need 4 samples to split
            min_samples_leaf=4,    # Need 4 samples in each leaf
            random_state=42        # For reproducibility
        )
        
        
        self.slaveer = slaver()
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(self.slaveer.categories())
        
        
        
        # Model state
        self.is_trained = False
        self.model_version = 0
    
    def load_model(self, model_path):
        """Load a pre-trained model from disk"""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.forest = model_data['forest']
            self.label_encoder = model_data['label_encoder'] 
            self.model_version = model_data.get('version', 0)
            self.is_trained = True
            
            print(f"Model loaded successfully (version {self.model_version})")
            return True
            
        except Exception as e:
            print(f"Failed to load model: {e}")
            return False
    
    def save_model(self, model_path):
        """Save the trained model to disk"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        
        model_data = {
            'forest': self.forest,
            'label_encoder': self.label_encoder,
            'version': self.model_version,
            'categories': self.categories
        }
        
        try:
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            print(f"Model saved successfully (version {self.model_version})")
            return True
            
        except Exception as e:
            print(f"Failed to save model: {e}")
            return False
    
    def train(self, features, labels):
        """Train the AI brain with prepared features and labels"""
        if len(features) == 0:
            raise ValueError("No training data provided")
        
        print(f"Training AI brain on {len(features)} samples...")
        
        # Fit the model
        self.forest.fit(features, labels)
        self.is_trained = True
        self.model_version += 1
        
        print(f"Training completed! Model version: {self.model_version}")
        return True
    
    def predict(self, features):
        """Predict action for a single file/folder based on its features"""
        if not self.is_trained:
            raise ValueError("AI brain not trained yet")
        
        # Ensure features is 2D array for sklearn
        if len(features) == 8:  # Single sample
            features = np.array([features])
        
        # Get prediction and probabilities
        prediction = self.forest.predict(features)[0]
        probabilities = self.forest.predict_proba(features)[0]
        
        # Convert prediction back to category name
        action = self.label_encoder.inverse_transform([prediction])[0]
        confidence = np.max(probabilities)
        
        return {
            'action': action,
            'confidence': confidence,
            'probabilities': dict(zip(self.categories, probabilities))
        }
    
    def predict_batch(self, features_list):
        """Predict actions for multiple files/folders"""
        if not self.is_trained:
            raise ValueError("AI brain not trained yet")
        
        features_array = np.array(features_list)
        predictions = self.forest.predict(features_array)
        probabilities = self.forest.predict_proba(features_array)
        
        results = []
        for i, (pred, probs) in enumerate(zip(predictions, probabilities)):
            action = self.label_encoder.inverse_transform([pred])[0]
            confidence = np.max(probs)
            
            results.append({
                'action': action,
                'confidence': confidence,
                'probabilities': dict(zip(self.slaveer.categories, probs))
            })
        
        return results
    
    def get_feature_importance(self):
        """Get feature importance from the trained model"""
        if not self.is_trained:
            raise ValueError("AI brain not trained yet")
        
        feature_names = [
            'Path Hash', 'Type', 'Log Size', 'Days Since Modified',
            'Days Since Created', 'Parent Folder Hash', 'File Type Hash', 'Special'
        ]
        
        importance = self.forest.feature_importances_
        return dict(zip(feature_names, importance))
    
    def get_model_info(self):
        """Get information about the current model"""
        return {
            'is_trained': self.is_trained,
            'model_version': self.model_version,
            'n_estimators': self.forest.n_estimators,
            'max_depth': self.forest.max_depth,
            'categories': self.categories,
            'feature_importance': self.get_feature_importance() if self.is_trained else None
        }
    
    def set_sleep_mode(self, sleep=True):
        """Put AI to sleep or wake it up (for coordination with Utils)"""
        self.is_sleeping = sleep
        status = "sleeping" if sleep else "awake"
        print(f"AI brain is now {status}")
