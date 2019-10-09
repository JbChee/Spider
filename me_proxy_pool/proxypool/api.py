from flask import Flask, g

from .db import RedisClient
import json

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to USE github/JbChee/Spider Proxy Pool API</h2>'


@app.route('/get')
def get_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.count())

@app.route('/all_use')
def get_all_use():
    """
    Get the count of proxies
    :return: 代理池分数大于98分的总量
    """
    conn = get_conn()
    result = conn.all_use()
    counts = len(result)
    proxies = {
        'counts':counts,
        'proxies':result,
    }
    datas = json.dumps(proxies)
    return datas

@app.route('/all')
def get_all():
    """
    Get the count of proxies
    :return: 代理池总量
    """
    conn = get_conn()
    result = conn.all()
    counts = conn.count()
    proxies = {
        'counts':counts,
        'proxies':result,
    }
    datas = json.dumps(proxies)
    return datas


if __name__ == '__main__':
    app.run()
