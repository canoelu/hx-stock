#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from routers import k_line
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

app.include_router(k_line.router)

app.add_middleware(GZipMiddleware, minimum_size=1000)  # 可选参数 minimum_size 指定最小压缩尺寸，默认为 500 字节
