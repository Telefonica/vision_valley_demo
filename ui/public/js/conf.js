var CONF = {
    VIDEO_FEED_PEOPLE : "http://localhost:8090/crowd/stream.m3u8",
    VIDEO_FEED_MASK : "http://localhost:8090/mask/stream.m3u8",
    VIDEO_FEED_DISTANCE : "http://localhost:8090/dist/stream.m3u8"
}

var MQTT = {
	SERVER : "localhost",
    PORT : "3000",
    TOPIC_PERSON:"person",
    TOPIC_TIME_INFERENCE:"person/inference",
    TOPIC_FPS:"video/fps",
    TOPIC_RESOLUTION: "video/resolution",
    TOPIC_MASK: "mask",
    TOPIC_NO_MASK: "no_mask",
    TOPIC_TIME_INFERENCE_M:"mask/inference",
    TOPIC_FPS_M:"video_m/fps",
    TOPIC_RESOLUTION_M: "video_m/resolution",
    TOPIC_TIME_INFERENCE_D:"dist/inference",
    TOPIC_FPS_D:"video_d/fps",
    TOPIC_RESOLUTION_D: "video_d/resolution",
    TOPIC_TOTAL: "dist/total",
    TOPIC_SAFE: "dist/safe",
    TOPIC_LOWRISK: "dist/lowrisk",
    TOPIC_HIGHRISK: "dist/highrisk"
}