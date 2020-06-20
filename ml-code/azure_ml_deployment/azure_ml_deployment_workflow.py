#!/usr/bin/env python
# coding: utf-8

# In[27]:


from azureml.core import Workspace, Experiment, Run
import math, random, pickle
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment
from azureml.core.conda_dependencies import CondaDependencies


# Create the environment
myenv = Environment(name="myenv")
conda_dep = CondaDependencies()

# Define the packages needed by the model and scripts
conda_dep.add_pip_package("h5py")
conda_dep.add_pip_package("pillow")
conda_dep.add_pip_package("tensorflow")
conda_dep.add_conda_package("numpy")
conda_dep.add_pip_package("pandas")
conda_dep.add_conda_package("opencv")
conda_dep.add_pip_package("keras")
conda_dep.add_pip_package("scikit-image")
# Adds dependencies to PythonSection of myenv
myenv.python.conda_dependencies=conda_dep

inference_config = InferenceConfig(entry_script="score.py",
                                   environment=myenv)
ws = Workspace.from_config()

from azureml.core.model import Model
model = Model.register(model_path = "./models",
                       model_name = "weeddetector",
                       description = "Classifies weeds and crops",
                       workspace = ws)

from azureml.core.webservice import AciWebservice, Webservice
from azureml.core.model import Model

model = Model(ws, name='weeddetector')

deployment_config = AciWebservice.deploy_configuration(cpu_cores = 1, memory_gb = 1)
service = Model.deploy(ws, "aciservice", [model], inference_config, deployment_config)
service.wait_for_deployment(show_output = True)
print(service.state)
print("scoring URI: " + service.scoring_uri)




