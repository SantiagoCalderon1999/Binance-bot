import plotting
import pandas as np
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import A2C

def compare_data(array):
    plotting.plot_comparison(array)

def save(model, name):
    model.save(name)
    
def load(name):
    model = A2C.load(name)
    return model