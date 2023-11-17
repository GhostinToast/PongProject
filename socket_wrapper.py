# =================================================================================================
# Contributing Authors:	    Alexander Wise, Ruby Harris
# Email Addresses:          Alex.Wise@uky.edu, Ruby.Harris@uky.edu
# Date:                     11/17/2023
# Purpose:                  Simplifies the connection code
# =================================================================================================

import socket
import json
from typing import Tuple
#wrapper class for sending and receiving data
class sock_wrapper:
    def __init__ (self, clientSocket:socket.socket):
        self.holder = clientSocket
        self.closed = False
    def send(self, data) -> Tuple[bool, dict]:
        try:
            jsinfo = json.dumps(data)
            self.holder.send((jsinfo.encode()))
        except socket.error as e:
            print('error: ', e)
            self.close()
            return False, None
        except UnicodeEncodeError as e:
            print('error: ', e)
            return False, None
        return True, jsinfo
    
    def recv(self) -> Tuple[bool, dict]:
        try:
            info = self.holder.recv(1024).decode()
            jsinfo = json.loads(info)
        except socket.error as e:
            print('socket error: ', e)
            self.close()
            return False, None
        except json.JSONDecodeError as e:
            print('JSON decoding error: ', e)
            return False, None
        except UnicodeDecodeError as e:
            print('error: ', e)
            return False, None
        return True, jsinfo
    def close(self) -> bool:
        self.holder.close()
        self.closed = True