from flask import Flask, render_template, json, request, url_for, jsonify
from flask_assets import Bundle, Environment
from models import Querydata
from visual import Visual
import pandas as pd
################################################
app = Flask(__name__)
bundles = {
    # js
    'main_js': Bundle('js/myjs/home.js',
                      'js/myjs/myscript.js',
                      'js/myjs/explore.js',
                      'js/myjs/compare.js',
                      'js/myjs/factor.js',
                      output='js/myjs/gen/main.js'),
    'lib_js': Bundle(
        'js/myjs/lib/jquery.min.js',
        'js/myjs/lib/plotly-latest.min.js',
        'js/myjs/lib/popper.js',
        output='js/lib/gen/lib.js'),
    # css
    'main_css': Bundle('css/mycss/summary.css',
                       'css/mycss/explore.css',
                       'css/mycss/map.css',
                       'css/mycss/compare.css',
                       'css/mycss/mycss.css',
                       output='css/mycss/gen/my_main.css'),
    'lib_css': Bundle('css/mycss/lib/bootstrap.min.css',

                      output='css/lib/gen/lib.css'),

}
assets = Environment(app)
assets.register(bundles)
# connect database
query = Querydata()
visual = Visual()
vn_json = query.read_json_vn()
##################################################

def listToString(s):
    str1 = " "
    for ele in s:
        str1 += ele
    return str1


@app.route('/')
def summary():
    columns = query.get_columns()
    # get columns disease
    disease = columns['disease']
    disease = disease.drop([1, 3, 5])
    # get columns climate
    climate1 = columns['climate1'].append(columns['climate2'].dropna())
    # get columns climate 2
    climate2 = columns['climate2'].dropna()
    climate1 = climate1.reset_index(drop=True)
    climate1 = climate1.drop([10, 11])
    data = query.groupby_disease_year()
    years = data['year'].nunique()
    diseases = query.read_disease()
    data2 = query.disease_death_rate()
    barJson = visual.bar_chart_disease(data2)
    barJsonDeath = visual.bar_chart_disease_death(data2)
    barStackDeath = visual.bar_chart_month_disease_death(diseases, years)
    barStack = visual.bar_chart_month_disease(diseases, years)
    return render_template('home.html',
                           disease=disease,
                           climate1=climate1,
                           climate2=climate2,
                           barJson=barJson,
                           barJsonDeath=barJsonDeath,
                           barStack=barStack,
                           barStackDeath=barStackDeath
                           )
# response data home


@app.route("/summary_response", methods=['GET', 'POST'])
def summary_response():
    data = query.read_heatmap_population()
    disease = query.read_disease()

    begin = request.args['begin']
    end = request.args['end']
    data = data[data['year'].between(int(begin), int(end))]
    disease = disease[disease['year'].between(int(begin), int(end))]
    #end between time
    feature_selected = []
    # get attribute columns
    years = data['year'].nunique()


    disease = (disease.groupby(["year", "month", "province_code"], as_index=False).first())
  #  print(disease.head(100).to_string())

    cases_per_year = disease.groupby(["year"]).sum()
  #  print(cases_per_year.head(100).to_string())



    feature_selected.append(
        {
            'population': round(data['population'].sum(), 0),
            'influenza_mean_cases': round(disease['influenza'].sum()/years, 0),
            'influenza_mean_deaths': round(disease['influenza_death'].sum()/years, 0),
            'influenza_min_cases': round(cases_per_year['influenza'].min(), 0),
            'year_min_influenza': cases_per_year.influenza.idxmin(),
            'influenza_min_deaths': round(cases_per_year['influenza_death'].min(), 0),
            'year_min_death_influenza': cases_per_year.influenza_death.idxmin(),
            'influenza_max_cases': round(cases_per_year['influenza'].max(), 0),
            'year_max_influenza': cases_per_year.influenza.idxmax(),
            'influenza_max_deaths': round(cases_per_year['influenza_death'].max(), 0),
            'year_max_death_influenza': cases_per_year.influenza_death.idxmax(),
            'diarrhoea_mean_cases': round(disease['diarrhoea'].sum()/years, 0),
            'diarrhoea_mean_deaths': round(disease['diarrhoea_death'].sum() / years, 0),
            'diarrhoea_min_cases': round(cases_per_year['diarrhoea'].min(), 0),
            'year_min_diarrhoea': cases_per_year.diarrhoea.idxmin(),
            'diarrhoea_min_deaths': round(cases_per_year['diarrhoea_death'].min(), 0),
            'year_min_death_diarrhoea': cases_per_year.diarrhoea_death.idxmin(),
            'diarrhoea_max_cases': round(cases_per_year['diarrhoea'].max(), 0),
            'year_max_diarrhoea': cases_per_year.diarrhoea.idxmax(),
            'diarrhoea_max_deaths': round(cases_per_year['diarrhoea_death'].max(), 0),
            'year_max_death_diarrhoea': cases_per_year.diarrhoea_death.idxmax(),
            'dengue_mean_cases': round(disease['dengue_fever'].sum()/years, 0),
            'dengue_mean_deaths': round(disease['dengue_fever_death'].sum() / years, 0),
            'dengue_min_cases': round(cases_per_year['dengue_fever'].min(), 0),
            'year_min_dengue': cases_per_year.dengue_fever.idxmin(),
            'dengue_min_deaths': round(cases_per_year['dengue_fever_death'].min(), 0),
            'year_min_death_dengue': cases_per_year.dengue_fever_death.idxmin(),
            'dengue_max_cases': round(cases_per_year['dengue_fever'].max(), 0),
            'year_max_dengue': cases_per_year.dengue_fever.idxmax(),
            'dengue_max_deaths': round(cases_per_year['dengue_fever_death'].max(), 0),
            'year_max_death_dengue': cases_per_year.dengue_fever_death.idxmax(),

        }
    )

    return jsonify({'data': render_template('response_home.html',
                                            feature_selected=feature_selected)})

