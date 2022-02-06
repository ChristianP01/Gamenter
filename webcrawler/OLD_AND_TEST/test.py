'''
import requests
import urllib.parse
encodedStr = 'Hunter%27s_Moon_(video_game)'
s = urllib.parse.unquote(encodedStr)
response = requests.get(
    'https://en.wikipedia.org/w/api.php',
    params={
        'action': 'query',
        'format': 'json',
        'titles': s,
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True,
    }).json()
page = next(iter(response['query']['pages'].values()))
print(page['extract'])
'''

import re

pattern_id = "^[0-9]+"
test_string="12351124###coppelungo\n"

result = re.match(pattern_id, test_string)
start = result.start()
end = result.end()
print(start)
print(end)
print(test_string[start:end])
print(test_string[end+3:-1])