# -*- coding: utf-8 -*-
from videofile import VideoFile

logging.basicConfig(level=logging.DEBUG)

def main():

    d = "/media/Video/Video/movie/Doomsday Book (2012)/"
    m = "Dooms.Day.Report.2012.KOREA.720p.HDRip.x264.AC3-JYK.avi"
    f = d + m
    
    vf = VideoFile(f)

    print vf.subs.local
    vf.subs.get_shooter()
    print vf.subs.shooter
    # vf.subs.organize()
    vf.subs.sync()

if __name__ == '__main__':
    main()
