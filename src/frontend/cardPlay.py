from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button

from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle
from kivy.graphics import Line
from kivy.graphics import BoxShadow

from frontend.globals import Globals

from backend.boxes import box_ambil
from backend.boxes import box_simpan
from backend.date import tanggal_parse
from backend.date import tanggal_format
from backend.scheduler import jadwal_update

from datetime import date

class CardPlay(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 40
        self.size = Globals.windowSize

        self.name = App.get_running_app().data['deckName']
        self.data = box_ambil(self.name)

        self.playCards = []
        self.stashCard = []
        for card in self.data['kartu']:
            if tanggal_parse(card[3]) == date.today():
                self.playCards.append(card)
            else:
                self.stashCard.append(card)

        self.currentIdx = -1
        self.lastIdx = len(self.playCards)-1
        self.rate = [0, 0, 0, 0]

        self.cardFlipped = False

        with self.canvas:
            Rectangle(source='res/textures/bg1.png', size=self.size)

        header = BoxLayout(orientation='horizontal', size_hint=(1,.15))
        # header.add_widget(Button(text='<-', color=(0,0,0,1), font_name='Jersey10', font_size=34, halign='center', valign='center', size_hint=(.2, 1), background_color=(0,0,0,0)))
        header.add_widget(Button(text=self.name, color=(0,0,0,1), font_name='Jersey10', font_size=35, halign='center', valign='center', background_color=(0,0,0,0)))
        header.text_size=header.size
        self.add_widget(header)

        score = BoxLayout(orientation='horizontal',size_hint=(.2, .05), pos_hint={'center_x':.5})
        score.arr = [
            Label(text=f'{self.rate[0]}', color=(1,0,0,1), font_name='Jersey10', font_size=30, halign='center', valign='center'),
            Label(text=f'{self.rate[0]}', color=(0,0,0,1), font_name='Jersey10', font_size=30, halign='center', valign='center'),
            Label(text=f'{self.rate[0]}', color=(0,1,0,1), font_name='Jersey10', font_size=30, halign='center', valign='center'),
            Label(text=f'{self.rate[0]}', color=(0,0,1,1), font_name='Jersey10', font_size=30, halign='center', valign='center')
        ]
        score.add_widget(score.arr[0])
        score.add_widget(score.arr[1])
        score.add_widget(score.arr[2])
        score.add_widget(score.arr[3])
        self.add_widget(score)
        self.score = score

        main = BoxLayout(orientation='vertical', size_hint=(.8, 1), pos_hint={'center_x':.5}, padding=(20,0,20,50), spacing=20)

        card = BoxLayout(orientation='vertical', padding=30, size_hint=(1,1))
        with card.canvas:
            Color(0,0,0,.25)
            card.shadow = BoxShadow(card.size, card.pos, offset=(0,-4), blur_radius=4.0)
            card.shadow.border_radius=(30,30,30,30)
            Color(.984,.941,.874,1)
            card.border = Line(rounded_rectangle=(card.pos[0],card.pos[1],card.size[0],card.size[1], 30), width=2)
            Color(1,.9675,.9215,1)
            card.bg = RoundedRectangle(size=card.size, radius=(30,30,30,30))
            card.bind(size=self.updateCardSizePos)
            card.bind(pos=self.updateCardSizePos)
        # card.image = Image(source='res/textures/img1.png', fit_mode='contain')
        card.label = Label(text='', color=(0,0,0,1), font_name='Inconsolata', font_size=28, halign='center', valign='center')
        card.label.bind(size=self.updateCardLabelSizePos)
        # card.add_widget(card.image)
        card.add_widget(card.label)

        layout = RelativeLayout(size_hint=(1,1))
        layout.flipArea = Button(background_color=(0,0,0,0), size_hint=(1,1), on_press=self.flipCard)
        layout.card = card
        layout.add_widget(layout.flipArea)
        layout.add_widget(layout.card)
        main.add_widget(layout)
        main.layout = layout

        rate = BoxLayout(orientation='horizontal', size_hint=(1, .12), disabled=True, opacity=0)
        with rate.canvas:
            Color(0,0,0,.25)
            rate.shadow = BoxShadow(size=rate.size, pos=rate.pos, offset=(0,-4), blur_radius=4.0)
            rate.shadow.border_radius=(30,30,30,30)
            Color(.984,.941,.874,1)
            rate.border = Line(rounded_rectangle=(rate.pos[0], rate.pos[1], rate.size[0], rate.size[1], 30), width=2)
            Color(1,.9675,.9215,1)
            rate.bg = RoundedRectangle(size=rate.size, radius=(30,30,30,30))
            rate.bind(size=self.updateRateSizePos)
            rate.bind(pos=self.updateRateSizePos)
        rateAgain = Button(text='Again', color=(1,0,0,1), font_name='Inconsolata', font_size=20, halign='center', valign='center', background_color=(0,0,0,0), on_press=self.rateCard)
        rateAgain.value = 0
        rateHard = Button(text='Hard', color=(0,0,0,1), font_name='Inconsolata', font_size=20, halign='center', valign='center', background_color=(0,0,0,0), on_press=self.rateCard)
        rateHard.value = 1
        rateGood = Button(text='Good', color=(0,1,0,1), font_name='Inconsolata', font_size=20, halign='center', valign='center', background_color=(0,0,0,0), on_press=self.rateCard)
        rateGood.value = 2
        rateEasy = Button(text='Easy', color=(0,0,1,1), font_name='Inconsolata', font_size=20, halign='center', valign='center', background_color=(0,0,0,0), on_press=self.rateCard)
        rateEasy.value = 3
        rate.add_widget(rateAgain)
        rate.add_widget(rateHard)
        rate.add_widget(rateGood)
        rate.add_widget(rateEasy)
        rate.rateAgain = rateAgain
        rate.rateHard = rateHard
        rate.rateGood = rateGood
        rate.rateEasy = rateEasy
        main.add_widget(rate)
        main.rate = rate

        self.add_widget(main)
        self.main = main

        tab = Button(text='Next', font_name='Jersey10', font_size=25, size_hint=(1, .15), color=(.8,.8,.8,1), background_color=(0,0,0,0), on_press=self.next, disabled=True)
        with tab.canvas.before:
            Color(.07,.07,.07,.8)
            tab.bg=RoundedRectangle(size=tab.size, radius=(30,30,0,0))
            tab.bind(size=self.updateTabSizePos)
            tab.bind(pos=self.updateTabSizePos)
        self.add_widget(tab)
        self.tab = tab

        self.nextQuestion(self)

    def rateCard(self, instance):
        self.rate[instance.value] = self.rate[instance.value] + 1
        self.score.arr[instance.value].text = f'{self.rate[instance.value]}'
        print(instance.value)
        self.playCards[self.currentIdx] = jadwal_update(self.playCards[self.currentIdx], instance.value, tanggal_format(date.today()))

        self.tab.disabled=False
        self.tab.color=(1,1,1,1)

        self.main.rate.disabled=True
        self.main.rate.opacity=0
        

    def nextQuestion(self, instance):
        if self.cardFlipped:
            self.flipCard(self)
        # Kartu sudah di review semua?
        if self.currentIdx == self.lastIdx:
            # Selesai
            self.showEndPlay(self)
        else:
            # Tampilkan kartu selanjutnya
            self.currentIdx = self.currentIdx+1
            self.main.layout.card.label.text = self.playCards[self.currentIdx][self.cardFlipped][0]
            self.tab.disabled=True
            self.tab.color=(.8,.8,.8,.8)
            

    def flipCard(self, instance):
        # Balik kartu
        if not self.cardFlipped:
            self.main.layout.card.label.text = self.playCards[self.currentIdx][1][0]
            self.main.rate.disabled = False
            self.main.rate.opacity = 1
        else:
            self.main.layout.card.label.text = self.playCards[self.currentIdx][0][0]
            self.main.rate.disabled = True
            self.main.rate.opacity = 0

        self.cardFlipped = not self.cardFlipped

    def showEndPlay(self, instance):
        card = self.main.layout.card
        card.label.text = 'Yeay!'
        card.label.font_size = 30
        card.label.font_name = 'Jersey10'
        card.padding = (30, 200)
        card.add_widget(Label(text='Thats\'s all for today!', color=(0,0,0,1), font_name='Jersey10', font_size=25, halign='center', valign='center', size_hint=(1, .2)))
        # card.remove_widget(card.image)
        self.tab.on_press=self.back

        self.stashCard.append(self.playCards)
        self.data['kartu'] = self.stashCard
        box_simpan(self.name, self.data)

    def next(self, instance):
        self.nextQuestion(self)

    def back(self):
        App.get_running_app().SwitchScreen(3, {'deckName': self.name})

    def updateCardSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos
        instance.border.rounded_rectangle = (instance.pos[0], instance.pos[1], instance.size[0], instance.size[1], 30)
        instance.shadow.size = instance.size
        instance.shadow.pos = instance.pos
        self.main.layout.flipArea.size = instance.size
        self.main.layout.flipArea.pos = instance.pos

    def updateCardLabelSizePos(self, instance, value):
        instance.text_size = instance.size

    def updateRateSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos
        instance.border.rounded_rectangle = (instance.pos[0], instance.pos[1], instance.size[0], instance.size[1], 30)
        instance.shadow.size = instance.size
        instance.shadow.pos = instance.pos

    def updateTabSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos