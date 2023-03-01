# importing all necessary modules
# like MDApp, MDLabel Screen, MDTextField
# and MDRectangleFlatButton
from kivy.config import Config
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextFieldRect, MDTextField
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock

import threading
import time
import sys

sys.path.append("..")

from backend.db import db
from backend.FileGenerator import Generator
from backend.tcp import tcp

#Window.maximize()
#Config.set('kivy', 'window_icon', '.\\imagens\\icone.ico')

# creating Provisorio Class(base class)
class Provisorio(MDApp):
    def build(self):
        self.icon = '.\\imagens\\icone.ico'
        self.screen = Screen()
        self.Generator = Generator.Gen()
        self.db = db.db()
        self.ip, self.port = self.db.get_ip()

        
        #Criando TextField da String que vai chegar do clp
        self.CLPStringLabel = MDLabel(
            text = "String recebida do CLP",
            pos_hint = {"center_x":0.9,"center_y":0.9}
        )

        self.CLPStringTF = MDTextFieldRect(
            size_hint = (0.75, 0.05),
            pos_hint = {"center_x":0.5,"center_y":0.95},
            disabled_foreground_color = [0, 0, 1, 1],
            halign = "center",
            background_color=[1,1,1,1], 
            disabled = True
        )
        self.screen.add_widget(self.CLPStringLabel)
        self.screen.add_widget(self.CLPStringTF)

        self.IPlbl = MDLabel(
            text = "IP:",
            halign = "center",
            pos_hint = {"center_x":0.04,"center_y":0.8}
        )

        self.IPtf = MDTextFieldRect(
            text = self.ip,
            size_hint = (0.2,0.05),
            pos_hint = {"center_x":0.151,"center_y":0.8}
        )

        self.portlbl = MDLabel(
            text = "Porta:",
            halign = "center",
            pos_hint = {"center_x":0.3,"center_y":0.8}
        )

        self.porttf = MDTextFieldRect(
            text = str(self.port),
            size_hint = (0.1,0.05),
            pos_hint = {"center_x":0.38,"center_y":0.8}
        )

        self.screen.add_widget(self.IPlbl)
        self.screen.add_widget(self.IPtf)
        self.screen.add_widget(self.portlbl)
        self.screen.add_widget(self.porttf)

        self.SuccessCard = []
        self.substring = []
        self.inicio = []
        self.fim = []
        self.check = []

        for i in range(5):
            self.SuccessCard.append(
                MDCard(
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    style="outlined",
                    md_bg_color= "#FDFDFD",
                    #shadow_softness=12,
                    #shadow_offset=(0, 2),
                    size_hint = (None,None),
                    size = (150,180),
                    pos_hint = {"center_x":0.1 + i*0.2,"center_y":0.58},
                )
            )

            flayout = FloatLayout()

            self.build_template(flayout,i)

            self.SuccessCard[i].add_widget(flayout)
            self.screen.add_widget(self.SuccessCard[i])
        
        for i in range(5,10):
            self.SuccessCard.append(MDCard(
                line_color=(0.2, 0.2, 0.2, 0.8),
                style="outlined",
                md_bg_color= "#FDFDFD",
                #shadow_softness=12,
                #shadow_offset=(0, 2),
                size_hint = (None,None),
                size = (150,170),
                pos_hint = {"center_x":0.1 + (i-5)*0.2,"center_y":0.25} 
            ))

            flayout = FloatLayout()

            self.build_template(flayout,i)

            self.SuccessCard[i].add_widget(flayout)
            self.screen.add_widget(self.SuccessCard[i])

        self.Save = MDRectangleFlatButton(
            text = "Salvar Alterações",
            pos_hint = {"center_x":0.5 ,"center_y":0.05},
            on_press =  self.updateprocess
        )

        self.screen.add_widget(self.Save)

        self.PasswordCard = MDCard(
            line_color=(0, 0, 1, 0.8),
            style="outlined",
            md_bg_color= "#FFFFFF",
            #shadow_softness=12,
            #shadow_offset=(0, 2),
            size_hint = (None,None),
            size = (200,80),
            pos_hint = {"center_x":0.5,"center_y":0.5} 
        )

        self.PasswordCardLabel = MDLabel(
            text = "Alterações aplicadas",
            halign = "center",
            valign = "center",
            theme_text_color="Custom",
            text_color = [0,0,1,0.5]
        )
        self.PasswordCard.add_widget(self.PasswordCardLabel)
    
        self.ConnectionIcon = MDIconButton(
            icon="connection",
            halign = "center",
            disabled = True,
            pos_hint={"center_x": 0.5, "center_y": 0.8},
        )
        
        threading.Thread(target = self.systemFlow,daemon = True).start()

        self.init_recipes()

        self.tab_order = []
        [self.tab_order.append(item) for pair in zip(self.inicio, self.fim) for item in pair]
        for i in self.tab_order:
            print(i.text)
            i.bind(on_text_validate=self.on_text_validate)

        # returning the screen
        return self.screen

    def on_text_validate(self, instance):
        print('on_text_validate')
        if instance.focus:
            instance.focus = False
            next = instance.get_focus_next()
            if next:
                next.focus = True

    def build_template(self,flayout,i):
        self.substring.append(
            MDTextFieldRect(
                disabled = True,
                height = 30,
                size_hint = (0.8,None),
                halign = 'center',
                disabled_foreground_color= (.20,.30,1,1),
                pos_hint = {"center_x":0.5,"center_y":0.75},
        ))

        self.inicio.append(
            MDTextFieldRect(
                height = 30,
                size_hint = (0.4,None),
                halign = 'center',
                foreground_color= (.20,.30,1,1),
                pos_hint = {"center_x":0.7,"center_y":0.55},
            ))
        
        self.fim.append(
            MDTextFieldRect(
                height = 30,
                size_hint = (0.4,None),
                halign = 'center',
                foreground_color= (.20,.30,1,1),
                pos_hint = {"center_x":0.7,"center_y":0.3},
            ))

        self.check.append(
            CheckBox(
                active = False,
                size_hint = (None,None),
                size = (20,20),
                color = [0,0,1,1],
                pos_hint = {"center_x":0.15,"center_y":0.1}
            ))

        flayout.add_widget(self.substring[i])

        flayout.add_widget(self.inicio[i])

        flayout.add_widget(self.fim[i])

        flayout.add_widget(self.check[i])

        flayout.add_widget(
            MDLabel(
                text  = "Início",
                pos_hint = {"center_x":0.6,"center_y":0.55}
        ))

        flayout.add_widget(
            MDLabel(
                text  = "Fim",
                pos_hint = {"center_x":0.61,"center_y":0.3}
        ))

        flayout.add_widget(
            MDLabel(
                text  = "habilitado",
                pos_hint = {"center_x":0.72,"center_y":0.1}
        ))
        flayout.add_widget(
            MDLabel(
                text = f'Receita{i+1}',
                theme_text_color="Custom",
                text_color= (.2,.2,.25,1),
                pos_hint = {"center_x":0.52,"center_y":1.05}
            )
        )
    
    def init_recipes(self):
        try:
            recipes_from_db = self.db.get_all_config()
        except Exception as e:
            print(e)
            self.erro_popup("Erro","Falha ao carregar receitas do banco de dados")
            return
        
        print('recipes from db',recipes_from_db)
    
        for i in recipes_from_db:
            self.inicio[i[2]].text = str(i[0])
            self.fim[i[2]].text = str(i[1])
            self.check[i[2]].active = True

    def erro_popup(self,Ttitle,message):
        layout = GridLayout(cols = 1, padding = 10)
        # Cria um MDLabel para exibir a mensagem
        label = MDLabel(
            text=message,
            bold = True,
            theme_text_color="Custom",
            text_color= (.14,.37,.60,1),
            halign = "center"
        )

        # Cria o Popup com o MDLabel
        self.popup = Popup(
            title = Ttitle,
            title_color = (.14,.37,.60,1),
            title_align = "center",
            content = layout,
            size_hint =(None, None),
            size =(200, 200))
        
        closeButton = MDRectangleFlatButton(text = "Fechar",
        pos_hint = {"center_x":0.5,"center_y":0.5},
        size_hint=  (1, None),
        on_press = self.popup.dismiss)
        
        layout.add_widget(label)
        layout.add_widget(closeButton)

        self.popup.open()  

    def updateprocess(self,btn):
        recipes = self.get_all_recipes()
        # Cria um MDTextField para receber a senha do usuário
        textfield = MDTextField(
            hint_text="Digite a senha",
            password=True
        )
        self.change_button = MDFlatButton(
            text="Alterar Senha",
            pos_hint = {"center_x":0},
            on_release=self.Update_Password    
        )

        # Cria um botão para confirmar a entrada da senha
        self.confirm_button = MDFlatButton(text="Confirmar",on_release=lambda btn: self.check_password(btn,textfield.text))

        self.cancel_button = MDFlatButton(text="Cancelar",on_release=self.PasswordPoppuDimiss)

        # Cria o Popup com o MDTextField e o botão
        self.dialog = MDDialog(
            title="Senha",
            type="custom",
            content_cls=textfield,
            buttons=[
                self.change_button,
                self.confirm_button,
                self.cancel_button
            ]
        )
        
        # Abre o Popup
        self.dialog.open()
        textfield.focus = True

    def get_all_recipes(self):
        recipes = []
        for i in range(10):
            if(self.check[i].active):
                try:
                    recipes.append((int(self.inicio[i].text),int(self.fim[i].text),i))
                except:
                    return []
        return recipes
        
    def insert_recipes(self):
        recipes = self.get_all_recipes()

        for i in recipes:
            try:
                self.db.insert_config(i[0],i[1],i[2])
            except:
                return False
        return True

    def check_password(self,btn,password):
        if(self.db.check_password(password)):
            Clock.schedule_once(lambda dt: self.PopPasswordCard(),0)
            Clock.schedule_once(lambda dt: self.PopPasswordCardDismiss(),1)
            self.dialog.dismiss()
            
            self.db.delete_all_config()
            self.insert_recipes()
        else:
            self.erro_popup('Credenciais Incorretas','Senha Incorreta')

    def PasswordPoppuDimiss(self,btn):
        self.dialog.dismiss()

    def PopPasswordCard(self,*args):
        self.screen.add_widget(self.PasswordCard)

    def PopPasswordCardDismiss(self,*args):
        self.screen.remove_widget(self.PasswordCard)

    def Update_Password(self, *args):
        self.password = MDTextField(
            hint_text="Digite a senha",
            password=True,
            required=True,
        )
        self.new_password_field = MDTextField(
            hint_text="Digite a nova senha",
            password=True,
            required=True,
        )
        self.repeat_password_field = MDTextField(
            hint_text="Repita a nova senha",
            password=True,
            required=True,
        )

        self.dialog_pupdate = MDDialog(
            title="Alterar Senha",
            type="custom",
            content_cls=self.dialog_content(),
            auto_dismiss=False,
            buttons=[
                MDFlatButton(
                    text="Confirmar",
                    on_release=self.check_uPassword
                ),
                MDFlatButton(
                    text="Cancelar",
                    on_release=self.close_uPassword
                ),
            ],
            size_hint=(0.7, 0.1)  # Define o tamanho do dialog
        )
        self.dialog_pupdate.open()

    def check_uPassword(self,btn):
        password = self.password.text
        new_password = self.new_password_field.text
        repeat_password = self.repeat_password_field.text

        if(password == '' or new_password == '' or repeat_password == ''):
            self.erro_popup("Erro","Preencha Todos os Campos")
            return False
        elif(new_password != repeat_password):
            self.erro_popup("Erro","Senhas Precisam Ser Iguais")
        elif(self.db.check_password(password)):
            self.db.update_password(new_password)
            self.dialog_pupdate.dismiss()
            return True
        else:
            self.erro_popup("Credencial Inválida","Senha Incorreta")
            return False

    def close_uPassword(self,btn):
        self.dialog_pupdate.dismiss()

    def dialog_content(self,*args):
        # Define o layout do conteúdo do dialog usando GridLayout
        content = GridLayout(cols=1, padding=[10,100,0,0], spacing=10, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Cria as labels e textfields
        current_password_label = MDLabel(text="Senha atual")
        content.add_widget(current_password_label)
        content.add_widget(self.password)

        new_password_label = MDLabel(text="Nova senha")
        content.add_widget(new_password_label)
        content.add_widget(self.new_password_field)

        repeat_password_label = MDLabel(text="Repita a nova senha")
        content.add_widget(repeat_password_label)
        content.add_widget(self.repeat_password_field)

        return content

    def update_string(self, new_string):
        # Atualiza o valor do TextField
        self.CLPStringTF.text = new_string

    def InsertConnIcon(self,*args):
        print('Inserticon')
        try:
            self.screen.add_widget(self.ConnectionIcon)
        except:
            pass

    def RemoveConnIcon(self,*args):
        print('removeicon')
        try:
            self.screen.remove_widget(self.ConnectionIcon)
        except:
            pass

    
    def get_configuration(self,string):
        allconfig_raw = self.db.get_all_config()
        if(allconfig_raw == []):
            return [(1,len(string))]
        
        return allconfig_raw

    def fill_substring_fields(self):
        print("substrings",self.substrings)
        for i in range(10):
            self.substring[i].text = ""

        for substring,recipe in self.substrings:
            print(substring)
            self.substring[recipe].text = substring
        
    def filesGeneration(self):
        self.Generator.remove_substrings_folder('Arquivos_de_Texto')
        for i in range(len(self.substrings)):
            self.Generator.create_substring_file(
                f'./Arquivos_de_Texto/receita{self.substrings[i][1]+1}.txt',
                self.substrings[i][0]
            )
            
    def systemFlow(self):
        rc = 0
        
        while(not rc):
            ip,port = self.db.get_ip()
            tcpConn = tcp.TCP_Handler(ip,port)
            print(f'Erro ao conectar: {ip}/{port}')
            Clock.schedule_once(lambda dt: self.InsertConnIcon())
            time.sleep(0.2)
            rc = tcpConn.connect()

        while(1):
            try:
                Clock.schedule_once(lambda dt: self.RemoveConnIcon())
                rcv_data = tcpConn.receive()
                Clock.schedule_once(lambda dt: self.update_string(rcv_data))
                
                config = self.get_configuration(rcv_data)          
                self.substrings = self.Generator.parse(rcv_data,config)
                self.fill_substring_fields()
                self.filesGeneration()

                tcpConn.sendACK()
            except Exception as e:
                self.erro_popup("Erro",f'Falha ao se comunicar com o clp.')
                self.systemFlow()
                return

Provisorio().run()
