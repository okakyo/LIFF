#外部から学習器として、サーバーよりデータを予測、回帰する。

import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import KFold,GridSearchCV
from sklearn.naive_bayes import BernoulliNB
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

