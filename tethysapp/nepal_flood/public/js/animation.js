var map;
      require([
        "esri/map", "esri/layers/ArcGISDynamicMapServiceLayer",
        "esri/TimeExtent", "esri/dijit/TimeSlider",
        "dojo/_base/array", "dojo/dom", "dojo/domReady!"
      ], function(
        Map, ArcGISDynamicMapServiceLayer,
        TimeExtent, TimeSlider,
        arrayUtils, dom
      ) {
        map = new Map("mapDiv", {
          basemap: "streets",
          center: [81.80, 28.004],
          zoom: 11
        });

        var opLayer = new ArcGISDynamicMapServiceLayer("http://geoserver.byu.edu/arcgis/rest/services/sandbox/nepal_animation/MapServer");
//        opLayer.setVisibleLayers([0]);

        //apply a definition expression so only some features are shown
//        var layerDefinitions = [];
//        layerDefinitions[0] = "FIELD_KID=1000148164";
//        opLayer.setLayerDefinitions(layerDefinitions);

        //add the gas fields layer to the map
        map.addLayers([opLayer]);

        map.on("layers-add-result", initSlider);

        function initSlider() {
          var timeSlider = new TimeSlider({
            style: "width: 100%;"
          }, dom.byId("timeSliderDiv"));
          map.setTimeSlider(timeSlider);

          var timeExtent = new TimeExtent();
          timeExtent.startTime = new Date("1/1/2017");
          timeExtent.endTime = new Date("1/5/2017");
          timeSlider.setThumbCount(2);
          timeSlider.createTimeStopsByTimeInterval(timeExtent, 1, "esriTimeUnitsDays");
          timeSlider.setThumbIndexes([0,1]);
          timeSlider.setThumbMovingRate(2000);
          timeSlider.startup();
          timeSlider.setLoop(true);

          //add labels for every other time stop
          var labels = arrayUtils.map(timeSlider.timeStops, function(timeStop, i) {
            if ( i % 1 === 0 ) {
              return timeStop.toDateString();
            } else {
              return "";
            }
          });

          timeSlider.setLabels(labels);

          timeSlider.on("time-extent-change", function(evt) {
            var startValString = "1/1/17";
            var endValString = "1/5/17";
            dom.byId("daterange").innerHTML = "<i>" + startValString + " to " + endValString  + "<\/i>";
          });
        }
      });