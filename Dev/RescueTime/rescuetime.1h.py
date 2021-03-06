#!/usr/bin/env python
# <bitbar.title>RescueTime</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Paul Traylor</bitbar.author>
# <bitbar.author.github>kfdm</bitbar.author.github>
# <bitbar.desc>Show your RescueTime productivity pulse in the status bar</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
#
# To install, you will want to generate an API key for rescue time and then store the
# key in ~/Library/RescueTime.com/api.key
# https://www.rescuetime.com/anapi/manage
import datetime
import json
import os
import urllib
import urllib2

API_KEY = os.path.expanduser('~/Library/RescueTime.com/api.key')

MAPPING = {
    2: 'Very Productive',
    1: 'Productive',
    0: 'Neutral',
    -1: 'Distracting',
    -2: 'Very Distracting'
}

ICON = ('iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAA1VBMVEUAAAAAAAAAAAAAAAAg' +
        'ICAcHBwZGRkYGBgYGBgYGBgaGhobGBgYGBgbGBgaGhoaGhoZGRkaGhoaGhoaGhoZGRkaGBga' +
        'GhobGRkbGBgaGBgaGhoaGBgbGRkaGhoaGhoaGRkaGRkaGBgaGRkaGRkaGRkZGRkaGBgaGRka' +
        'GBgaGRkaGRkaGRkaGRkaGRkaGRkaGRkaGBgZGRkaGRkaGRkaGRkaGRkaGRkaGRkaGRkaGBga' +
        'GhoZGRkaGRkaGRkaGRkaGRkaGRkbGhocGhocGhscGxsdGxsdHByE7nCRAAAAQHRSTlMAAwQF' +
        'CAkpKjY/RUtUVmJkZWxtbnF0d3t9f4CIj5+gpaaorq+7v8fP0dXW3t/g4eLl5+jr7fP0+Pn6' +
        '+vv7/P3+KMtxrAAAAMVJREFUGNMFwb1OAmEQhtHnnRlggwSMYkKhtiYWVt7/RdhbYmIE/CmA' +
        'Zfeb8RyBavFaifxtr8JAXMc54uIrBCFZVptv86E1jLLKkcIPn04xZsXtquWicFHLR/khXjyt' +
        'nRYS57tN85tovZUHl0a0oc36sClU/P3k+1Z67hQlUM03w3qGzVCo9zYxnpQLqi+iXUFLDXjz' +
        'CJPmyxzW96OT/rFz+43jETo/Ozk97QGTTbCqzLEZYYoqIe9EF04mAcn31yCy21HwD7isX+jx' +
        'FQgEAAAAAElFTkSuQmCC')

def get(url, params):
    '''Simple function to mimic the signature of requests.get'''
    params = urllib.urlencode(params)
    result = urllib2.urlopen(url + '?' + params).read()
    return json.loads(result)

if not os.path.exists(API_KEY):
    print('X | image=%s' % (ICON))
    print('---')
    print('Missing API Key at ~/Library/RescueTime.com/api.key')
    exit()

with open(API_KEY) as fp:
    key = fp.read().strip()
    date = datetime.date.today().strftime('%Y-%m-%d')
    result = get('https://www.rescuetime.com/anapi/data', params={
        'format': 'json',
        'key': key,
        'resolution_time': 'day',
        'restrict_begin': date,
        'restrict_end': date,
        'restrict_kind': 'productivity',
    })
    pulse = get('https://www.rescuetime.com/anapi/current_productivity_pulse.json', params={
        'key': key,
    })

productivity_seconds = result['rows'][0][1] + result['rows'][1][1]
print('%sm (%s%%) | color=%s image=%s' % (productivity_seconds / 60, pulse['pulse'], pulse['color'], ICON))
print('---')
print('Rescue Time | href=https://www.rescuetime.com/dashboard?src=bitbar')
for rank, seconds, people, productivty in result['rows']:
    print('%s %s Minutes' % (MAPPING[productivty], seconds / 60))
