from PyInstaller.__main__ import run


def main():
    run(["--onefile", "src/tinbox/__main__.py"])
