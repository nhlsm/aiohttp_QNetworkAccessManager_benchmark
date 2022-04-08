import sys
import json
import logging
import time

import aiohttp
import asyncio
import ssl

async def Httpc_aio(seq, size=4096, cnt=2_000, use_ssl=False):
    if use_ssl:
        uri = "https://localhost:8080/post"
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # logging.info(f'{ssl_context.verify_mode} {ssl.CERT_REQUIRED}')
        # ssl_context.verify_mode = ssl.CERT_REQUIRED
        # ssl_context.verify_mode = ssl.CERT_NONE
        conn = aiohttp.TCPConnector(ssl=ssl_context)
    else:
        uri = "http://localhost:8080/post"
        conn = None

    async with aiohttp.ClientSession(connector=conn) as session:
        data = {
            'seq' : seq,
            'd': 'a' * size
        }
        async with session.post(uri, data=json.dumps(data) ) as resp:
            text = await resp.text()
            rsp_json = json.loads(text)
            if rsp_json['seq'] == cnt - 1:
                logging.info(f'last!!!')

async def main(size=256, cnt=5_000, use_ssl=False):
    t0 = time.time()
    tasks = [ Httpc_aio(seq, size, cnt, use_ssl) for seq in range(cnt) ]
    t0_1 = time.time()
    results = await asyncio.gather(*tasks)
    t1 = time.time()
    logging.info(f'elapsed: {t1-t0:.06f}, {t1-t0_1:.06f} size:{size:,}, cnt:{cnt:,}, use_ssl:{use_ssl}')
    '''
    | t0_1 -  t1 | < 1 ms
    elapsed: 4.995999, 4.995000 size:256, cnt:2,000, use_ssl:True
    '''

if __name__ == '__main__':
    # debug
    LOG_FORMAT = '%(pathname)s:%(lineno)03d | %(asctime)s | %(levelname)s | %(message)s'
    # LOG_LEVEL = logging.DEBUG  # DEBUG(10), INFO(20), (0~50)
    LOG_LEVEL = logging.INFO  # DEBUG(10), INFO(20), (0~50)

    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

    ##################################################
    if sys.platform == 'win32':
        '''
        https://stackoverflow.com/questions/47675410/python-asyncio-aiohttp-valueerror-too-many-file-descriptors-in-select-on-win
        prevent exception:
        too many file descriptors in select()
        '''
        logging.info(f'win32 ProactorEventLoop')
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

    loop = asyncio.get_event_loop()
    # 2022-0408
    # elapsed: 2.448966, size:256, cnt:2,000, use_ssl:False
    # elapsed: 2.481996, size:256, cnt:2,000, use_ssl:False
    # elapsed: 2.400015, size:256, cnt:2,000, use_ssl:False
    # loop.run_until_complete( main(size=256, cnt=2_000, use_ssl=False) )

    # 2022-0408
    # elapsed: 4.344965, size:256, cnt:2,000, use_ssl:True
    # elapsed: 4.245755, size:256, cnt:2,000, use_ssl:True
    # elapsed: 4.329581, size:256, cnt:2,000, use_ssl:True
    loop.run_until_complete( main(size=256, cnt=2_000, use_ssl=True) )

    logging.info(f'end!')





