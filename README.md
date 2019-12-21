<p align="center"><img src="https://habrastorage.org/webt/bi/od/mp/biodmpylxpnkxhjtewsjro_-8ps.jpeg" height="180"></p>
<p align="center"><a href="https://www.apache.org/licenses/LICENSE-2.0"><img src="https://img.shields.io/pypi/l/requests.svg" alt="Apache 2.0 License" height="18"></a></p>

# Credits

This library is based on <a href="https://github.com/gadzhi/pyiiko">https://github.com/gadzhi/pyiiko</a>. My goal is to update and improve it without backward compatibility to the original library.

# About

Pyiiko is the easy-to-use library for iiko ERP. This library provides a pure Python interface for the iiko Server API, iikoBiz and FrontWebApi. 

iiko company development of innovative systems for HoReCa industry.

## Example:

```python
    from Pyiiko2 import IikoServer

    i = IikoServer(ip = 'your ip', port = 'port', login = 'login', password = 'password in MD5 HASH')
    i.token()
    
```
