import json
import plotly
import plotly.graph_objs as go
import pandas as pd
import calendar
import chart_studio.plotly as py
import numpy as np
from plotly.subplots import make_subplots
from statsmodels.tsa.stattools import pacf, acf
import plotly.express as px


class Visual():
    """docstring for"""

    ########################summary pages################################
    # process  don vi

    def title_climate(self, climate):
        dv = " "
        dict_climate = {
            "rain": "(mm)",
            "max_rain": "(mm)",
            "temperature": "(oC)",
            "temperature_min": "(oC)",
            "temperature_max": "(oC)",
            "temperature": "(oC)",
            "temperature_abs_min": "(oC)",
            "temperature_abs_max": "(oC)",
            "humidity": "(%)",
            "humidity_min": "(%)",
            "raining_day": "(day)",
            "vaporation": "(mm)",
            "sun_hour": "hour"
        }
        for keys, values in dict_climate.items():

            if (str(climate) == keys):
                dv = values

        return dv

    # get string

    def listToString(self, s):
        str1 = " "
        for ele in s:
            str1 += ele
        return str1

    # replace ky tu

    def replaceList(self, a):
        arr = []
        for elemt in a:
            arr.append(elemt.replace('_', ' '))
        return arr

    # bar chart default in Viet Nam

    def bar_chart_disease(self, df):
        df = df.groupby(["date1", "province_code"], as_index=False).first()
        df = df.groupby(["year"], as_index=False).sum()
        df['Influenza_per_100,000'] = df.apply(
            lambda x: x['influenza'] if x['influenza'] < 1 else x['influenza'] / x['population'],
            axis=1)
        df['Influenza_per_100,000'] = df['Influenza_per_100,000'].apply(lambda x: x * 100)
        df['Dengue_per_100,000'] = df.apply(
            lambda x: x['dengue_fever'] if x['dengue_fever'] < 1 else x['dengue_fever'] / x[
                'population'],
            axis=1)
        df['Dengue_per_100,000'] = df['Dengue_per_100,000'].apply(lambda x: x * 100)
        df['Diarrhoea_per_100,000'] = df.apply(
            lambda x: x['diarrhoea'] if x['diarrhoea'] < 1 else x['diarrhoea'] / x[
                'population'],
            axis=1)
        df['Diarrhoea_per_100,000'] = df['Diarrhoea_per_100,000'].apply(lambda x: x * 100)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['year'],
                             y=df['Influenza_per_100,000'],
                             name='Influenza rate per 100,000',
                             marker_color='rgb(55, 83, 109)',
                             showlegend=True
                             ))
        fig.add_trace(go.Bar(x=df['year'],
                             y=df['Dengue_per_100,000'],
                             name='Dengue Fever rate per 100,000',
                             marker_color='red',
                             showlegend=True
                             ))
        fig.add_trace(go.Bar(x=df['year'],
                             y=df['Diarrhoea_per_100,000'],
                             name='Diarrhoea rate per 100,000',
                             marker_color='rgb(26, 118, 255)',
                             showlegend=True
                             ))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "line"],
                            label="Line Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),

            ],
            showlegend=True,
            xaxis_tickfont_size=14,
            xaxis=dict(
                title='Year',
                titlefont_size=16,
                tickfont_size=14,
            ),
            yaxis=dict(
                title='Cases per 100,000',
                titlefont_size=16,
                tickfont_size=14,
            ),
            template="plotly_white",
            margin={"r": 10, "t": 10, "l": 10, "b": 10},
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1
        )
        BarJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return BarJson

    # bar chart death

    def bar_chart_disease_death(self, df):
        df= df.groupby(["date1", "province_code"], as_index=False).first()
        df = df.groupby(["year"], as_index=False).sum()
        df['Influenza_death_per_100,000'] = df.apply(lambda x: x['influenza_death'] if x['influenza_death'] < 1 else x['influenza_death'] / x['population'], axis=1)
        df['Influenza_death_per_100,000'] = df['Influenza_death_per_100,000'].apply(lambda x: x *100)
        df['Dengue_death_per_100,000'] = df.apply(
            lambda x: x['dengue_fever_death'] if x['dengue_fever_death'] < 1 else x['dengue_fever_death'] / x['population'],
            axis=1)
        df['Dengue_death_per_100,000'] = df['Dengue_death_per_100,000'].apply(lambda x: x * 100)
        df['Diarrhoea_death_per_100,000'] = df.apply(
            lambda x: x['diarrhoea_death'] if x['diarrhoea_death'] < 1 else x['diarrhoea_death'] / x[
                'population'],
            axis=1)
        df['Diarrhoea_death_per_100,000'] = df['Diarrhoea_death_per_100,000'].apply(lambda x: x * 100)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['year'],
                             y=df['Influenza_death_per_100,000'],
                             name='Influenza Death rate per 100,000',
                             marker_color='rgb(55, 83, 109)',
                             showlegend=True
                             ))
        fig.add_trace(go.Bar(x=df['year'],
                             y=df['Dengue_death_per_100,000'],
                             name='Dengue Death rate per 100,000',
                             marker_color='red',
                             showlegend=True
                             ))
        fig.add_trace(go.Bar(x=df['year'],
                             y=df['Diarrhoea_death_per_100,000'],
                             name='Diarrhoea Death rate per 100,000',
                             marker_color='rgb(26, 118, 255)',
                             showlegend=True
                             ))
        fig.update_layout(
            title="Number of Deaths per 100,000",
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "line"],
                            label="Line Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            xaxis_tickfont_size=14,
            legend=dict(
                yanchor="top",
                y=1.0,
                xanchor="right",
                x=1.02
            ),
            xaxis=dict(
                title='Year',
                titlefont_size=16,
                tickfont_size=14,
            ),
            yaxis=dict(
                title='Deaths per 100,000',
                titlefont_size=16,
                tickfont_size=14,
            ),
            template="plotly_white",
            margin={"r": 10, "t": 10, "l": 10, "b": 10},
            barmode='group',
            bargap=0.15,  # gap between bars of adjacent location coordinates.
            # gap between bars of the same location coordinate.
            bargroupgap=0.1
        )
        BarJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return BarJson

    # end bar chart
    # box chart climate and disease

    def yearlyCaseNumbersTrendLines(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df = df.groupby(['province_code', 'date1']).first().reset_index()
        dfTotalCases = df.groupby(['date1']).sum().reset_index()
        dfMean = dfTotalCases.groupby(['year']).mean().reset_index()
        dfTemp =pd.merge(dfTotalCases, dfMean, how='outer', on=['year', 'year'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dfTemp['date1'],
            y=dfTemp[str(disease)+"_x"],
            mode='lines',
            name='Total Cases per month'
        ))
        fig.add_trace(go.Scatter(
            x=dfTemp['date1'],
            y=dfTemp[str(disease)+'_y'],
            mode='lines',
            name='Average Cases per year'
        ))

        fig.update_layout(
            xaxis_title="Year", template="plotly_white",
            margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(disease.replace('_', ' ')).title())
        )

        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    def compYearlyCaseNumbersTrendLines(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df = df.groupby(['date1']).first().reset_index()
        dfTotalCases = df.groupby(['date1']).sum().reset_index()
        dfMean = dfTotalCases.groupby(['year']).mean().reset_index()
        dfTemp =pd.merge(dfTotalCases, dfMean, how='outer', on=['year', 'year'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dfTemp['date1'],
            y=dfTemp[str(disease)+"_x"],
            mode='lines',
            name='Total Cases per month'
        ))
        fig.add_trace(go.Scatter(
            x=dfTemp['date1'],
            y=dfTemp[str(disease)+'_y'],
            mode='lines',
            name='Average Cases per year'
        ))

        fig.update_layout(
            xaxis_title="Year", template="plotly_white",
            margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(disease.replace('_', ' ')).title())
        )

        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON


    def monthlyCaseNumbersTrendLines(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df = df.groupby(['province_code', 'date1']).first().reset_index()
        df = df.groupby(['year', 'month']).sum().reset_index()
        dfMean = df.groupby(['month']).mean().reset_index()
        dfTemp= pd.merge(df, dfMean, how='inner', on=['month', 'month'])
        #print(dfTemp)
        dfTemp['monthYear'] = dfTemp['month'].astype(str)+'-'+dfTemp['year_x'].astype(str)
        #print(list(dfTemp.columns))
        dfTemp2=dfTemp[['monthYear', str(disease)+'_x', str(disease)+'_y']]


        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dfTemp2['monthYear'],
            y=dfTemp[str(disease) + "_x"],
            mode='lines',
            name='Total Cases per month'
        ))
        fig.add_trace(go.Scatter(
            x=dfTemp2['monthYear'],
            y=dfTemp[str(disease) + '_y'],
            mode='lines',
            name='Average Cases per year'
        ))

        fig.update_layout(
            xaxis_title="Year", template="plotly_white",
            margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(disease.replace('_', ' ')).title())
        )

        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


        return linesJSON


    def yearlyClimateNumbersTrendLines(self, df, climate, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df = df.groupby(['province_code', 'date1']).max().reset_index()
        dfTotalCases = df.groupby(['date1']).sum().reset_index()
        dfMean = dfTotalCases.groupby(['year']).mean().reset_index()
        dfTemp =pd.merge(dfTotalCases, dfMean, how='outer', on=['year', 'year'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dfTemp['date1'],
            y=dfTemp[str(climate)+"_x"],
            mode='lines',
            name='Total '+str(climate)+' per month'
        ))
        fig.add_trace(go.Scatter(
            x=dfTemp['date1'],
            y=dfTemp[str(climate)+'_y'],
            mode='lines',
            name='Average '+str(climate)+' per year'
        ))

        fig.update_layout(
            xaxis_title="Year", template="plotly_white",
            margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(climate.replace('_', ' ')).title())
        )

        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    def box_chart_mean_feature(self, df, feature, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df = df.groupby(['year', 'month']).mean().reset_index()
        fig = px.box(df, x=df['year'], y=df[str(feature)], color=df['year'])
        dv = self.title_climate(str(feature))
        fig.update_layout(
            xaxis_title='Year', template="plotly_white",
            margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(feature.replace('_', ' ')).title()) + ' yearly mean ' + str(dv))
        BoxJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return BoxJson

    # end box chart
    # heatmap disease Viet Nam

    def heatmap_vn(self, df, vn_json, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df = (df.groupby(["year", "month", "fips"], as_index=False).first())

        cases = df.groupby(['year', 'fips', 'province_name']).sum().reset_index()

        # get data
        fig = px.choropleth(cases, geojson=vn_json, locations='fips', color=str(disease),
                            color_continuous_scale="Viridis",hover_data=["province_name"], animation_frame="year"
                            )
        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        VNJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return VNJson

#ORIGINAL NON ANIMATED HEATMAP (AVERAGE)
    # def heatmap_vn(self, df, vn_json, disease, begin, end):
    #
    #     df = df[df['year'].between(int(begin), int(end))]
    #     df = (df.groupby(["year", "month", "fips"], as_index=False).first())
    #     mean = df.groupby(['fips', 'province_name']).mean().reset_index()
    #         # get data
    #     fig = go.Figure(go.Choroplethmapbox(geojson=vn_json, locations=mean['fips'], z=mean[str(disease)],
    #                                         colorscale="Viridis", hovertext=mean['province_name'],
    #                                         marker_opacity=0.5, marker_line_width=0
    #                                         ))
    #     fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.0,
    #                       margin={"r": 20, "t": 20, "l": 20, "b": 20},
    #                       mapbox_center={"lat": 16.4,
    #                                      "lon": 107.683333333333})
    #
    #     VNJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #     return VNJson

    # heatmap population in Viet Nam

    def heatmap_population(self, df, vn_json, begin, end):
        # group by
        df = df[df['year'].between(int(begin), int(end))]
        mean = df.groupby(['fips', 'province_name', 'year']).max().reset_index()
        mean = mean.groupby(['fips', 'province_name']).mean().reset_index()
        # map in here
        fig = go.Figure(go.Choroplethmapbox(
            geojson=vn_json, locations=mean['fips'], z=mean['population'],
            colorscale="Viridis", hovertext=mean['province_name'],
            marker_opacity=0.5, marker_line_width=0))

        fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.0,
                          margin={"r": 20, "t": 20, "l": 20, "b": 20},
                          mapbox_center={"lat": 16.4, "lon": 107.683333333333})

        PopuJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return PopuJson

    # line chart population

    def line_chart_population(self, df, begin, end):

        df = df[df['year'].between(int(begin), int(end))]
        # get mean
        df = df.groupby(['year', 'province_name']).max().reset_index()
        df = df.groupby('year').sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['year'],
            y=df['population'],
            mode='lines+markers', name="Population",
            marker_symbol='triangle-up', line_color="red",
            showlegend=True
        ))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle",
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            xaxis_title='Year', yaxis_title='Yearly Population (1000)',
            template="plotly_white", margin={"r": 10, "t": 10, "l": 10, "b": 10}
        )
        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON



    # heatmap ratio disease/population

    def heatmap_ratio(self, df, vn_json, disease, begin, end):
        # group by
        df = df[df['year1'].between(int(begin), int(end))]
        mean = df.groupby(['fips', 'province_name']).mean().reset_index()
        # map in here
        fig = go.Figure(go.Choroplethmapbox(geojson=vn_json, locations=mean['fips'],
                                            z=(mean[str(disease)] / (100000)),
                                            colorscale="Viridis",
                                            hovertext=mean['province_name'],
                                            marker_opacity=0.5, marker_line_width=0))

        fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.0,
                          margin={"r": 20, "t": 20, "l": 20, "b": 20},
                          mapbox_center={"lat": 16.4, "lon": 107.683333333333})

        RatioJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return RatioJson

    # line chart ratio

    def line_chart_ratio(self, df, disease, begin, end):
        df = df[df['year1'].between(int(begin), int(end))]
        mean = df.groupby(['year1']).mean().reset_index()
        df = df.loc[:, ~df.columns.duplicated()]
        df = df.groupby(["date1", "province_name"], as_index=False).first()
        df = df.groupby(["year1"], as_index=False).sum()

        df[str(disease + " rate per 100,000")] = df.apply(lambda x: x[str(disease)] if x[str(disease)] < 1 else x[str(disease)] / x['population'], axis=1)
        df[str(disease + " rate per 100,000")] = df[str(disease + " rate per 100,000")].apply(lambda x: x* 100)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['year1'],
            # mean['population']
            y=(df[str(disease+ " rate per 100,000")]),
            mode='lines+markers', marker_symbol='triangle-up', line_color="red"))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            xaxis_title='Year', yaxis_title='Incidence rate per 100000',
            template="plotly_white", margin={"r": 10, "t": 10, "l": 10, "b": 10}
        )

        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    def casesAndDeathsChart(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df = df.loc[:, ~df.columns.duplicated()]
        df = df.groupby(["date1", "province_code"], as_index=False).first()
        df = df.groupby(["year"], as_index=False).sum()
        #print(list(df.columns))
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['year'],
            y=(df[str(disease)]),
            mode='lines', line_color="red", name=(str(disease.replace('_', ' '))).title()))
        fig.add_trace(go.Scatter(
            x=df['year'],
            y=(df[str(disease+"_death")]),
            mode='lines', line_color="blue", name=(str(disease.replace('_', ' '))).title()+" death"))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            xaxis_title='Year', yaxis_title='Number of Cases',
            template="plotly_white", margin={"r": 10, "t": 10, "l": 10, "b": 10}
        )

        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    # heatmap climate

    def heatmap_climate(self, df, vn_json, climate, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        #print(list(df.columns))
        mean = df.groupby(['fips', 'province_name', 'date1']).first().reset_index()
        mean = mean.groupby(['fips', 'province_name']).mean().reset_index()
        fig = go.Figure(go.Choroplethmapbox(geojson=vn_json, locations=mean['fips'], z=mean[str(climate)],
                                            colorscale="Viridis", hovertext=mean['province_name'],
                                            marker_opacity=0.5, marker_line_width=0))
        fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.0,
                          margin={"r": 20, "t": 20, "l": 20, "b": 20},
                          mapbox_center={"lat": 16.4,
                                         "lon": 107.683333333333},
                          )
        # Add dropdown

        VNJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return VNJson

    # line chart region population tung vung mien
    def chart_region_population(self, df, begin, end):
        fig = go.Figure()
        df = df[df['year'].between(int(begin), int(end))]
        df = df.groupby('year').mean().reset_index()
        fig.add_trace(go.Scatter(
            x=df['year'],
            y=df['population'],
            line_color="red",
            mode='lines+markers', marker_symbol='triangle-up'))

        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            xaxis_title='Year', template="plotly_white", yaxis_title=('Population yearly mean'),
            margin={"r": 20, "t": 20, "l": 20, "b": 20}
        )
        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    # line chart region ratio tung vung mien

    def chart_region_ratio(self, df, disease, begin, end):
        fig = go.Figure()
        df = df[df['year1'].between(int(begin), int(end))]
        df = df.groupby('year1').mean().reset_index()
        fig.add_trace(go.Scatter(
            x=df['year1'],
            y=(df[str(disease)] / (100000)),
            line_color="red",
            mode='lines+markers', marker_symbol='triangle-up'))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            xaxis_title='Year', template="plotly_white", yaxis_title=(str(
                disease) + '/' + 'Population '), margin={"r": 20, "t": 20, "l": 20, "b": 20}
        )
        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return linesJSON

    # heatmap disease

    def heatmap_vn_region(self, df, vn_json, disease, begin, end):

        df = df[df['year'].between(int(begin), int(end))]
        mean = df.groupby(['fips', 'province_name']).mean().reset_index()
        fig = go.Figure(go.Choroplethmapbox(geojson=vn_json, locations=mean['fips'], z=mean[str(disease)],
                                            colorscale="Viridis", hovertext=mean['province_name'],
                                            marker_opacity=0.5, marker_line_width=0
                                            ))
        fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.0,
                          margin={"r": 20, "t": 20, "l": 20, "b": 20},
                          mapbox_center={"lat": 16.4,
                                         "lon": 107.683333333333})

        VNJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return VNJson

    # heatmap population

    def heatmap_pop_region(self, df, vn_json, begin, end):
        # group by
        df = df[df['year'].between(int(begin), int(end))]
        mean = df.groupby(['fips', 'province_name']).mean().reset_index()
        # map in here
        fig = go.Figure(go.Choroplethmapbox(
            geojson=vn_json, locations=mean['fips'], z=mean['population'],
            colorscale="Viridis", hovertext=mean['province_name'],
            marker_opacity=0.5, marker_line_width=0))

        fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.0,
                          margin={"r": 20, "t": 20, "l": 20, "b": 20},
                          mapbox_center={"lat": 16.4, "lon": 107.683333333333})

        PopuJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return PopuJson

    # heatmap radio

    def heatmap_radio_region(self, df, vn_json, disease, begin, end):
        # group by
        df = df[df['year1'].between(int(begin), int(end))]
        mean = df.groupby(['fips', 'province_name']).mean().reset_index()
        # map in here
        fig = go.Figure(go.Choroplethmapbox(geojson=vn_json, locations=mean['fips'],
                                            z=(mean[str(disease)] / (100000)),
                                            colorscale="Viridis",
                                            hovertext=mean['province_name'],
                                            marker_opacity=0.5, marker_line_width=0))
        fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.0,
                          margin={"r": 20, "t": 20, "l": 20, "b": 20},
                          mapbox_center={"lat": 16.4, "lon": 107.683333333333})

        RatioJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return RatioJson

    # heatmap climate region

    def heatmap_climate_region(self, df, vn_json, climate, begin, end):

        df = df[df['year'].between(int(begin), int(end))]
        mean = df.groupby(['fips', 'province_name']).mean().reset_index()

        fig = go.Figure(go.Choroplethmapbox(geojson=vn_json, locations=mean['fips'], z=mean[str(climate)],
                                            colorscale="Viridis", hovertext=mean['province_name'],
                                            marker_opacity=0.5, marker_line_width=0))
        fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=4.0,
                          margin={"r": 20, "t": 20, "l": 20, "b": 20},
                          mapbox_center={"lat": 16.4,
                                         "lon": 107.683333333333},
                          title_text="Number of case" + " " + str(climate) + str(begin) + "-" + str(end))

        VNJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return VNJson

    ##############################Explorer pages data###############################
    # error band

    def stat_disease_year(self, mean, max_, min_, disease, begin, end):
        fig = go.Figure()
        mean = mean[mean['year'].between(int(begin), int(end))]
        max_ = max_[max_['year'].between(int(begin), int(end))]
        min_ = min_[min_['year'].between(int(begin), int(end))]

        fig = go.Figure([
            go.Scatter(
                name=str(disease),
                x=mean['year'],
                y=mean[str(disease)],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
                showlegend=True
            ),
            go.Scatter(
                name='Max ' + str(disease),
                x=max_['year'],
                y=max_[str(disease)],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                # fill='tonexty',
                showlegend=False
            ),
            go.Scatter(
                name='Min ' + str(disease),
                x=min_['year'],
                y=min_[str(disease)],
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=False
            )
        ])

        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            # showlegend=True,
            xaxis_title='Year', template="plotly_white",
            width=450,
            margin=dict(l=50, r=50, b=50, t=50, pad=4),
            yaxis_title=str(disease.replace('_', ' ')).title() + " yearly mean",
        )
        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    # month disease error band
    def stat_disease_month(self, df, disease, begin, end):
        fig = go.Figure()
        df = df[df['year'].between(int(begin), int(end))]
        #df = df[df[str(disease)] != 0]
        # get mean
        mean = df.groupby('month').mean().reset_index()
        max_ = df.groupby('month').max().reset_index()
        min_ = df.groupby('month').min().reset_index()

        # convert month
        mean['month'] = mean['month'].apply(lambda x: calendar.month_abbr[x])
        max_['month'] = max_['month'].apply(lambda x: calendar.month_abbr[x])
        min_['month'] = min_['month'].apply(lambda x: calendar.month_abbr[x])
        fig = go.Figure([
            go.Scatter(
                name=str(disease),
                x=mean['month'],
                y=mean[str(disease)],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
                showlegend=True
            ),
            go.Scatter(
                name='Max ' + str(disease),
                x=max_['month'],
                y=max_[str(disease)],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False
            ),
            go.Scatter(
                name='Min ' + str(disease),
                x=min_['month'],
                y=min_[str(disease)],
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=False
            )
        ])

        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            # showlegend=True,
            xaxis_title='Month', template="plotly_white",
            width=450,
            margin=dict(l=50, r=50, b=50, t=50, pad=4),
            yaxis_title=str(disease.replace('_', ' ')).title() + " monthly mean"
        )
        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    # year climate

    def stat_climate_year(self, mean, max_, min_, climate, begin, end):

        fig = go.Figure()
        mean = mean[mean['year'].between(int(begin), int(end))]
        max_ = max_[max_['year'].between(int(begin), int(end))]
        min_ = min_[min_['year'].between(int(begin), int(end))]

        fig = go.Figure([
            go.Scatter(
                name=str(climate),
                x=mean['year'],
                y=mean[str(climate)],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
                showlegend=True
            ),
            go.Scatter(
                name='Max ' + str(climate),
                x=max_['year'],
                y=max_[str(climate)],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False
            ),
            go.Scatter(
                name='Min' + str(climate),
                x=min_['year'],
                y=min_[str(climate)],
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=False
            )
        ])
        dv = self.title_climate(str(climate))

        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            # showlegend=True,
            xaxis_title='Year', template="plotly_white",
            margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(climate.replace('_', ' ')).title()) +
                        ' yearly mean' + str(dv)
        )
        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    # month climate

    def stat_climate_month(self, df, climate, begin, end):
        fig = go.Figure()
        df = df[df['year'].between(int(begin), int(end))]
        # get mean
        mean = df.groupby('month').mean().reset_index()
        max_ = df.groupby('month').max().reset_index()
        min_ = df.groupby('month').min().reset_index()

        # convert month
        mean['month'] = mean['month'].apply(lambda x: calendar.month_abbr[x])
        max_['month'] = max_['month'].apply(lambda x: calendar.month_abbr[x])
        min_['month'] = min_['month'].apply(lambda x: calendar.month_abbr[x])
        fig = go.Figure([
            go.Scatter(
                name=str(climate),
                x=mean['month'],
                y=mean[str(climate)],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
                showlegend=True
            ),
            go.Scatter(
                name='Max ' + str(climate),
                x=max_['month'],
                y=max_[str(climate)],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False
            ),
            go.Scatter(
                name='Min ' + str(climate),
                x=min_['month'],
                y=min_[str(climate)],
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=False
            )
        ])

        dv = self.title_climate(str(climate))

        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            xaxis_title='Month', template="plotly_white",
            margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(climate.replace('_', ' ')).title()) +
                        ' yearly mean' + str(dv)
        )
        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    # seasonal analyst

    def seasonal_disease_exp(self, df, disease, begin, end):
        fig = go.Figure()
        df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
        year = [y for y in range(int(begin), int(end) + 1)]
        for y in year:
            mean = df.loc[(df['year'] == int(y))]
            fig.add_trace(go.Scatter(x=mean['month'], y=mean[str(disease)],
                                     mode='lines',
                                     marker_symbol='triangle-left-open',
                                     marker=dict(size=10),
                                     name=str(y),
                                     ))
        fig.update_layout(xaxis_title='Month', template="plotly_white",
                          # width=450, height=300,
                          margin=dict(l=20, r=20, t=20, b=20),
                          yaxis_title=(str(disease.replace('_', ' ')).title() + ' monthly mean'))

        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    def seasonal_climate_exp(self, df, climate, begin, end):
        fig = go.Figure()
        df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
        year = [y for y in range(int(begin), int(end) + 1)]
        for y in year:
            mean = df.loc[(df['year'] == int(y))]
            fig.add_trace(go.Scatter(x=mean['month'], y=mean[str(climate)],
                                     mode='lines',
                                     marker_symbol='triangle-left-open',
                                     marker=dict(size=10),
                                     name=str(y),
                                     ))

        dv = self.title_climate(str(climate))

        fig.update_layout(xaxis_title='Month', template="plotly_white",
                          margin=dict(l=30, r=30, b=30, t=30),
                          yaxis_title=(str(climate.replace('_', ' ')).title()) + ' monthly mean' + str(dv))

        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    # correlation disease

    def corr_disease_exp(self, df, feature, begin, end):
        fig = go.Figure()
        df = df[df['year'].between(int(begin), int(end))]

        fig.add_trace(
            go.Heatmap(
                z=df[feature].corr(),
                x=self.replaceList(df[feature].columns.values),
                y=self.replaceList(df[feature].columns.values)),
        )
        fig.update_layout(height=450, template="plotly_white",
                          margin=dict(l=20, r=20, t=20, b=20))
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line



    # date1 disease province

    def line_date1_home(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df=(df.groupby(['date1', 'province_code'], as_index=False).first())
        # get mean
        dfMean = df.groupby(['date1']).mean().reset_index()
        dfMax = df.groupby(['date1']).max().reset_index()
        dfMin = df.groupby(['date1']).min().reset_index()

        # Create figure with secondary y-axis
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dfMean['date1'], y=dfMean[str(disease)],
                                 mode='lines',
                                 line=dict(color='blue'),
                                 name="Mean " + (str(disease.replace('_', ' '))).title()
                                 ))
        fig.add_trace(go.Scatter(x=dfMax['date1'], y=dfMax[str(disease)],
                                 mode='lines',
                                 line=dict(color='aqua'),
                                 name="Maximum " + (str(disease.replace('_', ' '))).title()
                                 ))
        fig.add_trace(go.Scatter(x=dfMin['date1'], y=dfMin[str(disease)],
                                 mode='lines',
                                 line=dict(color='teal'),
                                 name="Minimum " + (str(disease.replace('_', ' '))).title()
                                 ))
        fig.add_trace(go.Bar(x=dfMean['date1'], y=dfMean[str(disease)],
                             marker_color="blue",
                             name="Mean " + (str(disease.replace('_', ' '))).title(),
                             visible=False
                             ))
        fig.add_trace(go.Bar(x=dfMax['date1'], y=dfMax[str(disease)],
                             marker_color="aqua",
                             name="Maximum " + (str(disease.replace('_', ' '))).title(),
                             visible=False
                             ))
        fig.add_trace(go.Bar(x=dfMin['date1'], y=dfMin[str(disease)],
                             marker_color="teal",
                             name="Minimum " + (str(disease.replace('_', ' '))).title(),
                             visible=False
                             ))
        fig.add_trace(go.Box(x=df['date1'], y=df[str(disease)],
                             name="Box " + (str(disease.replace('_', ' '))).title(),
                             visible=False
                             ))

        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=[{"visible": [True, True, True, False, False, False, False]}],
                            label="Line Chart",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [False, False, False, True, True, True, False]}],
                            label="Bar Chart",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [False, False, False, False, False, False, True]}],
                            label="Box Chart",
                            method="update"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            showlegend=True,
            template="plotly_white",
            xaxis_title='Month',
            yaxis_title=(str(disease).title()).replace(
                '_', ' ') + ' monthly max/min/mean'
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    def line_mortality_home(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df=(df.groupby(['date1', 'province_code'], as_index=False).first())
        df=df.groupby(['year'], as_index=False).sum()
        # get mean
        df[str(disease)+" mortality rate"] = (df[str(disease)+"_death"]/df[str(disease)])*100
        # Create figure with secondary y-axis
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['year'], y=df[str(disease)+" mortality rate"],
                                 mode='lines',
                                 line=dict(color='blue'),
                                 name=(str(disease.replace('_', ' '))).title()+" mortality rate"
                                 ))
        fig.update_layout(
            showlegend=True,
            template="plotly_white",
            xaxis_title='Month',
            yaxis_title=(str(disease).title()).replace(
                '_', ' ') + ' mortality rate(%)'
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    def line_date1_exp(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        # get mean
        dfTotal = df.groupby(['date1']).sum().reset_index()

        # Create figure with secondary y-axis
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dfTotal['date1'], y=dfTotal[str(disease)],
                                 mode='lines',
                                 line=dict(color='blue'),
                                 name="Number of Cases of " + (str(disease.replace('_', ' '))).title()
                                 ))
        fig.add_trace(go.Bar(x=dfTotal['date1'], y=dfTotal[str(disease)],
                             marker_color="blue",
                             name="Number of Cases of " + (str(disease.replace('_', ' '))).title(),
                             visible=False
                             ))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=[{"visible": [True, False]}],
                            label="Line Chart",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [False, True]}],
                            label="Bar Chart",
                            method="update"
                        )

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            showlegend=True,
            template="plotly_white",
            xaxis_title='Month',
            yaxis_title=(str(disease).title()).replace(
                '_', ' ') + ' monthly Total'
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    def line_monthly_climate(self, df, climate, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df=(df.groupby(['date1', "province_code"], as_index=False).max())
        #print(list(df.columns))
        # get mean
        dfMean = df.groupby(['year', 'month']).mean().reset_index()
        years = [y for y in range(int(begin), int(end) + 1)]
        # Create figure with secondary y-axis
        fig = go.Figure()
        for year in years:
            df = dfMean.loc[(dfMean['year'] == int(year))]
            fig.add_trace(go.Scatter(x=df['month'], y=df[str(climate)],
                                     mode='lines',
                                     marker_symbol='triangle-left-open',
                                     marker=dict(size=10),
                                     name=str(year),
                                     ))
        dv = self.title_climate(str(climate))
        fig.update_layout(
            showlegend=True,
            template="plotly_white",
            xaxis_title='Month',
            yaxis_title=(str(climate).title()).replace(
                '_', ' ') + ' monthly mean'
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    def line_province_climate(self, df, climate, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df=(df.groupby(['date1', "province_code", "province_name"], as_index=False).max())
        #print(list(df.columns))
        # get mean
        dfMean = df.groupby(['date1', 'province_code', "province_name"]).mean().reset_index()
        years = [y for y in range(int(begin), int(end) + 1)]
        provinces=dfMean.province_name.unique()
        # Create figure with secondary y-axis
        fig = go.Figure()
        for province in provinces:
            df = dfMean.loc[(dfMean['province_name'] == str(province))]
            fig.add_trace(go.Scatter(x=df['date1'], y=df[str(climate)],
                                     mode='lines',
                                     marker_symbol='triangle-left-open',
                                     marker=dict(size=10),
                                     name=str(province),
                                     ))
        dv = self.title_climate(str(climate))
        fig.update_layout(
            showlegend=True,
            template="plotly_white",
            xaxis_title='Month',
            yaxis_title=(str(climate).title()).replace(
                '_', ' ') + ' monthly mean'
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line


    # date1 in climate

    def line_month_disease(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df=(df.groupby(['date1', "province_code"], as_index=False).first())
        df=(df.groupby(['year', 'month'], as_index=False).sum())
        df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
        fig = go.Figure()
        years = [y for y in range(int(begin), int(end) + 1)]
        for year in years:
            dfYear = df.loc[(df['year'] == int(year))]
            fig.add_trace(go.Scatter(x=dfYear['month'], y=dfYear[str(disease)],
                                     mode='lines',
                                     marker_symbol='triangle-left-open',
                                     marker=dict(size=10),
                                     name=str(year),
                                     ))
        dv = self.title_climate(str(disease))

        fig.update_layout(
            xaxis_title='Year', template="plotly_white",
            margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(disease.replace('_', ' ')).title()) + ' ' + str(dv)

        )
        # Create figure with secondary y-axis
        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    # date1 in climate


    def line_date1_climate_exp(self, df, climate, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        # get mean
        dfMean = df.groupby(['date1']).mean().reset_index()
        dfMax = df.groupby(['date1']).max().reset_index()
        dfMin = df.groupby(['date1']).min().reset_index()

        # Create figure with secondary y-axis
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dfMean['date1'], y=dfMean[str(climate)],
                                 mode='lines',
                                 line=dict(color='blue'),
                                 name="Mean " + (str(climate.replace('_', ' ')).title())
                                 ))
        fig.add_trace(go.Scatter(x=dfMax['date1'], y=dfMax[str(climate)],
                                 mode='lines',
                                 line=dict(color='aqua'),
                                 name="Maximum " + (str(climate.replace('_', ' ')).title())
                                 ))
        fig.add_trace(go.Scatter(x=dfMin['date1'], y=dfMin[str(climate)],
                                 mode='lines',
                                 line=dict(color='teal'),
                                 name="Minimum " + (str(climate.replace('_', ' ')).title())
                                 ))
        fig.add_trace(go.Bar(x=dfMean['date1'], y=dfMean[str(climate)],
                             marker_color="blue",
                             name="Mean " + (str(climate.replace('_', ' '))).title(),
                             visible=False
                             ))
        fig.add_trace(go.Bar(x=dfMax['date1'], y=dfMax[str(climate)],
                             marker_color="aqua",
                             name="Maximum " + (str(climate.replace('_', ' '))).title(),
                             visible=False
                             ))
        fig.add_trace(go.Bar(x=dfMin['date1'], y=dfMin[str(climate)],
                             marker_color="teal",
                             name="Minimum " + (str(climate.replace('_', ' '))).title(),
                             visible=False
                             ))
        fig.add_trace(go.Box(x=df['date1'], y=df[str(climate)],
                             name="Box " + (str(climate.replace('_', ' '))).title(),
                             visible=False
                             ))
        dv = self.title_climate(str(climate))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=[{"visible": [True, True, True, False, False, False, False]}],
                            label="Line Chart",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [False, False, False, True, True, True, False]}],
                            label="Bar Chart",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [False, False, False, False, False, False, True]}],
                            label="Box Chart",
                            method="update"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            showlegend=True,
            template="plotly_white",
            xaxis_title='Month', margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(climate.replace('_', ' ')).title()) +
                        ' monthly mean' + str(dv),
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # region date1  disease

    def region_date1_exp(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        # get mean
        df = df.groupby(['date1']).mean().reset_index()

        # Create figure with secondary y-axis
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date1'], y=df[str(disease)],
                                 mode='lines',
                                 line=dict(color='rgb(31, 119, 180)'),
                                 name=str(disease)))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            showlegend=True,
            template="plotly_white",
            xaxis_title='Month',
            yaxis_title=(str(disease.replace('_', ' ')
                             ).title() + ' monthly mean'),
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # region climate data 1

    def region_date1_climate_exp(self, df, climate, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        # get mean
        df = df.groupby(['date1']).mean().reset_index()

        # Create figure with secondary y-axis
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date1'], y=df[str(climate)],
                                 mode='lines',
                                 line=dict(color='rgb(31, 119, 180)'),
                                 name=str(climate)))
        dv = self.title_climate(str(climate))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            showlegend=True,
            template="plotly_white",
            xaxis_title='Month', margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(climate.replace('_', ' ')).title()) +
                        ' monthly mean' + str(dv)
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    ###############################region disease###############################

    # lag correlation

    def lag_correlation(self, df, feature, begin, end):

        df = df[df['year'].between(int(begin), int(end))]
        saw_auto = []
        saw_pauto = pacf(df[str(feature)], nlags=11)
        fig = go.Figure()
        # lag calculation
        for i in range(0, 13):
            saw_auto.append(df[str(feature)].autocorr(lag=i))
        lag = list([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

        fig.add_trace(go.Scatter(x=lag, y=saw_auto, name="ACF", mode='lines'))
        fig.add_trace(go.Scatter(x=lag, y=saw_pauto, name="PACF",
                                 mode='lines', line=dict(color='rgb(255, 102, 0)')))

        fig.update_layout(xaxis_title='Lag (month)', template="plotly_white",
                          yaxis_title='ACF/PACF meanly mean',
                          margin=dict(l=20, r=20, t=20, b=20))
        lagJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return lagJson

    # seasonal region climate

    def region_season_climate(self, df, climate, begin, end):
        fig = go.Figure()
        df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
        year = [y for y in range(int(begin), int(end) + 1)]
        for y in year:
            mean = df.loc[(df['year'] == int(y))]
            fig.add_trace(go.Scatter(x=mean['month'], y=mean[str(climate)],
                                     mode='lines',
                                     marker_symbol='triangle-left-open',
                                     marker=dict(size=10),
                                     name=str(y),
                                     ))
        dv = self.title_climate(str(climate))

        fig.update_layout(
            xaxis_title='Year', template="plotly_white",
            margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(climate.replace('_', ' ')).title()) + ' ' + str(dv)

        )
        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    # seasonal region disease

    def region_season_disease(self, df, disease, begin, end):
        fig = go.Figure()
        df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
        year = [y for y in range(int(begin), int(end) + 1)]
        for y in year:
            mean = df.loc[(df['year'] == int(y))]
            fig.add_trace(go.Scatter(x=mean['month'], y=mean[str(disease)],
                                     mode='lines',
                                     marker_symbol='triangle-left-open',
                                     marker=dict(size=10),
                                     name=str(y),
                                     ))
        fig.update_layout(xaxis_title='Month', template="plotly_white",
                          # width=450, height=300,
                          margin=dict(l=20, r=20, t=20, b=20),
                          yaxis_title=str(disease.replace('_', ' ')))

        linesJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return linesJSON

    ###########################compare factor##########################

    def compare_factor(self, df, feature, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        # get mean
        df = df.groupby('month').mean().reset_index()
        df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])

        fig = make_subplots(rows=3, cols=2, start_cell="bottom-left",
                            specs=[[{"secondary_y": True}, {"secondary_y": True}],
                                   [{"secondary_y": True}, {
                                       "secondary_y": True}],
                                   [{"secondary_y": True}, {"secondary_y": True}]],
                            subplot_titles=(
                            '<b> Monthly mean ' + str(feature) + ' and temperature' + '<br>' + str(begin) + '-' + str(
                                end) + '</b>',
                            '<b> Monthly mean ' +
                            str(feature) + ' and rain' + '<br>' +
                            str(begin) + '-' + str(end) + '</b>',
                            '<b> Monthly mean incidence rates of ' +
                            str(feature) + '<br>' +
                            str(begin) + '-' + str(end) + '</b>',
                            '<b> Monthly mean ' +
                            str(feature) + ' and humidity' + '<br>' +
                            str(begin) + '-' + str(end) + '</b>',
                            # title in here
                            '<b> Monthly mean ' + \
                            str(feature) + ' and vaporation' + \
                            '<br>' + str(begin) + '-' + \
                            str(end) + '</b>',
                            '<b> Monthly mean ' + str(feature) + ' and sun hour' + '<br>' + str(begin) + '-' + str(
                                end) + '</b>'))
        # Create figure with secondary y-axis

        fig.add_trace(go.Scatter(x=df['month'], y=df[str(feature)], name=(str(feature).replace('_', ' ')).title(),
                                 line_color="red", marker_symbol='triangle-up'),
                      row=2, col=1, secondary_y=False)

        fig.add_trace(go.Scatter(x=df['month'], y=df[str(feature) + '_death'],
                                 name=(str(feature).replace('_', ' ') + '_death').title(), line_color="blue",
                                 marker_symbol='x'),
                      row=2, col=1, secondary_y=True)

        fig.add_trace(go.Scatter(x=df['month'], y=df['temperature'], name='Temperature', mode='lines+markers',
                                 marker_symbol='x'),
                      row=1, col=1, secondary_y=True)

        fig.add_trace(go.Scatter(x=df['month'], y=df[str(feature)], name=(str(feature).replace('_', ' ')).title(),
                                 line_color="red", marker_symbol='triangle-up'),
                      row=1, col=1, secondary_y=False)
        fig.add_trace(go.Scatter(x=df['month'], y=df['rain'], name='Rain', marker_symbol='star'),
                      row=1, col=2, secondary_y=True)

        fig.add_trace(go.Scatter(x=df['month'], y=df[str(feature)], name=(str(feature).replace('_', ' ')).title(),
                                 line_color='red', marker_symbol='triangle-up'),
                      row=1, col=2, secondary_y=False)

        fig.add_trace(go.Scatter(x=df['month'], y=df['humidity'], name='Humidity', line_color='green',
                                 marker_symbol='asterisk-open'),
                      row=2, col=2, secondary_y=True)

        fig.add_trace(go.Scatter(x=df['month'], y=df[str(feature)], name=(str(feature).replace('_', ' ')).title(),
                                 line_color='red', marker_symbol='triangle-up'),
                      row=2, col=2, secondary_y=False)
        # vaporation
        fig.add_trace(go.Scatter(x=df['month'], y=df['vaporation'], name='Vaporation', line_color='black',
                                 marker_symbol='asterisk-open'),
                      row=3, col=1, secondary_y=True)

        fig.add_trace(go.Scatter(x=df['month'], y=df[str(feature)], name=(str(feature).replace('_', ' ')).title(),
                                 line_color='red', marker_symbol='triangle-up'),
                      row=3, col=1, secondary_y=False)
        # sun hour
        fig.add_trace(go.Scatter(x=df['month'], y=df['sun_hour'], name='Sun hour', line_color='orange',
                                 marker_symbol='asterisk-open'),
                      row=3, col=2, secondary_y=True)

        fig.add_trace(go.Scatter(x=df['month'], y=df[str(feature)], name=(str(feature).replace('_', ' ')).title(),
                                 line_color='red', marker_symbol='triangle-up'),
                      row=3, col=2, secondary_y=False)
        fig.update_xaxes(title_text="Month")
        # y title
        # disease
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=2,
                         col=1, secondary_y=False)
        fig.update_yaxes(title_text=(str(feature) + '  Death').title() +
                                    '  mean', row=2, col=1, secondary_y=True)
        # disease and humidity
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=2,
                         col=2, secondary_y=False)
        fig.update_yaxes(title_text='Humidity(%)  mean',
                         row=2, col=2, secondary_y=True)
        # disease and Temperature
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=1,
                         col=1, secondary_y=False)
        fig.update_yaxes(title_text='Temperature(oC)  mean',
                         row=1, col=1, secondary_y=True)
        # disease and Rain
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=1,
                         col=2, secondary_y=False)
        fig.update_yaxes(title_text='Rain(mm)  mean',
                         row=1, col=2, secondary_y=True)
        # disease and vaporation
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=3,
                         col=1, secondary_y=False)
        fig.update_yaxes(title_text='Vaporation(mm)  mean',
                         row=3, col=1, secondary_y=True)
        # sun hour
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=3,
                         col=2, secondary_y=False)
        fig.update_yaxes(title_text='Sun hour(hour)  mean',
                         row=3, col=2, secondary_y=True)
        fig.update_layout(height=700, showlegend=True, template="plotly_white", margin=dict(l=30, r=10)
                          )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # compare factor year

    def compare_factor_year(self, df, feature, y_m, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        years = df['year'].nunique()
        df = (df.groupby(["year", "month", "province_code"], as_index=False).first())
        disease_names = ["influenza", "diarrhoea", "dengue_fever", "influenza_death", "diarrhoea_death","dengue_fever_death"]


        agg_dict = {"vaporation": 'mean', "rain": 'mean', "raining_day": 'mean', "temperature": 'mean',
                    "humidity": 'mean', "sun_hour": 'mean', "influenza": 'sum', "diarrhoea": 'sum',
                    "dengue_fever": 'sum', "influenza_death": 'sum', "diarrhoea_death": 'sum', "dengue_fever_death": 'sum' }

        if y_m == "year":
            df = df.groupby("year").agg(agg_dict).reset_index()
            titles='<b>'+'Total ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and average temperature'+'<br>'+str(begin)+'-'+str(end)+'</b>',\
                   '<b>'+'Total ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and average rain'+'<br>'+str(begin)+'-'+str(end)+'</b>',\
                   '<b>'+'Total ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and death incidence'+'<br>'+str(begin)+'-'+str(end)+'</b>',\
                   '<b>'+'Total ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and average humidity'+'<br>'+str(begin)+'-'+str(end)+'</b>',\
                   '<b>'+'Total ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and average evaporation'+'<br>'+str(begin)+'-'+str(end)+'</b>',\
                   '<b>'+'Total ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and average sun hour'+'<br>'+str(begin)+'-'+str(end)+'</b>'
        else:
            titles='<b>'+'Mean ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and average temperature'+'<br>'+str(begin)+'-'+str(end)+'</b>',\
                   '<b>'+'Mean ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and average rain'+'<br>'+str(begin)+'-'+str(end)+'</b>',\
                   '<b>'+'Mean ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and death incidence'+'<br>'+str(begin)+'-'+str(end)+'</b>',\
                   '<b>'+'Mean ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and average humidity'+'<br>'+str(begin)+'-'+str(end)+'</b>',\
                   '<b>'+'Mean ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and average evaporation'+'<br>'+str(begin)+'-'+str(end)+'</b>',\
                   '<b>'+'Mean ' +str(feature).replace('_', ' ')+" "+str(y_m).title() + 'ly cases and average sun hour'+'<br>'+str(begin)+'-'+str(end)+'</b>'
            df = df.groupby("month").agg(agg_dict).reset_index()
            for col in df.columns:
                if col in disease_names:
                    df[col] = df[col]/years



        fig = make_subplots(rows=3, cols=2, start_cell="bottom-left", specs=[[{"secondary_y": True}, {"secondary_y": True}],
                                                                             [{"secondary_y": True}, {
                                                                                 "secondary_y": True}],
                                                                             [{"secondary_y": True}, {"secondary_y": True}]],
                            subplot_titles=(titles ))
        # Create figure with secondary y-axis

        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df[str(feature)], name=(str(feature).replace('_', ' ')).title(), line_color="red",
                                 marker_symbol='triangle-up'),
                      row=2, col=1, secondary_y=False)

        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df[str(feature)+'_death'],
                                 name=(str(feature)+'_death').title(), line_color="blue", marker_symbol='x'),
                      row=2, col=1, secondary_y=True)

        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df['temperature'], name='Temperature'),
                      row=1, col=1, secondary_y=True)

        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df[str(feature)], name=str(feature).replace('_', ' '), line_color="red",
                                 marker_symbol='triangle-up'),
                      row=1, col=1, secondary_y=False)

        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df['rain'], name='Rain', marker_symbol='asterisk-open'),
                      row=1, col=2, secondary_y=True)

        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df[str(feature)], name=str(feature).replace('_', ' '), line_color='red', marker_symbol='triangle-up'),
                      row=1, col=2, secondary_y=False)

        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df['humidity'], name='Humidity', line_color='green', marker_symbol='star'),
                      row=2, col=2, secondary_y=True)

        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df[str(feature)], name=str(feature).replace('_', ' '), line_color='red', marker_symbol='triangle-up'),
                      row=2, col=2, secondary_y=False)
        # vaporation
        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df['vaporation'], name='Vaporation', line_color='black', marker_symbol='asterisk-open'),
                      row=3, col=1, secondary_y=True)

        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df[str(feature)], name=(str(feature).replace('_', ' ')).title(), line_color='red', marker_symbol='triangle-up'),
                      row=3, col=1, secondary_y=False)
        # sun hour
        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df['sun_hour'], name='Sun hour', line_color='orange', marker_symbol='asterisk-open'),
                      row=3, col=2, secondary_y=True)

        fig.add_trace(go.Scatter(x=df[str(y_m)], y=df[str(feature)], name=(str(feature).replace('_', ' ')).title(), line_color='red', marker_symbol='triangle-up'),
                      row=3, col=2, secondary_y=False)
        # xtitle
        fig.update_xaxes(title_text=str(y_m))
        # y title
        # disease
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=2,
                         col=1, secondary_y=False)
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title()+'  Death',
                         row=2, col=1, secondary_y=True)
        # disease and humidity
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=2,
                         col=2, secondary_y=False)
        fig.update_yaxes(title_text='Humidity(%)  mean',
                         row=2, col=2, secondary_y=True)
        # disease and Temperature
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=1,
                         col=1, secondary_y=False)
        fig.update_yaxes(title_text='Temperature(oC)  mean',
                         row=1, col=1, secondary_y=True)
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=3,
                         col=1, secondary_y=False)
        fig.update_yaxes(title_text='Vaporation(mm)  mean',
                         row=3, col=1, secondary_y=True)
        # sun hour
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=3,
                         col=2, secondary_y=False)
        fig.update_yaxes(title_text='Sun hour(hour)  mean',
                         row=3, col=2, secondary_y=True)
        # disease and Rain
        fig.update_yaxes(title_text=(str(feature).replace('_', ' ')).title(), row=1,
                         col=2, secondary_y=False)
        fig.update_yaxes(title_text='Rain(mm)  mean',
                         row=1, col=2, secondary_y=True)
        fig.update_layout(height=700, showlegend=True, template="plotly_white", margin=dict(l=30, r=10)
                          )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # correlation
    def corr_factor(self, df, feature, begin, end):
        fig = make_subplots(rows=1, cols=2, subplot_titles=(
            "<b>Yearly cases correlation Viet Nam" + '<br>' + str(begin) + '-' + str(end),
            "<b>Yearly deaths correlation Viet Nam " + '<br>' + str(begin) + '-' + str(end)))
        df = df[df['year'].between(int(begin), int(end))]

        agg_dict = {"vaporation": 'mean', "rain": 'mean', "raining_day": 'mean', "temperature": 'mean',
                    "humidity": 'mean', "sun_hour": 'mean', "influenza": 'first', "diarrhoea": 'first',
                    "dengue_fever": 'first', "influenza_death": 'first', "diarrhoea_death": 'first', "dengue_fever_death": 'first' }
        df = df.groupby(["year", "month", "province_code"]).agg(agg_dict).reset_index()


        corr1 = df[['influenza','diarrhoea','dengue_fever', 'rain', 'vaporation',
                    'humidity', 'sun_hour', 'raining_day']].corr()

        disease_names = ['influenza','diarrhoea', 'dengue_fever']
        death_names = ['influenza_death','diarrhoea_death', 'dengue_fever_death']
        weather_names = ['rain', 'vaporation', 'humidity', 'sun_hour', 'raining_day']

        cols =[]
        for col in corr1.columns:
            row = []
            if col in disease_names:
                for ind in corr1.index:
                    if ind in weather_names:
                        row.append(corr1[col][ind])
            cols.append(row)

        correlated_df = pd.DataFrame(cols, columns=weather_names)


        corr2 = df[['influenza_death','diarrhoea_death', 'dengue_fever_death', 'temperature', 'rain',
                    'vaporation', 'humidity', 'sun_hour', 'raining_day']].corr()


        cols2 =[]
        for col in corr2.columns:
            row = []
            if col in death_names:
                for ind in corr2.index:
                    if ind in weather_names:
                        row.append(corr2[col][ind])
            cols2.append(row)

        correlated_death_df = pd.DataFrame(cols2, columns=weather_names)


        fig.add_trace(
            go.Heatmap(
                z=correlated_df,
                x=weather_names,
                y=disease_names,
                hoverongaps=False,
                showscale=True),
            row=1, col=1)

        fig.add_trace(
            go.Heatmap(
                z=correlated_death_df,
                x=weather_names,
                y=death_names,
                hoverongaps=False,
                showscale=False),
            row=1, col=2
        )
        fig.update_layout(height=600, template="plotly_white")
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line


    def corr_compare_factor(self, df1, df2, begin, end, name1, name2):
        name1 = name1["province_name"].iloc[0]
        name2 = name2["province_name"].iloc[0]
        fig = make_subplots(rows=1, cols=2, subplot_titles=(
            "<b>Yearly cases correlation " + name1 + '<br>' + str(begin) + '-' + str(end),
            "<b>Yearly cases correlation " + name2 + '<br>' + str(begin) + '-' + str(end)))

        df1 = df1[df1['year'].between(int(begin), int(end))]
        df2 = df2[df2['year'].between(int(begin), int(end))]

        agg_dict = {"vaporation": 'mean', "rain": 'mean', "raining_day": 'mean', "temperature": 'mean',
                    "humidity": 'mean', "sun_hour": 'mean', "influenza": 'first', "diarrhoea": 'first',
                    "dengue_fever": 'first', "influenza_death": 'first', "diarrhoea_death": 'first', "dengue_fever_death": 'first' }
        df1 = df1.groupby(["year", "month", "province_code"]).agg(agg_dict).reset_index()
        print(df1.to_string())
        df2 = df2.groupby(["year", "month", "province_code"]).agg(agg_dict).reset_index()

        corr1 = df1[['influenza','diarrhoea','dengue_fever', 'rain', 'vaporation',
                    'humidity', 'sun_hour', 'raining_day']].corr()

        disease_names = ['influenza','diarrhoea', 'dengue_fever']
        weather_names = ['rain', 'vaporation', 'humidity', 'sun_hour', 'raining_day']

        cols =[]
        for col in corr1.columns:
            row = []
            if col in disease_names:
                for ind in corr1.index:
                    if ind in weather_names:
                        row.append(corr1[col][ind])
            cols.append(row)

        correlated_df1 = pd.DataFrame(cols, columns=weather_names)

        corr2 = df2[['influenza','diarrhoea','dengue_fever', 'rain', 'vaporation',
                    'humidity', 'sun_hour', 'raining_day']].corr()

        cols2 =[]
        for col in corr2.columns:
            row = []
            if col in disease_names:
                for ind in corr2.index:
                    if ind in weather_names:
                        row.append(corr2[col][ind])
            cols2.append(row)

        correlated_df2 = pd.DataFrame(cols2, columns=weather_names)

        fig.add_trace(
            go.Heatmap(
                z=correlated_df1,
                x=weather_names,
                y=disease_names,
                hoverongaps=False,
                showscale=True),
            row=1, col=1)

        fig.add_trace(
            go.Heatmap(
                z=correlated_df2,
                x=weather_names,
                y=disease_names,
                hoverongaps=False,
                showscale=False),
            row=1, col=2
        )
        fig.update_layout(height=600, template="plotly_white")
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line


    #########################compare two province########################
    # compare date1 disease 2 province

    def compare_disease_date1(self, df1, df2, disease, begin, end):
        # get data province 1
        df1 = df1[df1['year'].between(int(begin), int(end))]
        # get data province 2
        df2 = df2[df2['year'].between(int(begin), int(end))]
        # get
        df1 = df1.groupby(['date1', 'name']).mean().reset_index()
        df2 = df2.groupby(['date1', 'name']).mean().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df1['date1'], y=df1[str(disease)],
                                 name=str(df1['name'][0]),
                                 line=dict(color='rgb(31, 119, 180)'),
                                 mode='lines+markers', marker_symbol='triangle-up'
                                 ))
        fig.add_trace(go.Scatter(x=df2['date1'], y=df2[str(disease)],
                                 name=str(df2['name'][0]),
                                 mode='lines+markers',
                                 marker_symbol='star'))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            showlegend=True,
            template="plotly_white",
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title='Month',
            yaxis_title=(str(disease).replace('_', ' ')
                         ).title() + ' monthly mean'
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # compare date1 climate 2 province

    def compare_climate_date1(self, df1, df2, climate, begin, end):
        # get data province 1
        df1 = df1[df1['year'].between(int(begin), int(end))]
        # get data province 2
        df2 = df2[df2['year'].between(int(begin), int(end))]
        # get mean
        df1 = df1.groupby(['date1', 'name']).mean().reset_index()
        df2 = df2.groupby(['date1', 'name']).mean().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df1['date1'], y=df1[str(climate)],
                                 name=str(df1['name'][0]),
                                 line=dict(color='rgb(31, 119, 180)'),
                                 mode='lines+markers', marker_symbol='triangle-up'
                                 ))
        fig.add_trace(go.Scatter(x=df2['date1'], y=df2[str(climate)],
                                 name=str(df2['name'][0]),
                                 mode='lines+markers',
                                 marker_symbol='star'
                                 ))
        dv = self.title_climate(str(climate))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            showlegend=True,
            xaxis_title='Month', template="plotly_white", margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(climate.replace('_', ' ')).title()) +
                        ' montly mean' + str(dv)
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # compareation 2 province

    def compare_disease_year(self, df1, df2, disease, begin, end):
        # get data province 1
        df1 = df1[df1['year'].between(int(begin), int(end))]
        # get data province 2
        df2 = df2[df2['year'].between(int(begin), int(end))]

        mean1 = df1.groupby(['year', 'name']).mean().reset_index()
        mean2 = df2.groupby(['year', 'name']).mean().reset_index()
        max1 = df1.groupby(['year', 'name']).max().reset_index()
        max1 = df1.groupby(['year', 'name']).agg({str(disease): ['mean', 'min', 'max']})

        # get mean
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=mean1['year'], y=mean1[str(disease)],
                                  name=str(mean1['name'][0]) + " Mean",
                                  mode='lines+markers',
                                  marker_symbol='triangle-up', showlegend=True
                                  ))
        fig.add_trace(go.Scatter(x=mean2['year'], y=mean2[str(disease)],
                                  name=str(mean2['name'][0]) + " Mean",
                                  mode='lines+markers',
                                  marker_symbol='star', showlegend=True
                                  ))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            template="plotly_white",
            margin=dict(l=20, r=20, t=20, b=20),
            hovermode='x unified',
            xaxis_title='Year',
            yaxis_title=(str(disease).replace('_', ' ')
                         ).title() + ' yearly mean'
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # compare province month

    def compare_disease_month(self, df1, df2, disease, begin, end):
        # get data province 1
        df1 = df1[df1['year'].between(int(begin), int(end))]
        # get data province 2
        df2 = df2[df2['year'].between(int(begin), int(end))]

        # get mean
        mean1 = df1.groupby(['month', 'name']).mean().reset_index()
        mean2 = df2.groupby(['month', 'name']).mean().reset_index()
        max1 = df1.groupby(['month', 'name']).max().reset_index()
        max2 = df2.groupby(['month', 'name']).max().reset_index()
        min1 = df1.groupby(['month', 'name']).min().reset_index()
        min2 = df2.groupby(['month', 'name']).min().reset_index()
        mean1['month'] = mean1['month'].apply(lambda x: calendar.month_abbr[x])
        mean2['month'] = mean2['month'].apply(lambda x: calendar.month_abbr[x])
        max1['month'] = max1['month'].apply(lambda x: calendar.month_abbr[x])
        max2['month'] = max2['month'].apply(lambda x: calendar.month_abbr[x])
        min1['month'] = min1['month'].apply(lambda x: calendar.month_abbr[x])
        min2['month'] = min2['month'].apply(lambda x: calendar.month_abbr[x])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=mean1['month'], y=mean1[str(disease)],
                                 name=str(mean1['name'][0]) + " Mean",
                                 mode='lines+markers',
                                 marker_symbol='triangle-up'
                                 ))
        fig.add_trace(go.Scatter(x=mean2['month'], y=mean2[str(disease)],
                                 name=str(mean2['name'][0]) + " Mean",
                                 mode='lines+markers',
                                 marker_symbol='star'
                                 ))
        fig.add_trace(go.Scatter(x=max1['month'], y=max1[str(disease)],
                                 name=str(max1['name'][0]) + " Max",
                                 mode='lines+markers',
                                 marker_symbol='triangle-up'
                                 ))
        fig.add_trace(go.Scatter(x=max2['month'], y=max2[str(disease)],
                                 name=str(max2['name'][0]) + " Max",
                                 mode='lines+markers',
                                 marker_symbol='star'
                                 ))
        fig.add_trace(go.Scatter(x=min1['month'], y=min1[str(disease)],
                                 name=str(min1['name'][0]) + " Min",
                                 mode='lines+markers',
                                 marker_symbol='triangle-up'
                                 ))
        fig.add_trace(go.Scatter(x=min2['month'], y=min2[str(disease)],
                                 name=str(min2['name'][0]) + " Min",
                                 mode='lines+markers',
                                 marker_symbol='star'
                                 ))

        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            template="plotly_white",
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            hovermode='x unified',
            xaxis_title='Month',
            yaxis_title=(str(disease).replace('_', ' ')).title()+' monthly mean')
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # compare disease line chart

    def compare_disease(self, df, disease, begin, end):

        df = df[df['year'].between(int(begin), int(end))]
        # get mean
        df = df.groupby(['date1']).mean().reset_index()

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df['date1'], y=df[str(disease)],
                                 mode='lines',
                                 name=str(disease), showlegend=True), secondary_y=False, )
        fig.add_trace(go.Scatter(x=df['date1'], y=df[str(disease) + '_death'],
                                 mode='lines',
                                 name=str(disease) + ' death', showlegend=True), secondary_y=True, )

        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text=((str(disease).replace('_', ' ')).title() +
                                     ' yearly mean'), secondary_y=False)
        fig.update_yaxes(title_text=((str(disease).replace(
            '_', ' ')).title() + ' death yearly mean'), secondary_y=True)
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],

        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # pie chart compare get model year edit

    def pie_chart_disease(self, df1, df2, disease, begin, end):
        df1 = df1[df1['year'].between(int(begin), int(end))]
        df2 = df2[df2['year'].between(int(begin), int(end))]
        label1 = df1['name'].unique()
        label2 = df2['name'].unique()
        years = df1['year'].nunique()
        value0 = df1[str(disease)].mean()
        value1 = df2[str(disease)].mean()


        fig = go.Figure(data=[
            go.Bar(name=str(label1[0]), x=[disease], y=[value0], text=round(value0, 2), textposition='auto'),
            go.Bar(name=str(label2[0]), x=[disease], y=[value1], text=round(value1, 2), textposition='auto')
        ])

        fig.update_layout(barmode='stack')
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        bar = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return bar

    # pie chart climate

    def pie_chart_climate(self, df1, df2, climate, begin, end):
        df1 = df1[df1['year'].between(int(begin), int(end))]
        df2 = df2[df2['year'].between(int(begin), int(end))]
        label1 = df1['name'].unique()
        label2 = df2['name'].unique()
        value0 = df1[str(climate)].mean()
        value1 = df2[str(climate)].mean()
        fig = go.Figure(data=[
            go.Bar(name=str(label1[0]), x=[climate], y=[value0], text=round(value0, 2), textposition='auto'),
            go.Bar(name=str(label2[0]), x=[climate], y=[value1], text=round(value1, 2), textposition='auto')
        ])
        fig.update_layout(barmode='stack')

        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

        pie = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return pie

    # comparation region climate

    def compare_climate_province(self, df1, df2, climate, begin, end):
        # get data province 1
        df1 = df1[df1['year'].between(int(begin), int(end))]
        # get data province 2
        df2 = df2[df2['year'].between(int(begin), int(end))]
        # get mean

        mean1 = df1.groupby(['year', 'name']).mean().reset_index()
        mean2 = df2.groupby(['year','name']).mean().reset_index()
        max1 = df1.groupby(['year','name']).max().reset_index()
        max2 = df2.groupby(['year','name']).max().reset_index()
        min1 = df1.groupby(['year','name']).min().reset_index()
        min2 = df2.groupby(['year','name']).min().reset_index()


        fig = go.Figure()
        fig.add_trace(go.Scatter(x=mean1['year'], y=mean1[str(climate)],
                                 name=self.listToString(mean1['name'].unique()) + " Mean",
                                 mode='lines', showlegend=True
                                 ))
        fig.add_trace(go.Scatter(x=mean2['year'], y=mean2[str(climate)],
                                 name=self.listToString(mean2['name'].unique()) + " Mean",
                                 mode='lines', showlegend=True
                                 ))
        fig.add_trace(go.Scatter(x=max1['month'], y=max1[str(climate)],
                                 name=str(max1['name'][0]) + " Max",
                                 mode='lines', showlegend=True
                                 ))
        fig.add_trace(go.Scatter(x=max2['month'], y=max2[str(climate)],
                                 name=str(max2['name'][0]) + " Max",
                                 mode='lines', showlegend=True
                                 ))
        fig.add_trace(go.Scatter(x=min1['month'], y=min1[str(climate)],
                                 name=str(min1['name'][0]) + " Min",
                                 mode='lines', showlegend=True
                                 ))
        fig.add_trace(go.Scatter(x=min2['month'], y=min2[str(climate)],
                                 name=str(min2['name'][0]) + " Min",
                                 mode='lines', showlegend=True
                                 ))

        dv = self.title_climate(str(climate))
        fig.update_layout(
            hovermode='x unified',
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            xaxis_title='Year', template="plotly_white",
            margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(climate.replace('_', ' ')).title()) +
            ' yearly mean' + str(dv)
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # compate region climate month

    def compare_climate_province_month(self, df1, df2, climate, begin, end):
        # get data province 1
        df1 = df1[df1['year'].between(int(begin), int(end))]
        # get data province 2
        df2 = df2[df2['year'].between(int(begin), int(end))]
        # get mean, max and min
        mean1 = df1.groupby(['month', 'name']).mean().reset_index()
        mean2 = df2.groupby(['month', 'name']).mean().reset_index()
        max1 = df1.groupby(['month', 'name']).max().reset_index()
        max2 = df2.groupby(['month', 'name']).max().reset_index()
        min1 = df1.groupby(['month', 'name']).min().reset_index()
        min2 = df2.groupby(['month', 'name']).min().reset_index()
        # month
        mean1['month'] = mean1['month'].apply(lambda x: calendar.month_abbr[x])
        mean2['month'] = mean2['month'].apply(lambda x: calendar.month_abbr[x])
        max1['month'] = max1['month'].apply(lambda x: calendar.month_abbr[x])
        max2['month'] = max2['month'].apply(lambda x: calendar.month_abbr[x])
        min1['month'] = min1['month'].apply(lambda x: calendar.month_abbr[x])
        min2['month'] = min2['month'].apply(lambda x: calendar.month_abbr[x])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=mean1['month'], y=mean1[str(climate)],
                                 name=str(mean1['name'][0]) + " Mean",
                                 mode='lines', showlegend=True
                                 ))
        fig.add_trace(go.Scatter(x=mean2['month'], y=mean2[str(climate)],
                                 name=str(mean2['name'][0]) + " Mean",
                                 mode='lines', showlegend=True
                                 ))
        fig.add_trace(go.Scatter(x=max1['month'], y=max1[str(climate)],
                                 name=str(max1['name'][0]) + " Max",
                                 mode='lines', showlegend=True
                                 ))
        fig.add_trace(go.Scatter(x=max2['month'], y=max2[str(climate)],
                                 name=str(max2['name'][0]) + " Max",
                                 mode='lines', showlegend=True
                                 ))
        fig.add_trace(go.Scatter(x=min1['month'], y=min1[str(climate)],
                                 name=str(min1['name'][0]) + " Min",
                                 mode='lines', showlegend=True
                                 ))
        fig.add_trace(go.Scatter(x=min2['month'], y=min2[str(climate)],
                                 name=str(min2['name'][0]) + " Min",
                                 mode='lines', showlegend=True
                                 ))
        dv = self.title_climate(str(climate))

        fig.update_layout(
            hovermode='x unified',
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "scatter"],
                            label="Line Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            xaxis_title='Month', template="plotly_white",
            margin=dict(l=30, r=30, b=30, t=30),
            yaxis_title=(str(climate.replace('_', ' ')).title()) +
            ' monthly mean' + str(dv)
        )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # visulization linear year compare data

    def linear_comp_year(self, df0, df1, feature, begin, end):
        df0 = df0[df0['year'].between(int(begin), int(end))]
        # get data province 2
        df1 = df1[df1['year'].between(int(begin), int(end))]
        pd.to_numeric(df0[str(feature)], errors='ignore')
        pd.to_numeric(df1[str(feature)], errors='ignore')
        fig = px.scatter(x=df0[str(feature)], y=df1[str(feature)],
                         trendline="ols", color=df0['year'])

        fig.update_layout(
            xaxis_title=str(df0['name'][0]),
            yaxis_title=str(df1['name'][0]),
            showlegend=True)
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    # visulization linear month compare data

    def linear_comp_month(self, df0, df1, feature, begin, end):

        df0 = df0[df0['year'].between(int(begin), int(end))]
        df1 = df1[df1['year'].between(int(begin), int(end))]
        pd.to_numeric(df0[str(feature)], errors='ignore')
        pd.to_numeric(df1[str(feature)], errors='ignore')
        mean1 = df0.groupby(['month', 'name']).mean().reset_index()
        mean2 = df1.groupby(['month', 'name']).mean().reset_index()
        # month
        # mean1['month'] = mean1['month'].apply(lambda x: calendar.month_abbr[x])
        # mean2['month'] = mean2['month'].apply(lambda x: calendar.month_abbr[x])
        fig = px.scatter(x=mean1[str(feature)], y=mean2[str(feature)],
                         trendline="ols", color=mean1['month'])

        fig.update_layout(
            xaxis_title=str(mean1['name'][0]),
            yaxis_title=str(mean2['name'][0]), showlegend=True)
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    def bar_chart_month_disease_death(self, df, years):

        df = (df.groupby(["year", "month", "province_code"], as_index=False).first())
        df = (df.groupby(["month"], as_index=False).sum())

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=months,
                             y=df['influenza_death']/years,
                             name='Influenza Death',
                             marker_color='rgb(55, 83, 109)',
                             showlegend=True
                             ))
        fig.add_trace(go.Bar(x=months,
                             y=df['dengue_fever_death']/years,
                             name='Dengue Death',
                             marker_color='red',
                             showlegend=True
                             ))
        fig.add_trace(go.Bar(x=months,
                             y=df['diarrhoea_death']/years,
                             name='Diarrhoea Death',
                             marker_color='rgb(26, 118, 255)',
                             showlegend=True
                             ))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle",

                        ),
                        dict(
                            args=["type", "line"],
                            label="Line Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            xaxis_tickfont_size=14,
            legend=dict(
                yanchor="top",
                y=1,
                xanchor="right",
                x=1.2
            ),
            xaxis=dict(
                title='Year',
                titlefont_size=16,
                tickfont_size=14,
            ),
            yaxis=dict(
                title='Monthly mean',
                titlefont_size=16,
                tickfont_size=14,
            ),
            template="plotly_white",
            margin={"r": 10, "t": 10, "l": 10, "b": 10},
            barmode='stack',
            bargap=0.15,  # gap between bars of adjacent location coordinates.
            # gap between bars of the same location coordinate.
            bargroupgap=0.1
        )
        BarJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return BarJson

    def bar_chart_month_disease(self, df, years):
        df = (df.groupby(["year", "month", "province_code"], as_index=False).first())
        df = (df.groupby(["month"], as_index=False).sum())
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=months,
                             y=df["influenza"] / years,
                             name="Influenza",
                             marker_color='rgb(55, 83, 109)',
                             showlegend=True
                             ))
        fig.add_trace(go.Bar(x=months,
                             y=df["dengue_fever"] / years,
                             name="Dengue fever",
                             marker_color='red',
                             showlegend=True
                             ))
        fig.add_trace(go.Bar(x=months,
                             y=df["diarrhoea"] / years,
                             name="Diarrhoea",
                             marker_color='rgb(26, 118, 255)',
                             showlegend=True
                             ))
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=["type", "bar"],
                            label="Bar Chart",
                            method="restyle"
                        ),
                        dict(
                            args=["type", "line"],
                            label="Line Chart",
                            method="restyle"
                        ),

                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.2,
                    xanchor="right",
                    y=1.2,
                    yanchor="top"
                ),
            ],
            xaxis_tickfont_size=14,
            legend=dict(
                yanchor="top",
                y=1.0,
                xanchor="right",
                x=1.2
            ),
            xaxis=dict(
                title='Year',
                titlefont_size=16,
                tickfont_size=14,
            ),
            yaxis=dict(
                title='Monthly mean',
                titlefont_size=16,
                tickfont_size=14,
            ),
            template="plotly_white",
            margin={"r": 10, "t": 10, "l": 10, "b": 10},
            barmode='stack',
            bargap=0.15,  # gap between bars of adjacent location coordinates.
            # gap between bars of the same location coordinate.
            bargroupgap=0.1
        )
        BarJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return BarJson
        # box chart climate and disease
    def compare_weather_diseases(self, df, y_m, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        years = df['year'].nunique()
        df = (df.groupby(["year", "month", "province_code"], as_index=False).first())
        disease_names = ["influenza", "diarrhoea", "dengue_fever"]

        weather_cols = ["vaporation", "rain", "raining_day", "temperature", "humidity", "sun_hour"]

        agg_dict = {"vaporation": 'mean', "rain": 'mean', "raining_day": 'mean', "temperature": 'mean',
                    "humidity": 'mean', "sun_hour": 'mean', "influenza": 'sum', "diarrhoea": 'sum',
                    "dengue_fever": 'sum'}

        if y_m == "year":
            df = df.groupby("year").agg(agg_dict).reset_index()
            titles = '<b>' + 'Total ' + str(y_m).title() + 'ly cases and average temperature' + '<br>' + str(
                begin) + '-' + str(end) + '</b>', \
                     '<b>' + 'Total ' + str(y_m).title() + 'ly cases and average rain' + '<br>' + str(
                         begin) + '-' + str(end) + '</b>', \
                     '<b>' + 'Total ' + str(y_m).title() + 'ly cases and average rainy days' + '<br>' + str(
                         begin) + '-' + str(end) + '</b>', \
                     '<b>' + 'Total ' + str(y_m).title() + 'ly cases and average humidity' + '<br>' + str(
                         begin) + '-' + str(end) + '</b>', \
                     '<b>' + 'Total ' + str(y_m).title() + 'ly cases and average evaporation' + '<br>' + str(
                         begin) + '-' + str(end) + '</b>', \
                     '<b>' + 'Total ' + str(y_m).title() + 'ly cases and average sun hour' + '<br>' + str(
                         begin) + '-' + str(end) + '</b>'
        else:
            titles = '<b>' + 'Mean ' + str(y_m).title() + 'ly cases and average temperature' + '<br>' + str(
                begin) + '-' + str(end) + '</b>', \
                     '<b>' + 'Mean ' + str(y_m).title() + 'ly cases and average rain' + '<br>' + str(
                         begin) + '-' + str(end) + '</b>', \
                     '<b>' + 'Mean ' + str(y_m).title() + 'ly cases and average rainy days' + '<br>' + str(
                         begin) + '-' + str(end) + '</b>', \
                     '<b>' + 'Mean ' + str(y_m).title() + 'ly cases and average humidity' + '<br>' + str(
                         begin) + '-' + str(end) + '</b>', \
                     '<b>' + 'Mean ' + str(y_m).title() + 'ly cases and average evaporation' + '<br>' + str(
                         begin) + '-' + str(end) + '</b>', \
                     '<b>' + 'Mean ' + str(y_m).title() + 'ly cases and average sun hour' + '<br>' + str(
                         begin) + '-' + str(end) + '</b>'
            df = df.groupby("month").agg(agg_dict).reset_index()
            for col in df.columns:
                if col in disease_names:
                    df[col] = df[col] / years

        # show chart
        fig = make_subplots(rows=3, cols=2, start_cell="bottom-left",
                            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                                   [{"secondary_y": False}, {
                                       "secondary_y": False}],
                                   [{"secondary_y": False}, {"secondary_y": False}]],
                            subplot_titles=(titles))

        max_v = df["dengue_fever"].max()  # used to scale the size of the bubbles
        # Create figure with secondary y-axis
        for disease in disease_names:
            fig.add_trace(
                go.Scatter(x=df[str(y_m)], y=df["raining_day"], name=disease, text=df[disease],
                           hoverinfo='all', mode='markers',
                           marker=dict(sizemode='area', size=((df[disease]) / max_v) * 100, line_width=2)), row=2,
                col=1)

            fig.add_trace(
                go.Scatter(x=df[str(y_m)], y=df["temperature"], name=disease, text=df[disease],
                           hoverinfo='all', mode='markers',
                           marker=dict(sizemode='area', size=((df[disease]) / max_v) * 100, line_width=2)), row=1,
                col=1)

            fig.add_trace(
                go.Scatter(x=df[str(y_m)], y=df["rain"], name=disease, text=df[disease],
                           hoverinfo='all', mode='markers',
                           marker=dict(sizemode='area', size=((df[disease]) / max_v) * 100, line_width=2)), row=1,
                col=2)

            fig.add_trace(
                go.Scatter(x=df[str(y_m)], y=df["humidity"], name=disease, text=df[disease],
                           hoverinfo='all', mode='markers',
                           marker=dict(sizemode='area', size=((df[disease]) / max_v) * 100, line_width=2)), row=2,
                col=2)

            fig.add_trace(
                go.Scatter(x=df[str(y_m)], y=df["vaporation"], name=disease, text=df[disease],
                           hoverinfo='all', mode='markers',
                           marker=dict(sizemode='area', size=((df[disease]) / max_v) * 100, line_width=2)), row=3,
                col=1)

            fig.add_trace(
                go.Scatter(x=df[str(y_m)], y=df["sun_hour"], name=disease, text=df[disease],
                           hoverinfo='all', mode='markers',
                           marker=dict(sizemode='area', size=((df[disease]) / max_v) * 100, line_width=2)), row=3,
                col=2)

        # xtitle
        fig.update_xaxes(title_text=str(y_m))
        # y title
        # disease
        fig.update_yaxes(title_text="Mean Raining Days", row=2,
                         col=1, secondary_y=False)

        # disease and humidity
        fig.update_yaxes(title_text="Humidity(%) mean", row=2,
                         col=2, secondary_y=False)

        # disease and Temperature
        fig.update_yaxes(title_text='Temperature(oC) mean', row=1,
                         col=1, secondary_y=False)

        fig.update_yaxes(title_text="Evaporation(mm) mean", row=3,
                         col=1, secondary_y=False)

        # sun hour
        fig.update_yaxes(title_text='Sun hour(hour) mean', row=3,
                         col=2, secondary_y=False)

        # disease and Rain
        fig.update_yaxes(title_text='Rain(mm)  mean', row=1,
                         col=2, secondary_y=False)

        fig.update_layout(height=700, showlegend=False, template="plotly_white", margin=dict(l=30, r=10)
                          )
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line

    def disease_and_weather_line_bar(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]

        agg_dict = {"vaporation": 'mean', "rain": 'mean', "raining_day": 'mean', "temperature": 'mean',
                    "humidity": 'mean', "sun_hour": 'mean', "influenza": 'first', "diarrhoea": 'first',
                    "dengue_fever": 'first', "influenza_death": 'first', "diarrhoea_death": 'first',
                    "dengue_fever_death": 'first'}
        df = df.groupby(["year", "month", "province_code"]).agg(agg_dict).reset_index()

        agg_dict2 = {"vaporation": 'mean', "rain": 'mean', "raining_day": 'mean', "temperature": 'mean',
                    "humidity": 'mean', "sun_hour": 'mean', "influenza": 'sum', "diarrhoea": 'sum',
                    "dengue_fever": 'sum', "influenza_death": 'sum', "diarrhoea_death": 'sum',
                    "dengue_fever_death": 'sum'}

        df = df.groupby(["year"]).agg(agg_dict2).reset_index()

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=df['year'],
                y=df[str(disease)],
                opacity=0.6,
                name=str(disease)
            ))

        fig.add_trace(
            go.Scatter(
                x=df['year'],
                y=df["vaporation"],
                name="mean vaporation",
                line_color="#ff7f0e",
                yaxis="y2"
            ))

        fig.add_trace(
            go.Scatter(
                x=df['year'],
                y=df["sun_hour"],
                name="mean sun hour",
                line_color="#d62728",
                yaxis="y3"
            ))

        fig.add_trace(
            go.Scatter(
                x=df['year'],
                y=df["rain"],
                name="mean rain",
                line_color="#9467bd",
                yaxis="y4"
            ))

        fig.add_trace(
            go.Scatter(
                x=df['year'],
                y=df["temperature"],
                name="mean temperature",
                line_color="#1f77b4",
                yaxis="y5"
            ))

        fig.add_trace(
            go.Scatter(
                x=df['year'],
                y=df["raining_day"],
                name="mean raining days",
                line_color="#ffe476",
                yaxis="y6"
            ))

        fig.add_trace(
            go.Scatter(
                x=df['year'],
                y=df["humidity"],
                name="mean humidity",
                line_color="#0000ff",
                yaxis="y7"
            ))


        # Create axis objects
        fig.update_layout(
            plot_bgcolor="#FFF",
            hovermode='x unified',
            yaxis=dict(
                title=str(disease),
                showgrid=False
            ),
            yaxis2=dict(
                visible=False,
                anchor="x",
                overlaying="y",
                side="right",
                showgrid=False
            ),
            yaxis3=dict(
                visible=False,
                anchor="free",
                overlaying="y",
                side="right",
                position=0.9,
                showgrid=False
            ),
            yaxis4 = dict(
                visible=False,
                anchor="free",
                overlaying="y",
                side="right",
                position=0.92,
                showgrid=False

            ),
            yaxis5=dict(
                visible=False,
                anchor="free",
                overlaying="y",
                side="right",
                showgrid=False,
                position=0.95,

            ),
            yaxis6=dict(
                visible=False,
                anchor="free",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
            yaxis7=dict(
                visible=False,
                anchor="free",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
        )

        bar = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return bar

    def compare_disease_bar(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df = df.groupby(["date1", "province_name"], as_index=False).first()
        df = (df.groupby(["year", "province_name"], as_index=False).sum())
        fig = px.bar(df, x="province_name", y=disease, color="province_name", animation_frame="year",
                     animation_group="province_name",
                     log_y=True, range_y=[1, 100000])
        bar = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return bar

    def compare_disease_boxplot(self, df, disease, begin, end):
        df = df[df['year'].between(int(begin), int(end))]
        df = df.groupby(["date1", "province_name"], as_index=False).first()
        df = (df.groupby(["year", "month", "province_name"], as_index=False).sum())
        fig = px.box(df, x="province_name", y=disease, log_y=True, points="outliers", color="province_name",
                     animation_frame="year", animation_group="province_name", hover_data=[df[disease]]
                     )
        boxplot = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return boxplot

    def climate_comp_bubble(self, df0, df1, feature, begin, end):
        df0 = df0[df0['year'].between(int(begin), int(end))]
        df1 = df1[df1['year'].between(int(begin), int(end))]
        pd.to_numeric(df0[str(feature)], errors='ignore')
        pd.to_numeric(df1[str(feature)], errors='ignore')
        df = pd.concat([df0, df1])
        df = (df.groupby(["year", "name", "month"], as_index=False).sum())
        maxdf = (df.groupby(["year", "name", "month"], as_index=False).max())
        max = df[str(feature)].max()
        fig = px.line(df, x="month", y=str(feature), color="name", animation_frame="year",
                      animation_group="name", range_y=(0, max))
        line = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return line






