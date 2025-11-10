# -*- coding: UTF-8 -*-


"""https://github.com/ValentinBELYN/icmplib/blob/main/docs/6-use-icmplib-without-privileges.md
echo 'net.ipv4.ping_group_range = 0 2147483647' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
#icmplib.exceptions.SocketPermissionError: Root privileges are required to create the socket

"""

import sys, os

from libs.config import GlobalConfig
from libs.objs import O_check_work
from libs.utils_popen import ExecuteCmd

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
                            ("os_icmp", (int, 0)), 
                            #("", (str, "")), 
                        )
    def __init__(self,):
        """Startup. Host is O_conf_host"""
        super(Check_Icmp).__init__()
        
        # class that represent our work
        self.check_work = O_check_work()
        
        self._host = None
        self._gc = GlobalConfig()
        
    def do_check(self, host, address):
        """"""
        self._address = address
        self._host = host
        self.check_work.host = host
        
        self.debug_log("Start ICMP check for: %s"% (host.name, ))
        
        if HAVE_ICMPLIB and not self._host.specific_config.os_icmp == 1:
            return self._do_icmp_pythonic()
        else:
            return self._do_icmp_os()
            
    
    def _do_icmp_pythonic(self):
        """"""
        errcode = 0
        msg = ""
        
        try:
            self.debug_log("Execute internal ICMP command: count=%s, interval=%s, timeout=%s"% 
                (self._host.specific_config.icmp_count,  self._host.specific_config.interval,  self._host.specific_config.timeout)
            )
            icmplib.ping(self._address,
                count=self._host.specific_config.icmp_count,
                interval=self._host.specific_config.interval,
                timeout=self._host.specific_config.timeout
            )
        except Exception as err:
            errcode = 1
            msg_text = (f"ICMP {err=}, {type(err)=}")
            msg = "Error on icmplib: %s" % msg_text
            
        return (errcode, msg)
        
    def _do_icmp_os(self):
        """"""
        if sys.platform == "linux":
            ping_cmd = "/usr/bin/ping"
            ping_cmd = [ping_cmd, "-c", self._host.specific_config.icmp_count, "-W", self._host.specific_config.timeout, "-i", self._host.specific_config.interval, ]
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
        
        # cleanup all the commands for call ping cmd
        ping_cmd = [str(x).strip() for x in ping_cmd]

        cmd_exe = ping_cmd +[self._address]
        
        self.debug_log("Execute ICMP command: %s"% (cmd_exe, ))
        
        timeout_max = self._host.specific_config.interval * self._host.specific_config.timeout + 5
        errcode, msg = ExecuteCmd().do_execute(cmd_exe, timeout_max)
        return (errcode, msg)
        
    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional


def get_check_workers():
    return Check_Icmp
