<p align="center"><img src="https://habrastorage.org/webt/bi/od/mp/biodmpylxpnkxhjtewsjro_-8ps.jpeg" height="180"></p>
<p align="center"><a href="https://www.apache.org/licenses/LICENSE-2.0"><img src="https://img.shields.io/pypi/l/requests.svg" alt="Apache 2.0 License" height="18"></a><a href="https://pyup.io/repos/github/nareyko/pyiiko2/"><img src="https://pyup.io/repos/github/nareyko/pyiiko2/shield.svg" alt="Updates" height="18"/></a><a href="https://app.codeship.com/projects/379033"><img src="https://app.codeship.com/projects/cdd9a8d0-0671-0138-5b33-1a3a19f3ca85/status?branch=master" alt='Codeship Status for nareyko/pyiiko2' height="18"></a><a href="https://www.codacy.com/manual/nareyko/pyiiko2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=nareyko/pyiiko2&amp;utm_campaign=Badge_Grade" alt="www.codacy.com"><img src="https://api.codacy.com/project/badge/Grade/6bc86d309ce5459da06469b8e39ee996" alt="Codacy" height="18"></a><a href="https://lgtm.com/projects/g/nareyko/pyiiko2/alerts/"><img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/nareyko/pyiiko2.svg?logo=lgtm&logoWidth=18" height="18"/></a><a href="https://lgtm.com/projects/g/nareyko/pyiiko2/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/nareyko/pyiiko2.svg?logo=lgtm&logoWidth=18" height="18"/></a></p>

## Credits

This library is based on <a href="https://github.com/gadzhi/pyiiko">https://github.com/gadzhi/pyiiko</a>. My goal is to have lightweight library without backward compatibility to the original library.

## About

Pyiiko is the easy-to-use library for iiko ERP. This library provides a pure Python interface for the iiko Server API, iikoBiz and FrontWebApi. 

iiko company development of innovative systems for HoReCa industry.

## Example

```python
    from Pyiiko2.server import IikoServer

    iiko = IikoServer(ip = 'your ip', port = 'port', login = 'login', passhash = 'SHA1(password)')
    iiko.login()
    print(iiko.token)
    iiko.logout()
    
```
