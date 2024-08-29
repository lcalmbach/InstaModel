from fastai.vision.all import *
import pathlib
import streamlit as st
import os

class Model:
    def __init__(self, image_path, theme):
        self.image_path = image_path
        self.theme = theme.replace(" ", "_").lower()
        self.model_path = pathlib.Path(f'./{self.theme}.pkl')
        
        # Ensure the model directory exists
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.dls = ImageDataLoaders.from_folder(
            self.image_path,
            train='.',
            valid_pct=0.2,
            item_tfms=Resize(224),
            batch_tfms=aug_transforms(size=224)
        )
    
    def train_model(self):
        learn = cnn_learner(self.dls, resnet34, metrics=accuracy)
        learn.fine_tune(4)
        learn.export(self.model_path)
    
    def model_predict(self, file_path):
        learn_inf = load_learner(pathlib.Path('./data/cities.pkl'))
        img = PILImage.create(file_path)
        self.pred, self.pred_idx, self.probs = learn_inf.predict(img)
        
