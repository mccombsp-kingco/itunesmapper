import datetime, bisect

time_point = datetime.datetime(2015, 1, 29, 20, 42, 15)

print "time_point: " + str(time_point)

loc_tups = [(477644685, -1223128514, datetime.datetime(2015, 1, 29, 20, 41, 15)),
             (477644686, -1223128490, datetime.datetime(2015, 1, 29, 20, 36, 29)),
             (477644686, -1223128513, datetime.datetime(2015, 1, 29, 20, 31, 33)),
             (477644697, -1223128505, datetime.datetime(2015, 1, 29, 20, 45, 57)),
             (477644689, -1223128500, datetime.datetime(2015, 1, 29, 20, 45, 42))]

loc_tups = sorted(loc_tups, key=lambda loc: loc[2])

lats, lons, loc_dates = zip(*loc_tups)

locs = zip(lats, lons)

for date in loc_tups:
    print date[2]

order_pos = bisect.bisect(loc_dates, time_point)
before = loc_dates[order_pos -1]
after = loc_dates[order_pos]

print locs[order_pos - 1], before
print locs[order_pos], after

print "Time between two locations: ", after - before
