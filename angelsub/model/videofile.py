# -*- coding: utf-8 -*-
import logging
from path import path
from subtitles import Subtitles

class VideoFile(object):

    def __init__(self, filepath):
        self.filepath = path(filepath)

    @property
    def exists(self):
        try:
            return self.filepath.exists()
        except(), why:
            logging.error(why)
            return False

    @property
    def size(self):
        if self.exists:
            return self.filepath.getsize()
        else:
            return None

    @property
    def subs(self):
        if self.exists:
            return Subtitles(self)
        else:
            return None
