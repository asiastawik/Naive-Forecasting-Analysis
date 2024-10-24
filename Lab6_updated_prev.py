import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

pdfore = pd.read_csv("vic_elec_forecast_corr.csv")
pdfore.set_index('Time', inplace=True)
pdfore.index = pd.to_datetime(pdfore.index)

pdfore['weekday'] = pdfore.index.weekday #creating a new column called "weekday" that indicates the weekday of each observation (Monday = 0, Sunday = 6)

#a)
pdfore['1st naive_forecast'] = pdfore['Demand'].shift(1)
#print(pdfore)

#b)
pdfore['2nd naive_forecast'] = pdfore['Demand'].shift(48)
#print(pdfore)

#c)
holiday_or_sunday = []
current_date = datetime(2014, 12, 31, 23, 30)
date_range = pd.date_range(start='2014-12-31 23:30:00', end='2012-01-01 00:00:00', freq='-30min')

'''
while current_date >= datetime(2014, 12, 1, 0, 0):
    if current_date not in pdfore.index:
        current_date -= timedelta(minutes=30)
        continue
    else:
        if pdfore.loc[current_date, 'Holiday'] == 1 or pdfore.loc[current_date, 'weekday'] == 6:
            holiday_or_sunday.append(current_date)
            #print(holiday_or_sunday)
        current_date -= timedelta(minutes=30)
'''
#works faster, same result
holiday_or_sunday = pdfore[(pdfore['Holiday'] == 1) | (pdfore['weekday'] == 6)].index.tolist()

for date in date_range:
    if date not in pdfore.index:
        current_date -= timedelta(minutes=30)
        continue
    if date in holiday_or_sunday:
        previous_date = date - timedelta(days=1)
        while previous_date not in holiday_or_sunday and previous_date >= pdfore.index[0]:
            previous_date -= timedelta(days=1)
        if previous_date in holiday_or_sunday:
            pdfore.loc[date, '3rd naive_forecast'] = pdfore.loc[previous_date, 'Demand']
        elif previous_date < pdfore.index[0]:
            pdfore.loc[date, '3rd naive_forecast'] = np.nan
        else:
            pdfore.loc[date, '3rd naive_forecast'] = pdfore.loc[date, '2nd naive_forecast']

#d)
pdfore_2013_2014 = pdfore.loc['2013':'2014']
demand = pdfore_2013_2014['Demand']

pdfore_2013 = pdfore.loc['2013']
demand3 = pdfore_2013['Demand']

pd_mae_1st = pdfore_2013_2014['1st naive_forecast'].sub(demand).abs().mean()
pd_rmse_1st = ((pdfore_2013_2014['1st naive_forecast'] - demand) ** 2).mean() ** 0.5
#pd_rmse_1st3 = ((pdfore_2013['1st naive_forecast'] - demand3) ** 2).mean() ** 0.5
print(pd_mae_1st, pd_rmse_1st)

pd_mae_2nd = pdfore_2013_2014['2nd naive_forecast'].sub(demand).abs().mean()
pd_rmse_2nd = ((pdfore_2013_2014['2nd naive_forecast'] - demand) ** 2).mean() ** 0.5
#pd_rmse_2nd3 = ((pdfore_2013['2nd naive_forecast'] - demand3) ** 2).mean() ** 0.5
print(pd_mae_2nd, pd_rmse_2nd)

pd_mae_3rd = pdfore_2013_2014['3rd naive_forecast'].sub(demand).abs().mean()
pd_rmse_3rd = ((pdfore_2013_2014['3rd naive_forecast'] - demand) ** 2).mean() ** 0.5
#pd_rmse_3rd3 = ((pdfore_2013['3rd naive_forecast'] - demand3) ** 2).mean() ** 0.5
print(pd_mae_3rd, pd_rmse_3rd)

#print(pd_rmse_1st3, pd_rmse_2nd3, pd_rmse_3rd3)
pdfore_2013_2014.to_csv('pdfore_2013_2014.csv', index=True)

#e)
pdfore_daily = pdfore.resample("D").mean() #data being resampled daily ('D')
pdfore_daily['is_holiday'] = np.where(pdfore_daily['Holiday'] == 1, 'Holiday', 'Non-Holiday')
forecast_cols = ['1st naive_forecast', '2nd naive_forecast', '3rd naive_forecast']
#print(forecast_cols)

