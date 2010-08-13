import sys
import socket
import zlib
import re
import memcache

__version__ = '0.1'


class ExtendedClient(memcache.Client):

    def get_keys(self, slab_id, key_limit):
        data = []
        for s in self.servers:
            if not s.connect(): continue
            if s.family == socket.AF_INET:
                name = '%s:%s (%s)' % ( s.ip, s.port, s.weight )
            else:
                name = 'unix:%s (%s)' % ( s.address, s.weight )
            serverData = {}
            data.append((name, serverData))
            s.send_cmd('stats cachedump %d %d' % (slab_id, key_limit))
            readline = s.readline
            while 1:
                line = readline()
                if not line or line.strip() == 'END': break
                m = re.match('^ITEM (?P<key>\S+) '
                             '\[(?P<size>\d+) b; '
                             '(?P<expires>\d+) s\]', line)
                if m:
                    key = m.group('key')
                    serverData[key] = dict(size=m.group('size'),
                                           expires=m.group('expires'))
        return data


class Leacher(object):

    def __init__(self, mc):
        self.mc = mc

    def leach(self, slabs_to_retrieve=None, key_limit=0, key_regex=None):
        if slabs_to_retrieve:
            # just retrieve these slab IDs
            slabs_to_retrieve = set(slabs_to_retrieve)
        else:
            # get all slab IDs
            slabs_to_retrieve = set()
            for sname, sdata in self.mc.get_slabs():
                for slab_id in sdata.keys():
                    slabs_to_retrieve.add(int(slab_id))

        for slab_id in slabs_to_retrieve:
            for sname, sdata in self.mc.get_keys(slab_id, key_limit):
                for key in sdata.keys():
                    if key_regex and (not key_regex.search(key)):
                        continue
                    try:
                        val = self.mc.get(key)
                    except zlib.error, e:
                        val = e
                    yield key, val


def main(argv=None):
    from optparse import OptionParser
    opt = OptionParser(usage="usage: %prog [options] [PATTERN]",
                       version="%%prog %s" % __version__)
    opt.add_option('-s', '--server', dest='servers',
                   help="connect to server", action='append',
                   type='string')
    opt.add_option('-K', '--key-limit', dest='key_limit',
                   help="number of keys to pull per slab",
                   action='store', type='int', default=0)

    if argv is None:
        argv = sys.argv[1:]
    options, args = opt.parse_args(argv)

    if len(args) > 0:
        key_regex = re.compile(args[0])
    else:
        key_regex = None

    leacher = Leacher(ExtendedClient(options.servers))
    for key, val in leacher.leach(key_limit=options.key_limit,
                                  key_regex=key_regex):
        print key
        #print "%s:%s" % (key, val)


if __name__ == '__main__':
    main()