# data date1 home


@app.route('/date1_home_disease', methods=['GET', 'POST'])
def date1_home_disease():

    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']

    data = query.read_disease()
    line = visual.line_date1_home(data, disease, begin, end)
    return line
# data disease date1 home region


@app.route('/mortality_home_disease', methods=['GET', 'POST'])
def year_mortality_home_disease():

    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']

    data = query.read_disease()
    line = visual.line_mortality_home(data, disease, begin, end)
    return line


@app.route('/month_home_disease', methods=['GET', 'POST'])
def month_home_disease():

    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']

    data = query.read_disease()
    line = visual.line_month_disease(data, disease, begin, end)
    return line


@app.route('/region_date1_disease_home', methods=['GET', 'POST'])
def region_date1_disease_home():

    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['region']

    data = query.region_disease_month(region)
    line = visual.region_date1_exp(data, disease, begin, end)
    return line
# data date1 climate home


@app.route('/date1_home_climate', methods=['GET', 'POST'])
def date1_home_climate():

    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']

    data = query.read_climate()
    line = visual.line_date1_climate_exp(data, climate, begin, end)
    return line
# region date1 climate


@app.route('/line_monthly_climate', methods=['GET', 'POST'])
def line_monthly_climate():
    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']

    data=query.read_climate()
    line = visual.line_monthly_climate(data, climate, begin, end)
    return line


@app.route('/line_province_climate',methods=['GET', 'POST'])
def line_province_climate():
    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']

    data = query.read_climate_province()
    line = visual.line_province_climate(data, climate, begin, end)
    return line


@app.route('/region_date1_climate_home', methods=['GET', 'POST'])
def region_date1_climate_home():

    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['region']

    data = query.region_climate_month(region)
    line = visual.region_date1_climate_exp(data, climate, begin, end)
    return line
# disease ca nuoc heatmap VN


@app.route('/heatmap_vn', methods=['GET', 'POST'])
def heatmap_vn():
    df = query.read_heatmap_disease()

    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']

    VNJson = visual.heatmap_vn(df, vn_json, disease, begin, end)
    return VNJson
# line chart disease ca nuoc


@app.route('/line_chart_disease', methods=['GET', 'POST'])
def line_chart_disease():

    
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    mean = query.groupby_disease_year()
    max_ = query.groupby_disease_max()
    min_ = query.groupby_disease_min()
    LineJson = visual.stat_disease_year(mean,max_,min_ ,disease, begin, end)
    
    return LineJson
# population ca nuoc

@app.route('/casesAndDeaths', methods=['GET', 'POST'])
def cases_and_deaths_disease():
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    df=query.disease_death_rate()
    LineJson = visual.casesAndDeathsChart(df, disease, begin, end)

    return LineJson


# population ca nuoc

@app.route('/heatmap_population', methods=['GET', 'POST'])
def heatmap_population():

    data = query.read_heatmap_population()

    begin = request.args['begin']
    end = request.args['end']

    VNJson = visual.heatmap_population(data, vn_json, begin, end)

    return VNJson
