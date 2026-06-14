import json
import time
import os


# =========================
# SIMPLE FILE STORAGE ENGINE
# =========================
class StorageHandler:
    def __init__(self, base_path="fse_data"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    # -------------------------
    # SAVE JSON DATA
    # -------------------------
    def save(self, filename, data):
        path = os.path.join(self.base_path, f"{filename}.json")

        payload = {
            "timestamp": time.time(),
            "data": data
        }

        with open(path, "w") as f:
            json.dump(payload, f, indent=4)

        return True

    # -------------------------
    # LOAD JSON DATA
    # -------------------------
    def load(self, filename):
        path = os.path.join(self.base_path, f"{filename}.json")

        if not os.path.exists(path):
            return None

        with open(path, "r") as f:
            return json.load(f)

    # -------------------------
    # DELETE DATA
    # -------------------------
    def delete(self, filename):
        path = os.path.join(self.base_path, f"{filename}.json")

        if os.path.exists(path):
            os.remove(path)
            return True

        return False

    # -------------------------
    # APPEND LOG STYLE DATA
    # -------------------------
    def append_log(self, filename, entry):
        path = os.path.join(self.base_path, f"{filename}.json")

        data = []
        if os.path.exists(path):
            with open(path, "r") as f:
                try:
                    data = json.load(f).get("data", [])
                except:
                    data = []

        data.append({
            "time": time.time(),
            "entry": entry
        })

        with open(path, "w") as f:
            json.dump({"data": data}, f, indent=4)

        return True

    # -------------------------
    # GET ALL FILES
    # -------------------------
    def list_files(self):
        return os.listdir(self.base_path)
