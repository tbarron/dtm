import version
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    description='Embellished datetime objects',
    author='Tom Barron',
    url='URL to get it at.',
    download_url='Where to download it.',
    author_email='tom.barron@comcast.net',
    version=version._v,
    # 'install_requires': ['git://github.com/tbarron/tbx.git#egg=tbx'],
    packages=['dtm'],
    py_modules=['version'],
    scripts=[],
    name='dtm'
)
