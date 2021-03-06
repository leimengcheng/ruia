#!/usr/bin/env python
"""
 Created by howie.hu at 2019/1/28.
"""
import asyncio

from lxml import etree
from aiohttp.cookiejar import SimpleCookie

from ruia import Request


async def hello(response):
    return 'hello ruia'


sem = asyncio.Semaphore(3)
params = {
    "name": "ruia"
}
request = Request('http://www.httpbin.org/get',
                  method='GET',
                  metadata={'hello': 'ruia'},
                  params=params,
                  callback=hello)
_, response = asyncio.get_event_loop().run_until_complete(request.fetch_callback(sem))


def test_response():
    url = response.url
    method = response.method
    encoding = response.encoding
    html = response.html
    metadata = response.metadata
    cookies = response.cookies
    history = response.history
    headers = response.headers
    status = response.status
    html_etree = response.html_etree

    text = asyncio.get_event_loop().run_until_complete(response.text())
    json = asyncio.get_event_loop().run_until_complete(response.json())
    read = asyncio.get_event_loop().run_until_complete(response.read())

    assert url == 'http://www.httpbin.org/get'
    assert method == 'GET'
    assert encoding == 'utf-8'
    assert metadata == {'hello': 'ruia'}
    assert isinstance(html, str)
    assert isinstance(cookies, SimpleCookie)
    assert history == ()
    assert headers['Content-Type'] == 'application/json'
    assert status == 200
    assert response.ok == True
    assert isinstance(html_etree, etree._Element)
    assert isinstance(text, str)
    assert isinstance(json, dict)
    assert isinstance(read, bytes)

    assert str(response) == '<Response url[GET]: http://www.httpbin.org/get status:200>'


def test_callback():
    assert response.callback_result == 'hello ruia'
    response.callback_result = 'ruia'
    assert response.callback_result == 'ruia'


def test_index():
    assert response.index is None
    response.index = 'ruia'
    assert response.index == 'ruia'
