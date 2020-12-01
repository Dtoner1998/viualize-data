import pandas as pd
import collections
import json
from config import Model
config = Model()
conn = config.configure()

class Querydata():
    """docstring for ."""

    def __init__(self):
        query = '''
                    select DISTINCT  province_name,province_code from province_info
                '''
        # apply pandas
        df = pd.read_sql_query(query, conn)

        dict_code_pro = dict(zip(df['province_code'].astype(
            int).tolist(), df['province_name'].astype(str).tolist()))

        self.name_code_pro = collections.OrderedDict(
            sorted(dict_code_pro.items(), key=lambda t: t[0]))
    # get name province name

    def get_province_name(self):

        return self.name_code_pro.values()
    # get province  code

    def get_province_code(self):

        return self.name_code_pro.keys()
    # get coulmns name summary data

    def get_columns(self):
        name = pd.read_csv("./data/columns.csv")
        return name
    # read file json

    def read_json_vn(self):
        with open("./data/vietnam.json", 'r', encoding="utf8") as d:
            vn_json = json.load(d)

        return vn_json
    ###########################query data disease #################################
    # read disease

    def read_disease(self):
        query = ''' select year,month,date1,influenza,
                    influenza_death,dengue_fever_death,dengue_fever,
                    diarrhoea,diarrhoea_death,province_code
                    from
                    disease'''
        data = pd.read_sql_query(query, conn)
        return data
    # read heatmap disease and province_info join

    def read_heatmap_disease(self):
        query = '''
                select province_name,fips,year,month,influenza,
                influenza_death,dengue_fever_death,dengue_fever,
                diarrhoea,diarrhoea_death,date1
                from disease as a inner join province_info as b
                on a.province_code = b.province_code
                '''
        data = pd.read_sql_query(query, conn)
        return data
    # get data heatmap population

    def read_heatmap_population(self):
        query = '''
                select province_name,fips,month,
                year,population,date1
                from
                province_info as a inner join population as b
                on a.province_code = b.province_code
                '''
        data = pd.read_sql_query(query, conn)
        return data
    # get data ratio disease/population concat disease and mean

    def read_heatmap_ratio(self):
        query1 = '''select fips as fips1,province_name,population,
                    year as year1,date1
                    from population as a inner join
                    province_info as b
                    on a.province_code = b.province_code
                '''
        population = pd.read_sql_query(query1, conn)

        query2 = ''' select fips,influenza,dengue_fever,diarrhoea,
                    influenza_death,dengue_fever_death,diarrhoea_death,date1
                    from disease as a
                    inner join
                    province_info as b
                    on a.province_code =b.province_code'''
        disease = pd.read_sql_query(query2, conn)
        frame = [population, disease]
        data = pd.concat(frame, join='inner', axis=1)

        return data
    # read data mean  disease groupby

    def groupby_disease_year(self):
        query = ''' select year,month,influenza,
                    influenza_death,dengue_fever_death,dengue_fever,
                    diarrhoea,diarrhoea_death,date1
                    from
                    disease'''
        data = pd.read_sql_query(query, conn)
        data = data.groupby('year').mean().reset_index()
        return data
    # read data max disease groupby 
    def groupby_disease_max(self):
        query = ''' select year,month,influenza,
                    influenza_death,dengue_fever_death,dengue_fever,
                    diarrhoea,diarrhoea_death,date1
                    from
                    disease'''
        data = pd.read_sql_query(query, conn)
        data = data.groupby('year').max().reset_index()
        return data
    # read data min disease groupby
    def groupby_disease_min(self):
        query = ''' select year,month,influenza,
                    influenza_death,dengue_fever_death,dengue_fever,
                    diarrhoea,diarrhoea_death,date1
                    from
                    disease'''
        data = pd.read_sql_query(query, conn)
        data = data[(data['influenza'] !=0) & (data['dengue_fever'] !=0) &(data['diarrhoea'] !=0)]
        data = data.groupby('year').min().reset_index()
        return data
    ############query data disease region and province###
    # groupby disease region year
    def mean_region_disease_year(self, region_id):
        if (int(region_id) == 3):
            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,date1
                        from disease as a
                        inner join
                        province_info as b
                        on a.province_code = b.province_code '''

        else:

            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,date1
                        from disease as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                        where region = ''' + str(region_id)

        data = pd.read_sql_query(query, conn)
        data = data.groupby('year').mean().reset_index()

        return data

    # read region data population

    def read_region_population(self,  region_id):
        query = '''
                select population,year,month,date1 from population as a
                inner join province_info as b
                on a.province_code = b.province_code
                where region =
                ''' + str(region_id)
        data = pd.read_sql_query(query, conn)
        return data
    # read data disease/population ratio concat

    def region_heatmap_ratio(self,  region_id):
        if (int(region_id) == 3):
            query1 = '''select
                        fips as fips1,
                        province_name,
                        population,
                        region,
                        year as year1,date1
                        from population as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                    '''
            population = pd.read_sql_query(query1, conn)

            query2 = '''select fips,year as year2,influenza,
                    dengue_fever,diarrhoea,influenza_death,dengue_fever_death,
                    diarrhoea_death,date1
                    from disease as a
                    inner join province_info as b
                    on a.province_code =b.province_code
                    '''
            disease = pd.read_sql_query(query2, conn)
        else:
            query1 = '''select
                        fips as fips1,
                        province_name,
                        population,
                        region,
                        year as year1,date1
                        from population as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                        where region =''' + str(region_id)

            population = pd.read_sql_query(query1, conn)

            query2 = ''' select fips,year as year2,influenza,dengue_fever,
                    diarrhoea,influenza_death,dengue_fever_death,
                    diarrhoea_death,date1
                    from disease as a
                    inner join province_info as b on a.province_code =b.province_code
                    where region = ''' + region_id
            disease = pd.read_sql_query(query2, conn)
        frame = [population, disease]
        data = pd.concat(frame, join='inner', axis=1)

        return data
    # read data heatmap disease groupby

    def region_heatmap_disease(self,  region_id):
        if (int(region_id) == 3):
            query = '''select region,a.province_code as code,
                        province_name,year,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,date1
                        from disease as a
                        inner join province_info as b
                        on a.province_code = b.province_code '''
        else:

            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,date1
                        from disease as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                        where region = ''' + str(region_id)

        data = pd.read_sql_query(query, conn)

        return data
    # read data heatmap poppulation

    def region_heatmap_population(self,  region_id):
        if (int(region_id) == 3):
            query = '''select region,a.province_code as code,
                        province_name,population,
                        year,fips,date1
                        from population as a
                        inner join province_info as b
                        on a.province_code = b.province_code '''
        else:

            query = '''select region,a.province_code as code,
                        province_name,population,
                        year,fips,date1
                        from population as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                        where region = ''' + str(region_id)

        data = pd.read_sql_query(query, conn)

        return data

    #####################query data province################
    # population province code
    def population_province_exp(self, province):
        query = '''
                    select year,month,province_name,population,date1
                    from population as a inner join province_info as b on
                    a.province_code=b.province_code
                     where  a.province_code =''' + str(province)
        data = pd.read_sql_query(query, conn)
        # data = data[data['year'].between(int(begin), int(end))]
        return data
    # year  groupby mean disease

    def mean_disease_province_year(self, province):

        query = '''select year,month,influenza,influenza_death,
                    dengue_fever,dengue_fever_death,diarrhoea,diarrhoea_death,date1
                    from disease as a inner join province_info as b
                    on a.province_code = b.province_code
                    where a.province_code =
                    '''+str(province)

        data = pd.read_sql_query(query, conn)
        data = data.groupby('year').mean().reset_index()
        return data
    # year groupby max disease

    def max_disease_province_year(self, province):

        query = '''select year,month,influenza,influenza_death,
                    dengue_fever,dengue_fever_death,diarrhoea,diarrhoea_death,date1
                    from disease
                    where province_code =
                    '''+str(province)

        data = pd.read_sql_query(query, conn)
        data = data.groupby('year').max().reset_index()
        return data
    # min disease 
    def min_disease_province_year(self,province):
        query = '''select year,month,influenza,influenza_death,
                    dengue_fever,dengue_fever_death,diarrhoea,diarrhoea_death,date1
                    from disease
                    where province_code =
                    '''+str(province)
        data = pd.read_sql_query(query, conn)
        # data = data[(data['influenza'] !=0) & (data['dengue_fever'] !=0) &(data['diarrhoea'] !=0)]
        data = data.groupby('year').min().reset_index()
        return data
    # disease month province

    def disease_month_exp(self, province):
        query = '''select year,month,date1,influenza,influenza_death,
                    dengue_fever,dengue_fever_death,diarrhoea,diarrhoea_death
                    from disease
                    where province_code =
                    '''+str(province)

        data = pd.read_sql_query(query, conn)
        return data

    # seasonal analyst

    def disease_seasonal_exp(self, province):
        query = '''select year,month,influenza,influenza_death,
                    dengue_fever,dengue_fever_death,diarrhoea,diarrhoea_death,
                    date1
                    from disease
                    where province_code =
                    '''+str(province)
        data = pd.read_sql_query(query, conn)
        data = data.groupby(['year', 'month']).mean().reset_index()
        return data

    # lag query province
    def lag_query(self, province):
        query = '''select year,month,influenza,influenza_death,
                    dengue_fever,dengue_fever_death,diarrhoea,diarrhoea_death,
                    date1
                    from disease
                    where province_code =
                    '''+str(province)

        data = pd.read_sql_query(query, conn)
        data = data.groupby(['year', 'month']).mean().reset_index()
        return data
    #####################region north,south,central##########################
    # region north,south,central

    def mean_region_disease(self, region):
        if (int(region) == 3):
            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code '''

        else:

            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code
                        where region= ''' + str(region)

        data = pd.read_sql_query(query, conn)
        data = data.groupby('year').mean().reset_index()

        return data

    def max_region_disease(self, region):
        if (int(region) == 3):
            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code '''

        else:

            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code
                        where region= ''' + str(region)

        data = pd.read_sql_query(query, conn)
        data = data.groupby('year').max().reset_index()

        return data
    # min region disease 
    def min_region_disease(self,region):
        if (int(region) == 3):
            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code '''

        else:

            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code
                        where region= ''' + str(region)
        data = pd.read_sql_query(query, conn)
        # data = data[(data['influenza'] !=0) & (data['dengue_fever'] !=0) &(data['diarrhoea'] !=0)]
        data = data.groupby('year').min().reset_index()

        return data
    # seasonal disease analyst # lag region disease
    def region_disease(self, region):
        if (int(region) == 3):
            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,month,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code '''

        else:

            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,month,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code
                        where region= ''' + str(region)

        data = pd.read_sql_query(query, conn)
        data = data.groupby(['year', 'month']).mean().reset_index()
        return data
     # read region change year
    # region disease
    def region_disease_exp(self, region):
        if (int(region) == 3):
            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year as year1,month,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code '''
        else:
            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year as year1,month,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code
                        where region= ''' + str(region)

        data = pd.read_sql_query(query, conn)
        return data

    ######################climate##########################
     # max climate
    def read_climate_max(self):
        query = '''select province_code,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,temperature_abs_max,
                        temperature_abs_min,
                        humidity,humidity_min,sun_hour,date1,year
                        from climate
                         '''
        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(data['raining_day'], errors='coerce')
        data = data.groupby('year').max().reset_index()
        data = data[data['year'] != 0]
        return data
    # min climate
    def read_climate_min(self):
        query = '''select province_code,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,temperature_abs_max,
                        temperature_abs_min,
                        humidity,humidity_min,sun_hour,date1,year
                        from climate
                         '''
        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(data['raining_day'], errors='coerce')
        data = data.groupby('year').min().reset_index()
        data = data[data['year'] != 0]
        return data
     # read climate
    # read climte
    def read_climate(self):
        query = '''select province_code,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,temperature_abs_max,
                        temperature_abs_min,
                        humidity,humidity_min,sun_hour,date1,year,month
                        from climate
                         '''
        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        return data

     # concat
    #  climate +disease
    def climate_disease(self):
        query1 = ''' select year,month,influenza,
                    influenza_death,dengue_fever_death,dengue_fever,
                    diarrhoea,diarrhoea_death,province_code as code,date1
                    from disease'''
        query2 = '''select province_code,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,temperature_abs_max,
                        temperature_abs_min,
                        humidity,humidity_min,sun_hour,date1
                        from climate
                         '''
        df1 = pd.read_sql_query(query1, conn)
        df2 = pd.read_sql_query(query2, conn)
        df = pd.concat([df2, df1], axis=1, join='inner')
        df['raining_day'] = pd.to_numeric(df['raining_day'], errors='coerce')
        return df
     # read heatmap climate and province_info join
    # read climate and province_info
    def read_heatmap_climate(self):
        query = '''select b.region,a.province_code as code,
                        b.province_name,b.fips,a.year,a.vaporation,
                        a.rain,a.max_rain,a.raining_day,
                        a.temperature,a.temperature_max,
                        temperature_abs_max,temperature_abs_min,
                        a.temperature_min,a.humidity,a.humidity_min,
                        a.sun_hour,date1
                        from climate as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                         '''

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(data['raining_day'], errors='coerce')
        return data

     # read data mean climate groupby
    # read groupby year mean
    def groupby_climate_year(self):
        query = '''select year,month,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_abs_max,temperature_abs_min,
                        temperature_min,humidity,humidity_min,
                        sun_hour,date1
                        from climate
                         '''
        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(data['raining_day'], errors='coerce')
        data = data.groupby('year').mean().reset_index()
        return data
    ########################province climate##################
    # climate mean year groupby

    def mean_climate_year(self, province):
        query = '''select year,month,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,temperature_abs_max,temperature_abs_min,
                        date1
                        from climate
                        where province_code =
                         '''+str(province)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        data = data.groupby('year').mean().reset_index()
        return data
    # climate max year

    def max_climate_year(self, province):
        query = '''select year,month,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,temperature_abs_max,temperature_abs_min,
                        date1
                        from climate
                        where province_code =
                         '''+str(province)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        data = data.groupby('year').max().reset_index()
        return data
     # climate month province
    # climate max year

    def min_climate_year(self, province):
        query = '''select year,month,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,temperature_abs_max,temperature_abs_min,
                        date1
                        from climate
                        where province_code =
                         '''+str(province)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        data = data.groupby('year').min().reset_index()
        return data
    
    # climate month
    def climate_month_exp(self, province):
        query = '''select year,month,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,temperature_abs_max,temperature_abs_min,
                        date1
                        from climate
                        where province_code =
                         '''+str(province)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        return data

    #    seasonal climate analyst

    def climate_seasonal_exp(self, province):
        query = '''select year,month,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,temperature_abs_max,temperature_abs_min,
                        date1
                        from climate
                        where province_code =
                         '''+str(province)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        data = data.groupby(['year', 'month']).mean().reset_index()
        return data

    # lag climate province

    def lag_query_climate(self, province):
        query = '''select year,month,temperature,temperature_max,
                    temperature_min,rain,raining_day,max_rain,
                    sun_hour,humidity,humidity_min,vaporation,
                    temperature_abs_max,temperature_abs_min,date1
                    from climate
                    where province_code =
                    '''+str(province)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        data = data.groupby(['year', 'month']).mean().reset_index()
        return data

    ####################region climate########################
    # groupby climate region year

    def mean_region_climate_year(self,  region_id):
        if (int(region_id) == 3):
            query = '''select region,a.province_code as code,
                    province_name,fips,vaporation,
                    rain,max_rain,raining_day,
                    temperature,temperature_max,
                    temperature_min,humidity,humidity_min,
                    sun_hour,temperature_abs_max,temperature_abs_min,
                    year,date1,month
                    from climate as a
                    inner join province_info as b
                    on a.province_code = b.province_code
                    '''
        else:
            query = '''select region,a.province_code as code,
                        province_name,fips,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,temperature_abs_max,temperature_abs_min,
                        year,date1,month
                        from climate as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                        where region = ''' + str(region_id)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        data = data.groupby('year').mean().reset_index()
        return data
   
   # region climate region max 
    def max_region_climate(self,  region_id):
        if (int(region_id) == 3):
            query = '''select region,a.province_code as code,
                    province_name,fips,vaporation,
                    rain,max_rain,raining_day,
                    temperature,temperature_max,
                    temperature_min,humidity,humidity_min,
                    sun_hour,temperature_abs_max,temperature_abs_min,
                    year,date1
                    from climate as a
                    inner join province_info as b
                    on a.province_code = b.province_code
                    '''
        else:
            query = '''select region,a.province_code as code,
                        province_name,fips,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,temperature_abs_max,temperature_abs_min,
                        year,date1
                        from climate as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                        where region = ''' + str(region_id)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        data = data.groupby('year').max().reset_index()
        return data
    
    # region climate region min 
    def min_region_climate(self,  region_id):
        if (int(region_id) == 3):
            query = '''select region,a.province_code as code,
                    province_name,fips,vaporation,
                    rain,max_rain,raining_day,
                    temperature,temperature_max,
                    temperature_min,humidity,humidity_min,
                    sun_hour,temperature_abs_max,temperature_abs_min,
                    year,date1
                    from climate as a
                    inner join province_info as b
                    on a.province_code = b.province_code
                    '''
        else:
            query = '''select region,a.province_code as code,
                        province_name,fips,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,temperature_abs_max,temperature_abs_min,
                        year,date1
                        from climate as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                        where region = ''' + str(region_id)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
            
        data = data.groupby('year').min().reset_index()
        return data
    # read data heatmap climate

    def region_heatmap_climate(self, region_id):
        if (int(region_id) == 3):
            query = '''select region,a.province_code as code,
                    province_name,fips,vaporation,
                    rain,max_rain,raining_day,
                    temperature,temperature_max,
                    temperature_min,humidity,humidity_min,
                    sun_hour,temperature_abs_max,temperature_abs_min,
                    year,date1,month
                    from climate as a
                    inner join province_info as b
                    on a.province_code = b.province_code
                    '''
        else:
            query = '''select region,a.province_code as code,
                        province_name,fips,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,temperature_abs_max,temperature_abs_min,
                        year,date1,month
                        from climate as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                        where region = ''' + str(region_id)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        return data


     # region disease month

    def region_disease_month(self, region):
        if (int(region) == 3):
            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,month,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code '''
        else:
            query = '''select region,a.province_code as code,
                        province_name,fips,influenza,
                        influenza_death,dengue_fever,dengue_fever_death,
                        diarrhoea,diarrhoea_death,
                        year,month,date1
                        from province_info as a
                        inner join disease as b
                        on a.province_code = b.province_code
                        where region= ''' + str(region)

        data = pd.read_sql_query(query, conn)

        return data

    
    # climate month

    def region_climate_month(self,  region_id):
        if (int(region_id) == 3):
            query = '''select region,a.province_code as code,
                    province_name,fips,vaporation,
                    rain,max_rain,raining_day,
                    temperature,temperature_max,
                    temperature_min,humidity,humidity_min,
                    sun_hour,temperature_abs_max,temperature_abs_min,
                    year,month,date1
                    from climate as a
                    inner join province_info as b
                    on a.province_code = b.province_code
                    '''
        else:
            query = '''select region,a.province_code as code,
                        province_name,fips,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,temperature_abs_max,temperature_abs_min,
                        year,month,date1
                        from climate as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                        where region = ''' + str(region_id)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        return data
    # climate mean year

    def mean_climate_region_year(self, region_id):
        if (int(region_id) == 3):
            query = '''select region,a.province_code as code,
                    province_name,fips,vaporation,
                    rain,max_rain,raining_day,
                    temperature,temperature_max,
                    temperature_min,humidity,humidity_min,
                    sun_hour,temperature_abs_max,temperature_abs_min,
                    year,date1
                    from climate as a
                    inner join province_info as b
                    on a.province_code = b.province_code
                    '''
        else:
            query = '''select region,a.province_code as code,
                        province_name,fips,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,temperature_abs_max,temperature_abs_min,
                        year,date1
                        from climate as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                        where region = ''' + str(region_id)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        data = data.groupby('year').mean().reset_index()
        return data
    # seasonal analyst

    def group_climate_region(self, region_id):
        if (int(region_id) == 3):
            query = '''select region,a.province_code as code,
                    province_name,fips,vaporation,
                    rain,max_rain,raining_day,
                    temperature,temperature_max,
                    temperature_min,humidity,humidity_min,
                    sun_hour,temperature_abs_min,temperature_abs_max,
                    year,month,date1
                    from climate as a
                    inner join province_info as b
                    on a.province_code = b.province_code
                    '''
        else:
            query = '''select region,a.province_code as code,
                        province_name,fips,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,humidity,humidity_min,
                        sun_hour,
                        year,month,date1
                        from climate as a
                        inner join province_info as b
                        on a.province_code = b.province_code
                        where region = ''' +str(region_id)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        data = data.groupby(['year', 'month']).mean().reset_index()
        return data
    # explore climate disease

    def climate_disease_exp(self, provice):
        query1 = ''' select year,month,influenza,
                    influenza_death,dengue_fever_death,dengue_fever,
                    diarrhoea,diarrhoea_death,province_code as code,date1
                    from disease where province_code ='''+str(provice)
        query2 = '''select province_code,vaporation,
                        rain,max_rain,raining_day,
                        temperature,temperature_max,
                        temperature_min,temperature_abs_max,
                        temperature_abs_min,
                        humidity,humidity_min,sun_hour,date1
                        from climate where province_code =
                         '''+str(provice)
        df1 = pd.read_sql_query(query1, conn)
        df2 = pd.read_sql_query(query2, conn)
        df = pd.concat([df2, df1], axis=1, join='inner')
        df['raining_day'] = pd.to_numeric(df['raining_day'], errors='coerce')
        df = df.groupby('year').mean().reset_index()
        return df

    # correlation region

    def region_climate_disease(self, region):

        df1 = self.region_disease_exp(region)
        df2 = self.region_climate_month(region)
        df = pd.concat([df1, df2], axis=1, join='inner')
        return df
    ########################comparation factor############################
    # get name provice compare two province compare pages

    def compare_province(self, province):
        query = '''select year,month,influenza,influenza_death,
                    province_name as name,
                    dengue_fever,dengue_fever_death,diarrhoea,diarrhoea_death,
                    date1
                    from disease as a inner join province_info as b
                    on a.province_code = b.province_code
                    where a.province_code =
                    '''+str(province)

        data = pd.read_sql_query(query, conn)
        data = data.groupby(['year', 'name']).mean().reset_index()
        return data
    # get name provice month

    def compare_pro_month(self, province):
        query = '''select year,month,influenza,influenza_death,
                    province_name as name,
                    dengue_fever,dengue_fever_death,diarrhoea,diarrhoea_death,
                    date1
                    from disease as a inner join province_info as b
                    on a.province_code = b.province_code
                    where a.province_code =
                    '''+str(province)

        data = pd.read_sql_query(query, conn)
        return data
    # comparation 2 province

    def compare_pro_climate(self, province):
        query = '''select year,month,vaporation,rain,
                    b.province_name as name,
                    max_rain,raining_day,temperature,temperature_min,
                    temperature_max,humidity,humidity_min,sun_hour,
                    temperature_abs_max,temperature_abs_min,date1
                    from climate as a inner join province_info as b
                    on a.province_code = b.province_code
                    where a.province_code =
                    '''+str(province)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        data = data.groupby(['year', 'name']).mean().reset_index()
        return data
    # compare 2 province month

    def compare_pro_climate_month(self, province):
        query = '''select year,month,vaporation,rain,
                    b.province_name as name,
                    max_rain,raining_day,temperature,temperature_min,
                    temperature_max,humidity,humidity_min,sun_hour,
                    temperature_abs_max,temperature_abs_min,date1
                    from climate as a inner join province_info as b
                    on a.province_code = b.province_code
                    where a.province_code =
                    '''+str(province)

        data = pd.read_sql_query(query, conn)
        data['raining_day'] = pd.to_numeric(
            data['raining_day'], errors='coerce')
        return data
