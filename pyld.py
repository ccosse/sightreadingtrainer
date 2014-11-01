"""
**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@gmail.com

    Copyright       :(C) 2006-2011 Asymptopia Software

    License         :GPLv3

***********************************************************
"""
class Pyld:
	def __init__(self,hostname):
		self.hostname=hostname
		self.midi=60
		self.tempo=[4,4]
		self.RH=[]
		self.LH=[]
		
		self.img_dir="img/"
		self.image_names=['notehead-0.png']
		self.tempo=['4','4']
