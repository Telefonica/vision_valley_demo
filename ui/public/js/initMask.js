
(function ($) {
    //$("#gprdimageMask").attr("src", CONF.VIDEO_FEED_MASK);
    //$("#gprdimageMask").attr("type", "application/x-mpegURL");
    //$('#gprdimageMask').on("error", function() {
    //  $(this).attr('src', 'public/img/face_mask_detector/u222-new.png');
    //});

    $("#numberMask").text("0");
    $("#numberNoMask").text("0");
    $("#fps_m").text("0");
    $("#resolucion_m").text("0x0");
    $("#inferencia_m").text("0ms");
    $("#adoption_rate").text("0%");
    
    var countMask = 0;
    var a_r = 0;

    MQTTOpenvino.connect(function (topic, payload) {
      switch(topic){
        case MQTT.TOPIC_MASK:
          document.getElementById('numberMask').innerHTML = payload.toString(); 
        break;

        case MQTT.TOPIC_FPS_M:
          document.getElementById('fps_m').innerHTML = payload.toString(); 
        break;

        case MQTT.TOPIC_RESOLUTION_M:
          document.getElementById('resolucion_m').innerHTML = payload.toString(); 
        break;

        case MQTT.TOPIC_TIME_INFERENCE_M:
          document.getElementById('inferencia_m').innerHTML = payload.toString(); 
        break;

        case MQTT.TOPIC_NO_MASK:
          document.getElementById('numberNoMask').innerHTML = payload.toString(); 
        break;
        default:
      }
    
      a_r = (parseInt($("#numberMask"))*100/(parseInt($("#numberMask")) + parseInt($("#numberNoMask")))||0).toString().concat("%");
      document.getElementById('adoption_rate').innerHTML = a_r.toString(); 
      countMask = countMask + 1;
    

    });

}) (jQuery); // end of jQuery name space



