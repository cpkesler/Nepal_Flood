//Here we are declaring the projection object for Web Mercator
var projection = ol.proj.get('EPSG:3857');

//Define Basemap
//Here we are declaring the raster layer as a separate object to put in the map later
var baseLayer = new ol.layer.Tile({
    source: new ol.source.BingMaps({
        key: '5TC0yID7CYaqv3nVQLKe~xWVt4aXWMJq2Ed72cO4xsA~ApdeyQwHyH_btMjQS1NJ7OHKY8BK-W-EMQMrIavoQUMYXeZIQOUURnKGBOC7UCt4',
        imagerySet: 'AerialWithLabels'  // Options 'Aerial', 'AerialWithLabels', 'Road'
        })
    });

//Define all WMS Sources:

var FloodMap =  new ol.source.TileWMS({
        url:'',

        params:{
            LAYERS:"0",
//            FORMAT:"image/png", //Not a necessary line, but maybe useful if needed later
        },
        crossOrigin: 'Anonymous' //This is necessary for CORS security in the browser
        });

var FloodMapHiRes =  new ol.source.TileWMS({
        url:'',

        params:{
            LAYERS:"0",
//            FORMAT:"image/png", //Not a necessary line, but maybe useful if needed later
        },
        crossOrigin: 'Anonymous' //This is necessary for CORS security in the browser
        });


var flood = new ol.layer.Tile({
    source:FloodMap
    }); //Thanks to http://jsfiddle.net/GFarkas/tr0s6uno/ for getting the layer working

var floodHiRes = new ol.layer.Tile({
    source:FloodMapHiRes
    }); //Thanks to http://jsfiddle.net/GFarkas/tr0s6uno/ for getting the layer working

//Set opacity of layers
flood.setOpacity(0.8);
floodHiRes.setOpacity(0.8);

sources = [FloodMap, FloodMapHiRes];
layers = [baseLayer, flood, floodHiRes];

//Establish the view area. Note the reprojection from lat long (EPSG:4326) to Web Mercator (EPSG:3857)
var view = new ol.View({
        center: [9111517, 3258918],
        projection: projection,
        zoom: 11,
    })

//Declare the map object itself.
var map = new ol.Map({
    target: document.getElementById("map"),
    layers: layers,
    view: view,
});

map.addControl(new ol.control.ZoomSlider());

//This function is ran to set a listener to update the map size when the navigation pane is opened or closed
(function () {
    var target, observer, config;
    // select the target node
    target = $('#app-content-wrapper')[0];

    observer = new MutationObserver(function () {
        window.setTimeout(function () {
            map.updateSize();
        }, 350);
    });

    config = {attributes: true};

    observer.observe(target, config);
}());

//Here we set the styles and inital setting for the slider bar (https://jqueryui.com/slider/#steps)
$(function() {
    $( "#slider" ).slider({
      value:0,
      min: 0,
      max: 8,
      step: 1,
      slide: function( event, ui ) {
        $( "#amount" ).val( ui.value );
        var decimal_value = ui.value.toString().split(".").join("")
        if (ui.value != 0) {
            var url = 'http://geoserver.byu.edu/arcgis/services/Nepal_West/Nepal_' + decimal_value + '/MapServer/WmsServer?';
            var url1 = 'http://geoserver.byu.edu/arcgis/services/Nepal_West_HiRes/Nepal_' + decimal_value + '/MapServer/WmsServer?';
           }
        else {
            var url = ''
            var url1 = ''
        }
            FloodMap.setUrl(url);
            FloodMapHiRes.setUrl(url1);

      }
    });
    $( "#amount" ).val( $( "#slider" ).slider( "value" ) );
  });