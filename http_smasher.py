#!/usr/bin/env python3

import asyncio
import aiohttp
import click
import sys
import time
 
REQS_SENT = 0
START_TIME = time.time()
TOTAL_REQS = 0

CLICK_CONTEXT_SETTINGS = {'help_option_names': ('-h', '--help')}
SHORT_HELP = 'Hammer the SHIT out of a webserver'

async def send_req(url):
    global REQS_SENT, TOTAL_REQS
    try: 
        response = await aiohttp.request('GET', url)
        response.close()
    except Exception:
        TOTAL_REQS += 1
        return
    REQS_SENT += 1
    TOTAL_REQS += 1


@click.command(short_help=SHORT_HELP, context_settings=CLICK_CONTEXT_SETTINGS)
@click.version_option(version=69)
@click.option('-a', '--atonce', help='Number of reqs at once', default=100, type=int)
@click.option('-v', '--verbose', help='Print out status info', is_flag=True)
@click.argument('url')
@click.argument('slam_count', type=int)
def main(atonce, url, slam_count, verbose): 
    loop = asyncio.get_event_loop()

    if verbose:
        print("- Slamming {} {} @ once -".format(url, atonce))

    batch_count = 0
    slams_done = 0
    togo = slam_count
    while slams_done < slam_count:
        current_batch = atonce if atonce <= togo else togo
        togo -= current_batch

        tasks = [send_req('{}{}'.format(url, cunt)) for cunt in range(current_batch)]
        loop.run_until_complete(asyncio.wait(tasks))

        batch_count += 1
        slams_done += current_batch
        if verbose:
            print("--> Finished batch {}: {}/{} to {}".format(
                batch_count, slams_done, slam_count, url))

    loop.close()
    print("--> Finished slamming {} {} times ({} total attempts in {} seconds)".format(
        url, REQS_SENT, TOTAL_REQS, (time.time() - START_TIME)))


if __name__ == '__main__':
    sys.exit(main())
