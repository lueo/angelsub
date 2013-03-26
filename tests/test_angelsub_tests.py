# -*- coding: utf-8 -*-
from nose.tools import *
from angelsub.model.videofile import VideoFile
import angelsub
import logging

vf = None
f = None

def setup():
    """Setup tests."""
    global f
    global vf

    d = "/media/Video/Video/movie/Doomsday Book (2012)/"
    m = "Dooms.Day.Report.2012.KOREA.720p.HDRip.x264.AC3-JYK.avi"
    f = d + m
    vf = VideoFile(f)


def teardown():
    """Tear down tests."""
    logging.debug('tear Down.')
    pass

def test_get_version():
    assert type(angelsub.get_version()) == str


@with_setup(setup, teardown)
def test_get_shooter_hash():
    assert vf.subs.shooter_hash == '102e4264c2dfcdd94863e7bd736b4c1a;f0e558faee4adba6539f9a24bc9468a9;a545ac432fc0f6580bf57849e06e5324;2095412a05e9c217c847a51aafa9ad15', 'hash wrong!'

@with_setup(setup, teardown)
def test_get_shooter_subtitle():
    # assert len(vf.subs.shooter_subs) == 2, "returned subs not right!"
    pass

@with_setup(setup, teardown)
def test_videofile():
    f = "/non-exist/file.avi"
    vf = VideoFile(f)
    assert vf.exists() == False, "Can't detect non-exist file!"
