import json
from datetime import datetime

def crea_json(nome, posizione):
    dati = {
            "nome": nome,
            "creata": datetime.now().isoformat(timespec="seconds"),
            "brani": [],
            "impostazioni": {},
    }

    (posizione / "playlist.json").write_text(json.dumps(dati, ensure_ascii=False, indent=2), encoding="utf-8")

def leggi_json(posizione):
    file = posizione / "playlist.json"
    try:
        return json.loads(file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as er:
        print(er)
        return None