from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import SelectInput


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

    # house_count = [4,4,4,4,19,19,19,19,61,61,61,61,142,142,142,143,224,224,224,225]

    # I'm defining the context here because the items contained in this context are used  below (more items are added further down)
    context = {"forecast_select": forecast_select,
               "get_flood": get_flood,
               "get_forecast": get_forecast,
                "house_count_dict":house_count_dict}

    # Get input from gizmos
    forecast_range = None

    if request.GET.get('forecast_range'):
        forecast_range = request.GET['forecast_range']

        # Get forecast data
        if forecast_range:
            time_series_flood = [1.25, 1.25, 1.5, 2, 2.75, 3, 2.75, 2.5, 2.25, 1.75, 1.75, 1.5, 1.5, 1.5]
            house_count = [19,19,19,19,61,61,61,61,61,61,19,19,19,19]
            flood_date = ["7-Aug-2003","8-Aug-2003","9-Aug-2003","10-Aug-2003","11-Aug-2003","12-Aug-2003",
                          "13-Aug-2003","14-Aug-2003","15-Aug-2003","16-Aug-2003","17-Aug-2003","18-Aug-2003",
                          "19-Aug-2003","20-Aug-2003" ]

            forecast_range = range(1, 15)
            range_list = [list(a) for a in zip(forecast_range, time_series_flood, house_count)]
            context["forecast_range"] = forecast_range
            context["range_list"] = range_list
            context["flood_date"] = flood_date


    return render(request, 'nepal_flood/home.html', context)