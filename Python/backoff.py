import backoff
from backoff import on_predicate, constant

class CustomException(Exception):
    pass

counter = 0


@on_predicate(constant, max_tries=5, interval=1)
def poll():
    global counter
    if counter < 20:
        counter = counter + 1
        print(f"{counter}")
        return False
    return True


def giveup_func(exception):
    return exception is not CustomException  # only give up if CustomException


@backoff.on_exception(backoff.expo, Exception, max_time=10, max_tries=4, giveup=giveup_func)
def wait_until_poll_completes():
    if not poll():
        print("we failed x")
        raise CustomException("x didn't complete")
    print(f"x is okay")


if __name__ == '__main__':
    wait_until_poll_completes()
