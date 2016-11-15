class WebPage:
    page_id = None
    out_links = None
    in_links = None
    hab_index = None
    aut_index = None
    page_rank = None
    
    def __init__(self, page_id, all_out_links, in_link = None):
        
        self.page_id = page_id
        self.out_links = {}
        self.in_links = {}
        self.hab_index = 1
        self.aut_index = 1
        for url_id in all_out_links:
            self.out_links[int(url_id["id"])] = int(url_id["weight"])
        if in_link is not None:
            self.in_links[int(in_link["id"])] = int(in_link["weight"])
           
    def add_out_link(self, all_out_links):   
        for url_id in all_out_links:
            self.out_links[int(url_id["id"])] = int(url_id["weight"])
    
    def add_in_link(self, new_link_in_id, weight):
        self.in_links[new_link_in_id] = weight
    
    def get_out_links(self):
        return self.out_links
    
    def get_in_links(self):
        return self.in_links
    
    def get_hab_index(self):
        return self.hab_index
    
    def get_aut_index(self):
        return self.aut_index
    
    def update_hab_aut_index(self, new_hab_index, new_aut_index):
        self.hab_index = new_hab_index
        self.aut_index = new_aut_index
    
    def get_page_rank(self):
        return self.page_rank
    
    def update_page_rank(self, new_page_rank):
        self.page_rank = new_page_rank
        
    def get_page_rank_for_link(self, out_page_id):
        link_weight = self.out_links[out_page_id]
        all_weights = sum(self.out_links.values())
        return (link_weight/float(all_weights))*float(self.page_rank)
            
    def __repr__(self):
        return "Web Page with id " + str(self.page_id)
