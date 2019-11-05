"""
Usage:
    dtm calendar [DTSPEC]
    dtm ltu [-d] [LOC_DTSPEC] [TIMEZONE]
    dtm rdt [-d] [EPOCH]
    dtm rtd [-d] [SECONDS]
    dtm splat [-d]
    dtm utl [-d] [UTC_DTSPEC] [TIMEZONE]
    dtm westeast [-d]
    dtm zdetails [-d] TIMEZONE
    dtm zones [-d] [-r] [SEARCH]

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
from dtm import dt, td
import pdb
import pytz
import random
import time


# -----------------------------------------------------------------------------
@dispatch.on('calendar')
def calendar(**kw):
    """
    Generate calendars

        dtm calendar                 # calendar for current month
        dtm calendar DTSPEC          # calendar for month containing DTSPEC
    """
    if kw['d']:
        pdb.set_trace()                                      # pragma: no cover

    if kw['DTSPEC']:
        when = dt(kw['DTSPEC'])
    else:
        when = dt()

    mday = int(when("%d"))                    # month day
    start = when.previous_day(mday-1)         # beginning of month
    end = when.next_day(32 - mday)            # next month
    while end("%b") != start("%b"):           # back to end of target month
        end = end.previous_day()
    mlen = int(end("%d"))                     # number of last day
    op = start("%B %Y")                       # month name and year
    lsp = (22 - len(op)) // 2                   # count leading spaces
    wsp = lsp * " "                           # generate leading space
    op = wsp + op + wsp + "\n"                # insert leading & trailing space
    op += " mo tu we th fr sa su\n"           # weekday names
    lslots = weekday_ordinal(start.weekday()) - 1   # leading slots
    slot = 0
    for n in range(lslots):                   # generate leading slots
        op += "   "
        slot += 1
    for day in range(1, mlen + 1):            # add each day to the month
        op += " {:2d}".format(day)
        slot += 1
        if slot % 7 == 0:                     # newline on every 7th slot
            op += "\n"
    while slot % 7 != 0:
        op += "   "
        slot += 1
    print(op)


# -----------------------------------------------------------------------------
def weekday_ordinal(wkday):
    """
    Return the ordinal value of *wkday* where mo == 1, tu == 2, ... su == 7
    """
    done = False
    while not done:
        try:
            rval = weekday_ordinal.spread.index(wkday[0:2])
            done = True
        except AttributeError:
            weekday_ordinal.spread = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
    return rval + 1


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
        report_tzset('roots', zdict)
        for each in zdict:
            report_tzset(each, zdict[each])
            for item in zdict[each]:
                report_tzset("{}/{}".format(each, item), zdict[each][item])


# -----------------------------------------------------------------------------
def report_tzset(label, data):
    """
    Report *label* and *data*
    """
    if data:
        print("{}:".format(label))
        line = ""
        for item in data:
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
@dispatch.on('rdt')
def dtm_rdt(**kw):
    """
    Generate a random date
    """
    if kw['d']:                                              # pragma: no cover
        pdb.set_trace()
    x = kw['EPOCH'] or random.randint(0, int(time.time() * 1.25))
    thunk = dt(epoch=x)
    print("{} (epoch = {})".format(thunk(), thunk._utc))


# -----------------------------------------------------------------------------
@dispatch.on('rtd')
def dtm_rtd(**kw):
    """
    Generate a random td
    """
    if kw['d']:                                              # pragma: no cover
        pdb.set_trace()
    ssec = kw['SECONDS'] or random.randint(0, 5*24*3600)
    sec = int(ssec)
    obj = td(sec)
    print("{} (seconds = {})".format(dhhmmss(obj._duration), obj._duration))


# -----------------------------------------------------------------------------
def hhmm(secs):
    """
    Format a number of seconds in hours and minutes
    """
    hr = int(secs // 3600)
    mn = int((secs % 3600) / 60)
    return "{:02d}:{:02d}".format(hr, mn)


# -----------------------------------------------------------------------------
def dhhmmss(secs):
    """
    Format a number of seconds in hours and minutes
    """
    r = secs
    v = []
    for div in [24*3600, 3600, 60]:
        v.append(r // div)
        r = r % div
    v.append(r)
    return "{}d{:02d}:{:02d}:{:02d}".format(*tuple(v))


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    dispatch(__doc__)                                        # pragma: no cover


"""
==TAGGABLE==
"""
