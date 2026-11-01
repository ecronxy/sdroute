# Быстрый старт с проверенной точки маршрута (создано автоматически, см. routes/ROUTES.md).
# Включается файлом game/start_at.txt с одним словом внутри (например end15 или kf15_late).
# «Новая игра» тогда прыгает на нужную сцену с нужными очками. Удалить файл: игра стартует как обычно.
# Каждая точка проверена прогоном движка: оставшиеся выборы маршрута приводят в ожидаемую концовку.
init -1 python:
    ROUTE_CKPT = {
 "end0": {
  "label": "sd04_04_SB_A00",
  "vars": {
   "var001": 69,
   "var002": 28,
   "flag944": 1
  }
 },
 "end1": {
  "label": "sd04_04_SB_A00",
  "vars": {
   "var001": 69,
   "var002": 28,
   "flag944": 1
  }
 },
 "end2": {
  "label": "sd04_04_SE_A00",
  "vars": {
   "var001": 65,
   "var002": 56
  }
 },
 "end3": {
  "label": "sd04_04_SG_A00",
  "vars": {
   "flag976": 1,
   "flag801": 1,
   "var001": 26,
   "flag974": 1,
   "var002": 96,
   "flag973": 1,
   "flag970": 1
  }
 },
 "end4": {
  "label": "sd04_04_SE_A00",
  "vars": {
   "var001": 65,
   "var002": 56
  }
 },
 "end5": {
  "label": "sd04_04_KA_A00",
  "vars": {
   "var001": 106,
   "var002": 50
  }
 },
 "end6": {
  "label": "sd04_04_KA_A00",
  "vars": {
   "var001": 96,
   "var002": 50
  }
 },
 "end7": {
  "label": "sd04_04_KE_A00",
  "vars": {
   "var001": 65,
   "var002": 76
  }
 },
 "end8": {
  "label": "sd04_04_SB_A00",
  "vars": {
   "var001": 69,
   "var002": 28,
   "flag944": 1
  }
 },
 "end9": {
  "label": "sd04_04_KC_A00",
  "vars": {
   "var001": 49,
   "flag940": 1,
   "flag978": 1,
   "var002": 62
  }
 },
 "end10": {
  "label": "sd04_04_KE_A00",
  "vars": {
   "var001": 61,
   "var002": 72
  }
 },
 "end11": {
  "label": "sd04_04_SC_A00",
  "vars": {
   "flag801": 1,
   "var001": 26,
   "var002": 96
  }
 },
 "end12": {
  "label": "sd04_04_SC_A00",
  "vars": {
   "flag801": 1,
   "var001": 26,
   "var002": 96
  }
 },
 "end13": {
  "label": "sd04_04_SC_A00",
  "vars": {
   "flag801": 1,
   "var001": 30,
   "flag978": 1,
   "var002": 101
  }
 },
 "end14": {
  "label": "sd04_04_SC_A00",
  "vars": {
   "flag801": 1,
   "var001": 42,
   "flag978": 1,
   "var002": 65
  }
 },
 "end15": {
  "label": "sd04_04_KE_A00",
  "vars": {
   "var001": 65,
   "var002": 100
  }
 },
 "end16": {
  "label": "sd04_04_KE_A00",
  "vars": {
   "var001": 65,
   "var002": 100
  }
 },
 "end17": {
  "label": "sd04_04_SE_A00",
  "vars": {
   "var001": 65,
   "var002": 56
  }
 },
 "end18": {
  "label": "sd04_04_SB_A00",
  "vars": {
   "var001": 69,
   "var002": 52
  }
 },
 "end19": {
  "label": "sd04_04_SB_A00",
  "vars": {
   "var001": 69,
   "var002": 52
  }
 },
 "end20": {
  "label": "sd04_04_KE_A00",
  "vars": {
   "var001": 61,
   "var002": 72
  }
 },
 "end21": {
  "label": "sd04_04_SA_A00",
  "vars": {
   "var001": 130,
   "var002": 128,
   "flag942": 1,
   "flag802": 1
  }
 },
 "kf15": {
  "label": "sd04_04_KE_A00",
  "vars": {
   "var001": 65,
   "var002": 76
  }
 },
 "kf15_late": {
  "label": "sd05_05_KF_A00",
  "vars": {
   "var001": 94,
   "var002": 76
  }
 },
 "kf16": {
  "label": "sd04_04_KE_A00",
  "vars": {
   "var001": 64,
   "var002": 76
  }
 },
 "kf16_late": {
  "label": "sd05_05_KF_A00",
  "vars": {
   "var001": 93,
   "var002": 76
  }
 },
 "kf7": {
  "label": "sd04_04_KE_A00",
  "vars": {
   "var001": 65,
   "var002": 76
  }
 },
 "kf7_late": {
  "label": "sd05_05_KF_A00",
  "vars": {
   "var001": 94,
   "var002": 76
  }
 }
}

init 999 python:
    import os as _rs_os
    _rs_file = _rs_os.path.join(config.gamedir, "start_at.txt")
    if _rs_os.path.exists(_rs_file):
        config.label_overrides["start"] = "routes_start"

label routes_start:
    python:
        _rs_name = open(_rs_file).read().strip()
        _rs_ck = ROUTE_CKPT[_rs_name]
        for _rs_k, _rs_v in _rs_ck["vars"].items():
            setattr(store, _rs_k, _rs_v)
        store.lastB = -1
        store.latc = None
    $ renpy.jump(_rs_ck["label"])
