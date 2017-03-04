$(function() {
    $('#select_forecast_location').parent().addClass('hidden');
    $('#select_forecast_location').hide();
    $('label[for="select_location"]').hide();
    $('#select_location').on('change',function () {
    var loc = $('#select_location').val();
    $('#select_forecast_location').val(loc);
    if ($('#select_location').val() == 'Rapti') {
        console.log("f this shit");
        $('#forecast_date_start_macheli').parent().addClass('hidden');
        $('#forecast_date_start_kandra').parent().addClass('hidden');
        $('#forecast_date_start_rapti').parent().removeClass('hidden');
    }
    else if ($('#select_location').val() === 'Macheli') {
        $('#forecast_date_start_macheli').parent().removeClass('hidden');
        $('#forecast_date_start_kandra').parent().addClass('hidden');
        $('#forecast_date_start_rapti').parent().addClass('hidden');
    }
    else if ($('#forecast_range').val() === 'Kandra'){
        $('#forecast_date_start_macheli').parent().addClass('hidden');
        $('#forecast_date_start_kandra').parent().removeClass('hidden');
        $('#forecast_date_start_rapti').parent().addClass('hidden');
        }
    }).change();
});
