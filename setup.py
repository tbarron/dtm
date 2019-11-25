from dtm import version
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
    packages=['dtm'],
    install_requires=['pytz',
                      'tzlocal',
                      ],
    # dependency_links=['http://github.com/tbarron/tbx/tarball/master#egg=tbx-1.1.6'],
    dependency_links=['git+git://github.com/tbarron/tbx.git#egg=tbx>=1.1.6'],
    scripts=[],
    name='dtm'
)
