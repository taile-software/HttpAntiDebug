from setuptools import setup, find_packages
import os, codecs, re

dirname = os.path.abspath(os.path.dirname(__file__))

name_pkg = 'HttpAntiDebug'

with codecs.open(os.path.join(dirname, name_pkg, "__version__.py"), mode="r", encoding="utf-8") as fp:
    try:
        data = fp.read()
        version = re.findall(r"^__version__ = ['\"]([^'\"]*)['\"]", data, re.M)[0]
        email = re.findall(r"^__author_email__ = ['\"](.*?)['\"]", data, re.M)[0]
        author  = re.findall(r"^__author__ = ['\"]([^'\"]*)['\"]", data, re.M)[0]
    except Exception:
        raise RuntimeError("Unable to determine info")

description = (
    "Bạn là 1 nhà phát triển phần mềm, công cụ ?",
    "Thư viện này có thể giúp ích cho bạn đó, nó giúp bạn ẩn các traffic của http qua các phần mềm đọc traffic gửi đi nhằm gian lận phần mềm, công cụ, ...",
    "NOTE: Chỉ giúp bạn cải thiện phần nào bảo mật, không thể giúp bạn tránh hoàn toàn các cuộc gian lận",
)

setup(
    name=name_pkg,
    version=version,
    author=author,
    author_email=email,
    description=description,
    long_description=open(os.path.join(dirname, "README.md"), encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='URL Đến Repository Của Gói',
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)