from models import Querydata
from visual import Visual
from matplotlib import pyplot
import pandas as pd
query = Querydata()
visual = Visual()
vn_json = query.read_json_vn()

def allProvinces():
    data = query.climate_disease_LSTM()
    provinces=data.province_name.unique()
    y = query.read_heatmap_population()
    y = y.drop_duplicates(subset="province_name", keep="first")
    temp = y[["province_name", "fips"]]
    columns=query.get_columns()
    climate = columns['climate1'].append(columns['climate2'].dropna())
    climate=climate.values
    climate=climate.reshape(-1)
    climateArray=[]
    for each in climate:
        print("x")
        climateArray.append(each)
    print(climateArray)
    disease='influenza'
    columns=['province_code', 'province_name', 'year', 'date1', disease]
    columns=climateArray+columns
    data = query.climate_disease_LSTM()
    data = data.loc[:, data.columns.isin(columns)]
    data = data.loc[:, ~data.columns.duplicated()]
    print(data)
    dataset=[]
    for each in provinces:
        try:
            print(each)
            mulit_rmse,multi_history=visual.LSTM_evaluate(data, disease, each, climateArray, 1998, 2010, 2016)
            pyplot.plot(multi_history.history['loss'], label='train')
            pyplot.plot(multi_history.history['val_loss'], label='test')
            pyplot.title(each+"- Multivariate LSTM")
            pyplot.legend()
            pyplot.show()

            uni_rmse,uni_history=visual.LSTM_univariate_test(data, disease, each, 1998, 2010, 2016)
            pyplot.plot(uni_history.history['loss'], label='train')
            pyplot.plot(multi_history.history['val_loss'], label='test')
            pyplot.title(each + "- Univariate LSTM")
            pyplot.legend()
            pyplot.show()
        except:
            mulit_rmse="Insufficient Data"
            uni_rmse = "Insufficient Data"
        tempDataSet = [each, mulit_rmse, uni_rmse]
        dataset.append(tempDataSet)
        resultsDF=pd.DataFrame(dataset,columns=["province_name","multi_rmse", "uni_rmse"])
    resultsDF=(pd.merge(resultsDF, temp, on='province_name'))
    return resultsDF

#ModelResults=allProvinces()
#ModelResults.to_csv(r'D:\Downloads\ModelResults.csv', index = False, header=True)

y = query.read_heatmap_population()
y = y.drop_duplicates(subset="province_name", keep="first")
temp = y[["province_name", "fips"]]
print(temp)
def test():
    data = query.climate_disease_LSTM()
    provinces = data.province_name.unique()
    y = query.read_heatmap_population()
    y = y.drop_duplicates(subset="province_name", keep="first")
    temp = y[["province_name", "fips"]]
    print(temp)
    columns = query.get_columns()
    climate = columns['climate1'].append(columns['climate2'].dropna())
    climate = climate.values
    climate = climate.reshape(-1)
    climateArray = []
    for each in climate:
        print("x")
        climateArray.append(each)
    print(climateArray)
    disease = 'influenza'
    columns = ['province_code', 'province_name', 'year', 'date1', disease]
    columns = climateArray + columns
    data = query.climate_disease_LSTM()
    data = data.loc[:, data.columns.isin(columns)]
    data = data.loc[:, ~data.columns.duplicated()]
    print(data)
    dataset = []
    x=345
    for each in provinces:
        try:
            rmse=x
            x=x+1
        except:
            rmse = "Insufficient Data"
        tempDataSet = [each, rmse]
        dataset.append(tempDataSet)
        resultsDF = pd.DataFrame(dataset, columns=["province_name", "rmse"])
        print(resultsDF)
    resultsDF=(pd.merge(resultsDF, temp, on='province_name'))
    return resultsDF


