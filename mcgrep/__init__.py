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
            if not s.connect():
                continue
            if s.family == socket.AF_INET:
                name = '%s:%s (%s)' % ( s.ip, s.port, s.weight )
            else:
                name = 'unix:%s (%s)' % ( s.address, s.weight )
            sdata = {}
            data.append((name, sdata))
            s.send_cmd('stats cachedump %d %d' % (slab_id, key_limit))
            while 1:
                line = s.readline()
                if not line or line.strip() == 'END':
                    break
                m = re.match('^ITEM (?P<key>\S+) '
                             '\[(?P<size>\d+) b; '
                             '(?P<expires>\d+) s\]', line)
                if m:
                    key = m.group('key')
                    sdata[key] = dict(size=m.group('size'),
                                      expires=m.group('expires'))
        return data


class Leecher(object):

    def __init__(self, mc):
        self.mc = mc

    def leech(self, slabs_to_retrieve=None, key_limit=0, key_regex=None):
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
                   help="connect to server. defaults to localhost",
                   action='append', type='string')
    opt.add_option('-K', '--key-limit', dest='key_limit',
                   help="number of keys to pull per slab",
                   action='store', type='int', default=0)
    opt.add_option('-m', '--match-keys', dest='key_regex',
                   help="match keys against this regex",
                   action='store', type='string')
    opt.add_option('-V', '--values', dest='print_values',
                   help="print full values of keys",
                   action='store_true', default=False)

    if argv is None:
        argv = sys.argv[1:]
    options, args = opt.parse_args(argv)

    if not options.servers:
        servers = ['localhost:11211']
    else:
        servers = options.servers
    leecher = Leecher(ExtendedClient(servers))

    if options.key_regex:
        key_regex = re.compile(options.key_regex)
    else:
        key_regex = None

    if len(args) > 0:
        all_regex = re.compile(args[0])
    else:
        all_regex = None

    for key, val in leecher.leech(key_limit=options.key_limit,
                                  key_regex=key_regex):
        val = repr(val)
        if all_regex and (not (all_regex.search(val) or
                               all_regex.search(key))):
            continue
        if options.print_values:
            print "%s:%s" % (key, val)
        else:
            print key


if __name__ == '__main__':
    main()
