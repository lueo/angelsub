# -*- coding: utf-8 -*-

class SubtitleFile(object):
    '''
    Subtitle files
    '''
    def __init__(self, filepath):
        self.filepath = path(filepath)
        self.lang = None
        self.ext = None
        self.delay = None
        self.online = None
        self.online_from = None
        self.content = None

