from zzasciiart import *
import random

config_critial_key = ["iface", "iplist", "subprocess_encode"]
config_ipobj_critial_key = ["name", "address", "netmask"]

def hello_world():
    print("====================")
    print("ZZ IP切换器")
    print("home.asec01.net")
    print("====================")
    print(enabled_art[random.randint(0,len(enabled_art)-1)])