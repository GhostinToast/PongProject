# =================================================================================================
# Contributing Authors:	    Alexander Wise, Ruby Harris, Michaela Winfree
# Email Addresses:          Alex.Wise@uky.edu, Ruby.Harris@uky.edu, Michaela.winfree@uky.edu
# Date:                     11/16/2023
# Purpose:                  Simplifies the connection code
# =================================================================================================

import socket
import json
from typing import Tuple

# wrapper class for sending and receiving data
class sock_wrapper:
    def __init__ (self, clientSocket:socket.socket):
        self.holder = clientSocket      # the connection itself
        self.closed = False             # which is open :)

    # sending of a message:
    def send(self, data) -> Tuple[bool, dict]:
        
        try:        # change into json string, then shoot it out
            jsinfo = json.dumps(data)
            self.holder.send((jsinfo.encode()))

        except socket.error as e:   # if we have a socket error, close the socket
            print('error: ', e)
            self.close()
            return False, None
        
        except UnicodeEncodeError as e: # if we have a unicode error, just return nothing
            print('error: ', e)
            return False, None
        
        return True, jsinfo     # if everything worked, return the info we squished to check it if need be
    
    # receiving of a message:
    def recv(self) -> Tuple[bool, dict]:

        try:        # try to receive the packet from the socket
            info = self.holder.recv(1024).decode()
            jsinfo = json.loads(info)   # and decompress from the json string

        except socket.error as e:   # if we have a socket error, close the socket
            print('socket error: ', e)
            self.close()
            return False, None
        
        except json.JSONDecodeError as e:       # if we have a json error, just return nothing
            print('JSON decoding error: ', e)
            return False, None
        
        except UnicodeDecodeError as e:     # if we have a unicode error, just return nothing
            print('error: ', e)
            return False, None
        
        return True, jsinfo
    
    # this is the closing of the wrapper
    def close(self) -> bool:
        self.holder.close()     # close the socket itself
        self.closed = True      # & label this item as closed