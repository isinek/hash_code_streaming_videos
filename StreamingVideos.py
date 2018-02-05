from collections import OrderedDict
from operator import itemgetter

class Video:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.available = True
    
    def __str__(self):
        return 'VideoID:' + str(self.id) + '\t- VideoSIZE:' + str(self.size) + 'MB'

class Cache:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.videos = []

    def __str__(self):
        return 'CacheID:' + str(self.id) + '\t- CacheSIZE:' + str(self.size) + 'MB' + '\t- CachedVideosSIZE:' + str(sum([v.size for v in self.videos])) + 'MB'

class Endpoint:
    def __init__(self, id, latency):
        self.id = id
        self.latency = latency
        self.caches = []
        self.requests = {}
    
    def __str__(self):
        print('\tEndpointID:', self.id, '\t- EndpointLAT:', self.latency)
        print('\tCaches:')
        for x in self.caches:
            print('\t\t', x[0], '\t- CacheLAT:', str(x[1])+'ms')
        print('\tRequests:')
        for x in self.requests:
            print('\t\t', x[0], '\t- #Reqs:', x[1])
        return ''

class Datacenter:
    def __init__(self):
        self.videos = []
        self.caches = []
        self.endpoints = []

    def __str__(self):
        print('Videos:')
        for x in self.videos:
            print('\t', x)
        print('Caches:')
        for x in self.caches:
            print('\t', x)
        print('Endpoints:')
        for x in self.endpoints:
            print(x)
        return ''
    
    def sortRequests(self):
        for x in self.endpoints:
            sortedVideoIDs = OrderedDict(sorted(x.requests.items(), key=itemgetter(1), reverse=True))
            x.requests = [(self.videos[x], sortedVideoIDs[x]) for x in sortedVideoIDs]
    
    def numberOfEndpointsPerCache(self):
        endpointsPerCache = {}
        nEndpointsPerCache = {}
        for x in self.endpoints:
            for c in x.caches:
                if c[0].id in endpointsPerCache:
                    endpointsPerCache[c[0].id] += [x.id]
                    nEndpointsPerCache[c[0].id] += 1
                else:
                    endpointsPerCache[c[0].id] = [x.id]
                    nEndpointsPerCache[c[0].id] = 1
        sortedEndpointsPerCache = OrderedDict(sorted(nEndpointsPerCache.items(), key=itemgetter(1), reverse=True))
        sortedEndpointsPerCache = [(x, endpointsPerCache[x]) for x in sortedEndpointsPerCache]
        #print('Endpoints per cache: ', sortedEndpointsPerCache)
        for x in sortedEndpointsPerCache:
            videoRequestsPerCache = {}
            for e in x[1]:
                for r in self.endpoints[e].requests:
                    if r[0].id in videoRequestsPerCache:
                        videoRequestsPerCache[r[0].id] += r[1]
                    else:
                        videoRequestsPerCache[r[0].id] = r[1]
            sortedVideoRequestsPerCache = OrderedDict(sorted(videoRequestsPerCache.items(), key=itemgetter(1), reverse=True))
            sortedVideoRequestsPerCache = [(x, sortedVideoRequestsPerCache[x]) for x in sortedVideoRequestsPerCache]
            #print('CacheId:', x[0], sortedVideoRequestsPerCache)
            for v in sortedVideoRequestsPerCache:
                if self.videos[v[0]].available and self.videos[v[0]].size + sum([cv.size for cv in self.caches[x[0]].videos]) <= self.caches[x[0]].size:
                    self.caches[x[0]].videos.append(self.videos[v[0]])
                    self.videos[v[0]].available = False
            #print(self.caches[x[0]])
            #print(self.caches[x[0]].videos)
    
    def printCachesAndVideos(self):
        cachesForPrint = [c for c in self.caches if len(c.videos)]
        print(len(cachesForPrint))
        for c in cachesForPrint:
            print(c.id, ' '.join([str(v.id) for v in c.videos]))

def main():
    datacenter = Datacenter()
    V, E, R, C, X = [int(x) for x in input().split()]
    for i in range(C):
        datacenter.caches.append(Cache(i, X))
    i = 0
    for x in input().split():
        datacenter.videos.append(Video(i, int(x)))
        i += 1
    for i in range(E):
        lat, n = [int(x) for x in input().split()]
        datacenter.endpoints.append(Endpoint(i, lat))
        for j in range(n):
            cacheId, cacheLatency = [int(x) for x in input().split()]
            datacenter.endpoints[-1].caches.append((datacenter.caches[cacheId], cacheLatency))
    for i in range(R):
        v, e, rs = [int(x) for x in input().split()]
        if datacenter.videos[v] in datacenter.endpoints[e].requests:
            datacenter.endpoints[e].requests[v] += rs
        else:
            datacenter.endpoints[e].requests[v] = rs
    datacenter.sortRequests()
    #print(datacenter)
    datacenter.numberOfEndpointsPerCache()
    datacenter.printCachesAndVideos()

if __name__ == "__main__":
    main()
