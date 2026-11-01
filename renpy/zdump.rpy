init python:
    import json as _j
    def _nm(n):
        return None if n is None else str(n.name)
    def _dump_cmd():
        out = []
        sc = renpy.game.script
        for name, n in sc.namemap.items():
            d = {"n": str(name), "t": n.__class__.__name__, "nx": _nm(getattr(n, "next", None)), "f": n.filename.split("/")[-1], "l": n.linenumber}
            t = d["t"]
            if t == "Jump":
                d["target"] = n.target; d["expr"] = n.expression
            elif t == "Call":
                d["target"] = n.label; d["expr"] = n.expression
            elif t == "If":
                d["entries"] = [[c, _nm(b[0]) if b else None] for c, b in n.entries]
            elif t == "Menu":
                d["items"] = [[l, c, _nm(b[0]) if b else None] for l, c, b in n.items]
            elif t in ("Python", "EarlyPython"):
                d["code"] = n.code.source
            elif t == "Label":
                d["label"] = n.name
            elif t == "UserStatement":
                d["line"] = n.line
            elif t == "Default":
                d["var"] = n.varname; d["code"] = n.code.source
            out.append(d)
        with open(config.basedir + "/ast_dump.json", "w") as f:
            _j.dump({"nodes": out, "overrides": dict(config.label_overrides)}, f, ensure_ascii=False)
        print("DUMPED", len(out))
        return False
    renpy.arguments.register_command("zdump", _dump_cmd)
