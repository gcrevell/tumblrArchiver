import urllib2
import re
import time
import random
import time

count = 30692

def getRequest(url):
    agents = ['Googlebot', 'Slurp', 'Yandex', 'msnbot']
    req = urllib2.Request(url, headers={ 'User-Agent': random.choice(agents) })
    return req

def readRequest(request, delay=1):
    response = None
    
    if delay > 400:
        print("Delay got over 400 seconds. Skipping this image...")
        return None
    
    try:
        response = urllib2.urlopen(request).read()
    except:
        print("HIT AN ERROR!!!")
        time.sleep(delay)
        response = readRequest(request, delay * 2)

    return response


def download_web_image(url):
    global count
    name = count
    full_name = str(name) + url[-4:]
    count = count + 1
    
    print("Image URL is:")
    print(url)
    print("Image will be saved as:")
    print(full_name)
    
    request = getRequest(url)
    img = readRequest(request)
    
    if img is None:
        return
    
    with open (full_name, 'w') as f: f.write(img)

def getHTML(url):
    html = None
    while html is None:
        html = readRequest(getRequest(url))
    return html

for i in range(2085, 2128):

    print("Downloading images for page " + str(i))

    url = "http://wowza7125.tumblr.com/page/" + str(i)

    #req = urllib2.Request('www.example.com', headers={ 'User-Agent': 'Mozilla/5.0' })
    html = getHTML(url)

    body = html[html.find("<body>"):html.find("</body>")]

    #print(body)

    regex = re.compile(r'src=\".*?\"')

    for src in regex.findall(body):
        if "srvcs" in src:
            continue
        if "https://" in src:
            continue
        if "assets" in src:
            continue
        if "instagram" in src:
            continue
        if "vine" in src:
            continue
        if "tinypic" in src:
            continue

        link = src[5:-1]

        if "photoset_iframe" in link:
            response = urllib2.urlopen(link)
            html = response.read()
            body = html[html.find("<body>"):html.find("</body>")]
            
            regex2 = re.compile(r'src=\".*?\"')

            for src2 in regex2.findall(body):
                if "assets" in src2:
                    continue
                if "instagram" in src2:
                    continue
                if "vine" in src2:
                    continue
                if "tinypic" in src2:
                    continue
                    
                link2 = src2[5:-1]
                #print link2
                download_web_image(link2)

        else:
            #print(link)
            download_web_image(link)

    #print(result.group(0))


