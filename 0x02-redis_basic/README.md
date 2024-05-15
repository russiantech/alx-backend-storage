# Redis Cache

This project demonstrates how to use Redis as a cache in Python.

## Requirements
- Python 3.7
- Redis

## Installation
To install Redis on Ubuntu 18.04:

```sh
$ sudo apt-get -y install redis-server
$ pip3 install redis
$ sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
