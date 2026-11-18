from devagent.main import writeFile
import json

def test_write_file(tmp_path):

    file_path = tmp_path / "mon_fichier.json"

    writeFile(file_path)

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["id"] == 1
    assert data["name"] == "Yves Lemée"
    assert data["active"] is True