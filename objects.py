try:
       import cPickle as pickle
except:
       import pickle

from datetime import date
import os

class Ticket:

    def __init__(self,name,jiraurl,repo,pr_url,branch_url,comments):
        self.create_date = date.today()
        self.name = name
        self.jiraurl = jiraurl
        self.repo = repo
        self.pr_url = pr_url
        self.branch_url = branch_url
        self.comments = comments
        self.finish_date = ''


class Disk:

    path=os.path.expanduser('~/env/tickets.txt')

    def __init__(self):
        if not os.path.exists(self.path):
            with open(self.path, 'w'): pass

    def save_to_disk(self,ticket_list):
        file = open(self.path,mode='w+b')
        for item in ticket_list:
            pickle.dump(item, file)
        file.close()

    def load_from_disk(self):
        ticket_list =[] 
        file = open(self.path,'rb')
        while True:
            try:
                ticket:Ticket= pickle.load(file)
                ticket_list.append(ticket)
            except EOFError:
                return ticket_list
        file.close()
