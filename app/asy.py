#!/usr/bin/env python3

import asyncio


async def mbuto():
    await asyncio.sleep(2)
    print("ciao")


async def primo():
    print("faccio prima?")


async def main():
    await asyncio.gather(mbuto(), primo())

if __name__ == '__main__':
    asyncio.run(main())
    print("finito")
