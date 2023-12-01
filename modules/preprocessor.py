import pandas as pd
from datetime import datetime

def merge(B, C, A):
    i = j = k = 0

    # Convert 'Date' columns to datetime.date objects
    B['Date'] = pd.to_datetime(B['Date']).dt.date
    C['Date'] = pd.to_datetime(C['Date']).dt.date
    A['Date'] = pd.to_datetime(A['Date']).dt.date

    while i < len(B) and j < len(C):
      if B['Date'].iloc[i] <= C['Date'].iloc[j]:
        A['Date'].iloc[k] = B['Date'].iloc[i]
        A['Sales'].iloc[k] = B['Sales'].iloc[i]
        i += 1
        
      else:
        A['Date'].iloc[k] = C['Date'].iloc[j]
        A['Sales'].iloc[k] = C['Sales'].iloc[j]
        j += 1
      k += 1

    while i < len(B):
      A['Date'].iloc[k] = B['Date'].iloc[i]
      A['Sales'].iloc[k] = B['Sales'].iloc[i]
      i += 1
      k += 1

    while j < len(C):
      A['Date'].iloc[k] = C['Date'].iloc[j]
      A['Sales'].iloc[k] = C['Sales'].iloc[j]
      j += 1
      k += 1

    return A

def merge_sort(dataframe):
  if len(dataframe) > 1:
      center = len(dataframe) // 2
      left = dataframe.iloc[:center]
      right = dataframe.iloc[center:]
      merge_sort(left)
      merge_sort(right)

      return merge(left, right, dataframe)

  else:
     return dataframe

def drop (dataframe):
  def get_columns_containing(dataframe, substrings):
    return [col for col in dataframe.columns if any(substring.lower() in col.lower() for substring in substrings)]

  columns_to_keep = get_columns_containing(dataframe, ["date", "sale"])
  dataframe = dataframe.drop(columns=dataframe.columns.difference(columns_to_keep))
  dataframe = dataframe.dropna()
      
  return dataframe

def date_format(dataframe):
  for i, d, s in dataframe.itertuples():
    dataframe['Date'][i] = dataframe['Date'][i].strip()

  for i, d, s in dataframe.itertuples():
    new_date = datetime.strptime(dataframe['Date'][i], "%m/%d/%Y").date()
    dataframe['Date'][i] = new_date

    return dataframe

def group_to_three(dataframe):
  dataframe['Date'] = pd.to_datetime(dataframe['Date'])
  dataframe = dataframe.groupby([pd.Grouper(key='Date', freq='3D')])['Sales'].mean().round(2)
  dataframe = dataframe.replace(0, pd.np.nan).dropna()

  return dataframe