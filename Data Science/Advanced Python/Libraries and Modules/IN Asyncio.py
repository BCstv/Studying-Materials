import asyncio

"""
asyncio is a library to write concurrent code using the async/await syntax.
"""

# ----------------------------------------------------------------------------------------------------------------------
#                                              LOW-LEVEL APIs
# ----------------------------------------------------------------------------------------------------------------------
#                                           'low-level API index'

# ----------------------------------------------------------------------------------------------------------------------

# Obtaining the Event Loop


# get_running_loop()
async def main():
    await asyncio.sleep(0.2)
    print(asyncio.get_running_loop())
    # Return the running event loop in the current OS thread.
    # ^ This function can only be called from a coroutine or a callback.

    print(asyncio.get_event_loop())
    # Get the current event loop.
    # When called from a coroutine or a callback (e.g. scheduled with call_soon or similar API), this function will
    # always return the running event loop.

    print('Hello')

asyncio.run(main())

loop = asyncio.new_event_loop()  # Create and return a new event loop object

asyncio.set_event_loop(loop)

loop.run_until_complete(main())
loop.close()




# ----------------------------------------------------------------------------------------------------------------------
#                                              HIGH-LEVEL APIs
# ----------------------------------------------------------------------------------------------------------------------



















# ----------------------------------------------------------------------------------------------------------------------

# Runners

# asyncio.run(coro, *, debug=None, loop_factory=None) - Execute async function within asyncio event loop
'''
Execute the coroutine coro and return the result

This function runs the passed coroutine, taking care of managing the asyncio event loop, finalizing asynchronous 
generators, and closing the executor

If debug is True, the event loop will be run in debug mode. False disables debug mode explicitly. None is used to 
respect the global Debug Mode settings.
    * Debug Mode
        By default asyncio runs in production mode. In order to ease the development asyncio has a debug mode.

If loop_factory is not None, it is used to create a new event loop; otherwise asyncio.new_event_loop() is used. The loop
is closed at the end. THis function should be used as a main entry point for asyncio programs, and should ideally only 
be called once. It is recommended to use loop_factory to configure the event loop instead of policies
'''
"""async def main():
    await asyncio.sleep(0.2)
    print('hello, run')

asyncio.run(main())

# asyncio.Runner(*, debug=None, loop_factory=None) - A context manager that simplifies multiple async function calls in the same context.

async def main():
    await asyncio.sleep(1)
    print('hello, Runner')

with asyncio.Runner() as runner:
    # run(coro, *, context=None)
    # Run a coroutine coro in the embedded loop. Return the coroutine’s result or raise its exception.
    runner.run(main())

    print(runner.get_loop())
    # Return the event loop associated with the runner instance.

    runner.close()
    # Close the runner."""

"""
NOTE!
Runner uses the lazy initialization strategy, its constructor doesn’t initialize underlying low-level structures.
Embedded loop and context are created at the with body entering or the first call of run() or get_loop().
"""























