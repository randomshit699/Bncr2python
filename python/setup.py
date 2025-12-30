import os
import shutil
from pathlib import Path

from Cython.Build import cythonize  # type: ignore
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

if __name__ != "__main__":
    raise ImportError("not import this")
# 指定要编译的目录
src_dir = "."
build_dir = Path(".") / "build"

# 获取所有 .py 文件的路径
py_files = list(Path(src_dir).rglob("*.py"))

# 过滤掉 __init__.py 文件（如果需要）
py_files = [f for f in py_files if f.name != "__init__.py"]
# 过滤掉自己
py_files = [f for f in py_files if f.name != __file__.split(os.sep)[-1]]

if len(py_files) == 0:
    raise FileNotFoundError("no .py file found")

for f in py_files:
    if f.name.startswith("__"):
        f = f.rename(f.parent / f.name[2:])

# 为每个 .py 文件创建一个 Extension 对象
extensions = []
for py_file in py_files:
    # 构建模块名称
    rel_path = py_file.relative_to(src_dir)
    module_name = rel_path.with_suffix("").as_posix().replace("/", ".")

    extensions.append(Extension(name=module_name, sources=[str(py_file)], include_dirs=[str(py_file.parent)]))

# 设置编译选项
setup(
    name="my_cython_modules",
    version="0.1",
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},  # 指定 Python 语言版本
    ),
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    script_args=["build_ext", "--inplace"],
)

shutil.rmtree(build_dir)
for f in py_files:
    c_file = f.with_suffix(".c")
    so_file = f.with_suffix(".cpython-311-x86_64-linux-musl.so")
    if c_file.exists():
        os.remove(str(c_file))
    if so_file.exists():
        so_file.rename(so_file.parent / so_file.name.replace("cpython-311-x86_64-linux-musl.", ""))
    if f.exists():
        f.rename(f.parent / f"__{f.name}")

