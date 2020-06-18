(function ($) {
  //$("#gprdimage").attr("src", overlapStreams(CONF.VIDEO_FEED, CONF.INFERENCE_FEED));
  //$("#gprdimage").attr("src", CONF.VIDEO_FEED_PEOPLE);
  /*$('#gprdimage').on("error", function() {
    $(this).attr('src', 'public/img/crow_event_detection/u139.png');
  });*/
  //$("#gprdimage").attr("type", "application/x-mpegURL");
  $("#numberPeople").text("0");
  //$("#numberPeopleMax").text("0");
  $("#lastAlert").text("DD:MM:YY:hh:mm:ss");
  $("#fps").text("0");
  $("#resolucion").text("0x0");
  $("#inferencia").text("0ms");


  /*var video;

  video = videojs(document.getElementById('gprdimage'), {
    autoplay: true,
    sources: [{
        type: "application/x-mpegURL",
        src: CONF.VIDEO_FEED_PEOPLE
      }]
  });

  video.poster('public/img/crow_event_detection/u139.png');
  */

  document.getElementsByClassName("warning")[0].style.display = 'none';
  var moment = new Date();
  //var timestring = moment.now()
  //var limit = document.getElementById("limit_people").value;

  var countPeople = 0;

  MQTTOpenvino.connect(function (topic, payload) {
        switch(topic){
          case MQTT.TOPIC_PERSON:
            document.getElementById('numberPeople').innerHTML = payload.toString();             

            if(parseInt(payload) > parseInt(document.getElementById("limit_people").value)){
              document.getElementsByClassName("warning")[0].style.display = 'block';  
              document.getElementById('lastAlert').innerHTML = Date(moment).toString().replace(" GMT+0200 (Central European Summer Time)","");                 
            } else {
              document.getElementsByClassName("warning")[0].style.display = 'none';
            }
          break;

          case MQTT.TOPIC_FPS:
            document.getElementById('fps').innerHTML = payload.toString();  
          break;

          case MQTT.TOPIC_RESOLUTION:
            document.getElementById('resolucion').innerHTML = payload.toString();      
          break;

          case MQTT.TOPIC_TIME_INFERENCE:
            document.getElementById('inferencia').innerHTML = payload.toString();  
          break;
          default:
        }
        
        countPeople = countPeople + 1;
      

  });

}) (jQuery); // end of jQuery name space