# line chart population


@app.route('/line_chart_population', methods=['GET', 'POST'])
def line_chart_population():
    data = query.read_heatmap_population()
    data = data.groupby(["date1", "province_name"], as_index=False).first()

    begin = request.args['begin']
    end = request.args['end']

    line = visual.line_chart_population(data, begin, end)

    return line
# chart region population


@app.route('/chart_region_population', methods=['GET', 'POST'])
def chart_region_population():
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['region']
    data = query.read_region_population(region)
    line = visual.chart_region_population(data, begin, end)

    return line
# ratio disease/population ca nuoc


@app.route('/heatmap_ratio', methods=['GET', 'POST'])
def heatmap_ratio():

    data = query.read_heatmap_ratio()

    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']

    VNJson = visual.heatmap_ratio(data, vn_json, disease, begin, end)
    return VNJson
# line chart ratio


@app.route('/line_chart_ratio', methods=['GET', 'POST'])
def line_chart_ratio():

    data = query.read_heatmap_ratio()

    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']

    line = visual.line_chart_ratio(data, disease, begin, end)
    return line
# line chart ratio region


@app.route('/chart_region_ratio', methods=['GET', 'POST'])
def chart_region_ratio():
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['region']
    disease = request.args['disease']
    data = query.region_heatmap_ratio(region)
    line = visual.chart_region_ratio(data, disease, begin, end)

    return line
# climate ca nuoc


@app.route('/heatmap_climate', methods=['GET', 'POST'])
def heatmap_climate():
    data = query.read_heatmap_climate()

    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']

    VNJson = visual.heatmap_climate(data, vn_json, climate, begin, end)
    return VNJson


# line chart climate ca nuoc


@app.route('/line_chart_climate', methods=['GET', 'POST'])
def line_chart_climate():
    data = query.read_climate()
    # df_max = query.read_climate_max()
    # df_min = query.read_climate_min()

    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']

    LineJson = visual.box_chart_mean_feature(data, climate, begin, end)

    return LineJson
##########################################################

# line chart disease region tung vung mien


@app.route('/line_chart_region_disease', methods=['GET', 'POST'])
def line_chart_region_disease():

    disease = request.args['disease']
    region = request.args['region']
    begin = request.args['begin']
    end = request.args['end']

    mean = query.mean_region_disease_year(region)
    max_ = query.max_region_disease(region)
    min_ = query.min_region_disease(region)

    LineJson = visual.stat_disease_year(mean,max_,min_,disease, begin, end)

    return LineJson
# line chart climate region tung vung mien


@app.route('/line_chart_region_climate', methods=['GET', 'POST'])
def line_chart_region_climate():

    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['region']

    data = query.region_climate_month(region)

    LineJson = visual.box_chart_mean_feature(data, climate, begin, end)

    return LineJson
# heatmap climate region tung vung mien


@app.route('/heatmap_climate_region', methods=['GET', 'POST'])
def heatmap_climate_region():

    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['region']

    data = query.region_heatmap_climate(region)

    VNJson = visual.heatmap_climate(data, vn_json, climate, begin, end)
    return VNJson
# heatmap disease viet nam


@app.route('/heatmap_vn_region', methods=['GET', 'POST'])
def heatmap_vn_region():

    disease = request.args['disease']
    region = request.args['region']
    begin = request.args['begin']
    end = request.args['end']

    data = query.region_heatmap_disease(region)

    LineJson = visual.heatmap_vn_region(data, vn_json, disease, begin, end)

    return LineJson
# heatmap population


@app.route('/yearlyCaseNumbersTrendLines', methods=['GET', 'POST'])
def yearlyCaseNumbersTrendLine():
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    data = query.read_disease()

    VNJSON= visual.yearlyCaseNumbersTrendLines(data, disease, begin, end)

    return VNJSON


@app.route('/compYearlyCaseNumbersTrendLines', methods=['GET', 'POST'])
def compYearlyCaseNumbersTrendLine():
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    province = request.args['province']
    data = query.compare_province_trend(province)
    print(list(data.columns))

    VNJSON= visual.compYearlyCaseNumbersTrendLines(data, disease, begin, end)

    return VNJSON


@app.route('/yearlyClimateNumbersTrendLines', methods=['GET','POST'])
def yearlyClimateNumbersTrendLines():
    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']
    data = query.read_climate()
    line = visual.yearlyClimateNumbersTrendLines(data, climate, begin, end)
    return line


