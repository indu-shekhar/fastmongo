import asyncio 

async def run_db(fn):
    return await asyncio.to_thread(fn)  # take a db sync function as input and then runs that in the separate thread.
