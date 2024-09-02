import streamlit as st
import fastai.vision.all as fava
from pathlib import Path
import shutil, os
import json

class Model:
    def __init__(self, project: dict):
        print(project)
        self.key = project['key']
        self.title = project['title']
        self.description = project['description']
        self.categories = project['categories']
        self.default = project['default']
        self.new = project['new']
        self.model_root = Path(f'./data/{self.key}')
        self.model_root.parent.mkdir(parents=True, exist_ok=True)
        self.model_path = Path(f'./data/{self.key}/export.pkl')
        self.synch_folders()
        self.load_images()
    
    @property
    def settings(self):
        return {
            'title': self.title,
            'description': self.description,
            'categories': self.categories,
            'image_number': self.image_number,
            'default': self.default,
            'new': self.new
        }

    @settings.setter
    def settings(self, settings):
        self.title = settings['title']
        self.description = settings['description']
        self.categories = settings['categories']
        self.image_number = settings['image_number']
        self.default = settings['default']
        self.new = settings['new']
    
    @settings.getter
    def settings(self):
        return {
            'title': self.title,
            'description': self.description,
            'categories': self.categories,
            'image_number': self.image_number,
            'default': self.default,
            'new': self.new
        }
    
    def synch_folders(self):
        for cat in self.categories:
            (self.model_root/cat.lower()).mkdir(parents=True, exist_ok=True)
        
        # delete folders that are not a category
        folders = [f for f in self.model_root.iterdir() if f.is_dir()]
        for folder in folders:
            st.write(folder)
            if folder.name not in [x.lower() for x in self.categories]:
                shutil.rmtree(folder)
    
    def save():
        with open('./projects.json', 'w') as f:
            json.dump(st.session_state.projects_dict, f)

    def load_images(self):
        def are_folders_empty(root):
            # Check if there are any files in the directory or its subdirectories
            for subdir in os.listdir(root):
                subdir_path = os.path.join(root, subdir)
                if os.path.isdir(subdir_path) and os.listdir(subdir_path):
                    return False  # Found a non-empty folder
            return True  
        
        if not are_folders_empty(self.model_root):
            self.dls = fava.ImageDataLoaders.from_folder(
                self.model_root,
                train='.',
                valid_pct=0.2,
                item_tfms=fava.Resize(224),
                batch_tfms=fava.aug_transforms(size=224)
            )
    
    def train_model(self):
        learn = fava.cnn_learner(self.dls, fava.resnet34, metrics=fava.accuracy)
        learn.fine_tune(4)
        learn.export(self.model_path)
    
    def model_predict(self, file_path):
        learn_inf = fava.load_learner(self.model_path)
        img = fava.PILImage.create(file_path)
        self.pred, self.pred_idx, self.probs = learn_inf.predict(img)
        
