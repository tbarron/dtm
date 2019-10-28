"""
Usage:
    dtm splat [-d]
    dtm utl [-d] [UTC_DTSPEC] [TIMEZONE]
    dtm ltu [-d] [LOC_DTSPEC] [TIMEZONE]
    dtm zones [-d] [-r] [SEARCH]
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
from dtm import dt
import pdb
import pytz
import time


# -----------------------------------------------------------------------------
@dispatch.on('ltu')
def utc_fr_local_tz(**kw):
    """
    Compute utc from local time and timezone
    """
    if kw['d']:
        pdb.set_trace()                                      # pragma: no cover
    dtspec = kw['LOC_DTSPEC'] or 'now'
    if dtspec == 'now':
        dtspec = dt().strftime("%F %T")

    tzname = kw['TIMEZONE'] or 'local'

    utc = pytz.timezone('utc')
    nl = dt(dtspec, tz=tzname)
    print(nl("%F %T %Z", tz=utc))


# -----------------------------------------------------------------------------
@dispatch.on('utl')
def local_fr_utc_tz(**kw):
    """
    Compute local time from utc and timezone
    """
    if kw['d']:
        pdb.set_trace()                                      # pragma: no cover
    (dtspec, tz) = (kw['UTC_DTSPEC'], kw['TIMEZONE'])
    dtspec = dtspec or 'now'
    if dtspec == 'now':
        dtspec = dt(tz='utc').strftime("%F %T")

    if tz == '':
        tz = 'local'

    when = dt(dtspec, tz='utc')
    print(when("%F %T %Z", tz=tz))


# -----------------------------------------------------------------------------
@dispatch.on('splat')
def splat(**kw):
    """
    Will the real UTC please stand up?
    """
    if kw['d']:
        pdb.set_trace()                                      # pragma: no cover
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
    """
    List all timezones that match kw['SEARCH'] (everything if kw['SEARCH'] is
    empty)
    """
    if kw['d']:
        pdb.set_trace()                                      # pragma: no cover

    zlist = pytz.all_timezones
    if kw['SEARCH']:
        for each in zlist:
            if kw['SEARCH'] in each:
                print(each)
    elif kw['r']:
        for each in zlist:
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
        pdb.set_trace()                                      # pragma: no cover
    olist = []
    for each in pytz.all_timezones:
        tz = pytz.timezone(each)
        tup = (tz.zone, tz.utcoffset(datetime.now()).total_seconds())
        olist.append(tup)
    for each in sorted(olist, key=lambda a: a[1]):
        print("{:35s} {:>8s}".format(each[0], hhmm(each[1])))


# -----------------------------------------------------------------------------
@dispatch.on('zdetails')
def zdetails(**kw):
    """
    Report the details of a specified timezone
    """
    if kw['d']:
        pdb.set_trace()                                      # pragma: no cover
    z = pytz.timezone(kw['TIMEZONE'])
    print("zone: {}".format(z.zone))
    print("_dst: {}".format(z._dst))
    print("dst: {}".format(z.dst(datetime.now())))
    print("tzname: {}".format(z.tzname(datetime.now())))

    tsecs = z.utcoffset(datetime.now()).total_seconds()
    print("utcoffset: {}".format(hhmm(tsecs)))


# -----------------------------------------------------------------------------
def hhmm(secs):
    """
    Format a number of seconds in hours and minutes
    """
    hr = int(secs // 3600)
    mn = int((secs % 3600) / 60)
    return "{:02d}:{:02d}".format(hr, mn)


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    dispatch(__doc__)                                        # pragma: no cover
