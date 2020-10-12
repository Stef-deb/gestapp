#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from datetime import datetime
from kivy.uix.scrollview import ScrollView
from kivy.config import Config
import threading, subprocess, os, sys
from kivy.uix.filechooser import FileChooserIconView

# outclass
var = subprocess.check_output("pwd", shell=True)
var = var.decode("utf-8")
var = var.split("/")
var.pop()
var = "/".join(var)
var = var.replace(" ", "")
os.chdir(var)

Window.size = (1920, 1080)

data_storage = JsonStore("data_store.json")

# vars

version = None
file_path = None
check5 = False
check4 = False
check3 = False
check2 = False
check1 = False
check = False
now = None
customer_name = None
customer_numberz = len(data_storage)

# MainApp

class MainApp(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # background,toolbar
        self.title = Label(text = "Gestionale", font_size = 40, outline_color = (0,0,0,0), outline_width = 2, pos_hint = {"center_x":0.5, "center_y":0.966})
        self.background = Button(background_color = (1,1,1,1), background_normal = "", background_down = "")
        self.toolbar =  Button(background_color = (64/255, 121/255, 191/255, 1), background_normal = "", background_down = "", size_hint = (1, 0.07), pos_hint = {"center_x":0.5, "top":1})
        self.new_customer = Button(text = "nuovo cliente", pos_hint = {"center_x":0.93, "center_y":0.966}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", size_hint = (0.1, 0.06), on_press = self.alertus)
        self.new_customer.bind(size = self.resize)
        self.options = Button(text = "opzioni", background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", pos_hint = {"center_x":0.07, "center_y":0.966}, size_hint = (0.1, 0.06), on_press = self.add_options_liv)
        self.customer_number = Label(text = f"Numero di clienti : {customer_numberz}", font_size = 20, outline_color = (0,0,0,0), outline_width = 2, pos_hint = {"center_x":0.3, "center_y":0.866})
        self.search = TextInput(size_hint = (0.2, 0.05), pos_hint = {"center_x":0.7, "center_y":0.866}, multiline = False, on_text_validate = self.search_fn)
        self.search_text = Label(text = "Cerca",  font_size = 20, outline_color = (0,0,0,1), outline_width = 2, pos_hint = {"center_x":0.55, "center_y":0.866})
        self.all_button = Button(text = "Tutti", size_hint = (0.05, 0.05), background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", pos_hint = {"center_x":0.85, "center_y":0.866}, on_press = self.refresh)
        self.add_widget(self.background)
        self.add_widget(self.toolbar)
        self.add_widget(self.title)
        self.add_widget(self.new_customer)
        self.add_widget(self.options)
        self.add_widget(self.customer_number)
        self.add_widget(self.search)
        self.add_widget(self.search_text)
        self.add_widget(self.all_button)

        # customers navigation

        self.widgets()
        self.add_widget(self.root)

        # new customer

        self.alertliv = RelativeLayout()
        self.alertliv.add_widget(Button(background_color = (0,0,0,0.2), background_down = "", background_normal = "", on_press = self.alertus))
        self.alertliv.add_widget(Button(size_hint = (0.3, 0.3), background_down = "assets/Button_white.png", background_normal = "assets/Button_white.png", pos_hint = {"center_x":0.5, "center_y":0.5}))
        self.labellotxt = Label(text = "   Digita il nome\ndel nuovo cliente", outline_color = (0,0,0,1), outline_width = 2, font_size = 20, pos_hint = {"center_x":0.5, "center_y":0.61})
        self.labello = TextInput(size_hint = (0.2, 0.05), pos_hint = {"center_x":0.5, "center_y":0.52}, multiline = False)
        self.labello.bind(on_text_validate = self.save)
        self.ex = Button(text = "Salva", pos_hint = {"center_x":0.5, "center_y":0.42}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", font_size = 20, size_hint = (0.1, 0.1), on_press = self.save)
        self.alertliv.add_widget(self.labello)
        self.alertliv.add_widget(self.ex)
        self.alertliv.add_widget(self.labellotxt)

        # customer_view

        self.livello1 = RelativeLayout()
        self.title2 = Label(text = "Gestionale", font_size = 40, outline_color = (0,0,0,0), outline_width = 2, pos_hint = {"center_x":0.5, "center_y":0.966})
        self.background2 = Button(background_color = (1,1,1,1), background_normal = "", background_down = "")
        self.toolbar2 =  Button(background_color = (191/255, 83/255, 64/255, 1), background_normal = "", background_down = "", size_hint = (1, 0.07), pos_hint = {"center_x":0.5, "top":1})
        self.exit = Button(text = "Indietro", pos_hint = {"center_x":0.93, "center_y":0.966}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", size_hint = (0.1, 0.06), on_press = self.add_customer_view)
        self.edit = Button(text = "Elimina cliente", pos_hint = {"center_x":0.07, "center_y":0.966}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", size_hint = (0.1, 0.06), on_press = self.alert3)
        self.works = TextInput(multiline = False, pos_hint = {"center_x":0.5, "center_y":0.35}, size_hint = (0.9, 0.65), on_text_validate = self.validatee)
        self.customer_namez = Label(text = f"Cliente : {customer_name}", font_size = 24, outline_color = (0,0,0,0), outline_width = 2, pos_hint =  {"center_x":0.08, "center_y":0.83})
        self.customer_namez.bind(text = self.text_input_change)

        self.livello1.add_widget(self.background2)
        self.livello1.add_widget(self.toolbar2)
        self.livello1.add_widget(self.exit)
        self.livello1.add_widget(self.edit)
        self.livello1.add_widget(self.title2)
        self.livello1.add_widget(self.works)
        self.livello1.add_widget(self.customer_namez)
        
        # work details
        
        self.text_work = TextInput(size_hint = (0.1, 0.03), multiline = False, pos_hint = {"center_x":0.31, "center_y":0.83})
        self.text_work_imp = TextInput(size_hint = (0.1, 0.03), multiline = False, pos_hint = {"center_x":0.58, "center_y":0.83})
        self.text_work_date = TextInput(size_hint = (0.1, 0.03), multiline = False, pos_hint = {"center_x":0.86, "center_y":0.83})
        self.text_work_details = TextInput(size_hint = (0.5, 0.03), multiline = False, pos_hint = {"center_x":0.5, "center_y":0.73})
        self.text_worK_text = Label(text = "Lavoro", font_size = 24, outline_color = (0,0,0,0), outline_width = 2, pos_hint = {"center_x":0.22, "center_y":0.83})
        self.text_worK_text_imp = Label(text = "Importo", font_size = 24, outline_color = (0,0,0,0), outline_width = 2, pos_hint = {"center_x":0.49, "center_y":0.83})
        self.text_worK_text_date = Label(text = "Data", font_size = 24, outline_color = (0,0,0,0), outline_width = 2, pos_hint = {"center_x":0.77, "center_y":0.83})
        self.text_worK_text_details = Label(text = "Dettagli", font_size = 24, outline_color = (0,0,0,0), outline_width = 2, pos_hint = {"center_x":0.21, "center_y":0.73})
        
        self.livello1.add_widget(self.text_work)
        self.livello1.add_widget(self.text_work_imp)
        self.livello1.add_widget(self.text_work_date)
        self.livello1.add_widget(self.text_worK_text)
        self.livello1.add_widget(self.text_work_details)
        self.livello1.add_widget(self.text_worK_text_imp)
        self.livello1.add_widget(self.text_worK_text_date)
        self.livello1.add_widget(self.text_worK_text_details)

        # work details save

        self.work_save = Button(text = "Salva", pos_hint =  {"center_x":0.08, "center_y":0.73}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", size_hint = (0.1, 0.06), on_press = self.save_work)
        self.livello1.add_widget(self.work_save)

        #generate file.txt with customer details

        self.work_file = Button(text = "Crea file.txt", pos_hint =  {"center_x":0.92, "center_y":0.73}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", size_hint = (0.1, 0.06), on_press = self.add_filechos)
        self.livello1.add_widget(self.work_file)

        # delete alert

        self.alertliv3 = RelativeLayout()
        self.alertliv3.add_widget(Button(background_color = (0,0,0,0.2), background_down = "", background_normal = ""))
        self.alertliv3.add_widget(Button(size_hint = (0.3, 0.3), background_down = "assets/Button_white.png", background_normal = "assets/Button_white.png", pos_hint = {"center_x":0.5, "center_y":0.5}))
        self.labello3 = Label(text = "Vuoi davvero eliminare\n il cliente e i relativi dati?", outline_color = (0,0,0,1), outline_width = 2, font_size = 20, pos_hint = {"center_x":0.5, "center_y":0.58})
        self.ex3 = Button(text = "Si", pos_hint = {"center_x":0.43, "center_y":0.42}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", font_size = 20, size_hint = (0.1, 0.1), on_press = self.deletez)
        self.ex3_1 = Button(text = "No", pos_hint = {"center_x":0.57, "center_y":0.42}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", font_size = 20, size_hint = (0.1, 0.1), on_press = self.alert3)
        self.alertliv3.add_widget(self.labello3)
        self.alertliv3.add_widget(self.ex3)
        self.alertliv3.add_widget(self.ex3_1)
        
        #general alert

        self.alertliv4 = RelativeLayout()
        self.alertliv4.add_widget(Button(background_color = (0,0,0,0.2), background_down = "", background_normal = "", on_press = self.add_generical_alert))
        self.alertliv4.add_widget(Button(size_hint = (0.3, 0.3), background_down = "assets/Button_white.png", background_normal = "assets/Button_white.png", pos_hint = {"center_x":0.5, "center_y":0.5}, on_press = self.add_generical_alert))
        self.labello4 = Label(text = "", outline_color = (0,0,0,1), outline_width = 2, font_size = 20, pos_hint = {"center_x":0.5, "center_y":0.58})
        self.ex4 = Button(text = "Ok", pos_hint = {"center_x":0.5, "center_y":0.42}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", font_size = 20, size_hint = (0.1, 0.1), on_press = self.add_generical_alert)
        self.alertliv4.add_widget(self.labello4)
        self.alertliv4.add_widget(self.ex4)

        #delete_all_customers extension

        self.yep = Button(text = "Si", pos_hint = {"center_x":0.42, "center_y":0.42}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", font_size = 20, size_hint = (0.1, 0.1), on_press = self.delete_all_customers_fn)
        self.nope = Button(text = "No", pos_hint = {"center_x":0.58, "center_y":0.42}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", font_size = 20, size_hint = (0.1, 0.1), on_press = self.add_generical_alert)

        #filechooser to get the path
        
        self.file_livl = RelativeLayout()
        self.title3 = Label(text = "Gestionale", font_size = 40, outline_color = (0,0,0,0), outline_width = 2, pos_hint = {"center_x":0.5, "center_y":0.966})
        self.backr = Button(background_color = (64/255, 121/255, 191/255, 1), background_normal = "", background_down = "", pos_hint = {"center_x":0.5, "center_y":0.5})
        self.toolbar3 =  Button(background_color = (191/255, 83/255, 64/255, 1), background_normal = "", background_down = "", size_hint = (1, 0.07), pos_hint = {"center_x":0.5, "top":1})
        self.filechos = FileChooserIconView(pos_hint = {"center_x":0.5, "center_y":0.4})
        self.exit_fl = Button(text = "Indietro", pos_hint = {"center_x":0.93, "center_y":0.966}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", size_hint = (0.1, 0.06), on_press = self.add_filechos)
        self.get_file_b = Button(text = "Genera file", pos_hint = {"center_x":0.5, "center_y":0.1}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", size_hint = (0.1, 0.06), on_press = self.get_file)
       

        self.file_livl.add_widget(self.backr)
        self.file_livl.add_widget(self.toolbar3)
        self.file_livl.add_widget(self.title3)
        self.file_livl.add_widget(self.exit_fl)
        self.file_livl.add_widget(self.filechos)
        self.file_livl.add_widget(self.get_file_b)

        #options label

        self.alertliv5 = RelativeLayout()
        self.alertliv5.add_widget(Button(background_color = (0,0,0,0.2), background_down = "", background_normal = "", on_press = self.add_options_liv))
        self.alertliv5.add_widget(Button(size_hint = (0.3, 0.3), background_down = "assets/Button_white.png", background_normal = "assets/Button_white.png", pos_hint = {"center_x":0.5, "center_y":0.5}, on_press = self.add_options_liv))
        self.alertliv5.add_widget(Label(text = "Opzioni", outline_color = (0,0,0,1), outline_width = 2, font_size = 20, pos_hint = {"center_x":0.5, "center_y":0.6}))
        self.alertliv5.add_widget(Button(text = "Elimina clienti", pos_hint = {"center_x":0.5, "center_y":0.52}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", size_hint = (0.1, 0.06), on_press = self.delete_all_customers))
        self.alertliv5.add_widget(Button(text = "Aggiorna app", pos_hint = {"center_x":0.5, "center_y":0.42}, background_down = "assets/Button_orange_2.png", background_normal = "assets/Button_orange_2.png", size_hint = (0.1, 0.06), on_press = self.update))
    
    # functions

    def text_input_change(self, *args):
        self.works.text = data_storage.get(customer_name)["data"]

    def resize(self, *args):
        if Window.size[0] < 955:
            self.new_customer.text = "nuovo\ncliente"
            self.edit.text = "Elimina\ncliente"                    # adapt button test in function of window size
        else:
            self.new_customer.text = "nuovo cliente"
            self.edit.text = "Elimina cliente"

    def alertus(self, *args):
        global check
        if check == False:
            self.add_widget(self.alertliv)
            check = True                                  # add or remove the layout with "new_customer"
        else:
            self.remove_widget(self.alertliv)
            check = False

    def refresh(self, *args):
        self.layout.clear_widgets()
        self.widgets()
        self.remove_widget(self.root)           # refresh scrollview (removes and adds it)
        self.add_widget(self.root)

    def search_fn(self, *args):
        self.layout.clear_widgets()
        self.widgets2()
        self.remove_widget(self.root)           # refresh scrollview (removes and adds it)
        self.add_widget(self.root)
        self.search.text = ""

    def save(self, *args):
        global data_storage
        if len(self.labello.text) == 0:
            self.add_generical_alert("Non puoi aggiungere un\n   cliente senza nome!")
        else:
            if not self.labello.text in data_storage:
                data_storage.put(self.labello.text, data = "")
                self.alertus()
                self.labello.text = ""                   # creates new customer and refreshes scrollview
                self.refresh()
                self.cus_num()
            else:
                self.add_generical_alert("    Il cliente che cerchi\ndi aggiungere esiste già!")

    def solution(self, *args):
            global customer_name
            var = customer_name
            while True:
                if var != customer_name:
                    self.customer_namez.text = f"Cliente : {customer_name}"
                    break
                else:
                    continue

    def add_customer_view(self, *args):
        global check1
        if check1 == False:
            self.add_widget(self.livello1)
            p = threading.Thread(target = self.solution)
            p.start()
            check1 = True                                         # adds layout with customer datas and options
        else:
            self.remove_widget(self.livello1)
            check1 = False

    def widgets(self, *args):
        global customer_name
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.root = ScrollView(size_hint=(0.77, 0.7), pos_hint = {"center_x":0.5, "center_y":0.42})
        self.layout.bind(minimum_height=self.layout.setter('height'))
        var =[]
        for i in data_storage:
            var.append(i)
        var = sorted(var)                                                                           # creates scrollview with customers
        for i in var:
            def press(self, *args):
                global customer_name
                customer_name = self.text
            self.layout.bind(minimum_height=self.layout.setter('height'))
            self.sol = RelativeLayout(size_hint_y=None, height=30)
            self.btn = Button(text = i, size_hint_y=None, height=30, background_down = "assets/Button_sky_4.png", background_normal = "assets/Button_sky_4.png", on_press = press)
            self.btn_text = Label(text = i, outline_color = (0,0,0,0), outline_width = 2)
            self.sol.add_widget(self.btn)
            self.sol.add_widget(self.btn_text)
            self.layout.add_widget(self.sol)
            self.btn.bind(on_press = self.add_customer_view)
        self.root.add_widget(self.layout)

    def widgets2(self, *args):
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.root = ScrollView(size_hint=(0.77, 0.7), pos_hint = {"center_x":0.5, "center_y":0.42})
        self.layout.bind(minimum_height=self.layout.setter('height'))
        var =[]
        for i in data_storage:
            if self.search.text in i:
                var.append(i)
        var = sorted(var)                                                                           # creates scrollview with customers
        for i in var:
            def press(self, *args):
                global customer_name
                customer_name = self.text
            self.layout.bind(minimum_height=self.layout.setter('height'))
            self.sol = RelativeLayout(size_hint_y=None, height=30)
            self.btn = Button(text = i, size_hint_y=None, height=30, background_down = "assets/Button_sky_4.png", background_normal = "assets/Button_sky_4.png", on_press = press)
            self.btn_text = Label(text = i, outline_color = (0,0,0,0), outline_width = 2)
            self.sol.add_widget(self.btn)
            self.sol.add_widget(self.btn_text)
            self.layout.add_widget(self.sol)
            self.btn.bind(on_press = self.add_customer_view)
        self.root.add_widget(self.layout)

    def alert3(self, *args):
        global check2
        if check2 == False:
            self.add_widget(self.alertliv3)
            check2 = True                            # adds a layout with "do you want really delete this customer?"
        else:
            self.remove_widget(self.alertliv3)
            check2 = False

    def deletez(self, *args):
        global customer_name
        data_storage.delete(customer_name)
        self.refresh()                             # function that deletes customer
        self.alert3()
        self.add_customer_view()
        self.cus_num()

    def cus_num(self, *args):
        global customer_numberz
        customer_numberz = len(data_storage)
        self.customer_number.text = f"Numero di clienti : {customer_numberz}"

    def save_work(self, *args):
        if self.works.text.endswith("\n") or len(self.works.text) == 0:
            self.works.text = self.works.text + self.text_work_date.text + " - " + self.text_work.text + " - " + self.text_work_imp.text + " - " + self.text_work_details.text + "\n"
        else:
            self.works.text = self.works.text + "\n" + self.text_work_date.text + " - " + self.text_work.text + " - " + self.text_work_imp.text + " - " + self.text_work_details.text + "\n"
        data_storage.put(customer_name, data = self.works.text)
        self.text_work.text = ""
        self.text_work_imp.text = ""
        self.text_work_date.text = ""
        self.text_work_details.text = ""

    def validatee(self, *args):
        data_storage.put(customer_name, data = self.works.text)        
        
    def get_file(self, *args):
        global customer_name, file_path
        file_path = self.filechos.path
        file = open(f"{file_path}/{customer_name}.txt", "w")
        file.write(self.works.text)
        file.close()
        self.add_customer_view()
        self.add_filechos()
        self.add_generical_alert(f"file creato nella\ndirectory {file_path}")

    def add_generical_alert(self, txt):
        global check3
        if check3 == False:
            self.labello4.text = txt
            self.add_widget(self.alertliv4)
            check3 = True
        else:
            self.remove_widget(self.alertliv4)
            check3 = False
            try:
                self.alertliv4.add_widget(self.ex4)
                self.alertliv4.remove_widget(self.yep)
                self.alertliv4.remove_widget(self.nope)
            except:
                pass
    
    def add_filechos(self, *args):
        global check4
        if check4 == False:
            self.add_widget(self.file_livl)
            check4 = True
        else:
            self.remove_widget(self.file_livl)
            check4 = False

    def add_options_liv(self, *args):
        global check5
        if check5 == False:
            self.add_widget(self.alertliv5)
            check5 = True
        else:
            self.remove_widget(self.alertliv5)
            check5 = False

    def delete_all_customers(self, *args):
        self.add_options_liv()
        self.alertliv4.remove_widget(self.ex4)
        self.add_generical_alert("Vuoi veramente eliminare\n            tutti i clienti?")
        self.alertliv4.add_widget(self.yep)
        self.alertliv4.add_widget(self.nope)

    def delete_all_customers_fn(self, *args):
        data_storage
        for x in data_storage:
            data_storage.delete(x)
        self.refresh()
        self.add_generical_alert("")
    
    def update(self, *args):
        global version
        try:
            self.add_options_liv()
            filee = open("version.txt", "r")
            file1 = filee.read()
            filee.close()
            file1 = file1.replace("\n", "")
            version = float(file1)
            os.system("rm -rf version.txt")
            os.system("git clone https://github.com/Stef-deb/Version")
            os.system("mv Version/version.txt version.txt")
            os.system("rm -rf Version")
            filez = open("version.txt", "r")
            filez1 = filez.read()
            filez.close()
            file1 = filez1.replace("\n", "")
            final_version = float(filez1)
            if final_version > version:
                subprocess.Popen("./update.py")
                sys.exit()
            else:
                self.add_generical_alert(f"L'app è alla versione\npiù aggiornata! {final_version}")
        except Exception as e:
            self.add_generical_alert(e)

class MyGest(App):
    def build(self):
        return MainApp()

MyGest().run()
