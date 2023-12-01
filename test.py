from ctypes import *

from retropy import RetroPy
from env import CORE, GAMES

def main():
    core = RetroPy(CORE)

    success = core.load(GAMES[0])

    if not success:
        raise RuntimeError()

    # core.unload()

    for _ in range(10):
        core.frame_advance()
    
    save = core.saveState()
    
    # print(save.data)
    
    core.reset()
    
    success = core.loadState(save)
    
    print(success)
    
    print("Done")

def test1():
    from retropy.core.environment import retro_variable

    def func(data: c_void_p):
        data = cast(data, POINTER(retro_variable)).contents
        data.value = b'456'

    v = retro_variable(key=b'okay', value=b'123')
    print(v.value)
    
    func(byref(v))
    
    print(v.value)

def test2():
    def func(data: c_void_p):
        data = cast(data, POINTER(c_bool)).contents
        data.value = True

    v = c_bool(False)
    print(v)
    
    func(byref(v))
    
    print(v)

if __name__ == "__main__":
    main()
    # test1()
    # test2()
