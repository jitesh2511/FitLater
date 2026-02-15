import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fitlater.core.overview import analyze
import pandas as pd
import numpy as np

data = pd.DataFrame({'name':['Jitesh','Bhanuj','Deepak','Jitesh'],
                     'marks':[45, np.nan, 67, 45],
                     'age':[18,20,19,18],
                     'pass':[True, True, False, True],
                     'iq':['average', 'good', 'bad', 'average']})

print(analyze(data))