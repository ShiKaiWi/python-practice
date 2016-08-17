import urllib.parse 
import socket
import re
from selectors import *

seen_urls = set('/')
urls_todo = set('/')
selector = DefaultSelector()
stopped = False

class Fetcher():
    
    def __init__(self,url):
       self.url = url
       self.response = b''
       self.sock = None

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)

        try:
            self.sock.connect(('localhost',3000))
        except BlockingIOError:
            pass
        
        selector.register(self.sock.fileno(), EVENT_WRITE,self.connected)

    def connected(self,key,mask):
        selector.unregister(key.fd)
        get = 'GET {} HTTP/1.1\r\nHost:localhost\r\n\r\n'.format(self.url)
        self.sock.send(get.encode('ascii'))
        selector.register(key.fd,EVENT_READ,self.read_response)

    def read_response(self,key,mask):
        global stopped
        chunk = self.sock.recv(4096)
        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)
            links = self.parseLink(self.url, self.response)
            for link  in links.difference(seen_urls):
                urls_todo.add(link)
                Fetcher(link).fetch()
            seen_urls.update(links)
            urls_todo.remove(self.url)

            if not urls_todo:
                stopped = True
            print(self.url)  


    def parseLink(self,current_url,response):
        if not response:
            print("error: {}".format(current_url))
            return set()
        if not self.isHtml(response):
            return set()
        
        response = response.decode('utf-8')
        body = self.extractBody(response)
        in_links = re.findall(r'''(?i)href=['"]+[^\s#"'<>]+''',body)
       
        links_set = set()
        for link in in_links:
            _,part_url = re.split(r'''['"]''',link) 
            if not part_url:
                return set()
            whole_url = urllib.parse.urljoin(current_url,part_url)
            url_parse_result = urllib.parse.urlparse(whole_url)
            # if url_parse_result.scheme in ['http','https']:
            #     continue
            hostname = url_parse_result.hostname 
            if  hostname :
                continue
            if url_parse_result.path :
                links_set.add(url_parse_result.path)
        
        return links_set
            


    def isHtml(self,text):
        header,_ = text.split(b'\r\n\r\n',1)
        header_dict = dict(h.split(b": ",1) for h in header.split(b"\r\n")[1:])
        is_html = header_dict.get(b'Content-type')
        if not is_html:
            return False
        else:
            return is_html.startswith(b'text/html')

    def extractBody(self, html):
        _,body = html.split('\r\n\r\n',1)
        return body


if __name__ == "__main__":
    Fetcher('/').fetch()
    while not stopped:
        event = selector.select()
        for  event_key, event_mask in event:
            callback = event_key.data
            callback(event_key,event_mask)
    print("Done")
