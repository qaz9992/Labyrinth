__all__ = ['main']

def OverWrite(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return res
    if func.__doc__ is None:
        func.__doc__ = ''
    wrapper.__doc__ = '@overWrite\n' + func.__doc__
    return wrapper
def LoadStart(func):
    def wrapper(*args, **kwargs):
        
        res = func(*args, **kwargs)
        return res
    if func.__doc__ is None:
        func.__doc__ = ''
    wrapper.__doc__ = '@loadStart\n' + func.__doc__
    return wrapper

# @LoadStart
@OverWrite
def main():
    print('example plugin loaded')
    __import__('time').sleep(0.5)
