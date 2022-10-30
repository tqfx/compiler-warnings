#!/usr/bin/env python
from subprocess import Popen
from bs4 import BeautifulSoup
import os
import re

version3 = (
    "3.0.3",
    "3.1.1",
    "3.2.1",
    "3.3.1",
    "3.4.0",
    "4.0.0",
    "4.1.0",
    "4.2.0",
    "4.3.0",
    "4.4.0",
    "4.5.0",
    "4.6.0",
    "4.7.0",
    "4.8.0",
    "4.9.0",
    "5.1.0",
    "5.2.0",
    "5.3.0",
    "5.4.0",
    "5.5.0",
    "6.1.0",
    "6.2.0",
    "6.3.0",
    "6.4.0",
    "6.5.0",
    "7.1.0",
    "7.2.0",
    "7.3.0",
    "7.4.0",
    "7.5.0",
    "8.1.0",
    "8.2.0",
    "8.3.0",
    "8.4.0",
    "8.5.0",
    "9.1.0",
    "9.2.0",
    "9.3.0",
    "9.4.0",
    "9.5.0",
    "10.1.0",
    "10.2.0",
    "10.3.0",
    "10.4.0",
    "11.1.0",
    "11.2.0",
    "11.3.0",
    "12.1.0",
    "12.2.0",
)
versions = ["2.95.3"]
urls = [("https://gcc.gnu.org/onlinedocs/gcc-2.95.3/gcc_2.html", "2.95.3")]
for version in version3:
    versions.append(version)
    urls.append(
        (
            "https://gcc.gnu.org/onlinedocs/gcc-%s/gcc/Warning-Options.html" % version,
            version,
        )  # type: ignore
    )
shell = os.path.join(os.getcwd(), "gcc.sh")
with open(shell, "w", encoding="UTF-8") as f:
    f.write("#!/usr/bin/env bash\n")
    for url in urls:
        f.write("wget -c -nv {} -O {}.html\n".format(*url))
Popen(["bash", "-c", shell]).wait()
warning = []
options = set()
for version in versions:
    with open(version + ".html", "r") as f:
        version = ".".join(version.split('.')[:2]) + '+'
        text = str(BeautifulSoup(f.read(), "html.parser").text)
        for option in sorted(set(re.findall(r"(-W[0-9a-z+-]+)", text))):
            if "-Wno-" in option or len(option) < 4:
                continue
            if option not in options:
                warning.append((option, version))
                options.add(option)
warning = sorted(warning, key=lambda x: x[0])
with open("gcc.md", "w", encoding="UTF-8") as f:
    f.write("# GCC\n\n|warnings|version+|\n|:-|:-|\n")
    for warn in warning:
        f.write("|{}|{}|\n".format(*warn))
