$(function() {
    var url =  window.location.href;
    if(url.indexOf("select_forecast_location") > 0) {
        $("#gen-alert").removeClass("hidden");
    }
    var onSuccess = function(e){
   var image1 = document.createElement("image1");
   image1.id = "image1";
    document.body.appendChild(image1);
   document.getElementById('image1').setAttribute("dataurl",e.data);
  };
    var onSuccess2 = function(e){
   var image2 = document.createElement("image2");
   image2.id = "image2";
    document.body.appendChild(image2);
   document.getElementById('image2').setAttribute("dataurl",e.data);
  };

  var onError = function(e){
  alert(e.message);
  };

 getImageDataURL('http://tethys.byu.edu/static/servir/images/servir.png', onSuccess, onError);
getImageDataURL('http://tethys.byu.edu/static/nepal_flood/images/icimod.png',onSuccess2,onError);

 function getImageDataURL(url, success, error) {
    var data, canvas, ctx;
    var img = new Image();
    img.setAttribute('crossOrigin', 'anonymous');
    img.onload = function(){
        // Create the canvas element.
        canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        // Get '2d' context and draw the image.
        ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        // Get canvas data URL
        try{
            data = canvas.toDataURL();
            success({image:img, data:data});
        }catch(e){
            error(e);
        }
    };
    // Load image URL.
    try{
        img.src = url;
    }catch(e){
        error(e);
    }
};
    $('#select_forecast_location').parent().addClass('hidden');
    $('#select_forecast_location').hide();
    $('label[for="select_location"]').hide();
    $('#select_location').on('change',function () {
    var loc = $('#select_location').val();
    $('#select_forecast_location').val(loc);
    if ($('#select_location').val() == 'Rapti') {
        $('#forecast_date_start_macheli').parent().addClass('hidden');
        $('#forecast_date_start_kandra').parent().addClass('hidden');
        $('#forecast_date_start_rapti').parent().removeClass('hidden');
    }
    else if ($('#select_location').val() === 'Macheli') {
        $('#forecast_date_start_macheli').parent().removeClass('hidden');
        $('#forecast_date_start_kandra').parent().addClass('hidden');
        $('#forecast_date_start_rapti').parent().addClass('hidden');
    }
    else if ($('#select_location').val() === 'Kandra'){
        $('#forecast_date_start_macheli').parent().addClass('hidden');
        $('#forecast_date_start_kandra').parent().removeClass('hidden');
        $('#forecast_date_start_rapti').parent().addClass('hidden');
        }
    }).change();
});

 function createExportCanvas(mapCanvas) {

        var exportCanvas;
        var context;

        exportCanvas = $('#export-canvas')[0];
        exportCanvas.width = mapCanvas.width;
        exportCanvas.height = mapCanvas.height;
        mapCanvas.crossOrigin = 'Anonymous';
        context = exportCanvas.getContext('2d');
        context.drawImage(mapCanvas, 0, 0);

        return exportCanvas;
    };