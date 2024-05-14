#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from pytdx.reader import TdxDailyBarReader, TdxFileNotFoundException
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
api = TdxHq_API()

# Ensure that the TDX file path is correctly formatted for Windows
tdx_file_path = r"D:\software\vipdoc\sz\lday\sz000612.day"


def getKline():
    if api.connect('119.147.212.81', 7709):
        data=api.get_history_minute_time_data(1, '600690', 20240510)


        # data = api.to_df(data) # 返回DataFrame
        print('---',data)
if __name__ == '__main__':
    getKline()
    reader = TdxDailyBarReader()
    
    try:
        # Attempt to read the TDX file
        df = reader.get_df(tdx_file_path)
        # If successful, you can continue processing the DataFrame
        # print(df)  # Example: print the first few rows of the DataFrame
    except TdxFileNotFoundException:
        # Handle the case where the file is not found
        print(f"Error: TDX file not found at path {tdx_file_path}")
