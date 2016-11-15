from web_page import WebPage
class WebGraph:
    all_urls = None
    id_url_dict = None
    def __init__(self, file_path):      
        self.id_url_dict = {}
        with open("urls.txt", "r") as f:
            for line in f:
                id_url = line.strip().split("\t")
                self.id_url_dict[int(id_url[0])] = id_url[1]
        self.all_urls = {}
        with open(file_path, "r") as f:
            print "File has been succesfully opened"
            for line in f:
                line = line.strip()
                url_id_out_links = line.split("\t")
                new_url_id = int(url_id_out_links[0])
                split_url_weight = lambda x : {"id" : int(x.split(":")[0]), "weight" : int(x.split(":")[1])}
                out_links = map(split_url_weight, url_id_out_links[1].split(" "))
                j = 0
                if not new_url_id in self.all_urls: 
                    new_page = WebPage(new_url_id, out_links)
                    self.all_urls[new_url_id] = new_page
                else:
                    new_page = self.all_urls[new_url_id]               
                    new_page.add_out_link(out_links)
                    
                for out_link in out_links:
                    j += 1
                    if out_link["id"] in self.all_urls:
                        new_page = self.all_urls[out_link["id"]]
                        new_page.add_in_link(new_url_id, out_link["weight"])
                    else:
                        new_in_link = {"id" : new_url_id, "weight" : out_link["weight"]}
                        self.all_urls[out_link["id"]] = WebPage(out_link["id"], [], new_in_link)    
        
    def check_is_graph_correct(self):
        all_in = 0
        all_out = 0
        for i in self.all_urls:
            in_links = self.all_urls[i].in_links
            out_links = self.all_urls[i].out_links
            all_out += sum(out_links[i] for i in out_links)
            all_in += sum(in_links[i] for i in in_links)
        if all_in == all_out:
            print "Congratulations, graph is correct!"
        else:
            print "Graph is not correct!"
        
    def __repr__(self):
        graph_len = len(self.all_urls)
        hank_link_count = 0
        for i in self.all_urls:
            if i < 0:
                hank_link_count += 1
        hank_percent = hank_link_count/float(graph_len) * 100
        return "This web graph contains " + str(graph_len) + " web pages and " \
                + str(hank_link_count) + " hank links." + " Percent of hank links is " + str(round(hank_percent,2))
               
    def make_hits_iter(self, last_iter_values, verbose=0):
        new_ind = {}
        this_iter_values = {"hab" : 0, "aut" : 0}
        for page_id in self.all_urls:
            new_page = self.all_urls[page_id]
            list_in_links = new_page.get_in_links()
            list_out_links = new_page.get_out_links()
            new_hab = new_page.get_hab_index()
            new_aut = new_page.get_aut_index()            
            for out_link in list_out_links:
                new_hab += self.all_urls[out_link].get_aut_index()
            for in_link in list_in_links:
                new_aut += self.all_urls[in_link].get_hab_index()
            new_ind[page_id] = {"hab" : new_hab, "aut" : new_aut}
        for page_id in new_ind:
            new_page = self.all_urls[page_id]
            new_hab = new_ind[page_id]["hab"]
            new_aut = new_ind[page_id]["aut"]
            new_page.update_hab_aut_index(new_hab, new_aut)
            this_iter_values["hab"] += new_hab
            this_iter_values["aut"] += new_aut
        hab_rel_diff =  (this_iter_values["hab"] - last_iter_values["hab"])/  \
                            float(this_iter_values["hab"] + last_iter_values["hab"])
        aut_rel_diff = (this_iter_values["aut"] - last_iter_values["aut"])/  \
                            float(this_iter_values["aut"] + last_iter_values["aut"])
        rel_diff = (hab_rel_diff + aut_rel_diff)/2.0   
        if verbose:    
            print "Hab relative difference " + str(round(hab_rel_diff,2)) 
            print "Aut relative difference " + str(round(aut_rel_diff,2)) 
            print "Relative difference beetween last and new iter is " + str(round(rel_diff,2))
        return this_iter_values, rel_diff, new_ind
    
    def calculate_hits(self, max_iters=10, top_size=30, eps=None, verbose=0):
        last_iter_values = {"hab" : len(self.all_urls), "aut" : len(self.all_urls)}
        is_cycle_out = False
        for new_iter in range(0, max_iters):
            if verbose:
                print "Hits iter number "  + str(new_iter)
            last_iter_values, new_rel_diff, new_ind = self.make_hits_iter(last_iter_values, verbose)
            if eps is not None:
                if abs(1.0 - new_rel_diff) < eps:
                    if verbose:
                        print "Iterations of Hits is stopped because there is no significant changes " \
                               "in hab and aut indices"
                    is_cycle_out = True
                    break
        if not is_cycle_out and verbose:
             print "Iteration is stopped because maximum num of iterations"
        final_habs = map(lambda x: new_ind[x]["hab"], new_ind)
        final_auts = map(lambda x: new_ind[x]["aut"], new_ind)
        all_pages = new_ind.keys()
        best_by_habs = [self.id_url_dict[x] for (y,x) in sorted(zip(final_habs,all_pages)) \
                        if x > 0][::-1][0:top_size]
        best_by_auts = [self.id_url_dict[x] for (y,x) in sorted(zip(final_auts,all_pages)) \
                        if x > 0][::-1][0:top_size]
        return {"best_by_habs" : best_by_habs, "best_by_auts" : best_by_auts}
    
    
    
        
    def initialize_page_rank(self):
        start_page_rank_value = 1.0 /float(len(self.all_urls))
        for url in self.all_urls:
            self.all_urls[url].update_page_rank(start_page_rank_value)
    
    def check_page_rank(self, iter_num):
        sum_page_rank = 0.0
        sum_hunk_page_rank = 0.0
        for url in self.all_urls:
            new_page_rank = self.all_urls[url].get_page_rank()
            sum_page_rank += new_page_rank
            if url < 0:
                sum_hunk_page_rank += new_page_rank
        print "Sum page rank on iter " + str(iter_num) + " is " + str(round(sum_page_rank,2))
        print "Sum page rank (only hank links) on iter " + str(iter_num) + " is " + str(round(sum_hunk_page_rank,2))
        return sum_page_rank
    
    def calculate_iter_page_rank(self, iter_num, verbose=0):
        sum_page_rank = self.check_page_rank(iter_num)
        new_page_rank = {}
        sum_page_rank = 0.0
        k = 0
        graph_size = len(self.all_urls)
        alpha_teleport = 0.3                  #teleportaion coef alpha
        page_rank_rel_diff = 0.0
        for url in self.all_urls:
            new_page = self.all_urls[url]
            in_pages = new_page.get_in_links()
            old_page_rank = new_page.get_page_rank()
            if len(new_page.out_links) == 0:    #loop (for working with hank links)
                new_url_page_rank = old_page_rank
            else:
                new_url_page_rank = 0.0
            for in_page in in_pages:
                new_url_page_rank += self.all_urls[in_page].get_page_rank_for_link(url)
            new_url_page_rank = (1-alpha_teleport)*new_url_page_rank + alpha_teleport * 1/float(graph_size) 
            page_rank_rel_diff += abs(new_url_page_rank - old_page_rank)/float(new_url_page_rank + old_page_rank)
            new_page_rank[url] = new_url_page_rank
        for url in new_page_rank:
            self.all_urls[url].update_page_rank(new_page_rank[url])
        page_rank_rel_diff = page_rank_rel_diff/graph_size
        if verbose:
            print "Page rank relative difference on iteration " + str(iter_num) + " is " + str(page_rank_rel_diff)
        return page_rank_rel_diff
        
    def calculate_page_rank(self, eps=1e-5, max_iters=10, top_size=30, verbose=0):
        self.initialize_page_rank()
        is_cycle_out = False
        for p_r_iter in range(0, max_iters):
            iter_error = self.calculate_iter_page_rank(p_r_iter, verbose)
            if abs(iter_error) < eps:
                is_cycle_out = True
                print "Iterations of Page Rank is stopped because there is no significant changes "
                break
        if not is_cycle_out and verbose:
             print "Iteration is stopped because maximum num of iterations"
        final_page_rank = map(lambda x: self.all_urls[x].get_page_rank(), self.all_urls.keys())
        all_pages = self.all_urls.keys()
        best_by_page_rank = [self.id_url_dict[x] for (y,x) in sorted(zip(final_page_rank,all_pages)) \
                             if x > 0][::-1][0:top_size]
        return best_by_page_rank
if __name__ == "__main__":                                   
    test_graph = WebGraph("graph.txt") 
    test_graph.check_is_graph_correct()
    best_p_r = test_graph.calculate_page_rank(max_iters=10, eps=1e-6, verbose=True)
    print best_p_r
    hits_res = test_graph.calculate_hits(max_iters=10, eps=0.03, verbose=1)
    print hits_res["best_by_auts"]
    print hits_res["best_by_habs"]
