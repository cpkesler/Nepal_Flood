from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import SelectInput
from tethys_sdk.gizmos import DatePicker, TimeSeries
from datetime import datetime, timedelta
import urllib2
from owslib.waterml.wml11 import WaterML_1_1 as wml11
import requests
import ast


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    context = {}
    forecast_location_initialize = 'Rapti'
    forecast_time_initialize = '20170206.1200'

    # context = {
    #             # "forecast_select": forecast_select,
    #            "get_flood": get_flood,
    #            "get_forecast": get_forecast,
    #            # "house_count_dict":house_count_dict,
    #            # "agriculture_count_dict": agriculture_count_dict,
    #            "forecast_date_picker_rapti": forecast_date_picker_rapti,
    #            "forecast_date_picker_macheli": forecast_date_picker_macheli,
    #            "forecast_date_picker_kandra": forecast_date_picker_kandra
    # }

    # Get input from gizmos

    select_location = 'Rapti'
    select_forecast_location = None
    forecast_date_start_rapti = None
    forecast_date_start_macheli = None
    forecast_date_start_kandra = None


    if request.GET.get('select_location'):
            select_location = request.GET['select_location']
    if request.GET.get('select_forecast_location'):
            select_forecast_location = request.GET['select_forecast_location']
    if request.GET.get('forecast_date_start_rapti'):
        forecast_date_start_rapti = request.GET['forecast_date_start_rapti']
    if request.GET.get('forecast_date_start_macheli'):
        forecast_date_start_macheli = request.GET['forecast_date_start_macheli']
    if request.GET.get('forecast_date_start_kandra'):
        forecast_date_start_kandra = request.GET['forecast_date_start_kandra']

    if select_location == 'Rapti':
        forecast_location_initialize = 'Rapti'
    if select_location == 'Macheli':
        forecast_location_initialize = 'Macheli'
    if select_location == 'Kandra':
        forecast_location_initialize = 'Kandra'

    # Get forecast data
    if select_forecast_location == 'Rapti':
        time_series_list_api = []
        # house_count_list = []
        subbasin = "West"
        reach_id = "4576"
        forecast_date_start_input = str(forecast_date_start_rapti)
        sfpt = 'https://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetWaterML/?watershed_name=Nepal&subbasin_name={0}&reach_id={1}&start_folder={2}&stat_type=mean'.format(subbasin, reach_id, forecast_date_start_input)
        nepal_sfpt = get_wml_values(sfpt)

        forecast_location_initialize = 'Rapti'
        forecast_time_initialize = str(forecast_date_start_rapti)

        # house_count_dict = {
        #     0: 0,
        #     0.25: 4,
        #     0.5: 4,
        #     0.75: 4,
        #     1: 4,
        #     1.25: 19,
        #     1.5: 19,
        #     1.75: 19,
        #     2.0: 19,
        #     2.25: 61,
        #     2.5: 61,
        #     2.75: 61,
        #     3: 61,
        #     3.25: 142,
        #     3.5: 142,
        #     3.75: 142,
        #     4: 143,
        #     4.25: 224,
        #     4.5: 224,
        #     4.75: 224,
        #     5: 225
        # }
        #
        # agriculture_count_dict = {
        #     0: 0,
        #     0.25: 6.3,
        #     0.5: 6.3,
        #     0.75: 6.3,
        #     1: 6.3,
        #     1.25: 16.3,
        #     1.5: 16.3,
        #     1.75: 16.3,
        #     2.0: 16.3,
        #     2.25: 28.2,
        #     2.5: 28.2,
        #     2.75: 28.2,
        #     3: 28.3,
        #     3.25: 38.6,
        #     3.5: 38.6,
        #     3.75: 38.6,
        #     4: 38.7,
        #     4.25: 46.9,
        #     4.5: 46.9,
        #     4.75: 47.0,
        #     5: 47.1
        # }

        # Plot AHPS flow data
        timeseries_plot = TimeSeries(
            height='500px',
            width='500px',
            engine='highcharts',
            title='Streamflow Plot',
            y_axis_title='Flow',
            y_axis_units='cms',
            series=[{
                'name': 'Streamflow',
                'data': nepal_sfpt
            }],
            colors=['#7cb5ec']
        )

        for flow in (i[1] for i in nepal_sfpt):
            if flow < 5:
                flow = 0
            elif flow >= 5 and flow < 25:
                flow = 0.25
            elif flow >= 25 and flow < 46:
                flow = 0.5
            elif flow >= 46 and flow < 96:
                flow = 0.75
            elif flow >= 96 and flow < 250:
                flow = 1
            elif flow >= 250 and flow < 460:
                flow = 1.25
            elif flow >= 460 and flow < 720:
                flow = 1.5
            elif flow >= 720 and flow < 1191:
                flow = 1.75
            elif flow >= 1191 and flow < 1700:
                flow = 2
            elif flow >= 1700 and flow < 2400:
                flow = 2.25
            elif flow >= 2400 and flow < 3150:
                flow = 2.5
            elif flow >= 3150 and flow < 4050:
                flow = 2.75
            elif flow >= 4050:
                flow = 3

            time_series_list_api.append(flow)
            # house_count_list.append(house_count_dict[flow])

        length = len(nepal_sfpt)

        range_slider = range(1, length + 1)
        range_list = [list(a) for a in zip(range_slider, time_series_list_api)]
        # print range_list

        forecast_start = nepal_sfpt[0][0]

        # Items to be added to context, but not defined until just before this point
        context["range_list"] = range_list
        context["forecast_start"] = forecast_start
        context["select_forecast_location"] = select_forecast_location
        context["timeseries_plot"] = timeseries_plot
        # context["house_count_dict"] = house_count_dict

    if select_forecast_location == 'Kandra':
        time_series_list_api = []
        # house_count_list = []
        subbasin = "Kandra"
        reach_id = "3"
        forecast_date_start_input = str(forecast_date_start_kandra)
        sfpt = 'https://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetWaterML/?watershed_name=Nepal&subbasin_name={0}&reach_id={1}&start_folder={2}&stat_type=mean'.format(
            subbasin, reach_id, forecast_date_start_input)
        nepal_sfpt = get_wml_values(sfpt)

        forecast_location_initialize = 'Kandra'
        forecast_time_initialize = forecast_date_start_kandra

        # house_count_dict = {
        #     0: 0,
        #     0.25: 4,
        #     0.5: 4,
        #     0.75: 4,
        #     1: 4,
        #     1.25: 19,
        #     1.5: 19,
        #     1.75: 19,
        #     2.0: 19,
        #     2.25: 61,
        #     2.5: 61,
        #     2.75: 61,
        #     3: 61,
        #     3.25: 142,
        #     3.5: 142,
        #     3.75: 142,
        #     4: 143,
        #     4.25: 224,
        #     4.5: 224,
        #     4.75: 224,
        #     5: 225
        # }
        #
        # agriculture_count_dict = {
        #     0: 0,
        #     0.25: 6.3,
        #     0.5: 6.3,
        #     0.75: 6.3,
        #     1: 6.3,
        #     1.25: 16.3,
        #     1.5: 16.3,
        #     1.75: 16.3,
        #     2.0: 16.3,
        #     2.25: 28.2,
        #     2.5: 28.2,
        #     2.75: 28.2,
        #     3: 28.3,
        #     3.25: 38.6,
        #     3.5: 38.6,
        #     3.75: 38.6,
        #     4: 38.7,
        #     4.25: 46.9,
        #     4.5: 46.9,
        #     4.75: 47.0,
        #     5: 47.1
        # }

        # Plot AHPS flow data
        timeseries_plot = TimeSeries(
            height='500px',
            width='500px',
            engine='highcharts',
            title='Streamflow Plot',
            y_axis_title='Flow',
            y_axis_units='cms',
            series=[{
                'name': 'Streamflow',
                'data': nepal_sfpt
            }],
            colors=['#7cb5ec']
        )

        for flow in (i[1] for i in nepal_sfpt):
            if flow < 3:
                flow = 0
            elif flow >= 3 and flow < 5:
                flow = 0.25
            elif flow >= 5 and flow < 7:
                flow = 0.5
            elif flow >= 7 and flow < 9:
                flow = 0.75
            elif flow >= 9 and flow < 11:
                flow = 1
            elif flow >= 11 and flow < 13:
                flow = 1.5
            elif flow >= 13 and flow < 15:
                flow = 2
            elif flow >= 15 and flow < 17:
                flow = 2.5
            elif flow >= 17 and flow < 19:
                flow = 3
            elif flow >= 19 and flow < 21:
                flow = 4
            elif flow >= 21 and flow < 23:
                flow = 4.25
            elif flow >= 23 and flow < 25:
                flow = 4.5
            elif flow >= 25:
                flow = 5

            time_series_list_api.append(flow)
            # house_count_list.append(house_count_dict[flow])

        length = len(nepal_sfpt)

        range_slider = range(1, length + 1)
        range_list = [list(a) for a in zip(range_slider, time_series_list_api)]
        # print range_list

        forecast_start = nepal_sfpt[0][0]

        # Items to be added to context, but not defined until just before this point
        context["range_list"] = range_list
        context["forecast_start"] = forecast_start
        context["select_forecast_location"] = select_forecast_location
        context["timeseries_plot"] = timeseries_plot
        # context["house_count_dict"] = house_count_dict

    if select_forecast_location == 'Macheli':
        time_series_list_api = []
        # house_count_list = []
        subbasin = "Macheli"
        reach_id = "80"
        forecast_date_start_input = str(forecast_date_start_macheli)
        sfpt = 'https://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetWaterML/?watershed_name=Nepal&subbasin_name={0}&reach_id={1}&start_folder={2}&stat_type=mean'.format(subbasin, reach_id, forecast_date_start_input)
        nepal_sfpt = get_wml_values(sfpt)

        forecast_location_initialize = 'Macheli'
        forecast_time_initialize = forecast_date_start_macheli


        house_count_dict = {
            0: 0,
            0.25: 4,
            0.5: 4,
            0.75: 4,
            1: 4,
            1.25: 19,
            1.5: 19,
            1.75: 19,
            2.0: 19,
            2.25: 61,
            2.5: 61,
            2.75: 61,
            3: 61,
            3.25: 142,
            3.5: 142,
            3.75: 142,
            4: 143,
            4.25: 224,
            4.5: 224,
            4.75: 224,
            5: 225
        }

        agriculture_count_dict = {
            0: 0,
            0.25: 6.3,
            0.5: 6.3,
            0.75: 6.3,
            1: 6.3,
            1.25: 16.3,
            1.5: 16.3,
            1.75: 16.3,
            2.0: 16.3,
            2.25: 28.2,
            2.5: 28.2,
            2.75: 28.2,
            3: 28.3,
            3.25: 38.6,
            3.5: 38.6,
            3.75: 38.6,
            4: 38.7,
            4.25: 46.9,
            4.5: 46.9,
            4.75: 47.0,
            5: 47.1
        }

        # Plot AHPS flow data
        timeseries_plot = TimeSeries(
            height='500px',
            width='500px',
            engine='highcharts',
            title='Streamflow Plot',
            y_axis_title='Flow',
            y_axis_units='cms',
            series=[{
                'name': 'Streamflow',
                'data': nepal_sfpt
            }],
            colors=['#7cb5ec']
        )

        for flow in (i[1] for i in nepal_sfpt):
            if flow < 20:
                flow = 0
            elif flow >= 20 and flow < 43:
                flow = 0.25
            elif flow >= 43 and flow < 120:
                flow = 0.5
            elif flow >= 120 and flow < 214:
                flow = 0.75
            elif flow >= 214 and flow < 330:
                flow = 1
            elif flow >= 330 and flow < 436:
                flow = 1.25
            elif flow >= 436 and flow < 567:
                flow = 1.5
            elif flow >= 567 and flow < 712:
                flow = 1.75
            elif flow >= 712 and flow < 872:
                flow = 2
            elif flow >= 872 and flow < 1045:
                flow = 2.25
            elif flow >= 1045:
                flow = 2.5

            time_series_list_api.append(flow)
            # house_count_list.append(house_count_dict[flow])

        length = len(nepal_sfpt)

        range_slider = range(1, length + 1)
        range_list = [list(a) for a in zip(range_slider, time_series_list_api)]
        # print range_list

        forecast_start = nepal_sfpt[0][0]

        # Items to be added to context, but not defined until just before this point
        context["range_list"] = range_list
        context["forecast_start"] = forecast_start
        context["select_forecast_location"] = select_forecast_location
        context["timeseries_plot"] = timeseries_plot
        # context["house_count_dict"] = house_count_dict

    select_location_select = SelectInput(display_text='Select Location',
                                         name='select_location',
                                         multiple=False,
                                         options=[('Rapti', 'Rapti'),
                                                  ('Macheli', 'Macheli'),
                                                  ('Kandra', 'Kandra')
                                                  ],
                                         initial=forecast_location_initialize,
                                         original=['Rapti'])


    select_forecast_location_select = SelectInput(display_text='Select Location',
                                              name='select_forecast_location',
                                              multiple=False,
                                              options=[('Rapti', 'Rapti'),
                                                       ('Macheli', 'Macheli'),
                                                       ('Kandra', 'Kandra')
                                                       ],
                                              initial=forecast_location_initialize,
                                              original=['Rapti'])

    # View flood button
    get_flood = Button(display_text='View Flood ',
                       name='flood_view',
                       attributes='form=flood-form',
                       submit=True)

    # View flood forecast button
    get_forecast = Button(display_text='View Flood Forecast',
                          name='flood_forecast',
                          attributes='form=forecast-form',
                          submit=True)

    dates_rapti = 'https://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetAvailableDates/?watershed_name=Nepal&subbasin_name=West&reach_id=4576'
    dates_sfpt = get_sfpt_dates(dates_rapti)
    x = ast.literal_eval(dates_sfpt)
    y = [n.strip() for n in x]
    dates_range_rapti = []
    for date in y:
        if len(date) > 10:
            display_date = date[6:8] + '/' + date[4:6] + '/' + date[:4] + ' Noon'
        else:
            display_date = date[6:8] + '/' + date[4:6] + '/' + date[:4] + ' Midnight'
        # print display_date
        dates_range_rapti.append([display_date, date])


    forecast_date_picker_rapti = SelectInput(display_text='Forecast Date Start',
                                             name='forecast_date_start_rapti',
                                             multiple=False,
                                             options=dates_range_rapti,
                                             initial=forecast_time_initialize,
                                             original=True)

    dates_macheli = 'https://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetAvailableDates/?watershed_name=Nepal&subbasin_name=Macheli&reach_id=80'
    dates_sfpt = get_sfpt_dates(dates_macheli)
    x = ast.literal_eval(dates_sfpt)
    y = [n.strip() for n in x]
    dates_ranges_macheli = []
    for date in y:
        if len(date) > 10:
            display_date = date[6:8] + '/' + date[4:6] + '/' + date[:4] + ' Noon'
        else:
            display_date = date[6:8] + '/' + date[4:6] + '/' + date[:4] + ' Midnight'
        # print display_date
        dates_ranges_macheli.append([display_date, date])

    forecast_date_picker_macheli = SelectInput(display_text='Forecast Date Start',
                                               name='forecast_date_start_macheli',
                                               multiple=False,
                                               options=dates_ranges_macheli,
                                               initial=forecast_time_initialize,
                                               original=True)

    dates_kandra = 'https://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetAvailableDates/?watershed_name=Nepal&subbasin_name=Kandra&reach_id=3'
    dates_sfpt = get_sfpt_dates(dates_kandra)
    x = ast.literal_eval(dates_sfpt)
    y = [n.strip() for n in x]
    dates_ranges_kandra = []
    for date in y:
        if len(date) > 10:
            display_date = date[6:8] + '/' + date[4:6] + '/' + date[:4] + ' Noon'
        else:
            display_date = date[6:8] + '/' + date[4:6] + '/' + date[:4] + ' Midnight'
        # print display_date
        dates_ranges_kandra.append([display_date, date])

    forecast_date_picker_kandra = SelectInput(display_text='Forecast Date Start',
                                              name='forecast_date_start_kandra',
                                              multiple=False,
                                              options=dates_ranges_kandra,
                                              initial=forecast_time_initialize,
                                              original=True)

    context["select_location_select"] = select_location_select
    context["select_forecast_location_select"] = select_forecast_location_select
    context["get_flood"] = get_flood
    context["get_forecast"] = get_forecast
    context["forecast_date_picker_rapti"] = forecast_date_picker_rapti
    context["forecast_date_picker_macheli"] = forecast_date_picker_macheli
    context["forecast_date_picker_kandra"] = forecast_date_picker_kandra

    context["select_location"] = select_location


    return render(request, 'nepal_flood/home.html', context)

def animation(request):

    context = {}
    return render(request, 'nepal_flood/animation.html', context)


def get_wml_values(url):
    response = urllib2.urlopen(urllib2.Request(url,headers={'Authorization': 'Token 72b145121add58bcc5843044d9f1006d9140b84b'}))
    data = response.read()
    series = wml11(data).response
    var = series.get_series_by_variable(var_name='Flow Forecast')
    vals = var[0].values[0]
    date_vals = vals.get_date_values()
    data = [[a, float(b)] for a, b in date_vals]

    return data

def get_sfpt_dates(url):
    response = urllib2.urlopen(urllib2.Request(url,headers={'Authorization': 'Token 72b145121add58bcc5843044d9f1006d9140b84b'}))
    data = response.read()
    return data


# Check digits in month and day (i.e. 2016-05-09, not 2016-5-9)
def check_digit(num):
    num_str = str(num)
    if len(num_str) < 2:
        num_str = '0' + num_str
    return num_str