import json
import logging
import time

from PyQt5.QtCore import *
from PyQt5.QtNetwork import *

class Httpc_qt(QObject):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.m_nam = QNetworkAccessManager()
        self.m_nam.finished.connect(self.on_finishied)
        self.m_nam.encrypted.connect(self.on_encrypted)

        self.m_t0 = 0
        self.m_size = 0
        self.m_cnt = 0

    def start(self, size, cnt, use_ssl):
        self.m_t0 = 0
        self.m_size = size
        self.m_cnt = cnt
        self.m_use_ssl = use_ssl

        QTimer.singleShot(100, self._start)

    def _start(self):
        self.m_t0 = time.time()
        for i in range(self.m_cnt):
            self._request(i)
        logging.info(f'bulk req')

    def _request(self, seq):
        if self.m_use_ssl:
            req = QNetworkRequest()
            # req.setSslConfiguration(QSslConfiguration.defaultConfiguration())
            ssl_conf = QSslConfiguration.defaultConfiguration()
            # ssl_conf.setProtocol(QSsl.TlsV1_2)
            ssl_conf.setPeerVerifyMode(QSslSocket.VerifyNone)
            ssl_conf.setProtocol(QSsl.TlsV1SslV3)
            req.setSslConfiguration(ssl_conf)
            req.setUrl(QUrl('https://127.0.0.1:8080/post'))
        else:
            req = QNetworkRequest(QUrl('http://127.0.0.1:8080/post'))
        req.setHeader(QNetworkRequest.ContentTypeHeader, 'application/json')
        data = {
            'seq' : seq,
            'd': 'a'*self.m_size
        }
        self.m_nam.post(req, json.dumps(data).encode('utf-8') )

    def on_encrypted(self, reply):
        # logging.info(f'on_encrypted')
        pass

    def on_finishied(self, reply):
        content_raw = reply.readAll()
        content_json = json.loads(content_raw.data())

        if content_json['seq'] == self.m_cnt - 1:
            t1 = time.time()
            logging.info(f'elapsed: {t1-self.m_t0:.06f}, size:{self.m_size:,}, cnt:{self.m_cnt:,}, use_ssl:{self.m_use_ssl}')

if __name__ == '__main__':
    # debug
    LOG_FORMAT = '%(pathname)s:%(lineno)03d | %(asctime)s | %(levelname)s | %(message)s'
    # LOG_LEVEL = logging.DEBUG  # DEBUG(10), INFO(20), (0~50)
    LOG_LEVEL = logging.INFO  # DEBUG(10), INFO(20), (0~50)

    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

    ##################################################
    app = QCoreApplication([])

    httpc = Httpc_qt()

    # 2022-0408
    # elapsed: 1.048039, size:256, cnt:2,000, use_ssl:False
    # elapsed: 1.008009, size:256, cnt:2,000, use_ssl:False
    # elapsed: 1.086958, size:256, cnt:2,000, use_ssl:False
    # httpc.start(size=256, cnt=2_000, use_ssl=False)

    # 2022-0408
    # elapsed: 1.340373, size:256, cnt:2,000, use_ssl:True
    # elapsed: 1.236400, size:256, cnt:2,000, use_ssl:True
    # elapsed: 1.287815, size:256, cnt:2,000, use_ssl:True
    httpc.start(size=256, cnt=2_000, use_ssl=True)

    app.exec_()

