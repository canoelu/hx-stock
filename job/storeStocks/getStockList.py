#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
from enum import Enum

import os.path
import sys
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
# 获取 MongoDB 连接
from  lib.mongoDB import STOCK_DB

 
def get_stock_list():
    try:
        collection = STOCK_DB["stock_base"]
        searchData=collection.find({}, {'_id': False}).sort({"code":-1})
        result = list(searchData)
        return result
    except Exception as e:
        print(f"Error fetching stock list: {e}")
        return []

                
if __name__ == '__main__':
    get_stock_list()
