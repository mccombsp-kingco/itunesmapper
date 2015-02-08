import datetime, bisect, math

time_point = datetime.datetime(2015, 1, 9, 20, 42, 15)

print "time_point: " + str(time_point)

loc_tups = [(47.7644685, -122.3128514, datetime.datetime(2015, 1, 2, 20, 41, 15)),
            (47.7644339, -122.3128811, datetime.datetime(2015, 1, 14, 20, 36, 29)),
            (47.7644686, -122.3128513, datetime.datetime(2015, 1, 29, 20, 31, 33)),
            (47.7644697, -122.3128505, datetime.datetime(2015, 1, 29, 20, 45, 57)),
            (47.7644689, -122.3128500, datetime.datetime(2015, 1, 29, 20, 45, 42))]

loc_tups = sorted(loc_tups, key=lambda loc: loc[2])

lats, lons, loc_dates = zip(*loc_tups)

locs = zip(lats, lons)

for date in loc_tups:
    print date[2]

order_pos = bisect.bisect(loc_dates, time_point)
before = loc_dates[order_pos -1]
after = loc_dates[order_pos]
locs_time_interval = after - before
before_time_point_interval = time_point - before
before_ratio = ((float(before_time_point_interval.days)*86400+
                      before_time_point_interval.seconds)/
                     (locs_time_interval.days*86400+locs_time_interval.seconds))
lat_dist = (lats[order_pos]-lats[order_pos-1])
lon_dist = (lons[order_pos]-lons[order_pos-1])
interp_lat = lats[order_pos-1] + (lat_dist*before_ratio)
interp_lon = lons[order_pos-1] + (lon_dist*before_ratio)
interp_loc = (interp_lat,interp_lon)
 
# cart_slope = (float(lats[order_pos]-lats[order_pos-1])/
#                    (lons[order_pos]-lons[order_pos-1]))
# cart_konstant = ((cartesian_dist * before_ratio) / math.sqrt(1+(cart_slope**2)))*-1
# interp_loc = ((lats[order_pos-1]+cart_konstant),
#              (lons[order_pos-1]+(cart_slope*cart_konstant)))
# check_slope = (float(interp_loc[0]-lats[order_pos-1])/
#                     (interp_loc[1]-lons[order_pos-1]))

print locs[order_pos - 1], before
print locs[order_pos], after
print "Time between two locations:", locs_time_interval
print "Time between before location and time point:", before_time_point_interval
print "Ratio of before - time point to before - after:", before_ratio
print "Latitude distance in 'degrees':", lat_dist
print "Longitude distance in 'degrees':", lon_dist
print "New location is: ", interp_loc