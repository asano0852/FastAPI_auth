import os
import pathlib
import shutil
import pprint

# 絶対パスで取得
PATH_ROOT: str = str(pathlib.Path(__file__).resolve().parent)
PATH_PRODUCT: str = PATH_ROOT + "/product"


def build_directory(directoryname: str) -> str:
    target: str = PATH_ROOT + directoryname
    if not (os.path.exists(target)):
        os.mkdir(target)
    return target


def build_file(filename: str) -> str:
    result = ""
    source: str = PATH_ROOT + filename  # 絶対パスで取得
    target: str = PATH_PRODUCT + filename

    try:
        #os.remove(target) #プロダクト内のファイルを削除
        shutil.copy2(source, target)  # ディレクトリ下へコピー
    except:
        result = target + " error."

    return result


if __name__ == "__main__":
    build_directory("/product")
    pprint.pprint(list(map(build_directory, ["/product/templates",
                                             "/product/static",
                                             "/product/config",
                                             ])))
    pprint.pprint(list(map(build_file, ["/main.py",
                                        "/auth.py",
                                        "/accounts.py",
                                        "/models.py",
                                        "/setup.py",
                                        "/mongocopy.py",
                                        "/requirements.txt",
                                        "/config/default.json",
                                        "/static/.gitkeep",
                                        "/templates/index.j2",
                                        ])))