@app.route('/monthlyCaseNumbersTrendLines', methods=['GET','POST'])
def monthlyCaseNumbersTrendLines():
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    data = query.read_disease()

    VNJSON= visual.monthlyCaseNumbersTrendLines(data, disease, begin, end)

    return VNJSON

@app.route('/heatmap_pop_region', methods=['GET', 'POST'])
def heatmap_pop_region():

    # disease = request.args['disease']
    region = request.args['region']
    begin = request.args['begin']
    end = request.args['end']

    data = query.region_heatmap_population(region)

    VNJson = visual.heatmap_pop_region(data, vn_json, begin, end)

    return VNJson
# heatmap ratio


@app.route('/heatmap_radio_region', methods=['GET', 'POST'])
def heatmap_radio_region():

    disease = request.args['disease']
    region = request.args['region']
    begin = request.args['begin']
    end = request.args['end']

    data = query.region_heatmap_ratio(region)

    VNJson = visual.heatmap_radio_region(data, vn_json, disease, begin, end)

    return VNJson

########################### explorer pages#######################


@app.route('/explore', methods=['GET', 'POST'])
def explore():
    columns = query.get_columns()
    # get columns disease
    disease = columns['disease']
    disease = disease.drop([1, 3, 5])
    # get columns climate
    climate1 = columns['climate1'].append(columns['climate2'].dropna())
    # get columns climate 2
    climate2 = columns['climate2'].dropna()
    climate1 = climate1.reset_index(drop=True)
    climate1 = climate1.drop([10, 11])
    # name province
    province_name = query.get_province_name()
    province_code = query.get_province_code()
    # province=zip(province_name, province_code)
    # request data
    return render_template('explore.html',
                           disease=disease,
                           climate1=climate1,
                           climate2=climate2,
                           province=zip(province_name, province_code),
                           )
# information province response


@app.route("/explore_response/<id>")
def explore_response(id):
    data = query.population_province_exp(id)
    disease = query.disease_month_exp(id)
    begin = request.args['begin']
    end = request.args['end']
    data = data[data['year'].between(int(begin), int(end))]
    disease = disease[disease['year'].between(int(begin), int(end))]


    disease = (disease.groupby(["year", "month"], as_index=False).first())

    cases_per_year = disease.groupby(disease["year"]).sum()

    years = data['year'].nunique()

    feature_selected = []
    # get attribute columns
    feature_selected.append(
        {
            'name': listToString(data['province_name'].unique()),
            'population': round(data['population'].mean(), 4),
            'influenza': round(cases_per_year['influenza'].sum()/years, 4),
            'diarrhoea': round(cases_per_year['diarrhoea'].sum()/years, 4),
            'dengue': round(cases_per_year['dengue_fever'].sum()/years, 4)

        }
    )

    return jsonify({'data': render_template('explore_response.html',
                                            feature_selected=feature_selected)})
# information province climate


@app.route("/exp_climate_response/<id>", methods=['GET', 'POST'])
def exp_climate_response(id):
    climate = query.climate_month_exp(id)
    begin = request.args['begin']
    end = request.args['end']
    climate = climate[climate['year'].between(int(begin), int(end))]
    years = climate['year'].nunique()


    feature_selected = []

    feature_selected.append(
        {
            'vaporation': round(climate['vaporation'].mean(), 4),
            'rain': round(climate['rain'].mean(), 4),
            'raining_day': round(climate['raining_day'].mean(), 4),
            'temperature': round(climate['temperature'].mean(), 4),
            'temperature_max': round(climate['temperature_max'].mean(), 4),
            'temperature_min': round(climate['temperature_min'].mean(), 4),
            'temperature_absolute_min': round(climate['temperature_abs_min'].sum()/years, 4),
            'temperature_absolute_max': round(climate['temperature_abs_max'].sum()/years, 4),
            'sun_hour': round(climate['sun_hour'].mean(), 4),
            'humidity': round(climate['humidity'].mean(), 4),
            'humidity_min': round(climate['humidity_min'].mean(), 4),
        }
    )

    return jsonify({'data': render_template('exp_climate_response.html',
                                            feature_selected=feature_selected)})
# region disease response


