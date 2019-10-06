try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Embellished datetime objects',
    'author': 'Tom Barron',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'tom.barron@comcast.net',
    'version': '0.2',
    # 'install_requires': ['git://github.com/tbarron/tbx.git#egg=tbx'],
    'packages': ['dtm'],
    'scripts': [],
    'name': 'dtm'
}

setup(**config)
