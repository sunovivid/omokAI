import asyncio

def min_value(searching, loop, end_time):
    if loop.time() > end_time:
        return 9999#"eval func"
    m = 0
    for i in range(4):
        m = max(0,max_value(searching + i, loop, end_time))
    return m

def max_value(searching, loop, end_time):
    if loop.time() > end_time:
        return 8888#"eval func"
    m = 0
    for i in range(4):
        m = max(0,min_value(searching + i, loop, end_time))
    return m

async def minimax_search(loop, end_time):
    searching = 1
    if loop.time() > end_time:
        return "eval func"
    for i in range(4):
        min_value(i, loop, end_time)
    return

async def absearch(timeout):
    print('absearch start')
    loop = asyncio.get_running_loop()
    end_time = loop.time() + timeout
    await minimax_search(loop, end_time)

timeout = 0.2
asyncio.run(absearch(timeout))