#! /usr/bin/python
import requests

HTTP_PROXY = "http://10.134.107.108:3128"
proxyDict = {
              "http"  : HTTP_PROXY
            }
URL_FILENAME = "./post.url"

f = open(URL_FILENAME, "r")
f_result = open("%s.result" % URL_FILENAME, "w")

count = 0
client = requests.Session()
while True:
    line = f.readline()
    # No more file
    if not line:
        break

    status = "untest"
    line = line.rstrip('\n')
    if line.startswith("- url: "):
        url = line[7:]
        if url != "not exist":
            try:
                r = client.get(url, timeout = 1, proxies=proxyDict)
                if r.status_code == 200:
                    status = "SUCCESS 200"
                else:
                    status = "FAIL %d" % r.status_code
                    print("url: %s " % status)
            except Exception as e:
                    status = "FAIL %s" % str(e)
                    print("url: %s " % status)

            count += 1
            if count % 500 == 0:
                print("Test %d URLs..." % count)

    elif line.startswith("  status: "):
        continue

    f_result.write("%s\n" % line)
    if status != "untest":
        f_result.write("  status: %s\n" % status)


f.close()
f_result.close()
