import numpy as np
import pandas as pd
from datetime import datetime
import pmdarima as pm
from pmdarima import auto_arima

def train_test(dataframe, n):
  training_y = dataframe.iloc[:-n,0]
  test_y = dataframe.iloc[-n:,0]
  test_y_series = pd.Series(test_y, index=dataframe.iloc[-n:, 0].index)
  training_X = dataframe.iloc[:-n,1:]
  test_X = dataframe.iloc[-n:,1:]
  future_X = dataframe.iloc[0:,1:]
  return (training_y, test_y, test_y_series, training_X, test_X, future_X)

def model_fitting(dataframe, Exo):
    futureModel = pm.auto_arima(dataframe['Sales'], X=Exo, start_p=1, start_q=1,
                         test='adf',min_p=1,min_q=1,
                         max_p=3, max_q=3, m=12,
                         start_P=0, seasonal=True,
                         d=None, D=1, trace=True,
                         error_action='ignore',
                         suppress_warnings=True,
                         stepwise=True)
    model = futureModel
    return model

def test_fitting(dataframe, Exo, trainY):
    trainTestModel = auto_arima(X = Exo, y = trainY, start_p=1, start_q=1,
                           test='adf',min_p=1,min_q=1,
                           max_p=3, max_q=3, m=12,
                           start_P=0, seasonal=True,
                           d=None, D=1, trace=True,
                           error_action='ignore',
                           suppress_warnings=True,
                           stepwise=True)
    model = trainTestModel
    return model

def forecast_accuracy(forecast, actual):
    mape = np.mean(np.abs(forecast - actual)/np.abs(actual)).round(4)  # MAPE
    rmse = (np.mean((forecast - actual)**2)**.5).round(2)  # RMSE
    corr = np.corrcoef(forecast, actual)[0,1]   # corr
    mins = np.amin(np.hstack([forecast[:,None],
                            actual[:,None]]), axis=1)
    maxs = np.amax(np.hstack([forecast[:,None],
                            actual[:,None]]), axis=1)
    minmax = 1 - np.mean(mins/maxs)             # minmax
    return({'mape':mape, 'rmse':rmse, 'corr':corr, 'min-max':minmax})

def sales_growth(dataframe, fittedValues):
    sales_growth = fittedValues.to_frame()
    sales_growth = sales_growth.reset_index()
    sales_growth.columns = ("Date", "Sales")
    sales_growth = sales_growth.set_index('Date')

    sales_growth['Sales'] = (sales_growth['Sales']).round(2)

    #Calculate and create the column for sales difference and growth
    sales_growth['Forecasted Sales First Difference']=(sales_growth['Sales']-sales_growth['Sales'].shift(1)).round(2)
    sales_growth['Forecasted Sales Growth']=(((sales_growth['Sales']-sales_growth['Sales'].shift(1))/sales_growth['Sales'].shift(1))*100).round(2)

    #Calculate and create the first row for sales difference and growth
    sales_growth['Forecasted Sales First Difference'].iloc[0] = (dataframe['Sales'].iloc[-1]-dataframe['Sales'].iloc[-2]).round(2)
    sales_growth['Forecasted Sales Growth'].iloc[0]=(((dataframe['Sales'].iloc[-1]-dataframe['Sales'].iloc[-2])/dataframe['Sales'].iloc[-1])*100).round(2)


    return sales_growth