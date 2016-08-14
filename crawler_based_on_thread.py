from queue import Queue 
from threading import Thread, Lock
import urllib.parse 
import socket
import re
import time

seen_urls = set(['/'])
lock = Lock()

class Fetcher(Thread):
    
    def __init__(self,tasks):
        Thread.__init__(self)
        self.tasks = tasks 
        self.daemon = True
        self.start()

    def run(self):
        while True:
            url = self.tasks.get()
            print(url)
            get = 'GET {} HTTP/1.1\r\nHost:localhost\r\n\r\n'.format(url)
            sckt = socket.socket()
            sckt.connect(('localhost',3000))
            sckt.send(get.encode('ascii'))
            response = b''
            chunk = sckt.recv(4096)
            while chunk:
                response += chunk
                chunk = sckt.recv(4096)
              
            links = self.parseLink(url, response)

            lock.acquire()
            for link  in links.difference(seen_urls):
                print(link)
                self.tasks.put(link)
            seen_urls.update(links)
            lock.release()
            self.tasks.task_done()
            
         

    def parseLink(self,current_url,response):
        if not response:
            print("error: {}".format(current_url))
            return set()
        if not self.isHtml(response):
            return set()
        
        body = self.extractBody(response)
        in_links = re.findall(r'''(?i)href=['"]+[^\s#"'<>]+''',body)
       
        links_set = set()
        for link in in_links:
            _,part_url = re.split(r'''['"]''',link) 
            if not part_url:
                return set()
            whole_url = urllib.parse.urljoin(current_url,part_url)
            url_parse_result = urllib.parse.urlparse(whole_url)
            if url_parse_result.scheme in ['http','https']:
                continue
            # if url_parse_result.hostname:
            #     continue
            links_set.add(url_parse_result.path)
        
        # print(links_set)
        return links_set
            


    def isHtml(self,text):
        header,_ = text.split(b'\r\n\r\n',1)
        header_dict = dict(h.split(": ",1) for h in header.decode().split("\r\n")[1:])
        is_html = header_dict.get('Content-type')
        if not is_html:
            return False
        else:
            return is_html.startswith('text/html')

    def extractBody(self, html):
        _,body = html.split(b'\r\n\r\n',1)
        return body.decode('utf-8')

class Threadpool:
    def __init__(self, num_threads):
        self.tasks = Queue()
        for _  in range(num_threads):
            Fetcher(self.tasks)
    
    def addTask(self, item):
        self.tasks.put(item)

    def waitForCompletion(self):
        self.tasks.join()

if __name__ == "__main__":
    pool = Threadpool(4)
    pool.addTask("/")
    pool.waitForCompletion()  



