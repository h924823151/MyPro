# 根据数据库编写所有的实体类

# 导入 db 到 models.py
from . import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(30))
    upwd = db.Column(db.String(255))

    def __init__(self,uname,upwd):
        self.uname = uname
        self.upwd = upwd

    def to_dict(self):

        dic = {
            'id':self.id,
            'uname':self.uname,
            'upwd':self.upwd
        }
        return dic

class Hero(db.Model):
    __tablename__ = 'hero'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(30))
    avautar = db.Column(db.String(255))
    picture = db.Column(db.String(255))
    hero_story = db.Column(db.Text)
    #增加关联属性以及反向引用关系属性
    skill = db.relationship('Skill',backref='hero',lazy='dynamic')

    def __init__(self,name,avautor,picture,hero_story):
        self.name = name
        self.avautar = avautar
        self.picture = picture
        self.skill = skill
        self.hero_story = hero_story

    def to_dict(self):
        dic = {
            'id':self.id,
            'name':self.name,
            'avautar':self.avautar,
            'picture':self.picture,
            'hero_story':self.hero_story
        }
        return dic

class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer,primary_key=True)
    skill_name = db.Column(db.String(30))
    skill_content = db.Column(db.String(255))
    skill_exp = db.Column(db.String(255))
    skill_pic = db.Column(db.String(255))
    skill_hero_id = db.Column(db.Integer,db.ForeignKey('hero.id'))

    def __init__(self,skill_name,skill_exp,skill_pic,skill_hero_id):
        self.skill_name = skill_name
        self.skill_exp = skill_exp
        self.skill_pic = skill_pic
        self.skill_hero_id = skill_hero_id

    def to_dict(self):
        dic = {
            'id':self.id,
            'skill_name':self.skill_name,
            'skill_content':self.skill_content,
            'skill_exp':self.skill_exp,
            'skill_pic':self.skill_pic,
            'skill_hero_id':self.skill_hero_id
        }
        return dic

class Msg(db.Model):
    __tablename__='msg'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30))
    address=db.Column(db.String(30))
    def to_dict(self):
        dic={
            'id':self.id,
            'name':self.name,
            'address':self.address
        }
        return dic