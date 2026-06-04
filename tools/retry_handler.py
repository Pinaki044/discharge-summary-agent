import time


def safe_execute(
    function,
    *args,
    retries=2,
    delay=1
):

    last_error = None

    for attempt in range(retries + 1):

        try:

            result = function(*args)

            return result

        except Exception as e:

            last_error = e

            print(
                f"Tool failed: {function.__name__}"
            )

            print(
                f"Attempt {attempt + 1} failed"
            )

            time.sleep(delay)

    print(
        f"All retries failed for {function.__name__}"
    )

    return None