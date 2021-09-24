#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        request = self.data.decode().split()
        request_type = request[0]
        request_path = request[1]

        # if the request type is not GET, response 405
        if(request_type != "GET"):
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed",'utf-8'))

        else:
            isPathComplete = 0
            root = "www"
            url = "http://127.0.0.1:8080" + request_path 
            
            if(request_path[-1] == '/'):
                request_path = request_path + "index.html"
            
            request_split = request_path.split(".")
       

            # if curl path is like www/ab, we assume it's a folder

            if(len(request_split) == 1):
                request_path = request_path + "/index.html"
                request_split.append("html")
                url = url + '/'
                isPathComplete = 1 # it's 1 if there's no '.' from input, we do 301

            if(len(request_split) <= 2 and
                (request_split[-1] == "css" or request_split[-1] == "html")):  


                try:
                    # try to return the content at the path with a 200 code
                    with open(root+request_path, 'r') as file:
    
                        if (isPathComplete == 0):
                            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
                        elif (isPathComplete == 1):
                            # redirect if there no '/' from the input
                            self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\n",'utf-8'))
                            self.request.sendall(bytearray("Location: " + url + "\r\n",'utf-8'))
    
                        if (request_split[-1] == "html"):
                            content_type = "Content-Type: text/html\r\n"
                        else:
                            content_type = "Content-Type: text/css\r\n"

                        self.request.sendall(bytearray(content_type,'utf-8'))
                        
                        l = file.read(1024)
                        while (l):
                            self.request.send( bytearray(l,'utf-8') )
                            l = file.read(1024)
                        file.close()

                
                except:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))

                
            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))

        return 0





if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()