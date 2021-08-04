import os
import imp

from setuptools import setup, find_packages


version = imp.load_source("requests_api.version", os.path.join("requests_api", "version.py")).version


setup(
    name="requests-api",
    version=version,
    packages=find_packages(include=["requests_api", "requests_api.*"]),
    package_dir={"requests_api": "requests_api"},
    install_requires=[
        "urllib3",
        "nested-lookup",
        "requests>=2.25",
        "requests-oauthlib>=1.3",
        "requests-ntlm3",
        "requests-kerberos>=0.12",
    ],
    author="Deric Degagne",
    author_email="deric.degagne@gmail.com",
    description="HTTP requests library.",
    url="https://github.com/degagne/requests-api",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.6"
)