@app.route("/explore_response_region/<id>", methods=['GET', 'POST'])
def explore_response_region(id):
    data = query.read_region_population(id)
    disease = query.region_heatmap_disease(id)
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['name']
    # data = data[data['year'].between(int(begin), int(end))]
    # disease = disease[disease['year'].between(int(begin), int(end))]

    feature_selected = []
    # get attribute columns
    feature_selected.append(
        {
            'name': region,
            'population': round(data['population'].sum(), 4),
            'influenza': round(disease['influenza'].sum(), 4),
            'diarrhoea': round(disease['diarrhoea'].sum(), 4),
            'dengue': round(disease['dengue_fever'].sum(), 4)
        }
    )

    return jsonify({'data': render_template('explore_response.html',
                                            feature_selected=feature_selected)})
# region climate response


@app.route("/explore_region_climate/<id>", methods=['GET', 'POST'])
def explore_region_climate(id):
    climate = query.region_heatmap_climate(id)
    begin = request.args['begin']
    end = request.args['end']
    # climate = climate[climate['year'].between(int(begin), int(end))]
    feature_selected = []
    # get attribute columns
    feature_selected.append(
        {
            'vaporation': round(climate['vaporation'].sum(), 4),
            'rain': round(climate['rain'].sum(), 4),
            'max_rain': round(climate['max_rain'].sum(), 4),
            'raining_day': round(climate['raining_day'].sum(), 4),
            'temperature': round(climate['temperature'].sum(), 4),
            'temperature_max': round(climate['temperature_max'].sum(), 4),
            'temperature_min': round(climate['temperature_min'].sum(), 4),
            'temperature_absolute_min': round(climate['temperature_abs_min'].sum(), 4),
            'temperature_absolute_max': round(climate['temperature_abs_max'].sum(), 4),
            'sun_hour': round(climate['sun_hour'].sum(), 4),
            'humidity': round(climate['humidity'].sum(), 4),
            'humidity_min': round(climate['humidity_min'].sum(), 4),
        }
    )

    return jsonify({'data': render_template('exp_climate_response.html',
                                            feature_selected=feature_selected)})
# show chart in here lag correlation disease

# lag disease


@app.route('/lag_correlation', methods=['GET', 'POST'])
def lag_correlation():
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    province = request.args['province']
    data = query.lag_query(province)
    lag = visual.lag_correlation(data, disease, begin, end)
    return lag
# lag region disease


@app.route('/lag_region_disease', methods=['GET', 'POST'])
def lag_region_disease():
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['region']
    data = query.region_disease(region)
    lag = visual.lag_correlation(data, disease, begin, end)
    return lag

# lag climate correlation


@app.route('/lag_climate_correlation', methods=['GET', 'POST'])
def lag_climate_correlation():
    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']
    province = request.args['province']
    data = query.lag_query_climate(province)
    lag = visual.lag_correlation(data, climate, begin, end)
    return lag
# lag correlation region


@app.route('/lag_region_climate', methods=['GET', 'POST'])
def lag_region_climate():

    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['region']

    data = query.group_climate_region(region)
    lag = visual.lag_correlation(data, climate, begin, end)
    return lag
# line chart disease for year


@app.route('/line_province_disease_year', methods=['GET', 'POST'])
def province_disease_year():

    province = request.args['province']
    begin = request.args['begin']
    end = request.args['end']
    disease = request.args['disease']

    mean = query.mean_disease_province_year(province)
    max_ = query.max_disease_province_year(province)
    min_ = query.min_disease_province_year(province)

    LineJson = visual.stat_disease_year(
        mean, max_, min_, disease, begin, end)
    return LineJson
# chart disease month


@app.route('/line_province_disease_month', methods=['GET', 'POST'])
def province_disease_month():

    province = request.args['province']
    begin = request.args['begin']
    end = request.args['end']
    disease = request.args['disease']

    data = query.disease_month_exp(province)

    LineJson = visual.stat_disease_month(data, disease, begin, end)
    return LineJson
# seasonal analyst


@app.route('/seasonal_disease_exp', methods=['GET', 'POST'])
def seasonal_disease_exp():
    disease = request.args['disease']
    province = request.args['province']
    begin = request.args['begin']
    end = request.args['end']

    data = query.disease_seasonal_exp(province)
    seasonal = visual.seasonal_disease_exp(data, disease, begin, end)

    return seasonal
# seasonal disease


@app.route('/region_seasonal_disease', methods=['GET', 'POST'])
def region_seasonal_disease():

    begin = request.args['begin']
    end = request.args['end']
    disease = request.args['disease']
    region = request.args['region']

    data = query.region_disease(region)

    linejson = visual.region_season_disease(data, disease, begin, end)
    return linejson

