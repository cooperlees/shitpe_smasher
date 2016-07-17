#!/usr/bin/env python3

import asyncio
import aiohttp
import click
import concurrent.futures
import sys
import time
 
START_TIME = time.time()

CLICK_CONTEXT_SETTINGS = {'help_option_names': ('-h', '--help')}
SHORT_HELP = 'Hammer the SHIT out of a webserver - --slam_count is per process!!'

async def _send_req(url):
    try: 
        response = await aiohttp.request('GET', url)
        await response.close()
    except Exception:
        return (0,1)
    return (1,1)


def _slammer_proc(atonce, url, slam_count, verbose):
    loop = asyncio.get_event_loop()
    success_reqs = 0
    total_reqs = 0

    batch_count = 0
    slams_done = 0
    togo = slam_count
    while slams_done < slam_count:
        current_batch = atonce if atonce <= togo else togo
        togo -= current_batch

        tasks = [
            asyncio.ensure_future(_send_req(
                '{}{}'.format(url, cunt), 
            )) for cunt in range(current_batch)
        ]
        loop.run_until_complete(asyncio.wait(tasks))

        for task in tasks:
            current_success_reqs, current_total_reqs = task.result()
            success_reqs += current_success_reqs
            total_reqs += current_total_reqs

        batch_count += 1
        slams_done += current_batch
        if verbose:
            print("--> Finished batch {}: {}/{} to {}".format(
                batch_count, slams_done, slam_count, url))

    loop.close()
    return (success_reqs, total_reqs)


@click.command(short_help=SHORT_HELP, context_settings=CLICK_CONTEXT_SETTINGS)
@click.version_option(version=69)
@click.option('-a', '--atonce', help='Number of reqs at once', default=100, type=int)
@click.option('-v', '--verbose', help='Print out status info', is_flag=True)
@click.option('-w', '--workers', help='Number of procs to spawn', default=1, type=int)
@click.argument('url')
@click.argument('slam_count', type=int)
def main(atonce, url, slam_count, verbose, workers):
    success_reqs = 0
    total_reqs = 0

    if verbose:
        print("- Slamming {} {} at once in {} procs -".format(url, atonce, workers))


    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        slammers = {}
        for worker in range(workers):
            slammers[
                executor.submit(
                    _slammer_proc,
                    atonce,
                    url,
                    slam_count,
                    verbose
                )
            ] = worker

        for future in concurrent.futures.as_completed(slammers):
            current_success, current_total = future.result()
            success_reqs += current_success
            total_reqs += current_total


    print("--> Finished slamming {} {} times ({} total attempts) in {} seconds".format(
        url, success_reqs, total_reqs, (time.time() - START_TIME)))


if __name__ == '__main__':
    sys.exit(main())
