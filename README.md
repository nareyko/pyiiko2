<p align="center"><img src="https://habrastorage.org/webt/bi/od/mp/biodmpylxpnkxhjtewsjro_-8ps.jpeg" height="180"></p>
<p align="center">
<a href="https://www.apache.org/licenses/LICENSE-2.0"><img src="https://img.shields.io/pypi/l/requests.svg" alt="PyPI version" height="18"></a>
<a class="badge-align" href="https://www.codacy.com/app/gadzhi/pyiiko?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=nareyko/pyiiko2&amp;utm_campaign=Badge_Grade"><img src="https://api.codacy.com/project/badge/Grade/111e9dc6beb9422ca85f4810f01fb33c"/></a>

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
