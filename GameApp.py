#!/usr/bin/env python3
# coding:UTF-8
# author = 'HingLo.C'
""""
文件说明：这是我用来测试图形化界面的设计
"""

from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import *
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
from kivy.uix.widget import Widget


class Plane(Widget):
    def __init__(self, **kwargs):
        self.pos = (190, 60)
        self.size = (38, 52)
        super(Plane, self).__init__(**kwargs)


class Main(Widget):
    planetime = 0
    enemytime = 0
    pos_x = NumericProperty(0)
    pos_y = NumericProperty(630)
    my_pos = ReferenceListProperty(pos_x, pos_y)
    plane = ObjectProperty(None)  # 飞机
    enemyList = ListProperty(None)  # 敌人飞机集合
    bulletList = ListProperty(None)  # 子弹集合
    enemyBulletList = ListProperty(None)  # 敌人子弹集合
    enemy = ListProperty(
        ["enemy01.png", "enemy02.png", "enemy03.png", "enemy04.png", "enemy05.png", "enemy06.png"])
    score = NumericProperty(0)
    tip = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)

    def update(self, dt):
        if self.score >= 0:
            self.move()  # 移动背景图片
            self.enemyPlaneMove()  # 移动敌人飞机
            self.bulletMove()  # 移动座机的子弹
            self.draw()  # 画飞机，子弹等
        else:
            # 分数小数结束游戏
            self.tip = "游戏结束了！哈哈"

    def draw(self):
        self.enemytime += 1
        self.planetime += 1
        # 绘画敌人的飞机
        if self.enemytime % 30 == 0:
            self.enemytime = 0
            self.enemyPlane()
            self.enemyBullet()

        # 添加自己子弹
        if self.planetime % 30 == 0:
            self.planetime = 0
            self.bullet()

    def enemyPlane(self):
        """
        绘画敌人的飞机
        :return:
        """
        with self.canvas:
            temp = Rectangle(pos=(randint(0, self.width), self.height + 36), size=(47, 36),
                             source="./enemyPlane/" + str(self.enemy[randint(0, 5)]))
            self.enemyList.append(temp)

    def enemyPlaneMove(self):
        """
        敌人飞机移动
        :return:
        """
        for key, value in enumerate(self.enemyList):
            x, y = value.pos
            w, h = value.size
            y -= 1
            self.enemyList[key].pos = (x, y)
            if y < -36 or self.enemyPlaneAndPlane(value):
                self.enemyList[key].pos = (0, 0)
                self.enemyList[key].size = (0, 0)
                self.enemyList.remove(value)

    def enemyPlaneAndPlane(self, value):
        """
        敌人的飞机与自己的飞机碰撞检测
        :param value:
        :return:
        """
        x, y = value.pos
        w, h = value.size
        if self.isCollsionWithRect(self.plane.x, self.plane.y, self.plane.width, self.plane.height, x, y, w, h):
            self.score -= 1
            return True

    def bullet(self):
        """
        画子弹
        :return:
        """
        with self.canvas:
            self.bulletList.append(
                Rectangle(pos=(self.plane.center_x - 4, self.plane.center_y), size=(9, 25),
                          source="./bullet/bul06.png"))

    def enemyBullet(self):
        """
        画敌人的子弹
        :return:
        """
        for key, value in enumerate(self.enemyList):
            x, y = value.pos
            with self.canvas:
                if randint(1, 20) == 10:
                    self.enemyBulletList.append(
                        Rectangle(pos=(x + 20, y - 14), size=(10, 28), source="./bullet/bul01.png"))

    def bulletMove(self):
        """
        子弹移动
        :return:
        """
        for key, value in enumerate(self.bulletList):
            x, y = value.pos
            y += 1
            self.bulletList[key].pos = (x, y)
            if y > self.height or self.enemyAndbullet(value):
                self.bulletList[key].pos = (0, 0)
                self.bulletList[key].size = (0, 0)
                self.bulletList.remove(value)
        for key, value in enumerate(self.enemyBulletList):
            x, y = value.pos
            y -= 1.5
            self.enemyBulletList[key].pos = (x, y)
            if y < 0 or self.enemyBulletPlane(value):
                self.enemyBulletList[key].pos = (0, 0)
                self.enemyBulletList[key].size = (0, 0)
                self.enemyBulletList.remove(value)

    def enemyBulletPlane(self, bullet):
        """
        敌人的子弹与自己的飞机碰撞
        :param bullet:
        :return:
        """
        x, y = bullet.pos
        w, h = bullet.size
        if self.isCollsionWithRect(self.plane.x, self.plane.y, self.plane.width, self.plane.height, x, y, w, h):
            self.score -= 1
            return True

    def enemyAndbullet(self, bullet):
        """
        子弹与敌人的飞机碰撞检测
        :param bullet:
        :return:
        """
        for key, enemy in enumerate(self.enemyList):
            x, y = enemy.pos
            w, h = enemy.size
            x1, y1 = bullet.pos
            w1, h1 = bullet.size
            if self.isCollsionWithRect(x, y, w, h, x1, y1, w1, h1):
                self.enemyList[key].pos = (0, 0)
                self.enemyList[key].size = (0, 0)
                self.score += 1
                return True

    def move(self):
        """
        背景图片移动的算法
        :return:
        """
        self.y -= 1
        self.pos_y -= 1
        if self.pos_y == -630:
            self.pos_y = 630
        if self.y == -630:
            self.y = 630

    def on_touch_move(self, touch):
        if 0 < touch.x < self.width - self.plane.width:
            self.plane.x = touch.x
        if 0 < touch.y < self.height - self.plane.height:
            self.plane.y = touch.y

    def isCollsionWithRect(self, x1, y1, w1, h1, x2, y2, w2, h2):
        if x1 >= x2 and x1 >= x2 + w2:
            return False
        elif x1 <= x2 and x1 + w1 <= x2:
            return False
        elif y1 >= y2 and y1 >= y2 + h2:
            return False
        elif y1 <= y2 and y1 + h1 <= y2:
            return False
        return True


class GameApp(App):
    """
    主类,程序的入口就是从这人进入的
    """

    def build(self):
        main = Main()
        Window.size = (420, 630)
        self.title = "GamePlane"  # 设置标题
        self.icon = "icon.png"  # 设置图标
        # 指定的时间来更新的函数
        Clock.schedule_interval(main.update, 1.0 / 60.0)
        return main


if __name__ == '__main__':
    GameApp().run()
