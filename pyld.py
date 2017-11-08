"""
**********************************************************

    Author          :Charles Brissac

    Email           :cdbrissac@gmail.com

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
