#!/usr/bin/env python3
import os, sys

if __name__ == '__main__':
    # Parse args, parse list
    if len(sys.argv) <= 1:
        sys.exit('No filename given.  Answer: unknown')

    if len(sys.argv) > 2:
        sys.exit('Too many arguments.')

    import pandas as pd 
    
    df = pd.read_csv(
        sys.argv[1],
        sep=r'\]\s',
        names=['datetime', 'message'],
        engine='python'
    )

    df.datetime = pd.to_datetime(df.datetime.str.strip('['), format='%Y-%m-%d %H:%M:%S', errors='ignore')
    print(type(df.datetime))

    print(df)

    # df.time = pd.to_date

    # lines = list(map(lambda x: str(x).strip(','), lines))

    # # Parse data
    # import re
    # p = re.compile(r'\[\d+-(\d+-\d+)\s(\d+):(\d+)\]\s(.*)')

    # db = set()
    # # Parse each claim
    # for line in lines:
    #     x = p.search(line)
    #     db.add(x.groups())

