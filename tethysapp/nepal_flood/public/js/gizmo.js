$(function() {
    $('#select_forecast_location').parent().addClass('hidden');
    $('#select_forecast_location').hide();
    $('#select_location').on('change',function () {
    var loc = $('#select_location').val();
    $('#select_forecast_location').val(loc);
    }).change();
});
