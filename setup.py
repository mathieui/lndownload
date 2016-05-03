from setuptools import setup

setup(name='lndownload',
      version='1.0',
      description='A script to download light novels',
      log_description='A script to download light novels',
      licence='WTFPL',
      packages=['lndownload'],
      package_dir={'lndownload': 'lndownload'},
      install_requires=['beautifulsoup4', 'EbookLib', 'requests'],
      entry_points={'console_scripts': ['ln_download = lndownload.main:main']}
)

