from selenium import webdriver
from lxml import etree
import re
import pymysql


dbparams = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'wangzhe',
    'charset': 'utf8'
}
conn = pymysql.connect(**dbparams)
cursor = conn.cursor()

class Hero:
	index = 0

	def __init__(self, name, avautar, picture, hero_story, skill_list):
		self.name = name
		self.avautar = avautar
		self.picture = picture
		self.hero_story = hero_story
		self.skill_list = skill_list
		Hero.index += 1

	def sert_to_hero(self):
		sql = 'insert into hero(id,name,avautar,picture,hero_story) values(%s,%s,%s,%s,%s)'
		cursor.execute(sql,(Hero.index, self.name, self.avautar, self.picture, self.hero_story))
		conn.commit()

	def sert_to_skill(self):
		sql = 'insert into skill(skill_name,skill_content,skill_exp,skill_pic,skill_hero_id) values(%s,%s,%s,%s,%s)'
		for skill_info in self.skill_list:
			cursor.execute(sql,(skill_info['skill_name'],skill_info['skill_content'],skill_info['skill_exp'],skill_info['skill_pic'], Hero.index))
			conn.commit()

def get_hero():
	L = []
	hero_url = 'https://pvp.qq.com/web201605/herolist.shtml'
	driver = webdriver.Chrome()
	driver.get(hero_url)
	html = driver.page_source
	html = etree.HTML(html)
	lis = html.xpath('/html/body/div[3]/div/div/div[2]/div[2]/ul/li')
	urls = []
	for li in lis:
		url = li.xpath('./a/@href')[0]
		detail_url = 'https://pvp.qq.com/web201605/'+url
		urls.append(url)
		avautar = li.xpath('./a/img/@src')[0]
		name = li.xpath('./a/img/@alt')[0]
		driver.get(detail_url)
		html = etree.HTML(driver.page_source)
		pattern = re.compile("background:url\('([\s\S]*?)'\)")
		picture = re.findall(pattern, driver.page_source)[0]
		video = html.xpath('/html/body/div[3]/div[1]/div/div/div[1]/a')[0]
		hero_story = ''.join(html.xpath('//div[@class="pop-bd"]/p/text()'))

		skills = html.xpath('//div[@class="skill-show"]')[0]
		skills = skills.xpath('./div[@class="show-list"]')[:4]
		skill_list = []
		pic_list = []
		skill_lis = html.xpath('.//ul[@class="skill-u1"]/li')[:4]
		for skill_li in skill_lis:
			skill_pic = skill_li.xpath('./img/@src')[0]
			pic_list.append(skill_pic)

		for skill in skills:
			skill_name = skill.xpath('.//b/text()')[0]
			skill_content = skill.xpath('./p[@class="skill-desc"]/text()')[0]
			skill_exp = skill.xpath('./div[@class="skill-tips"]/text()')[0]
			skill_info = {'skill_name':skill_name,
						  'skill_content': skill_content,
						  'skill_exp':skill_exp
						  }
			skill_list.append(skill_info)
		for i in range(len(pic_list)):
			skill_list[i]['skill_pic'] = pic_list[i]

		aobject = Hero(name, avautar, picture, hero_story, skill_list)
		try:
			aobject.sert_to_hero()
			aobject.sert_to_skill()
			print('%s 已插入完成！！！' % aobject.name)
		except Exception as e:
			print('%s 插入失败！！！' % aobject.name, e)

if __name__ == '__main__':
	get_hero()











