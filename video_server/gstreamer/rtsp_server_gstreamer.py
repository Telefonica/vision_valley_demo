import gi
import argparse
import os
from configobj import ConfigObj
gi.require_version('Gst','1.0')
from gi.repository import GObject, Gst, GstVideo, GstRtspServer, GstRtsp
os.environ["GST_DEBUG"] = "3"

def main(args):
    
    config_path = args.config_path
         
    parser = ConfigObj(config_path)

    file_location = parser['file_location']
    rstp_host = parser['host']
    rstp_port = parser['port']
    factory_name = parser['factory_name']

    Gst.init(None)
    mainloop = GObject.MainLoop()


    server = GstRtspServer.RTSPServer.new()

    server.set_address(rstp_host)
    server.set_service(rstp_port)

    mounts = server.get_mount_points()

    factory = GstRtspServer.RTSPMediaFactory()
    factory.set_launch('filesrc location =%s ! qtdemux ! h264parse config-interval=-1 ! rtph264pay pt=96 config-interval=-1 name=pay0' % (file_location))
    factory.set_shared(True)
    factory.set_buffer_size(4294967295)
    factory.set_protocols(GstRtsp.RTSPLowerTrans(1))
    #factory.set_transport_mode(GstRtspServer.RTSPTransportMode.PLAY)

    mounts.add_factory(factory_name, factory)

    server.attach(None)

    print("Stream ready at rtsp://%s:%s%s" % (rstp_host, rstp_port, factory_name))
    mainloop.run()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser("RSTP stream (IP camera simulation for preloaded videos)")
    parser.add_argument('-config_path', help="Path to gserver.conf", type=str, required=True)
    args = parser.parse_args()

    main(args)
