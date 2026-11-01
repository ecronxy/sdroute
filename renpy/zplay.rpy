init 1001 python:
    import os as _os, json as _json, time as _time
    _zplan_path = _os.environ.get("ZPLAN")
    if _zplan_path:
        _zplan = _json.load(open(_zplan_path))
        _zlogf = open(_os.environ["ZLOG"], "w")
        _zstate = {"i": 0, "label": None}
        def _zlog(*a):
            _zlogf.write(" ".join(str(x) for x in a) + "\n"); _zlogf.flush()
        def _zlabel_cb(name, abnormal):
            if str(name).startswith("sd"):
                _zstate["label"] = name
                _zlog("L", name)
        config.label_callback = _zlabel_cb
        def set_lastb(a, b=None):
            global lastB, latc
            if a == -1 and isinstance(b, list):
                i = _zstate["i"]
                if i >= len(_zplan):
                    _zlog("PLAN_EXHAUSTED", _zstate["label"], b); renpy.quit()
                p = _zplan[i]
                if p["opts"] != b:
                    _zlog("MISMATCH", i, _zstate["label"], "game:", b, "plan:", p["opts"]); renpy.quit()
                _zstate["i"] = i + 1
                lastB = p["k"]; latc = None
                _zlog("C", i, _zstate["label"], p["k"], b, "v1=%s v2=%s" % (var001, var002))
            else:
                lastB, latc = a, b
        _zcs = renpy.call_screen
        def _zcall_screen(name, *args, **kw):
            if name == "subtitless":
                renpy.not_infinite_loop(600)
                return None
            return _zcs(name, *args, **kw)
        renpy.call_screen = _zcall_screen
        renpy.notify = lambda *a, **k: None
        for _i in range(22):
            config.label_overrides["sdend%d" % _i] = "zend%d" % _i
        config.label_overrides["splashscreen"] = "zsplash"
        preferences.transitions = 0
        config.skipping = None

label zsplash:
    python:
        import os, json
        if os.environ.get("ZCKPT"):
            _ck = json.load(open(os.environ["ZCKPT"]))
            for _k, _v in _ck["vars"].items():
                setattr(store, _k, _v)
            renpy.jump(_ck["label"])
    $ renpy.jump("start")

label zend0:
    $ _zlog("ENDING", 0); renpy.quit()
label zend1:
    $ _zlog("ENDING", 1); renpy.quit()
label zend2:
    $ _zlog("ENDING", 2); renpy.quit()
label zend3:
    $ _zlog("ENDING", 3); renpy.quit()
label zend4:
    $ _zlog("ENDING", 4); renpy.quit()
label zend5:
    $ _zlog("ENDING", 5); renpy.quit()
label zend6:
    $ _zlog("ENDING", 6); renpy.quit()
label zend7:
    $ _zlog("ENDING", 7); renpy.quit()
label zend8:
    $ _zlog("ENDING", 8); renpy.quit()
label zend9:
    $ _zlog("ENDING", 9); renpy.quit()
label zend10:
    $ _zlog("ENDING", 10); renpy.quit()
label zend11:
    $ _zlog("ENDING", 11); renpy.quit()
label zend12:
    $ _zlog("ENDING", 12); renpy.quit()
label zend13:
    $ _zlog("ENDING", 13); renpy.quit()
label zend14:
    $ _zlog("ENDING", 14); renpy.quit()
label zend15:
    $ _zlog("ENDING", 15); renpy.quit()
label zend16:
    $ _zlog("ENDING", 16); renpy.quit()
label zend17:
    $ _zlog("ENDING", 17); renpy.quit()
label zend18:
    $ _zlog("ENDING", 18); renpy.quit()
label zend19:
    $ _zlog("ENDING", 19); renpy.quit()
label zend20:
    $ _zlog("ENDING", 20); renpy.quit()
label zend21:
    $ _zlog("ENDING", 21); renpy.quit()
