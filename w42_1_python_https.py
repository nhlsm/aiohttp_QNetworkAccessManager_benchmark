import sys
import logging
import json

import asyncio
import ssl
from aiohttp import web

async def hello(request):
    logging.info(f'{request}')
    return web.Response(text="Hello, world")

async def post(request):
    # logging.info(f'{request}')
    # logging.info(f'{type(request)}')
    # logging.info(f'{dir(request)}')
    body = await request.text()
    # logging.info(f'{body}')
    return web.json_response(body=body)

if __name__ == '__main__':
    # debug
    LOG_FORMAT = '%(pathname)s:%(lineno)03d | %(asctime)s | %(levelname)s | %(message)s'
    # LOG_LEVEL = logging.DEBUG  # DEBUG(10), INFO(20), (0~50)
    LOG_LEVEL = logging.INFO  # DEBUG(10), INFO(20), (0~50)

    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

    ##################################################
    app = web.Application()
    app.add_routes([
        web.get('/', hello),
        web.post('/post', post)
    ])
    if sys.platform == 'win32':
        '''
        https://stackoverflow.com/questions/47675410/python-asyncio-aiohttp-valueerror-too-many-file-descriptors-in-select-on-win
        prevent exception:
        too many file descriptors in select()
        '''
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

    if False:
        # http
        ssl_context = None
    else:
        # https
        # ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem', password='****')

    web.run_app(app, host="localhost", port=8080, backlog=5_000, access_log=None, ssl_context=ssl_context)
