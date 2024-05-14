#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from routers import kLine,getStockList,getTech
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

app.include_router(getStockList.router,prefix="/stock")
app.include_router(getTech.router,prefix="/stock")
# app.include_router(getTechCxd.router,prefix="/stock")
# app.include_router(getTechCxg.router,prefix="/stock")
# app.include_router(getTechCxfl.router,prefix="/stock")
# app.include_router(getTechCxsl.router,prefix="/stock")
# app.include_router(getTechXzjp.router,prefix="/stock")
# app.include_router(getTechLxxd.router,prefix="/stock")
# app.include_router(getTechLxsz.router,prefix="/stock")
app.include_router(kLine.router,prefix="/stock")

app.add_middleware(GZipMiddleware, minimum_size=1000)  # 可选参数 minimum_size 指定最小压缩尺寸，默认为 500 字节
