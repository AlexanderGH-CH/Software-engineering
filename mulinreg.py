# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 18:10:31 2021

@author: Alexander
"""

# Import modules to process data and create the model
# Import numpy
import numpy as np
# Import pandas
import pandas as pd
# Import sklearn libraries to create the model
from sklearn.model_selection import train_test_split
# from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
# Import matplotlip to plot results
import matplotlib.pyplot as plt
# Import seaborn
import seaborn as sns
# Customized float (4 after the dot) formatting in a pandas DataFrame
pd.options.display.float_format = '{:.4f}'.format

def find_properties(rooms, typeprop, location, price):
    """ Find the properties with the specified characteristics"""
    if price == 0:
        found_properties = (df[(df['rooms'] == rooms) & (df['Type'] == typeprop) &
                               (df['Location'] == location)])
    else:
        # If price is given then only properties that cost less or that are
        # equal to the provided price are displayed
        found_properties = (df[(df['rooms'] == rooms) & (df['Type'] == typeprop) &
                               (df['Location'] == location) & (df['Price'] <= price)])
    return found_properties

# Load input data
Data = pd.read_excel(r'C:\Users\Alexander\Desktop\history.xlsx',
                     sheet_name='history_data')
# print(Data)
X = Data.drop(["Property_ID", "Price"], axis=1)
y = Data['Price'].values

# Split the data into training and test
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.33,
                                                    random_state=101)

# Scale the variables
s_scaler = StandardScaler()
X_train = s_scaler.fit_transform(X_train.astype(np.float))
X_test = s_scaler.transform(X_test.astype(np.float))

# Multiple Liner Regression
regressor = LinearRegression()
regressor.fit(X_train, y_train)
# Evaluate the model (intercept and slope)
# print(regressor.intercept_)
# print(regressor.coef_)
# Predicting the test set result
y_pred = regressor.predict(X_test)
# Put results as a DataFrame
coeff_df = pd.DataFrame(regressor.coef_, columns = ['Coefficient'])

# Visualizing residuals
fig = plt.figure(figsize= (10, 5))
residuals = (y_test- y_pred)
sns.distplot(residuals)

# Compare actual output values with predicted values
y_pred = regressor.predict(X_test)
df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
df1 = df.head(10)

# Evaluate the performance of the algorithm (MAE - MSE - RMSE)
# print('MAE:', metrics.mean_absolute_error(y_test, y_pred))
# print('MSE:', metrics.mean_squared_error(y_test, y_pred))
# print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
# print('VarScore:', metrics.explained_variance_score(y_test, y_pred))

# Import the property dataset to make the predictions
Property_data = pd.read_excel(r'C:\Users\Alexander\Desktop\property.xlsx',
                              sheet_name = 'Sheet1')

# Drop the columns list ID and Price
Property = Property_data.drop(['List_ID', 'Price'], axis=1)
# Scale the variables
Property = s_scaler.fit_transform(Property.astype(np.float))

# Use the multilinear regression model to predict the price
Y_pred = regressor.predict(Property)
# Reshape the numpy array to 250:1 to append it to a new dataframe
b = np.array([Y_pred])
b = np.reshape(b, (250, 1))
predictions = pd.DataFrame({'Predictions': b[:, 0]})

# Concatonate the two dataframes (Property_data and predictions) to one
df = pd.concat([Property_data, predictions], axis = 1)
df = df.rename(columns = {'#room': 'rooms'})