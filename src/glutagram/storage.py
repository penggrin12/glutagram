import pickle
from os import PathLike
from pathlib import Path


class Storage:
    def __init__(self, file_path: str | PathLike[str]):
        self._path = Path(file_path)

        self._ensure_file()

    def _ensure_file(self) -> None:
        if self._path.exists():
            return
        self._path.write_bytes(pickle.dumps(set()))

    def _read(self) -> set[int]:
        with self._path.open(mode="rb") as f:
            return pickle.load(f)

    def _write(self, obj: set[int]) -> None:
        with self._path.open(mode="wb") as f:
            pickle.dump(obj, f)

    def try_appending(self, value: int) -> bool:
        data = self._read()
        if value in data:
            return False
        data.add(value)
        self._write(data)
        return True
