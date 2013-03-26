# -*- coding: utf-8 -*-
from path import path
from subtitles import Subtitles

class VideoFile(object):

    def __init__(self, filepath):
        self.filepath = path(filepath)
        self.subs = Subtitles(self)

    @property
    def exists(self):
        try:
            if self.filepath.exists():
                return True
            else:
                logging.error('The file in ""%s" does not exist! ' % filepath)
                self.subs = None
                return False
        except(), why:
            logging.error(why)
            return False

    @property
    def size(self):
        if self.exists():
            return self.filepath.getsize()
        else:
            return None