# climate year


@app.route('/province_climate_year', methods=['GET', 'POST'])
def province_climate_year():
    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']
    province = request.args['province']

    mean = query.mean_climate_year(province)
    max_ = query.max_climate_year(province)
    min_ = query.min_climate_year(province)

    LineJson = visual.stat_climate_year(mean, max_, min_, climate, begin, end)
    return LineJson
# climate month


@app.route('/province_climate_month', methods=['GET', 'POST'])
def province_climate_month():

    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']
    province = request.args['province']
    data = query.climate_month_exp(province)

    LineJson = visual.stat_climate_month(data, climate, begin, end)
    return LineJson
# seasonal analyst


@app.route('/seasonal_climate_exp', methods=['GET', 'POST'])
def seasonal_climate_exp():
    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']
    province = request.args['province']

    data = query.climate_seasonal_exp(province)

    LineJson = visual.seasonal_climate_exp(data, climate, begin, end)
    return LineJson
    # region
    # end region
# seasonal climate region


@app.route('/region_seasonal_climate', methods=['GET', 'POST'])
def region_seasonal_climate():
    begin = request.args['begin']
    end = request.args['end']
    climate = request.args['climate']
    region = request.args['region']

    data = query.group_climate_region(region)

    linejson = visual.region_season_climate(data, climate, begin, end)
    return linejson

# correlation pages explore


@app.route('/corr_disease_exp', methods=['GET', 'POST'])
def corr_disease_exp():
    data = query.climate_disease()
    disease = request.args.getlist('disease[]')
    begin = request.args['begin']
    end = request.args['end']
    province = request.args['province']
    data = query.climate_disease_exp(province)
    corr = visual.corr_disease_exp(data, disease, begin, end)
    return corr
# correlation region disease


@app.route('/region_corr_disease_exp', methods=['GET', 'POST'])
def region_corr_disease_exp():

    data = query.climate_disease()
    disease = request.args.getlist('disease[]')
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['region']

    data = query.region_climate_disease(region)
    corr = visual.corr_disease_exp(data, disease, begin, end)
    return corr
# line chart date1


@app.route('/line_date1_exp', methods=['GET', 'POST'])
def line_date1_exp():
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    province = request.args['province']
    data = query.disease_month_exp(province)
    line = visual.line_date1_exp(data, disease, begin, end)
    return line
# date1 region


@app.route('/date1_region_disease', methods=['GET', 'POST'])
def date1_region_disease():

    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['region']

    data = query.region_disease_month(region)
    line = visual.region_date1_exp(data, disease, begin, end)
    return line

# line chart climate date1


@app.route('/line_date1_climate_exp', methods=['GET', 'POST'])
def line_date1_climate_exp():
    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']
    provice = request.args['province']
    data = query.climate_month_exp(provice)
    line = visual.line_date1_climate_exp(data, climate, begin, end)
    return line

# date1 climate


@app.route('/region_date1_climate_exp', methods=['GET', 'POST'])
def region_date1_climate_exp():

    # data = query.climate_disease()
    climate = request.args['climate']
    begin = request.args['begin']
    end = request.args['end']
    region = request.args['region']

    data = query.region_climate_month(region)
    line = visual.region_date1_climate_exp(data, climate, begin, end)
    return line
###############################region id province Viet Nam ###################
# region disease year


@app.route('/region_disease_year', methods=['GET', 'POST'])
def region_disease_year():

    begin = request.args['begin']
    end = request.args['end']
    disease = request.args['disease']
    region = request.args['region']

    mean = query.mean_region_disease(region)
    max_ = query.max_region_disease(region)
    min_ = query.min_region_disease(region)

    linejson = visual.stat_disease_year(
        mean, max_, min_, disease, begin, end)
    return linejson
# region disease month


@app.route('/region_disease_month', methods=['GET', 'POST'])
def region_disease_month():

    begin = request.args['begin']
    end = request.args['end']
    disease = request.args['disease']
    region = request.args['region']

    data = query.region_disease_month(region)

    linejson = visual.stat_disease_month(data, disease, begin, end)
    return linejson
# region climate


@app.route('/region_climate_year', methods=['GET', 'POST'])
def region_climate_year():

    begin = request.args['begin']
    end = request.args['end']
    climate = request.args['climate']
    region = request.args['region']

    mean = query.mean_climate_region_year(region)
    max_ = query.max_region_climate(region)
    min_ = query.min_region_climate(region)

    linejson = visual.stat_climate_year(mean, max_, min_, climate, begin, end)
    return linejson
