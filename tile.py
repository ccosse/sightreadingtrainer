from javax.imageio import ImageIO
from java.io import File
from java.net import URL

class Tile:
	
	def __init__(self,hostname,img_dir,img_fname,duration,xc,yc):
		#print hostname,img_dir,img_fname,duration,xc,yc
		self.hostname=hostname
		self.img_dir=img_dir
		self.img_fname=img_fname
		self.amrest=False
		self.ly=''
		if False:pass
		elif img_fname=='r1.png':
			self.amrest=True
			self.ly='r'
		elif img_fname=='r2.png':
			self.amrest=True
			self.ly='r'
		elif img_fname=='r4.png':
			self.amrest=True
			self.ly='r'
		elif img_fname=='r8.png':
			self.amrest=True
			self.ly='r'
		
		if hostname[0:7]=='http://':
			self.img=ImageIO.read(URL(hostname+img_dir+img_fname))
		else:
			self.img=ImageIO.read(File(hostname+img_dir+img_fname))
		
		self.duration=duration
		self.xc=xc
		self.yc=yc
		
		self.w=self.img.getWidth()
		self.h=self.img.getHeight()
		self.w2=self.w/2
		self.h2=self.h/2
		self.x=self.xc-self.w/2
		self.y=self.yc-self.h/2
		
		#self.bmp=self.img.ConvertToBitmap()

		
	#Tile.		
	def SetCenter(self,center):
		self.xc=center[0]
		self.yc=center[1]
		self.x=self.xc-self.w2
		self.y=self.yc-self.h2
		
