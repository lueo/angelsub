# -*- coding: utf-8 -*-
import codecs
import mafan
import chardet
import difflib
import gzip
import struct
import io
import random
import time
import ipdb
import logging
import requests
import hashlib
from path import path

logging.basicConfig(level=logging.DEBUG)

Class VideoFile(object):
    ```
    Class for video file
    ```

    def __init(self, filepath):
        self.filepath = path(filepath)
        self.size = self.filepath.getsize()
        self.shash = self.gen_filehash()

def genShash(filepath):
    result = []
    # calc shash
    sz = filepath.getsize()
    if sz < 8192:
        raise IOError, 'File size too small!'
    with open(filepath, 'rb') as f:
        for _ in [4096, sz/3*2, sz/3, sz - 8192]:
            f.seek(_)
            result.append(hashlib.md5(f.read(4096)).hexdigest())
    return ';'.join(result)

def fetchSubtitle(filepath):
    filehash = genShash(filepath)
    servers = ['www', 'splayer', 'svplayer'] + ['splayer'+str(i) for i in range(1,13)]
    splayer_rev = 2437 # as of 2012-07-02
    # tries = [2, 10, 30, 60, 120]

    # generate data for submission
    # shooter.cn uses UTF-8.
    head,tail = path.splitpath(filepath)
    pathinfo = '\\'.join(['D:', head.basename(), tail])
    v_fingerpint = b'SP,aerSP,aer {0} &e(\xd7\x02 {1} {2}'.format(splayer_rev,
            pathinfo.encode('utf_8'), filehash.encode('utf_8'))
    vhash = hashlib.md5(v_fingerpint).hexdigest()


    header = {'User-Agent': 'SPlayer Build {0}'.format(splayer_rev)}
    data = {'filehash': filehash, 'pathinfo': pathinfo, 'vhash': vhash}


    # Fetch it!

    url = random.choice(['http', 'https']) + '://' + random.choice(servers) + '.shooter.cn/api/subapi.php'
    logging.debug('URL: ' + url)

    res = requests.post(url, data=data, headers=header, verify=False)

    sub = parse_shooter_package(res.raw)

    return sub

def parse_shooter_package(fileobj):
    '''
    Parse shooter returned package of subtitles.
    Return subtitles encoded in UTF-8.

    result:
    1       SubPackage count(loop)
        4       Package Data Length
        4       Desc Data Length(iDescLength)
        iDescLength     Desc Data
        4       File Data Length
        1       File count(loop)
            4       File Pack Length
            4       File Ext Name Length(iExtLength)
            iExtLength      File Ext Name
            4       File Data Length
    '''
    subtitles = []

    # read contents
    f = fileobj
    c = f.read(1)
    package_count = struct.unpack(b'!b', c)[0]
    logging.debug('{0} package(s) fetched.'.format(package_count))

    for i in range(package_count):
        # NOTE: '_' is the length of following byte-stream
        c = f.read(8)
        _ , desc_length = struct.unpack(b'!II', c)
        description = f.read(desc_length).decode('utf_8')

        # delay in msec.
        # TODO: try to adjust subtitle automatically
        sub_delay = 0
        if description:
            logging.debug('Subtitle description: {0}'.format(description))
            if 'delay' in description:
                sub_delay = description.split('=')[1]

        # Files in package
        c = f.read(5)
        _ , file_count = struct.unpack(b'!IB', c)
        logging.debug('{0} file(s) fetched.'.format(file_count))

        for j in range(file_count):
            c = f.read(8)
            _ , ext_len = struct.unpack(b'!II', c)
            ext = f.read(ext_len)

            c = f.read(4)
            file_len = struct.unpack(b'!I', c)[0]
            sub = f.read(file_len)
            if sub.startswith(b'\x1f\x8b'):
                sub = gzip.GzipFile(fileobj=io.BytesIO(sub)).read()

            subtitles.append({'extension': ext,
                'delay': sub_delay,
                'content': sub})

    logging.debug('Total {0} subtitle(s) fetched.'.format(len(subtitles)))

    return dup_check(subtitles)

def dup_check(subtitles):
    ''' Check if there are dplicated subtitles.

    :returns: subtitles Subtitles without duplication.
    '''
    # convert all encoding to utf-8, trad -> simp
    for sub in subtitles:
        enc = chardet.detect(sub['content'])['encoding']
        # for simp. chinese
        if enc == 'GB2312':
            sub['content'] = sub['content'].decode('gb18030')
        else:
            sub['content'] = sub['content'].decode(enc)
        # for big5, convert!
        if enc == 'Big5':
            sub['content'] = mafan.simplify(sub['content'])

    # find dups
    dup_tags = [False] * len(subtitles)
    for i in range(len(subtitles)):
        for j in range(i+1, len(subtitles)):
            sub_a = subtitles[i]['content']
            sub_b = subtitles[j]['content']
            sim = difflib.SequenceMatcher(None, sub_a, sub_b).real_quick_ratio()
            logging.debug('Similar ratio between %d and %d is %f' % (i, j, sim))
            if sim >= 0.9:
                if len(sub_a) >= len(sub_b):
                    dup_tags[j] = True
                else:
                    dup_tags[i] = True

    new_subs = [s for i, s in enumerate(subtitles) if dup_tags[i] == False]

    logging.debug('Total %d subtitles remains.' % len(new_subs)) 

    return new_subs

def main():
    d = "/media/Video/Video/movie/Doomsday Book (2012)/"
    m = "Dooms.Day.Report.2012.KOREA.720p.HDRip.x264.AC3-JYK.avi"
    f = path(d) / m
    subs = []

    while (subs == []):
        try:
            subs = fetchSubtitle(f)
        except (requests.ConnectionError, OSError, IOError), why:
            logging.Error(why)

    filename, ext = f.basename().splitext() 
    dirname = f.dirname()

    for s in subs:
        print s['extension']
        print s['delay']
        print s['content'][:20]
        filepath = dirname + filename + s['extension']
        logging.debug('saving file to %s'% filepath)
        with codecs.open(filepath, 'w', encoding='utf-8') as f:
            f.write(s['content'])

if __name__ == '__main__':
    main()