# region climate month


@app.route('/region_climate_month', methods=['GET', 'POST'])
def region_climate_month():

    begin = request.args['begin']
    end = request.args['end']
    climate = request.args['climate']
    region = request.args['region']

    data = query.region_climate_month(region)

    linejson = visual.stat_climate_month(data, climate, begin, end)
    return linejson

############################# comparation factor##############################


@app.route('/compare')
def compare():
    columns = query.get_columns()
    # get columns disease
    disease = columns['disease']
    disease = disease.drop([1, 3, 5])
    # get columns climate
    climate1 = columns['climate1'].append(columns['climate2'].dropna())
    # get columns climate 2
    climate2 = columns['climate2'].dropna()
    climate1 = climate1.reset_index(drop=True)
    climate1 = climate1.drop([10, 11])
    # get province column
    province_name = query.get_province_name()
    province_code = query.get_province_code()

    return render_template('compare.html', disease=disease,
                           climate1=climate1, climate2=climate2,
                           province=zip(province_name, province_code)
                           )

# population response


@app.route("/popu_response/<id>/<id0>", methods=['GET', 'POST'])
def popu_response(id, id0):
    feature_selected = []
    data0 = query.population_province_exp(id)
    data1 = query.population_province_exp(id0)
    data0 = data0.groupby(['year', 'month', 'province_name']).mean().reset_index()
    data1 = data1.groupby(['year', 'month', 'province_name']).mean().reset_index()
    begin = request.args['begin']
    end = request.args['end']
    # data0 = data0[data0['year'].between(int(begin), int(end))]
    # data1 = data1[data1['year'].between(int(begin), int(end))]
    # data0['province_name'] == '' ? 0 : data0['province_name']

    # get attribute columns
    feature_selected.append(
        {
            'name0': listToString(data0['province_name'].unique()),
            'name1': listToString(data1['province_name'].unique()),
            'population0': round(data0['population'].iloc[1], 4),
            'population1': round(data1['population'].iloc[1], 4),
        }
    )

    return jsonify({'data': render_template('popu_response.html',
                                            feature_selected=feature_selected)})

# compare factor


@app.route('/factor')
def factor():
    # get columns disease
    disease_factor = [
        {'name': 'influenza'},
        {'name': 'dengue_fever'},
        {'name': 'diarrhoea'},
        # {'name':'disease'}
    ]

    columns = query.get_columns()
    province_name = query.get_province_name()
    province_code = query.get_province_code()
    return render_template('factor.html',
                           disease_factor=disease_factor,
                           columns=columns,
                           province=zip(province_name, province_code)

                           )
# show subplotly in here


@app.route('/subplotly', methods=['GET', 'POST'])
def subplotly():
    data = query.climate_disease()
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    sub = visual.compare_factor(data, disease, begin, end)
    return sub
# show subplotly year in here


@app.route('/subplotly_year', methods=['GET', 'POST'])
def subplotly_year():
    data = query.climate_disease()
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    y_m = request.args['y_m']
    sub = visual.compare_factor_year(data, disease,y_m,begin, end)
    return sub
# correlation

@app.route('/subplotly_bubble_year', methods=['GET', 'POST'])
def subplotly_bubble_year():
    data = query.climate_disease()
    begin = request.args['begin']
    end = request.args['end']
    y_m = request.args['y_m']
    sub = visual.compare_weather_diseases(data,y_m,begin, end)
    return sub

@app.route('/disease_and_weather', methods=['GET', 'POST'])
def disease_and_weather():
    data = query.climate_disease()
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    sub = visual.disease_and_weather_line_bar(data, disease, begin, end)
    return sub


@app.route('/corr_factor', methods=['GET', 'POST'])
def corr_factor():
    data = query.climate_disease()
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    sub = visual.corr_factor(data, disease, begin, end)
    return sub
###########################comparation two province disease#############################


@app.route('/compare_province', methods=['GET', 'POST'])
def compare_province():
    disease = request.args['disease']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_province(province1)
    df2 = query.compare_province(province2)

    line = visual.compare_disease_year(df1, df2, disease, begin, end)
    return line
# compare province month disease


