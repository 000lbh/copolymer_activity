import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import KFold

# Merged to predict.py
def base_predict():
    data = pd.read_csv('data/trainval.csv')
    data["A1A2"] = data["A1"] * data["A2"] / 0.25
    data["A1A3"] = data["A1"] * data["A3"] / 0.25
    data["A2A3"] = data["A2"] * data["A3"] / 0.25
    data["A1A2A3"] = data["A1"] * data["A2"] * data["A3"] / 0.125

    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    MAE, RMSE, R2 = [], [], []
    for train_index, test_index in kf.split(data):
        MAE.append([])
        RMSE.append([])
        R2.append([])
        train, val = data.iloc[train_index], data.iloc[test_index]
        train_X = train.drop(['Activity','A4'], axis=1)
        train_y = train['Activity'].values
        val_X = val.drop(['Activity','A4'], axis=1)
        val_y = val['Activity'].values
        baseline_models = [LinearRegression(), BayesianRidge(), MLPRegressor(), KNeighborsRegressor(), SVR(), RandomForestRegressor(), XGBRegressor()]
        for model in baseline_models:
            model.fit(train_X, train_y)
            pred = model.predict(val_X)
            MAE[-1].append(mean_absolute_error(val_y, pred))
            RMSE[-1].append(mean_squared_error(val_y, pred)**0.5)
            R2[-1].append(r2_score(val_y, pred))
    MAE = np.array(MAE)
    RMSE = np.array(RMSE)
    R2 = np.array(R2)
    for idx, model_name in enumerate(['LinearRegression', 'BayesianRidge', 'MLPRegressor', 'KNeighborsRegressor', 'SVR', 'RandomForestRegressor', 'XGBRegressor']):
        print(model_name+'\n'+'MAE:', round(np.mean(MAE[:, idx]).item(), 4), 'RMSE:', round(np.mean(RMSE[:, idx]).item(), 4), 'R2:', round(np.mean(R2[:, idx]).item(), 4))
    
if __name__ == '__main__':
    base_predict()