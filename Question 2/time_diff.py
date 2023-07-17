def time_diff(dist_above_20):
    time_30_mins = []

    for i in dist_above_20:
        x = (i[0][4]-i[1][4]).total_seconds()/60
        if x <= 30:
            time_30_mins.append(i[0][0])
            time_30_mins.append(i[1][0])
    return time_30_mins
