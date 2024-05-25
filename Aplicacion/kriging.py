
import numpy as np
import gstools as gs
import pandas as pd

from Procesamiento_data import tubos

def kriging_ordinario(combined_df):

    x = np.array(combined_df['x']).astype(float)
    y = np.array(combined_df['y']).astype(float)
    z = np.array(combined_df['z']).astype(float)
    cu_value = np.array(combined_df['CU%']).astype(float)
    
    model = gs.Spherical(dim=3, var=0.5, len_scale=1.5)

    krige = gs.krige.Ordinary(model, [x, y, z], cu_value)

    return krige


def predicciones(krige, data):
    x = np.array(data['x']).astype(float)
    y = np.array(data['y']).astype(float)
    z = np.array(data['z']).astype(float)
    cu_value = np.array(data['CU%']).astype(float)
    pred, varianza= krige([x,y,z])
    print(pred)
    print(cu_value)

    df= pd.DataFrame({"prediccion": pred, "real": cu_value})
    return df