dfh = pdfore.loc[pdfore.Holiday == 1]
dfnh = pdfore.loc[pdfore.Holiday == 0]

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

for i, forecast_col in enumerate(forecast_cols):
    pdfore.loc[pdfore.Holiday == 1, f'{forecast_col}'] = (np.abs(
        pdfore.loc[pdfore.Holiday == 1, forecast_col] - pdfore.loc[pdfore.Holiday == 1, 'Demand']) / pdfore.loc[
                                                                   pdfore.Holiday == 1, 'Demand']) * 100
    pdfore.loc[pdfore.Holiday == 0, f'{forecast_col}'] = (np.abs(
        pdfore.loc[pdfore.Holiday == 0, forecast_col] - pdfore.loc[pdfore.Holiday == 0, 'Demand']) / pdfore.loc[
                                                                   pdfore.Holiday == 0, 'Demand']) * 100

    dfh.boxplot(column=[f'{forecast_col}'], by='Holiday', ax=axes[i], positions=[2])
    dfnh.boxplot(column=[f'{forecast_col}'], by='Holiday', ax=axes[i], positions=[1])

    axes[i].set_xticks([1, 2])
    axes[i].set_xticklabels(['Not Holiday', 'Holiday'])
    axes[i].set_title(f"Boxplot of MAPE for {forecast_col}")
    axes[i].set_ylabel('MAPE')

plt.tight_layout() #Adjust the padding between and around subplots
plt.show()

#f)
pdfore_mod = pd.read_csv("pdfore_2013_2014.csv")
pdfore_mod.set_index('Time', inplace=True)
pdfore_mod.index = pd.to_datetime(pdfore_mod.index)

pdfore_2013 = pdfore_mod.loc['2013']
#print(pdfore_2013)
forecasts = ['Demand_forecast1', 'Demand_forecast2', 'Demand_forecast3', '1st naive_forecast', '2nd naive_forecast', '3rd naive_forecast']
demand_2013 = pdfore_2013['Demand']

for i in forecasts:
    rmse = ((pdfore_2013[i] - demand_2013) ** 2).mean() ** 0.5
    #print(rmse)
    print(f"RMSE for {i}: {rmse}")

combos = []
for i in range(1, 7):
    combos += combinations(forecasts, i)

best_combo = None
best_rmse = float('inf')
rmse_values = []

for combo in combos:
    combined_forecast = pdfore_2013[list(combo)].mean(axis=1)
    rmse = ((combined_forecast - pdfore_2013['Demand']) ** 2).mean() ** 0.5
    #print(rmse)
    #print(combo)

    #Update the best combination and RMSE
    if rmse < best_rmse:
        best_combo = combo
        best_rmse = rmse

    #print(f"RMSE for combination {combo}: {rmse}")
    rmse_values.append(rmse)

print(f"Best combination: {best_combo}")
print(f"RMSE for best combination: {best_rmse}")

plt.hist(rmse_values, bins=20)
plt.title(f"Histogram of RMSE values for all combined forecasts ({len(combos)} combinations)")
plt.xlabel("RMSE")
plt.ylabel("Frequency")
plt.show()

#g)
pdfore_2014 = pdfore_mod.loc['2014']
best_combo_mae = []
for forecast in best_combo:
    mae = pdfore_2014[forecast].loc['2014-03'].sub(pdfore_2014['Demand'].loc['2014-03']).abs().mean()
    print(f"The MAE of {forecast} in March 2014 is {mae:.2f}.")
    best_combo_mae.append(mae)

#first solution - wrong
average_mae = sum(best_combo_mae) / len(best_combo_mae)
print(f"The MAE of {best_combo} is March 2014 is {average_mae:.2f}.")

#second idea - correct
#pdfore_2014.loc[:, 'birthday_combination'] = pdfore_2014.loc[:, best_combo].mean(axis=1)
pdfore_2014_copy = pdfore_2014.copy()
pdfore_2014_copy.loc[:, 'birthday_combination'] = pdfore_2014_copy.loc[:, best_combo].mean(axis=1)
birthday_mae = pdfore_2014_copy.loc['2014-03', 'birthday_combination'].sub(pdfore_2014_copy.loc['2014-03', 'Demand']).abs().mean()
print('The MAE of the best combination in March 2014 is', birthday_mae)


