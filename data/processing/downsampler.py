def downsample(data, rule='1S', agg_func='mean'):
    return data.resample(rule).agg(agg_func)
