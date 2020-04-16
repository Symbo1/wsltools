# -*- coding: utf-8 -*-
#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="wsltools",
      version="0.1",
      description="Web Scan Lazy Tools",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="MIT",
      author="CongRong",
      author_email="tr3jer@gmail.com",
      url="https://github.com/symbo1/wsltools",
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
      packages=find_packages(),
      package_data = {'': ['*.bin']},
      keywords=["security","security-tools","security-scanner","security-automation","security-audit",
                "spider","spider-framework","scanner-web","security-tool","crawling-framework","web-vulnerability-scanners"],
      zip_safe=True,
      classifiers=[
	      'Development Status :: 5 - Production/Stable',
	      'Intended Audience :: Developers',
	      'License :: OSI Approved :: MIT License',
	      'Programming Language :: Python',
	      'Programming Language :: Python :: 2',
	      'Programming Language :: Python :: 2.7',
	      'Programming Language :: Python :: 3',
	      'Programming Language :: Python :: 3.5',
	      'Programming Language :: Python :: 3.6',
	      'Programming Language :: Python :: 3.7',
	      'Programming Language :: Python :: 3.8',
	      'Programming Language :: Python :: Implementation :: CPython',
	      'Programming Language :: Python :: Implementation :: PyPy'
      ],
      project_urls={
	      'Documentation': 'https://wsltools.readthedocs.io',
	      'Source': 'https://github.com/symbo1/wsltools',
      },
)