# proxyconnect
Tool for tunneling SSH through HTTP proxies by Python

## Usage

```
$ http_proxy=http://username:password@proxyhost:proxyport ssh -oProxyCommand='proxyconnect.py %h %p' targethost
```
