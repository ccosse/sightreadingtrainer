import java
from java import awt

from javax.imageio import ImageIO
from java.io import File
from java.net import URL

class Spot(java.awt.image.ImageObserver):

#	def __init__(self,hostname,offset,xidx,yidx,sig_idx,dx,dy,amline,amledger,note):
	def __init__(self,hostname,offset,xidx,tlcx,yidx,tlcy,sig_idx,dx,dy,amline,amledger,note):
		"""
		sharp_img_fname=hostname+'./img/'+"sharp.png"
		
		if hostname[0:7]=='http://':
			sharp_img=ImageIO.read(URL(sharp_img_fname))
		else:
			sharp_img=ImageIO.read(File(sharp_img_fname))
		sharp_img_dx=sharp_img.getWidth()
		sharp_img_dy=sharp_img.getHeight()
		
		
		treble_clef_img_fname=hostname+'./img/'+"treble_clef.png"
		if hostname[0:7]=='http://':
			treble_clef_img=ImageIO.read(URL(treble_clef_img_fname))
		else:
			treble_clef_img=ImageIO.read(File(treble_clef_img_fname))
		treble_clef_img_dx=treble_clef_img.getWidth()
		treble_clef_img_dy=treble_clef_img.getHeight()
		"""
		
		self.amline=amline
		self.amledger=amledger
		self.show_continuous_ledgers=True
		self.note=note
		self.xidx=xidx
		self.yidx=yidx
		self.dx=int(dx)
		self.dy=int(dy)

		nx_sig_spots=7
		
		#offset=0
		self.x=int(0)
#		if xidx==0:self.x=int(offset)
		self.x=tlcx
#		else:self.x=int(offset+treble_clef_img_dx+nx_sig_spots*sharp_img_dx+(xidx-1-nx_sig_spots)*dx)
#		else:self.x=treble_clef_img_dx+sig_idx*sharp_img_dx+(xidx-1-sig_idx)*dx
		
		"""		
		self.y=int((yidx/2.)*dy)#-1
#		print self.y
		"""
		self.y=tlcy
		self.xc=int(self.x+(0.5)*dx)
		self.yc=int(self.y+(0.5)*dy)
		self.occupied=False
		self.visitors=[]
		self.locked=False
		self.accidental=False
		
		self.rect=java.awt.Rectangle(self.x,self.y,self.dx,self.dy)
		self.HILIGHT=False
		
		
	#Spot.
	def clear(self):
		self.visitors.pop()
		self.occupied=False
	
	#Spot.
	def lock(self):
		self.locked=True
	
	#Spot.
	def isoccupied(self):
		return self.occupied
		
	#Spot.
	def unlock(self):
		self.locked=False
	
	#Spot.
	def islocked(self):
		return self.locked
		
	#Spot.
	def TakeVisitor(self,visitor):
		
		if self.islocked():
			if DEBUG:print 'locked spot: visitor rejected'
			return False
		
		self.occupied=True
		visitor.SetCenter((self.xc,self.yc))
		self.visitors.insert(0,visitor)
		
		#if accidental, set v[0].x:
		if len(self.visitors)>1:
			
			self.visitors[0].SetCenter((self.visitors[1].x-self.visitors[0].w/2,self.visitors[1].yc))
			self.visitors[0].duration=self.visitors[1].duration
			
			if visitor.img_fname=='flat.png':
				self.accidental='es'
			elif visitor.img_fname=='natural.png':
				self.accidental='!'
			elif visitor.img_fname=='sharp.png':
				self.accidental='is'
			
		#print self.note,self.accidental
		return True
		
	#Spot.
	def ReleaseVisitor(self):
		
		if self.islocked():return None
		
		if len(self.visitors)>1:
			#print "RELEASE: accidental"
			self.accidental=False
			return self.visitors.pop(0)
			
		if len(self.visitors)>0:
			#print "RELEASE:",self.xidx,self.yidx
			self.occupied=False
			return self.visitors.pop(0)
		else:
			self.occupied=False
			return None
				
	
	#Spot.
	def toggle_hilight(self):
		if self.HILIGHT:self.HILIGHT=False
		else:self.HILIGHT=True

	#Spot.
	def render(self,g):
		#print 'render'
		
		if self.HILIGHT:
			g.setColor(java.awt.Color.YELLOW)
			g.drawRect(self.x,self.y,self.dx,self.dy)
		
		if self.amline==True:
			if self.amledger==False:
				g.setColor(java.awt.Color.BLACK)
				g.drawLine(self.x,int(self.yc),(self.x+self.dx),int(self.yc))
			elif self.amledger==True and self.occupied==True:
				g.setColor(java.awt.Color.RED)
				g.drawLine(self.x,int(self.yc),(self.x+self.dx),int(self.yc))
			elif self.amledger==True and self.show_continuous_ledgers==True:
				g.setColor(java.awt.Color.RED)
				g.drawLine(self.x,int(self.yc),(self.x+self.dx),int(self.yc))
			else:
				pass
		
		
		if self.occupied==True:# and not self.islocked():
			for vidx in range(len(self.visitors)):
				visitor=self.visitors[vidx]
				g.drawImage(visitor.img,int(visitor.x),int(visitor.y),self)
				#print visitor.x,visitor.y,self.yidx,self.xc,self.yc,self.dy
		
		
	def renderOFF(self,dc):
		#print 'render'
		black=wx.Colour(0,0,0,wx.ALPHA_TRANSPARENT)
		white=wx.Colour(255,255,255,wx.ALPHA_TRANSPARENT)
		green=wx.Colour(0,200,0,wx.ALPHA_TRANSPARENT)
		yellow=wx.Colour(200,200,0,wx.ALPHA_TRANSPARENT)
		orange=wx.Colour(255,155,0,wx.ALPHA_TRANSPARENT)
		red=wx.Colour(255,0,0,wx.ALPHA_TRANSPARENT)
		
		rect=wx.Rect(0,0,self.dx,self.dy)
		rect.SetPosition((self.xc-self.dx/2,self.yc-self.dy/2))
		
		dc.SetPen(wx.Pen(orange,1))
		dc.SetBrush(wx.Brush(yellow))
		
			
		dc.SetPen(wx.Pen(white,1))
		if self.occupied==True:
			dc.SetBrush(wx.Brush(white))
			dc.SetPen(wx.Pen(orange,1))
			#if self.occupied:dc.DrawRectangleRect(rect)
			
		"""
		#Fill all spots
		dc.SetBrush(wx.Brush(yellow))
		dc.SetPen(wx.Pen(orange,1))
		dc.DrawRectangleRect(rect)
		"""
		
		
		#Rectangles now overlapping by dy/2
		#dc.DrawRectangleRect(rect)
		
		if self.amline==True:
			if self.amledger==False:
				dc.SetPen(wx.Pen(black,1))
				dc.DrawLine(self.x,(self.yidx/2.+0.5)*self.dy,(self.x+self.dx),(self.yidx/2.+0.5)*self.dy)
			elif self.amledger==True and self.occupied==True:
				dc.SetPen(wx.Pen(red,1))
				dc.DrawLine(self.x,(self.yidx/2.+0.5)*self.dy,(self.x+self.dx),(self.yidx/2.+0.5)*self.dy)
			else:
				pass#don't draw unoccupied ledger lines
							
		if self.occupied==True:
			for vidx in range(len(self.visitors)):
				visitor=self.visitors[vidx]
				dc.DrawBitmap(visitor.bmp,visitor.x,visitor.y,True)
		
