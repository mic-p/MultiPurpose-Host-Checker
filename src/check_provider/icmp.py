# -*- coding: UTF-8 -*-


"""https://github.com/ValentinBELYN/icmplib/blob/main/docs/6-use-icmplib-without-privileges.md
echo 'net.ipv4.ping_group_range = 0 2147483647' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
#icmplib.exceptions.SocketPermissionError: Root privileges are required to create the socket

"""

import subprocess
import sys, os

from libs.config import GlobalConfig
from .base_check import BaseCheck

try:
    import icmplib
    try:
        # check if we have permission to do alone icmp to the host. see docs above
        icmplib.ping("127.0.0.1")
    except icmplib.exceptions.SocketPermissionError:
        raise ModuleNotFoundError
    HAVE_ICMPLIB = True
except ModuleNotFoundError:
    HAVE_ICMPLIB = False


class Check_Icmp(BaseCheck):
    """"""
    __data_mandatory = (
                            #("", (str, "")),  
                        )
    __data_optional = (
                            ("icmp_count", (int, 4)), 
                            ("interval", (int, 1)),
                            ("timeout", (int, 2)),
                            #("", (str, "")), 
                        )
    def __init__(self,):
        """Startup. Host is O_conf_host"""
        super(Check_Icmp).__init__()

        self._host = None
        self._gc = GlobalConfig()
        
    def do_check(self, host):
        """"""
        self._host = host
        self._gc.log.debug("Start ICMP check for: %s"% (host.name, ))
        
        if HAVE_ICMPLIB:
            self._do_icmp_pythonic()
        else:
            self._do_icmp_os()
    
    def _do_icmp_pythonic(self):
        """"""
        icmplib.ping(self._host)
        
    def _do_icmp_os(self):
        """"""
        if sys.platform == "linux":
            ping_cmd = "/usr/bin/ping"
            ping_cmd = [ping_cmd, "-c", self._host.specific_config.icmp_count, "-W", self._host.specific_config.icmp_count, "-i", self._host.specific_config.interval, ]
        elif sys.platform == "win32":
            windir = os.getenv('windir')
            ping_cmd = os.path.join(windir, "system32", "ping.exe")
            "-n count -w timeout milliseconds"
        elif sys.platform == "darwin":
            ping_cmd = "/sbin/ping"
        else:
            msg = "No such platform: %s" % sys.platform
            self._gc.log.error(msg)
            raise ValueError(msg)
        
        ping_cmd = [str(x) for x in ping_cmd]
        hosts_list = self._host.host_details or (self._host.name, )
        
        for host in hosts_list:
            cmd_exe = ping_cmd +[host]
            self._gc.log.debug("Start from ICMP check command: %s"% (cmd_exe, ))
            p = subprocess.Popen(cmd_exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = p.communicate()
            self._gc.log.debug("ICMP check exit code: %s"% (p.returncode, ))
        
    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional


def get_check_workers():
    return Check_Icmp
