from PyQt5 import QtWidgets,QtGui
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox)

from objects import Ticket
from objects import Disk
from datetime import date
import pyperclip

from ui.ticketui import Ui_MainWindow  # importing our generated file




class mywindow(QtWidgets.QMainWindow):

    repos = {}
    ticket_list = []
    new_ticket = False

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.disk = Disk()
        
        #init components
        self.init_components()
        self.ui.setupUi(self)
        self.load_combobox()
        self.load_from_disk()
        self.init_search_box()
        
        #listeners
        self.ui.delete_button.clicked.connect(self.delete_button_action)
        self.ui.save_button.clicked.connect(self.save_button_action)
        self.ui.new_button.clicked.connect(self.new_button_action)
        self.ui.load_active.clicked.connect(self.load_active_button_action)
        self.ui.load_all.clicked.connect(self.load_all_button_action)
        self.ui.checkBox.stateChanged.connect(self.checkbox_action)
        self.ui.comborepo.currentIndexChanged.connect(self.combobox_action)
        self.ui.copy_selected_button.clicked.connect(self.copy_selected_button_action)
        self.ui.search_button.clicked.connect(self.search_button_action)
        self.ui.textsearch.returnPressed.connect(self.search_button_action)

        #copy
        self.ui.copy_name.clicked.connect(lambda: self.copy_button_action('name'))
        self.ui.copy_jira.clicked.connect(lambda: self.copy_button_action('jira'))
        self.ui.copy_repo.clicked.connect(lambda: self.copy_button_action('repo'))
        self.ui.copy_pr.clicked.connect(lambda: self.copy_button_action('pr'))
        self.ui.copy_branch.clicked.connect(lambda: self.copy_button_action('branch'))


    def combobox_action(self):
        print("combobox_action")
        self.ui.textrepo.clear()
        combo_current_text = self.ui.comborepo.currentText()
        text_to_set = self.repos[combo_current_text]
        self.ui.textrepo.insertPlainText(text_to_set)

    def init_components(self):
        print("init_components")
        self.repos['nothing'] = 'nothing selected'
        self.repos['exchange'] = 'https://github.com/AdaptiveConsulting/exchange'
        self.repos['web-api'] = 'https://github.com/ErisExchange/trading-web-api'
        self.repos['wlashTrader'] = 'https://github.com/ErisExchange/tradingWebApiClient'

    def closeEvent(self, event):
        print("closeEvent")
        self.save_button_action()
        event.accept()

    def init_search_box(self):
        print("init_search_box")
        for ticket in self.ticket_list:
            self.ui.listresult.addItem(ticket.name)
        self.ui.listresult.itemClicked.connect(self.on_ticket_clicked)

    def on_ticket_clicked(self,ticket):
        print("on_ticket_clicked")
        self.save_button_action()
        searched_ticket = self.search_ticket(ticket.text())
        self.display_ticket(searched_ticket)

    def load_combobox(self):
        print("load_combobox")
        self.ui.comborepo.addItem("nothing")
        self.ui.comborepo.addItem("exchange")
        self.ui.comborepo.addItem("web-api")
        self.ui.comborepo.addItem("wlashTrader")
        #TODO select the correct combo
        #self.ui.comborepo.setCurrentIndex(0)
        #self.ui.textrepo.insertPlainText(self.repos['exchange'])

    def grab_from_view(self):
        print("grab_from_view")
        text_name = self.ui.textname.toPlainText()
        text_jira_url = self.ui.textjiraurl.toPlainText()
        text_repo = self.ui.textrepo.toPlainText()
        text_pr_url = self.ui.textpr.toPlainText()
        text_branch_url = self.ui.textbranch.toPlainText()
        text_description = self.ui.commenttext.toPlainText()
        ticket = Ticket(text_name, text_jira_url, text_repo, text_pr_url, text_branch_url, text_description)
        if self.ui.checkBox.isChecked():
            ticket.finish_date = date.today()
        return ticket

    def search_ticket(self,ticket_name):
        print("search_ticket")
        for ticket in self.ticket_list: 
            if ticket.name == ticket_name:
                return ticket
        return None

    def display_ticket(self,ticket):
        print("display_ticket")
        self.clear_all_form()
        self.ui.textname.insertPlainText(ticket.name)
        self.ui.textjiraurl.insertPlainText(ticket.jiraurl)
        self.ui.textrepo.insertPlainText(ticket.repo)
        self.ui.textpr.insertPlainText(ticket.pr_url)
        self.ui.textbranch.insertPlainText(ticket.branch_url)
        self.ui.commenttext.setPlainText(ticket.comments)
        self.display_check_box(ticket)


    def  copy_button_action(self,field):
        print("copy_button_action")
        ticket = self.grab_from_view()
        if field == 'repo':
            pyperclip.copy(ticket.repo.strip())
        if field == 'jira':
            pyperclip.copy(ticket.jiraurl.strip())
        if field == 'pr':
            pyperclip.copy(ticket.pr_url.strip())
        if field == 'branch':
            pyperclip.copy(ticket.branch_url.strip())
        if field == 'name':
            pyperclip.copy(ticket.name.strip())

    def update_ticket(self,new_ticket):
        print("update_ticket")
        cont =0
        for ticket_in_list in self.ticket_list:
            if ticket_in_list.name == new_ticket.name:
                break
            cont = cont + 1
        self.ticket_list.pop(cont)
        self.ticket_list.append(new_ticket)

    def clear_selection(self):
        print("clear_selection")
        self.ui.listresult.clearSelection()

    def delete_button_action(self):
        print("delete_button_action")
        ticket_to_delete = self.grab_from_view()
        if ticket_to_delete.name == "":
            print("ticket is blank")
            return
        index =0
        self.clear_all_form()
        for ticket in self.ticket_list:
            if ticket.name == ticket_to_delete.name:
                print('i was here')
                break
            index = index +1
        self.ticket_list.pop(index)
        self.removeSel()
        self.clear_selection()


    def removeSel(self):
        print("removeSel")
        listItems = self.ui.listresult.selectedItems()
        if not listItems: return
        for item in listItems:
            self.ui.listresult.takeItem(self.ui.listresult.row(item))

    def save_button_action(self):
        print("save_button_action")
        ticket = self.grab_from_view()
        ticket_searched = self.search_ticket(ticket.name)
        if ticket_searched == None:
            print('adding new')
            if ticket.name == "":
                print("cancel update")
            else:
                self.ticket_list.append(ticket)
                self.ui.listresult.addItem(ticket.name)
        else:
            print('updating')
            self.update_ticket(ticket)
        self.disk.save_to_disk(self.ticket_list)



    def clear_all_form(self):
        print("clear_all_form")
        self.ui.textname.clear()
        self.ui.textjiraurl.clear()
        self.ui.textrepo.clear()
        self.ui.textpr.clear()
        self.ui.textbranch.clear()
        self.ui.commenttext.clear()

    def new_button_action(self):
        print("new_button_action")
        self.new_ticket = True
        self.clear_all_form()

    def load_all_button_action(self):
        print("load_all_button_action")
        self.ui.listresult.clear()
        for ticket in self.ticket_list:
            self.ui.listresult.addItem(ticket.name)

    def copy_selected_button_action(self):
        print("copy_selected_button_action")
        cursor = self.ui.commenttext.textCursor()
        plainText = self.ui.commenttext.toPlainText()
        pyperclip.copy(str(plainText[cursor.selectionStart():cursor.selectionEnd()]))

    def search_button_action(self):
        print("search_button_action")
        srch_txt = self.ui.textsearch.text();
        if srch_txt:
            self.search_in_tickets(srch_txt)

    def search_in_tickets(self,word):
        print("search_in_tickets")
        self.ticket_list
        newTicketList = list(filter(lambda x : self.search_filter(x,word)  ,self.ticket_list))
        if newTicketList:
            self.ui.listresult.clear()
            for ticket in newTicketList:
                self.ui.listresult.addItem(ticket.name)
            self.ui.textsearch.clear()


    def search_filter(self,ticket,word):
        print("search_filter")
        whole_text = ticket.name+ ticket.comments
        try:
            whole_text .index(word)
            return True
        except:
            return False

    def load_active_button_action(self):
        print("load_active_button_action")
        self.ui.listresult.clear()
        newTicketList = list(filter(lambda x :  x.finish_date == None ,self.ticket_list))
        for ticket in newTicketList:
            self.ui.listresult.addItem(ticket.name)

    def load_button_action(self):
        print("load_button_action")
        selected_item = self.ui.listresult.currentItem().text()
        print(selected_item)
        selected_ticket = self.search_ticket(selected_item)
        self.display_ticket(selected_ticket)
        print(self.print_ticket(selected_ticket))
        self.display_check_box(selected_ticket)

    def display_check_box(self,ticket):
        print("display_check_box")
        if ticket.finish_date is None:
            self.ui.checkBox.setChecked(False)
        else:
            self.ui.checkBox.setChecked(True)

    def checkbox_action(self):
        print("checkbox_action")
        if self.ui.checkBox.isChecked():
            print("CHECKED!")
            ticket = self.search_ticket(self.grab_from_view().name)
            ticket.finish_date = date.today()
            print("ticket name: "+ticket.name)
            self.update_ticket(ticket)
        else:
            print("UNCHECKED!")
            ticket = self.search_ticket(self.grab_from_view().name)
            ticket.finish_date = None
            self.update_ticket(ticket)

    #test utility
    def create_a_ticket(self):
        print("create_a_ticket")
        text_name = 'a name'
        text_jira_url = 'a jira url'
        text_repo = 'a repo url'
        text_pr_url = 'a pr url'
        text_branch_url ='a branch url'
        text_description = 'a description'
        ticket = Ticket(text_name, text_jira_url, text_repo, text_pr_url, text_branch_url, text_description)
        self.display_ticket(ticket)
        self.ticket_list.append(ticket)

    def print_ticket_list(self):
        print("print_ticket_list")
        for ticket in self.ticket_list:
            print("***********************")
            self.print_ticket(self) 
           
    def save_to_file(self):
        print("save_to_file")
        self.disk.save_to_disk(self.ticket_list)

    def load_from_disk(self):
       print("load_from_disk")
       self.ticket_list = self.disk.load_from_disk()

    def print_ticket(self,ticket):
        print("print_ticket")
        print(ticket.name)
        print(ticket.jiraurl)
        print(ticket.repo)
        print(ticket.pr_url)
        print(ticket.branch_url)
        print(ticket.comments)
        print(ticket.create_date)

        

app = QtWidgets.QApplication([])

application = mywindow()

application.show()

sys.exit(app.exec())
