# aiohttp_QNetworkAccessManager_benchmark
aiohttp vs QNetworkAccessManager benchmark
- check only POST performance.

## target
- QNetworkAccessManager (pyqt5)
- aiohttp (https://pypi.org/project/aiohttp/)

# result 
- QNetworkAccessManager > aiohttp
- QNetworkAccessManager is best.

```             
(http)                elapsed(sec) msg-size(bytes)  cnt  
QNetworkAccessManager     1.048039            256   2000  * BEST
aiohttp                   2.448966            256   2000  

(https)               elapsed(sec) msg-size(bytes)  cnt  
QNetworkAccessManager     1.287815            256   2000  * BEST
aiohttp                   4.245755            256   2000
```
