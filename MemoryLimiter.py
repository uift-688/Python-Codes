from sys import getsizeof as _getsizeof, _current_frames
from collections import ChainMap as _ChainMap
import threading as _th
from atexit import register as _register
from time import sleep as _sleep

_MAXMEMORY = 200
_is_activated = False

def _GetLocals():
    all_vars = {}
    # 現在のスレッド一覧を取得
    _threads = {_thread.ident: _thread.name for _thread in _th.enumerate()}
    
    # sys._current_frames() から全スレッドのスタックフレームを取得
    for _thread_id, frame in _current_frames().items():
        # スレッドIDからスレッド名を取得
        _thread_name = _threads.get(_thread_id, f"Unknown-{_thread_id}")
        all_vars[_thread_name] = {}
        
        # 各スタックフレームのローカル変数を取得
        while frame:
            # フレーム内のローカル変数を取得
            all_vars[_thread_name].update(frame.f_locals)
            frame = frame.f_back  # 親フレームに遡る
    return all_vars

def _MemoryMonitor(RPS: int):
    global _is_activated
    while _is_activated:
        Busy_Memory = _getsizeof(_ChainMap(globals(), _GetLocals()))
        if _MAXMEMORY < Busy_Memory:
            raise MemoryError("MemoryError By Limiter")
        _sleep(1 / RPS)

def Activate():
    global _is_activated
    if _is_activated:
        raise MemoryError("Memory limiter has already been activated.")
    _is_activated = True
    MM = _th.Thread(target=_MemoryMonitor, kwargs={"RPS": 120})
    MM.start()

def SetMaxMemory(MaxMemory: int):
    global _is_activated
    """Args:
    MaxMemory: int / Unit: Byte"""
    if _is_activated:
        raise UserWarning("Cannot modify settings because _the memory limiter is already activated.")
    global _MAXMEMORY
    _MAXMEMORY = int(MaxMemory)

def _Stop():
    global _is_activated
    _is_activated = False

_register(_Stop)