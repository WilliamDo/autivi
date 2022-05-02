#
# Use the kodi-tvvn plugin repository to understand this logic to extract m3u8 stream urls
#
import re, urllib

from http.cookiejar import CookieJar

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# url = 'http://au.tvnet.gov.vn/kenh-truyen-hinh/'+data['channels'][chn]['src']['page_id']
url = 'http://au.tvnet.gov.vn/kenh-truyen-hinh/1011/vtv1'
# url = 'http://au.tvnet.gov.vn/kenh-truyen-hinh/1018/vtc16'

url = 'http://vn.tvnet.gov.vn/kenh-truyen-hinh/1012/htv9'
# url = 'http://vn.tvnet.gov.vn/kenh-truyen-hinh/1009/vtv4'

stringA = opener.open(url).read().decode('utf-8')
stringB = 'data-file="'
stringC = '"'
url = re.search(stringB+"(.*?)"+re.escape(stringC),stringA).group(1)

stringA = opener.open(url).read().decode('utf-8')
stringB = '"url": "'
stringC = '"'
full_url_BC = re.search(stringB+"(.*?)"+re.escape(stringC),stringA).group(1)
full_url = full_url_BC

print(full_url)