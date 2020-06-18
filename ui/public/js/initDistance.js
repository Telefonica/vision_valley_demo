
(function ($) {
    //$("#gprdimageDist").attr("src", CONF.VIDEO_FEED_DISTANCE);
    //$("#gprdimageDist").attr("onerror", 'public/img/social_distance_monitor/u214.png');
    //$('#gprdimageDist').on("error", function() {
    //  $(this).attr('src', 'public/img/social_distance_monitor/u214.png');
    //});

    $("#numberTotal").text("0");
    $("#numberSafe").text("0");
    $("#numberLow").text("0");
    $("#numberHigh").text("0");
    $("#fps_d").text("0");
    $("#resolucion_d").text("0x0");
    $("#inferencia_d").text("0ms");

    var countDist = 0;
    
    MQTTOpenvino.connect(function (topic, payload) {
      switch(topic){

        case MQTT.TOPIC_FPS_D:
          document.getElementById('fps_d').innerHTML = payload.toString(); 
        break;

        case MQTT.TOPIC_RESOLUTION_D:
          document.getElementById('resolucion_d').innerHTML = payload.toString();
        break;

        case MQTT.TOPIC_TIME_INFERENCE_D:
          document.getElementById('inferencia_d').innerHTML = payload.toString();  
        break;

        case MQTT.TOPIC_HIGHRISK:
          document.getElementById('numberHigh').innerHTML = payload.toString();
        break;

        case MQTT.TOPIC_SAFE:
          document.getElementById('numberSafe').innerHTML = payload.toString();
        break;

        case MQTT.TOPIC_LOWRISK:
          document.getElementById('numberLow').innerHTML = payload.toString();
        break;
        default:
      }
    
    
      countDist = countDist + 1;
    

    });

}) (jQuery); // end of jQuery name space