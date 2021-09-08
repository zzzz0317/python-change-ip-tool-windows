from asciiart import *
import random
import os

config_critial_key = ["iface", "iplist", "subprocess_encode"]
config_ipobj_critial_key = ["name", "address", "netmask"]
zz_product_name = "IP切换器 by 张哲"
zz_header = """
==============================
{}
home.asec01.net
==============================
""".format(zz_product_name)
zz_license = """
MIT License

Copyright (c) 2021 张哲

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def zz_about():
    print(zz_header)
    print(zz_license)


def hello_world():
    os.system("title {}".format(zz_product_name))
    print(zz_header)
    print(enabled_art[random.randint(0, len(enabled_art) - 1)])