@app.route('/compare_pro_month', methods=['GET', 'POST'])
def compare_pro_month():
    disease = request.args['disease']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_pro_month(province1)
    df2 = query.compare_pro_month(province2)

    line = visual.compare_disease_month(df1, df2, disease, begin, end)
    return line
# comparation two province climate


@app.route('/compare_pro_climate', methods=['GET', 'POST'])
def compare_pro_climate():
    climate = request.args['climate']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_pro_climate(province1)
    df2 = query.compare_pro_climate(province2)

    line = visual.compare_climate_province(df1, df2, climate, begin, end)
    return line
# compare two province climate month


@app.route('/compare_pro_climate_month', methods=['GET', 'POST'])
def compare_pro_climate_month():
    climate = request.args['climate']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_pro_climate_month(province1)
    df2 = query.compare_pro_climate_month(province2)

    line = visual.compare_climate_province_month(df1, df2, climate, begin, end)
    return line
# pie chart in here


@app.route('/pie_disease_year', methods=['GET', 'POST'])
def pie_disease_year():
    disease = request.args['disease']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_province(province1)
    df2 = query.compare_province(province2)

    pie = visual.pie_chart_disease(df1, df2, disease, begin, end)
    return pie
# climate chart in here


@app.route('/pie_climate_year', methods=['GET', 'POST'])
def pie_climate_month():
    climate = request.args['climate']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_pro_climate(province1)
    df2 = query.compare_pro_climate(province2)

    pie = visual.pie_chart_climate(df1, df2, climate, begin, end)
    return pie
# compare disease


@app.route('/compare_disease', methods=['GET', 'POST'])
def compare_disease():
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    data = query.read_disease()
    line = visual.compare_disease(data, disease, begin, end)
    return line

# compare 2 province date1

@app.route('/compare_disease_box', methods=['GET', 'POST'])
def compare_disease_bar():
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    data = query.read_heatmap_disease()
    line = visual.compare_disease_bar(data, disease, begin, end)
    return line

@app.route('/compare_disease_boxplot', methods=['GET', 'POST'])
def compare_disease_boxplot():
    disease = request.args['disease']
    begin = request.args['begin']
    end = request.args['end']
    data = query.read_heatmap_disease()
    line = visual.compare_disease_boxplot(data, disease, begin, end)
    return line


@app.route('/comp_date1_disease', methods=['GET', 'POST'])
def comp_date1_disease():
    disease = request.args['disease']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_pro_month(province1)
    df2 = query.compare_pro_month(province2)
    line = visual.compare_disease_date1(df1, df2, disease, begin, end)
    return line
# line chart climate date1


@app.route('/comp_date1_climate', methods=['GET', 'POST'])
def comp_date1_climate():
    climate = request.args['climate']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_pro_climate_month(province1)
    df2 = query.compare_pro_climate_month(province2)
    line = visual.compare_climate_date1(df1, df2, climate, begin, end)
    return line
#  linear chart disease


@app.route('/linear_comp_year', methods=['GET', 'POST'])
def linear_comp_year():
    disease = request.args['disease']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_province(province1)
    df2 = query.compare_province(province2)
    line = visual.linear_comp_year(df1, df2, disease, begin, end)
    return line
#  linear chart disease  month


@app.route('/linear_comp_month', methods=['GET', 'POST'])
def linear_comp_month():
    disease = request.args['disease']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_pro_month(province1)
    df2 = query.compare_pro_month(province2)
    line = visual.linear_comp_month(df1, df2, disease, begin, end)
    return line
# linear climate year


@app.route('/linear_climate_year', methods=['GET', 'POST'])
def linear_climate_year():
    climate = request.args['climate']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_pro_climate(province1)
    df2 = query.compare_pro_climate(province2)
    line = visual.linear_comp_year(df1, df2, climate, begin, end)
    return line
# linear climate month


@app.route('/linear_climate_month', methods=['GET', 'POST'])
def linear_climate_month():
    climate = request.args['climate']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_pro_climate_month(province1)
    df2 = query.compare_pro_climate_month(province2)
    line = visual.linear_comp_month(df1, df2, climate, begin, end)
    return line

@app.route('/climate_disease_bubble', methods=['GET', 'POST'])
def climate_disease_bubble():
    climate = request.args['climate']
    province1 = request.args['province1']
    province2 = request.args['province2']
    begin = request.args['begin']
    end = request.args['end']
    df1 = query.compare_pro_month(province1)
    df2 = query.compare_pro_month(province2)
    line = visual.climate_comp_bubble(df1, df2, climate, begin, end)
    return line
