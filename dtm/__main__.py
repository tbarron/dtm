"""
Usage:
    dtm splat [-d]
    dtm utl [-d] UTC_DTSPEC TIMEZONE
    dtm ltu [-d] LOC_DTSPEC TIMEZONE
    dtm zones [-d] [SEARCH]
    dtm zdetails [-d] TIMEZONE
    dtm westeast [-d]

time.time() provides the number of seconds since the epoch and defines UTC

datetime.now().timestamp() provides the same value as time.time()

datetime.utcnow().timestamp() provides time.time() + utcoffset. For my timezone
currently, this is four hours beyond UTC.

The following sequences provide valid human-readable displays of UTC:

    a = time.time()
    time.strftime(fmt, time.gmtime(a))

    a = datetime.now().timestamp()
    datetime.utcfromtimestamp(a).strftime(fmt)

    a = datetime.utcnow().timestamp()
    datetime.fromtimestamp(a).strftime(fmt)
"""
from docopt_dispatch import dispatch
from datetime import datetime
import pdb
import pytz
import time


# -----------------------------------------------------------------------------
@dispatch.on('ltu')
def utc_fr_local_tz(**kw):
    """
    Compute local time from utc and timezone
    """
    if kw['d']:
        pdb.set_trace()
    dtspec = kw['UTC_DTSPEC']
    tz = kw['TIMEZONE']
    tzobj = pytz.timezone(tz)
    utc = pytz.timezone('utc')
    fmt = "%Y.%m%d %H:%M:%S"
    nl = datetime.strptime(dtspec, fmt)
    nl = tzobj.normalize(tzobj.localize(nl))
    print(nl.astimezone(utc).timestamp())
    print(nl.timestamp())


# -----------------------------------------------------------------------------
@dispatch.on('utl')
def utc_fr_local_tz(**kw):
    """
    Compute utc time from local time and timezone
    """

# -----------------------------------------------------------------------------
@dispatch.on('splat')
def splat(**kw):
    """
    Will the real UTC please stand up?
    """
    if kw['d']:
        pdb.set_trace()
    plugh("t", time.time())
    plugh("n", datetime.now().timestamp())
    plugh("u", datetime.utcnow().timestamp())


# -----------------------------------------------------------------------------
def plugh(label, value):
    """
    Contort the value and see what happens
    """
    value = int(value)
    print("{}: {}".format(label, value))

    fmt = "%Y.%m%d %H:%M:%S"
    print(time.strftime(fmt, time.gmtime(value)))
    print(datetime.utcfromtimestamp(value).strftime(fmt))

    g = time.gmtime(value)
    edge = value - (g.tm_sec + 60*(g.tm_min + 60*(g.tm_hour)))
    print(time.strftime(fmt, time.gmtime(edge)))

    print(edge / (24*3600))


# -----------------------------------------------------------------------------
@dispatch.on('zones')
def zones(**kw):
    if kw['d']:
        pdb.set_trace()

    zlist = pytz.all_timezones
    if kw['SEARCH']:
        for each in zlist:
            if kw['SEARCH'] in each:
                print(each)
    else:
        zdict = {}
        for each in zlist:
            pieces = each.split('/')
            dct = zdict
            for chunk in pieces:
                try:
                    dct = dct[chunk]
                except KeyError:
                    dct[chunk] = {}
                    dct = dct[chunk]
        for each in zdict:
            print("{}:".format(each))
            line = ""
            for item in zdict[each]:
                line += "  {:14s}".format(item)
                if 70 < len(line):
                    print(line)
                    line = ""
            if 4 < len(line):
                print(line)


# -----------------------------------------------------------------------------
@dispatch.on('westeast')
def westeast(**kw):
    """
    List the known timezones from west to east
    """
    if kw['d']:
        pdb.set_trace()
    olist = []
    for each in pytz.all_timezones:
        tz = pytz.timezone(each)
        tup = (tz.zone, tz.utcoffset(datetime.now()).total_seconds())
        olist.append(tup)
    for each in sorted(olist, key=lambda a: a[1]):
        print("{:30s} {:>8s}".format(each[0], hhmm(each[1])))
    
# -----------------------------------------------------------------------------
def hhmm(secs):
    hr = int(secs // 3600)
    mn = int((secs % 3600) / 60)
    return "{:02d}:{:02d}".format(hr, mn)

# -----------------------------------------------------------------------------
@dispatch.on('zdetails')
def zdetails(**kw):
    if kw['d']:
        pdb.set_trace()
    z = pytz.timezone(kw['TIMEZONE'])
    print("zone: {}".format(z.zone))
    print("_dst: {}".format(z._dst))
    print("dst: {}".format(z.dst(datetime.now())))
    print("tzname: {}".format(z.tzname(datetime.now())))

    tsecs = z.utcoffset(datetime.now()).total_seconds()
    # hr = int(tsecs // 3600)
    # mn = int((tsecs % 3600) / 60)
    print("utcoffset: {}".format(hhmm(tsecs)))
                      

if __name__ == "__main__":
    dispatch(__doc__)
