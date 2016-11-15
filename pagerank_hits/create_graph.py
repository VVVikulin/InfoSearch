from BeautifulSoup import  BeautifulSoup
import base64
import re
import zlib
import os
import time
all_urls = {}
max_hank_link_id = -1

class WebPage:
    page_id = None
    out_links = None
    in_links = None
    
    def __init__(self, page_id):
        
        self.page_id = page_id
        self.out_links = {}
        self.in_links = {}
        
    def add_out_link(self, new_link_url):
        global url_id_dict
        new_link_id = url_id_dict[new_link_url]       
        if new_link_id in self.out_links:
            self.out_links[new_link_id] += 1
        else:
            self.out_links[new_link_id] = 1
    
    def add_in_link(self, new_link_in_id):
        if new_link_in_id in self.in_links:
            self.in_links[new_link_in_id] =  self.in_links[new_link_in_id] + 1
        else: 
            self.in_links[new_link_in_id] = 1
    
    def __repr__(self):
        return "Web Page with id " + str(self.page_id)
    
        
url_id_dict = {}
id_url_dict = {}
with open("urls.txt", "r") as f:
    for line in f:
        id_url = line.strip().split("\t")
        url_id_dict[id_url[1]] = int(id_url[0])
        id_url_dict[int(id_url[0])] = id_url[1]

count = 0
path_for_data = "/home/vsevolod/info_data/urls_data/"
for subdir, dirs, files in os.walk(path_for_data):
    for file1 in files:
        file_path = os.path.join(subdir, file1)
        print "[FILE PATH] " + file_path
        with open(file_path, "r") as f:
            for line in f:
                id_html = line.strip().split("\t")
                url_id = int(id_html[0])
                url_html = id_html[1]
                new_page = WebPage(url_id)
                all_urls[url_id] = new_page
                decoded_data  = base64.b64decode(url_html).decode("zlib")
                try:
                    soup = BeautifulSoup(decoded_data.decode("utf-8"))
                    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                        new_link = link.get('href')
                        if new_link[-1] != "/":
                            new_link= new_link + "/"
                        if new_link in url_id_dict:
                            out_new_link_id = url_id_dict[new_link]
                        else:
                            out_new_link_id = max_hank_link_id
                            url_id_dict[new_link] = out_new_link_id
                            id_url_dict[out_new_link_id] = new_link
                            max_hank_link_id -= 1
                        new_page.add_out_link(new_link)
                    all_urls[url_id] = new_page
                except UnicodeEncodeError:
                    print "[ERROR  IN BS ENCODING]"
                if count % 1000 == 0:
                    print "[URL NUM]  ", count
                count += 1
def create_file(all_urls):
    with open("graph.txt", "w") as f:
        for i in all_urls:
            new_out = all_urls[i].out_links
            if len(new_out) != 0:
                new_str=str(i) + '\t'
                for j in new_out:
                    new_str = new_str + str(j) + ":" + str(new_out[j]) + " "
                new_str += "\n"
                f.write(new_str)
create_file(all_urls)
