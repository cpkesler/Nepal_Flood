from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import SelectInput
from tethys_sdk.gizmos import DatePicker, TimeSeries
from datetime import datetime, timedelta
import urllib2
from owslib.waterml.wml11 import WaterML_1_1 as wml11



@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    # View flood button

    t_now = datetime.now()
    now_str = "{0}-{1}-{2}".format(t_now.year, check_digit(t_now.month), check_digit(t_now.day))

    # forecast_select = SelectInput(display_text='Forecast Select',
    #                                     name='forecast_range',
    #                                     multiple=False,
    #                                     options=[('Current Forecast', 'current_forecast'),
    #                                              ],
    #                                     initial=['current_forecast'],
    #                                     original=['current_forecast'])

    get_flood = Button(display_text='View Flood ',
                           name='flood_view',
                           attributes='form=flood-form',
                           submit=True)

    # View flood forecast button
    get_forecast = Button(display_text='View Flood Forecast',
                           name='flood_forecast',
                           attributes='form=forecast-form',
                           submit=True)

    select_location_select = SelectInput(display_text='Select Location',
                                         name='select_location',
                                         multiple=False,
                                         options=[('Rapti', 'Rapti'), ('Machali', 'Machali'),
                                                  ('Kandra', 'Kandra')],
                                         initial=['Rapti'],
                                         original=['Rapti'])


    select_forecast_location_select = SelectInput(display_text='Select Location',
                                              name='select_forecast_location',
                                              multiple=False,
                                              options=[('Rapti', 'Rapti'), ('Machali', 'Machali'),
                                                       ('Kandra', 'Kandra')],
                                              initial=['Rapti'],
                                              original=['Rapti'])

    # Forecast start date selector
    forecast_date_picker = DatePicker(name='forecast_date_start',
                                            display_text='Forecast Date Start',
                                            end_date='0d',
                                            autoclose=True,
                                            format='yyyy-mm-dd',
                                            start_view='month',
                                            today_button=True,
                                            initial=now_str)



    # house_count_dict = {
    #     0: 0,
    #     0.25: 4,
    #     0.5: 4,
    #     0.75: 4,
    #     1: 4,
    #     1.25: 19,
    #     1.5:19,
    #     1.75:19,
    #     2.0:19,
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

    # I'm defining the context here because the items contained in this context are used  below (more items are added further down)
    context = {
                # "forecast_select": forecast_select,
               "get_flood": get_flood,
               "get_forecast": get_forecast,
               # "house_count_dict":house_count_dict,
               # "agriculture_count_dict": agriculture_count_dict,
               "select_location_select": select_location_select,
               "select_forecast_location_select": select_forecast_location_select,
               "forecast_date_picker": forecast_date_picker
               }

    # Get input from gizmos
    forecast_date_start = None
    select_location = 'Rapti'
    select_forecast_location = None

    if request.GET.get('forecast_date_start'):
        forecast_date_start = request.GET['forecast_date_start']
    if request.GET.get('select_location'):
            select_location = request.GET['select_location']
    if request.GET.get('select_forecast_location'):
            select_forecast_location = request.GET['select_forecast_location']

    # Get forecast data
    if select_forecast_location == 'Rapti':
        time_series_list_api = []
        subbasin = "West"
        reach_id = "4576"
        forecast_date_start_input = datetime.strptime(forecast_date_start, '%Y-%m-%d').strftime('%Y%m%d.1200')
        sfpt = "http://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetWaterML/?watershed_name=Nepal&subbasin_name={0}&reach_id={1}&start_folder={2}&stat_type=mean&token=72b145121add58bcc5843044d9f1006d9140b84b".format(subbasin, reach_id, forecast_date_start_input)
        nepal_sfpt = get_wml_values(sfpt)

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

        length = len(nepal_sfpt)

        range_slider = range(1, length + 1)
        range_list = [list(a) for a in zip(range_slider, time_series_list_api)]
        # print range_list

        forecast_start = nepal_sfpt[0][0]

        # Items to be added to context, but not defined until just before this point
        context["range_list"] = range_list
        context["forecast_start"] = forecast_start
        context["select_forecast_location"] = select_forecast_location
        context["timeseries_plot"]=timeseries_plot





    if select_forecast_location == 'Kandra':
        time_series_list_api = []
        subbasin = "West"
        reach_id = "4422"
        forecast_date_start_input = datetime.strptime(forecast_date_start, '%Y-%m-%d').strftime('%Y%m%d.1200')
        sfpt = "http://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetWaterML/?watershed_name=Nepal&subbasin_name={0}&reach_id={1}&start_folder={2}&stat_type=mean&token=72b145121add58bcc5843044d9f1006d9140b84b".format(
            subbasin, reach_id, forecast_date_start_input)
        nepal_sfpt = get_wml_values(sfpt)

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


    if select_forecast_location == 'Machali':
        time_series_list_api = []
        subbasin = "West"
        reach_id = "4371"
        forecast_date_start_input = datetime.strptime(forecast_date_start, '%Y-%m-%d').strftime('%Y%m%d.1200')
        sfpt = "http://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetWaterML/?watershed_name=Nepal&subbasin_name={0}&reach_id={1}&start_folder={2}&stat_type=mean&token=72b145121add58bcc5843044d9f1006d9140b84b".format(subbasin, reach_id, forecast_date_start_input)
        print sfpt
        nepal_sfpt = get_wml_values(sfpt)

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


    context["select_location"] = select_location

    return render(request, 'nepal_flood/home.html', context)

def animation(request):

    context = {}
    return render(request, 'nepal_flood/animation.html', context)


def get_wml_values(url):
    response = urllib2.urlopen(url)
    data = response.read()
    series = wml11(data).response
    var = series.get_series_by_variable(var_name='Flow Forecast')
    vals = var[0].values[0]
    date_vals = vals.get_date_values()
    data = [[a, float(b)] for a, b in date_vals]

    return data


# Check digits in month and day (i.e. 2016-05-09, not 2016-5-9)
def check_digit(num):
    num_str = str(num)
    if len(num_str) < 2:
        num_str = '0' + num_str
    return num_str