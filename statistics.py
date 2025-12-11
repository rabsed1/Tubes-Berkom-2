from globals import Globals

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle
from kivy.graphics import Line
from kivy.graphics import Color
from kivy.graphics import Ellipse

class Statistics(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size = Globals.windowSize

        with self.canvas:
            Rectangle(source='res/textures/bg1.png', size=self.size)

        layout = BoxLayout(orientation='vertical', padding=(70, 0, 70, 130), spacing=20)
        
        title = Label(text='Statistics', color=(0,0,0,1), font_name='Jersey10', font_size=35, size_hint=(1,.1))
        layout.add_widget(title)
        layout.title = title

        firstContainer = BoxLayout(orientation='horizontal', size_hint=(1,.25), spacing=60)
        mastery = BoxLayout(orientation='vertical', padding=18)
        with mastery.canvas:
            Color(1,1,1,1)
            mastery.bg = RoundedRectangle(size=mastery.size, radius=(30,30,30,30))
            Color(0,0,0,1)
            mastery.border = Line(rounded_rectangle=(mastery.pos[0], mastery.pos[1], mastery.size[0], mastery.size[1], 30), width=1.5)
            mastery.bind(size=self.updateSizePos)
            mastery.bind(pos=self.updateSizePos)
        
        mastery.title = Label(text='Mastery Rate', color=(0,0,0,1), font_name='Jersey10', font_size=30, size_hint=(1,.2))
        mastery.visual = Label(text='50%', color=(0,0,0,1), font_size=25)
        with mastery.visual.canvas.before:
            Color(.921,.921,.921,1)
            mastery.visual.ellipse1 = Ellipse(pos=mastery.visual.pos, size=mastery.visual.size)
            Color(.325,.730,.482,1)
            mastery.visual.ellipse2 = Ellipse(pos=mastery.visual.pos, size=mastery.visual.size, angle_start=0, angle_end=180)
            Color(1,1,1,1)
            mastery.visual.ellipse3 = Ellipse(pos=mastery.visual.pos, size=mastery.visual.size)

            mastery.visual.bind(size=self.updateMasteryVisualSizePos)
            mastery.visual.bind(pos=self.updateMasteryVisualSizePos)
        mastery.subTitle = Label(text='2 Cards Reviewed', color=(0,0,0,1), font_name='Jersey10', font_size=20, size_hint=(1,.2))

        mastery.add_widget(mastery.title)
        mastery.add_widget(mastery.visual)
        mastery.add_widget(mastery.subTitle)

        firstContainer.add_widget(mastery)
        firstContainer.mastery = mastery

        due = BoxLayout(orientation='vertical', padding=(18, 10))
        with due.canvas:
            Color(1,1,1,1)
            due.bg = RoundedRectangle(size=due.size, radius=(30,30,30,30))
            Color(0,0,0,1)
            due.border = Line(rounded_rectangle=(due.pos[0], due.pos[1], due.size[0], due.size[1], 30), width=1.5)
            due.bind(size=self.updateSizePos)
            due.bind(pos=self.updateSizePos)
        due.title = Label(text='Cards Due\nToday', color=(0,0,0,1), font_name='Jersey10', font_size=30, size_hint=(1,.38), line_height=.8, halign='center')
        due.number = Label(text='26', color=(0,0,0,1), font_name='Jersey10', font_size=100, size_hint=(1,.43))
        due.subTitle = Label(text='Estimated Time', color=(0,0,0,1), font_name='Jersey10', font_size=20, size_hint=(1,.1))
        due.minute = Label(text='6 Min', color=(0,0,0,1), font_name='Jersey10', font_size=20, size_hint=(1,.1))
        due.add_widget(due.title)
        due.add_widget(due.number)
        due.add_widget(due.subTitle)
        due.add_widget(due.minute)
        firstContainer.add_widget(due)
        firstContainer.mastery = due

        layout.add_widget(firstContainer)
        layout.firstContainer = firstContainer

        secondContainer = BoxLayout(orientation='vertical', size_hint=(1,.13), padding=10)
        with secondContainer.canvas:
            Color(1,1,1,1)
            secondContainer.bg = RoundedRectangle(size=secondContainer.size, radius=(30,30,30,30))
            Color(0,0,0,1)
            secondContainer.border = Line(rounded_rectangle=(secondContainer.pos[0], secondContainer.pos[1], secondContainer.size[0], secondContainer.size[1], 30), width=1.5)
            secondContainer.bind(size=self.updateSizePos)
            secondContainer.bind(pos=self.updateSizePos)

        secondContainer.title = Label(text='Difficulty Breakdown', color=(0,0,0,1), font_name='Jersey10', font_size=30, size_hint=(1,.4))
        secondContainer.add_widget(secondContainer.title)
        difficultyTitles = BoxLayout(orientation='horizontal', size_hint=(1,.3))
        difficultyTitles.add_widget(Label(text='Again', color=(1,0,0,1), font_name='Jersey10', font_size=25))
        difficultyTitles.add_widget(Label(text='Hard', color=(0,0,0,1), font_name='Jersey10', font_size=25))
        difficultyTitles.add_widget(Label(text='Good', color=(0,1,0,1), font_name='Jersey10', font_size=25))
        difficultyTitles.add_widget(Label(text='Easy', color=(0,0,1,1), font_name='Jersey10', font_size=25))
        secondContainer.add_widget(difficultyTitles)
        secondContainer.firstContainer = difficultyTitles
        
        difficultyCounts = BoxLayout(orientation='horizontal', size_hint=(1,.3))
        difficultyCounts.add_widget(Label(text='1', color=(1,0,0,1), font_name='Jersey10', font_size=25))
        difficultyCounts.add_widget(Label(text='0', color=(0,0,0,1), font_name='Jersey10', font_size=25))
        difficultyCounts.add_widget(Label(text='1', color=(0,1,0,1), font_name='Jersey10', font_size=25))
        difficultyCounts.add_widget(Label(text='1', color=(0,0,1,1), font_name='Jersey10', font_size=25))
        secondContainer.add_widget(difficultyCounts)
        secondContainer.firstContainer = difficultyCounts

        layout.add_widget(secondContainer)
        layout.secondContainer = secondContainer

        thirdContainer = BoxLayout(orientation='vertical', size_hint=(1,.32), padding=(20,10,20,20), spacing=10)
        with thirdContainer.canvas:
            Color(1,1,1,1)
            thirdContainer.bg = RoundedRectangle(size=thirdContainer.size, radius=(30,30,30,30))
            Color(0,0,0,1)
            thirdContainer.border = Line(rounded_rectangle=(thirdContainer.pos[0], thirdContainer.pos[1], thirdContainer.size[0], thirdContainer.size[1], 30), width=1.5)
            thirdContainer.bind(size=self.updateSizePos)
            thirdContainer.bind(pos=self.updateSizePos)

        titleContainer = BoxLayout(orientation='horizontal', size_hint=(1,.2))
        titleContainer.title = Label(text='Upcoming Reviews', color=(0,0,0,1), font_name='Jersey10', font_size=30, size_hint=(.6,1), halign='left')
        titleContainer.add_widget(titleContainer.title)
        titleContainer.month = Label(text='Jan 2026', color=(0,0,0,1), font_name='Jersey10', font_size=30, size_hint=(.4,1), halign='right')
        titleContainer.add_widget(titleContainer.month)

        thirdContainer.add_widget(titleContainer)
        thirdContainer.titleContainer = titleContainer

        calendar = GridLayout(cols=7, rows=6)
        calendar.add_widget(Label(text='S', color=(.4,.4,.4,1), font_name='Jersey10', font_size=23))
        calendar.add_widget(Label(text='M', color=(.4,.4,.4,1), font_name='Jersey10', font_size=23))
        calendar.add_widget(Label(text='T', color=(.4,.4,.4,1), font_name='Jersey10', font_size=23))
        calendar.add_widget(Label(text='W', color=(.4,.4,.4,1), font_name='Jersey10', font_size=23))
        calendar.add_widget(Label(text='T', color=(.4,.4,.4,1), font_name='Jersey10', font_size=23))
        calendar.add_widget(Label(text='F', color=(.4,.4,.4,1), font_name='Jersey10', font_size=23))
        calendar.add_widget(Label(text='S', color=(.4,.4,.4,1), font_name='Jersey10', font_size=23))
        for i in range(3):
            calendar.add_widget(Label(text='', color=(.1,.1,.1,1), font_name='Jersey10', font_size=20))
        for i in range(1, 32):
            calendar.add_widget(Label(text=f'{i}', color=(.1,.1,.1,1), font_name='Jersey10', font_size=20))
        for i in range(1):
            calendar.add_widget(Label(text='', color=(.1,.1,.1,1), font_name='Jersey10', font_size=20))

        thirdContainer.add_widget(calendar)
        thirdContainer.calendar = calendar

        layout.add_widget(thirdContainer)
        layout.thirdContainer = thirdContainer

        fourthContainer = BoxLayout(orientation='vertical', size_hint=(1,.1), padding=10, spacing=5)
        with fourthContainer.canvas:
            Color(1,1,1,1)
            fourthContainer.bg = RoundedRectangle(size=fourthContainer.size, radius=(30,30,30,30))
            Color(0,0,0,1)
            fourthContainer.border = Line(rounded_rectangle=(fourthContainer.pos[0], fourthContainer.pos[1], fourthContainer.size[0], fourthContainer.size[1], 30), width=1.5)
            fourthContainer.bind(size=self.updateSizePos)
            fourthContainer.bind(pos=self.updateSizePos)
        
        fourthContainer.title = Label(text='Next Reviews in: 1 Day', color=(.1,.1,.1,1), font_name='Jersey10', font_size=40)
        fourthContainer.add_widget(fourthContainer.title)

        layout.add_widget(fourthContainer)
        layout.fourthContainer = fourthContainer

        self.add_widget(layout)
        self.layout = layout

        tab = Button(text='Back', font_name='Jersey10', font_size=25, size_hint=(1,.1), background_color=(0,0,0,0))
        with tab.canvas.before:
            Color(.07,.07,.07,.8)
            tab.bg=RoundedRectangle(size=tab.size, radius=(30,30,0,0))
            tab.bind(size=self.updateTabSizePos)
            tab.bind(pos=self.updateTabSizePos)

        self.add_widget(tab)
        self.tab = tab

    def updateSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos
        instance.border.rounded_rectangle=(instance.pos[0], instance.pos[1], instance.size[0], instance.size[1], 30)

    def updateMasteryVisualSizePos(self, instance, value):
        instance.ellipse1.size = (min(instance.size[0], instance.size[1])-10,min(instance.size[0], instance.size[1])-10)
        instance.ellipse1.pos = (instance.pos[0]+(instance.size[0]-instance.ellipse1.size[0])/2, instance.pos[1]+(instance.size[1]-instance.ellipse1.size[1])/2)

        instance.ellipse2.size = (min(instance.size[0], instance.size[1])-10,min(instance.size[0], instance.size[1])-10)
        instance.ellipse2.pos = (instance.pos[0]+(instance.size[0]-instance.ellipse2.size[0])/2, instance.pos[1]+(instance.size[1]-instance.ellipse2.size[1])/2)

        instance.ellipse3.size = (min(instance.size[0], instance.size[1])-45,min(instance.size[0], instance.size[1])-45)
        instance.ellipse3.pos = (instance.pos[0]+(instance.size[0]-instance.ellipse3.size[0])/2, instance.pos[1]+(instance.size[1]-instance.ellipse3.size[1])/2)

    def updateTabSizePos(self, instance, value):
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos
        