from zzconst import *
import json
import subprocess
import ipaddress
import traceback
import sys
import time

config = {}


def read_config():
    try:
        with open('config.json', 'r', encoding="utf-8") as f:
            global config
            config = json.load(f)
    except FileNotFoundError:
        err_exit("配置文件 \"config.json\" 不存在")
    except json.decoder.JSONDecodeError as ex:
        err_exit("读取配置文件失败\n{}".format(repr(ex)))
    except Exception as ex:
        err_exit("读取配置文件失败，{}\n{}".format(repr(ex), traceback.format_exc()))


def check_config():
    for k in config_critial_key:
        if k not in config:
            err_exit("配置文件中 \"{}\" 节不存在".format(k))

    for d in config["iplist"]:
        for k in config_ipobj_critial_key:
            if k not in d:
                err_exit("\n{}\n该IP配置中缺少必要属性 \"{}\"".format(json.dumps(d), k))
        if "gateway" in d:
            network = ipaddress.ip_network("{}/{}".format(d["address"], d["netmask"]), strict=False)
            gateway = ipaddress.ip_address(d["gateway"])
            if gateway not in network:
                err_exit("\n{}\n该IP配置中网关不在网络内".format(json.dumps(d)))
        if "dns" in d:
            dns = []
            if isinstance(d["dns"], str):
                dns.append(d["dns"])
            elif isinstance(d["dns"], list):
                if len(d["dns"]) == 1:
                    dns.append(d["dns"][0])
                elif len(d["dns"]) > 1:
                    dns.append(d["dns"][0])
                    dns.append(d["dns"][1])
            for dnss in dns:
                if not is_ip_address(dnss):
                    err_exit("\n{}\n该IP配置中DNS地址有误".format(json.dumps(d)))


def get_config(key, default_value):
    if key in config:
        return config[key]
    return default_value


def is_ip_address(s):
    try:
        ipaddress.ip_address(s)
        return True
    except:
        return False


def err_exit(text):
    print("出现严重错误: {}".format(text))
    input("按回车退出\n")
    sys.exit(1)


def debug_print(text):
    if get_config("debug_std_output", False):
        print("DEBUG: {}".format(text))


def user_sel_ip():
    while True:
        print("========== 请选择 ===========")
        print("0. 使用DHCP自动配置IP和DNS")
        for i in range(1, len(config["iplist"]) + 1):
            print("{}. {}".format(i, config["iplist"][i - 1]["name"]))
            debug_print(config["iplist"][i - 1])

        print("q. 退出")
        print("a. 关于")
        input_valid_range = range(0, len(config["iplist"]) + 1)
        input_string = input("请输入序号:\n")
        if input_string.isdigit():
            input_number = int(input_string)
            if input_number in input_valid_range:
                if input_number == 0:
                    change_ip_dhcp()
                    break
                ipobj = config["iplist"][input_number - 1]
                change_ip(ipobj)
                break
            else:
                print("输入有误，不存在的配置项")
        elif input_string.lower() == "q":
            break
        elif input_string.lower() == "a":
            zz_about()
        else:
            print("输入有误，请重试")


def change_ip(ipobj):
    debug_print(ipobj)
    address = ipaddress.ip_address(ipobj["address"])
    network = ipaddress.ip_network("{}/{}".format(ipobj["address"], ipobj["netmask"]), strict=False)
    is_netaddr = address == network[0]
    if is_netaddr:
        tmp_ip_1 = str(network[1]).split(".")
        tmp_ip_2 = str(network[-2]).split(".")
        ip_same = ""
        for i in range(len(tmp_ip_1)):
            if tmp_ip_1[i] == tmp_ip_2[i]:
                ip_same = ip_same + tmp_ip_1[i] + "."
        while True:
            try:
                print("该配置不包含主机地址，请补全")
                print("范围: {}-{}".format(network[1], network[-2]))
                address = ipaddress.ip_address(ip_same + input(ip_same))
                if address not in network:
                    raise Exception("该IP地址不在网络内")
                break
            except Exception as ex:
                print("配置有误，请重试")
                print(ex)

    dns = []
    if "dns" in ipobj:
        if isinstance(ipobj["dns"], str):
            dns.append(ipobj["dns"])
        elif isinstance(ipobj["dns"], list):
            if len(ipobj["dns"]) == 1:
                dns.append(ipobj["dns"][0])
            if len(ipobj["dns"]) > 1:
                dns.append(ipobj["dns"][0])
                dns.append(ipobj["dns"][1])
    command = "netsh interface ip set address name=\"{}\" source=static address={} mask={}" \
        .format(config["iface"], address, network.netmask)
    print("\n\n最终核查:")
    print("适配器: {}\n地址: {}\n掩码: {}".format(config["iface"], address, network.netmask))
    if "gateway" in ipobj:
        print("网关: {}".format(ipobj["gateway"]))
        command = command + " gateway={}".format(ipobj["gateway"])
    if len(dns) != 0:
        print("DNS: {}".format(", ".join(dns)))
    if input("按回车继续，输入其它值将退出\n") != "":
        sys.exit(0)
    print("设置静态IP地址")
    run_windows_command(command)
    print("等待2s", end="")
    time.sleep(0.5)
    print(".", end="")
    time.sleep(0.5)
    print(".", end="")
    time.sleep(0.5)
    print(".", end="")
    time.sleep(0.5)
    print(".")
    print("清除DNS配置")
    run_windows_command(
        "netsh interface ip set dnsservers name=\"{}\" source=static address=none register=both"
            .format(config["iface"]))
    for dnss in dns:
        print("设置DNS: {}".format(dnss))
        run_windows_command("netsh interface ip add dnsservers name=\"{}\" address={}".format(config["iface"], dnss))


def change_ip_dhcp():
    print("将适配器 \"{}\" 切换为自动获取地址模式".format(config["iface"]))
    run_windows_command("netsh interface ip set address name=\"{}\" source=dhcp".format(config["iface"]))
    run_windows_command("netsh interface ip set dnsservers name=\"{}\" source=dhcp".format(config["iface"]))


def run_windows_command(c):
    print("执行命令: {}".format(c))
    if get_config("debug_subprocess_disable", False):
        print("由于在配置文件中设置了 \"debug_subprocess_disable\", 该命令未被执行。")
        return 0
    try:
        p = subprocess.run(c, capture_output=True)
        out = p.stdout.decode(config["subprocess_encode"])
        print("运行结果: {}".format(out))
        return p.returncode
    except:
        print("警告: 获得运行结果出错，请核查该命令是否被执行成功，以下为详细的错误信息。\n{}".format(traceback.format_exc()))
    return -1


if __name__ == '__main__':
    hello_world()
    try:
        read_config()
        check_config()
        user_sel_ip()
        print("运行结束，欢迎您下次使用")
        if get_config("debug_std_output", False):
            input("按回车退出\n")
            sys.exit(0)
        time.sleep(2)
        # print(config)
    except Exception as ex:
        # traceback.print_exc()
        err_exit("{}\n{}".format(repr(ex), traceback.format_exc()))
