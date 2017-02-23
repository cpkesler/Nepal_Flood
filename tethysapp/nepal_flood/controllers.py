from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import SelectInput
import urllib2



@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    # View flood button
    forecast_select = SelectInput(display_text='Forecast Select',
                                        name='forecast_range',
                                        multiple=False,
                                        options=[('Current Forecast', 'current_forecast'),
                                                 ],
                                        initial=['current_forecast'],
                                        original=['current_forecast'])

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
                                         options=[('Nepal1', 'nepal1'), ('Nepal2', 'nepal2'),
                                                  ('Nepal3', 'nepal3')],
                                         initial=['nepal1'],
                                         original=['nepal1'])


    select_forecast_location_select = SelectInput(display_text='Select Location',
                                              name='select_forecast_location',
                                              multiple=False,
                                              options=[('Nepal1', 'nepal1'), ('Nepal2', 'nepal2'),
                                                       ('Nepal3', 'nepal3')],
                                              initial=['nepal1'],
                                              original=['nepal1'])


    house_count_dict = {
        0: 0,
        0.25: 4,
        0.5: 4,
        0.75: 4,
        1: 4,
        1.25: 19,
        1.5:19,
        1.75:19,
        2.0:19,
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

    # I'm defining the context here because the items contained in this context are used  below (more items are added further down)
    context = {"forecast_select": forecast_select,
               "get_flood": get_flood,
               "get_forecast": get_forecast,
               "house_count_dict":house_count_dict,
               "agriculture_count_dict": agriculture_count_dict,
               "select_location_select": select_location_select,
               "select_forecast_location_select": select_forecast_location_select
               }

    # Get input from gizmos
    forecast_range = None
    select_location = 'nepal1'
    select_forecast_location = None

    if request.GET.get('forecast_range'):
        forecast_range = request.GET['forecast_range']
    if request.GET.get('select_location'):
            select_location = request.GET['select_location']
    if request.GET.get('select_forecast_location'):
            select_forecast_location = request.GET['select_forecast_location']


    if select_forecast_location == 'nepal1':
        # Get forecast data
        time_series_list_api = []
        subbasin = "West"
        reach_id = "4458"
        forecast_date = "20170222.1200"
        sfpt = "http://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetWaterML/?watershed_name=Nepal&subbasin_name={0}&reach_id={1}&start_folder={2}&stat_type=mean&token=72b145121add58bcc5843044d9f1006d9140b84b".format(subbasin, reach_id, forecast_date)
        print sfpt
        sfpt_api = urllib2.urlopen(sfpt)
        data_api = sfpt_api.read()
        values = data_api.split('dateTimeUTC=')
        values.pop(0)
        for elm in values:
            info = elm.split(' ')
            print info, ';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;'
            value = info[8].split('<')
            value1 = value[0].replace('>', '')
            value2 = float(value1)
            value_round = round(value2)
            value_round_int = int(value_round)
            #
            # if value_round_int < 36351:
            #     value_round_int = 0
            # elif value_round_int >= 36351 and value_round_int < 41646:
            #     value_round_int = 1
            # elif value_round_int >= 41646 and value_round_int < 46491:
            #     value_round_int = 2
            # elif value_round_int >= 46491 and value_round_int < 52236:
            #     value_round_int = 3
            # elif value_round_int >= 52236 and value_round_int < 57531:
            #     value_round_int = 4
            # elif value_round_int >= 57531 and value_round_int < 62826:
            #     value_round_int = 5
            # elif value_round_int >= 62826 and value_round_int < 68121:
            #     value_round_int = 6
            # elif value_round_int >= 68121 and value_round_int < 73416:
            #     value_round_int = 7
            # elif value_round_int >= 73416 and value_round_int < 78711:
            #     value_round_int = 8
            # elif value_round_int >= 78711 and value_round_int < 84006:
            #     value_round_int = 9
            # elif value_round_int >= 84006 and value_round_int < 89301:
            #     value_round_int = 10
            # elif value_round_int >= 94596 and value_round_int < 99891:
            #     value_round_int = 11
            # elif value_round_int >= 99891:
            #     value_round_int = 12

            time_series_list_api.append(value_round_int)

        length = len(time_series_list_api)

        range_slider = 121
        range_list = [list(a) for a in zip(range_slider, time_series_list_api)]
        print range_list

        # Items to be added to context, but not defined until just before this point
        context["range_list"] = range_list

        if forecast_range:
            time_series_flood = [1.25, 1.25, 1.5, 2, 2.75, 3, 2.75, 2.5, 2.25, 1.75, 1.75, 1.5, 1.5, 1.5]
            house_count = [19,19,19,19,61,61,61,61,61,61,19,19,19,19]
            agriculture_count = [16.3, 16.3, 16.3, 16.3, 28.2, 28.3, 28.2, 28.2, 28.2, 16.3, 16.3, 16.3, 16.3]
            flood_date = ["7-Aug-2003","8-Aug-2003","9-Aug-2003","10-Aug-2003","11-Aug-2003","12-Aug-2003",
                          "13-Aug-2003","14-Aug-2003","15-Aug-2003","16-Aug-2003","17-Aug-2003","18-Aug-2003",
                          "19-Aug-2003","20-Aug-2003" ]

            forecast_range = range(1, 15)
            range_list = [list(a) for a in zip(forecast_range, time_series_flood, house_count, agriculture_count)]
            context["forecast_range"] = forecast_range
            context["range_list"] = range_list
            context["flood_date"] = flood_date
            context["select_forecast_location"] = select_forecast_location
            # context["agriculture_count"] = agriculture_count

    if select_forecast_location == 'nepal2':
        # Get forecast data
        if forecast_range:
            time_series_flood = [1.25, 1.25, 1.5, 2, 2.75, 3, 2.75, 2.5, 2.25, 1.75, 1.75, 1.5, 1.5, 1.5]
            house_count = [19, 19, 19, 19, 61, 61, 61, 61, 61, 61, 19, 19, 19, 19]
            agriculture_count = [16.3, 16.3, 16.3, 16.3, 28.2, 28.3, 28.2, 28.2, 28.2, 16.3, 16.3, 16.3, 16.3]
            flood_date = ["7-Aug-2003", "8-Aug-2003", "9-Aug-2003", "10-Aug-2003", "11-Aug-2003", "12-Aug-2003",
                          "13-Aug-2003", "14-Aug-2003", "15-Aug-2003", "16-Aug-2003", "17-Aug-2003", "18-Aug-2003",
                          "19-Aug-2003", "20-Aug-2003"]

            forecast_range = range(1, 15)
            range_list = [list(a) for a in zip(forecast_range, time_series_flood, house_count, agriculture_count)]
            context["forecast_range"] = forecast_range
            context["range_list"] = range_list
            context["flood_date"] = flood_date
            context["select_forecast_location"] = select_forecast_location
            # context["agriculture_count"] = agriculture_count

    if select_forecast_location == 'nepal3':
        # Get forecast data
        if forecast_range:
            time_series_flood = [1.25, 1.25, 1.5, 2, 2.75, 3, 2.75, 2.5, 2.25, 1.75, 1.75, 1.5, 1.5, 1.5]
            house_count = [19, 19, 19, 19, 61, 61, 61, 61, 61, 61, 19, 19, 19, 19]
            agriculture_count = [16.3, 16.3, 16.3, 16.3, 28.2, 28.3, 28.2, 28.2, 28.2, 16.3, 16.3, 16.3, 16.3]
            flood_date = ["7-Aug-2003", "8-Aug-2003", "9-Aug-2003", "10-Aug-2003", "11-Aug-2003", "12-Aug-2003",
                          "13-Aug-2003", "14-Aug-2003", "15-Aug-2003", "16-Aug-2003", "17-Aug-2003", "18-Aug-2003",
                          "19-Aug-2003", "20-Aug-2003"]

            forecast_range = range(1, 15)
            range_list = [list(a) for a in zip(forecast_range, time_series_flood, house_count, agriculture_count)]
            context["forecast_range"] = forecast_range
            context["range_list"] = range_list
            context["flood_date"] = flood_date
            context["select_forecast_location"] = select_forecast_location
            # context["agriculture_count"] = agriculture_count

    context["select_location"] = select_location

    return render(request, 'nepal_flood/home.html', context)

def animation(request):

    context = {}
    return render(request, 'nepal_flood/animation.html', context)
