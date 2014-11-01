import java
from java import awt
from java.awt import FlowLayout,BorderLayout,Dimension
from javax import swing
from java.net import *
from java.io import File
from javax.imageio import ImageIO
from javax.swing import *
from javax.sound.midi import *

from spot import *
from tile import *
import math,random,thread,time
from pyld import *

DEBUG=True

class PopupActionListener(java.awt.event.ActionListener):
	def __init__(self,parent,callback):
		self.callback=callback
		self.parent=parent
	
	def actionPerformed(self,e):
		if DEBUG:print 'actionPerformed'
		print e.getSource().getText()
		self.callback(e)	

class GStaff(JPanel,java.awt.event.KeyListener):

	def __init__(self,frame,hostname,W,resolution,nbars,barwidth):
		self.frame=frame
		self.hostname=hostname
		self.resolution=resolution
		self.nbars=nbars
		self.barwidth=barwidth
		
		JPanel.__init__(self)
		#self.myparent=myparent
		
		self.SHOW_STAFF=True
		
		#H=Number of lines in staff(2)
		self.H=50
		
		#self.WIN_W=600
		#self.WIN_H=300
		self.setSize(W,400)
		self.size=self.getSize()

		self.scan_tlcx=0
		self.scan_tlcy=0
		self.scan_lrcx=1
		self.scan_lrcy=self.size.width
		

		#self.setSize(600,300)
		
		self.tempo=[4,4]
		self.sig_idx=6
		self.nx_sig_spots=7
		self.xoffset=1+self.nx_sig_spots
		
		self.img_dir="./img/"
		
		self.sigs=self.mksigs()
		self.keysigs=[
			"B  (G#m)",
			"Gb (Ebm)",
			"Db (Bbm)",
			"Ab (Fm)", 
			"Eb (Cm)", 
			"Bb (Gm)", 
			"F  (Dm)", 
			"C  (Am)", 
			"G  (Em)", 
			"D  (Bm)", 
			"A  (F#m)",
			"E  (C#m)",
			"B  (G#m)",
			"F# (D#m)",
			"C# (Bbm)",
		]
		"""
		img_prefixes=["treble_clef","sharp","flat","natural","skullbones"]
		img_names=["treble_clef.png","sharp.png","flat.png","natural.png","skullbones.png"]
		for idx in range(len(img_names)):
			fname=img_names[idx]
			prefix=img_prefixes[idx]
		"""
		if hostname[0:7]=='http://':
			self.treble_clef_img=ImageIO.read(URL(hostname+self.img_dir+'treble_clef.png'))
			self.treble_clef_img_dx=self.treble_clef_img.getWidth()
			self.treble_clef_img_dy=self.treble_clef_img.getHeight()

			self.sharp_img=ImageIO.read(URL(hostname+self.img_dir+'sharp.png'))
			self.sharp_img_dx=self.sharp_img.getWidth()
			self.sharp_img_dy=self.sharp_img.getHeight()

			self.flat_img=ImageIO.read(URL(hostname+self.img_dir+'flat.png'))
			self.flat_img_dx=self.flat_img.getWidth()
			self.flat_img_dy=self.flat_img.getHeight()

			self.natural_img=ImageIO.read(URL(hostname+self.img_dir+'natural.png'))
			self.natural_img_dx=self.natural_img.getWidth()
			self.natural_img_dy=self.natural_img.getHeight()

			self.skullbones_img=ImageIO.read(URL(hostname+self.img_dir+'skullbones.png'))
			self.skullbones_img_dx=self.skullbones_img.getWidth()
			self.skullbones_img_dy=self.skullbones_img.getHeight()

			
		else:
			self.treble_clef_img=ImageIO.read(File(hostname+self.img_dir+'treble_clef.png'))
			self.treble_clef_img_dx=self.treble_clef_img.getWidth()
			self.treble_clef_img_dy=self.treble_clef_img.getHeight()

			self.sharp_img=ImageIO.read(File(hostname+self.img_dir+'sharp.png'))
			self.sharp_img_dx=self.sharp_img.getWidth()
			self.sharp_img_dy=self.sharp_img.getHeight()

			self.flat_img=ImageIO.read(File(hostname+self.img_dir+'flat.png'))
			self.flat_img_dx=self.flat_img.getWidth()
			self.flat_img_dy=self.flat_img.getHeight()

			self.natural_img=ImageIO.read(File(hostname+self.img_dir+'natural.png'))
			self.natural_img_dx=self.natural_img.getWidth()
			self.natural_img_dy=self.natural_img.getHeight()

			self.skullbones_img=ImageIO.read(File(hostname+self.img_dir+'skullbones.png'))
			self.skullbones_img_dx=self.skullbones_img.getWidth()
			self.skullbones_img_dy=self.skullbones_img.getHeight()

		#
		note_images=[
			'notehead-0.png',
			'notehead-1.png',
			'notehead-2.png',
		]
		if hostname[0:7]=='http://':
			note_img=ImageIO.read(URL(hostname+self.img_dir+note_images[0]))
		else:
			note_img=ImageIO.read(File(hostname+self.img_dir+note_images[0]))
		note_img_dx=note_img.getWidth()
		note_img_dy=note_img.getHeight()


		self.spot_dx=self.barwidth/(4*resolution)
		self.spot_dy=note_img_dy
		staff_width_for_centering=self.treble_clef_img_dx+self.nx_sig_spots*self.sharp_img_dx+self.nbars*(4*resolution+1)*self.spot_dx
		if DEBUG:print 'staff_width_for_centering=',staff_width_for_centering
		if DEBUG:print self.treble_clef_img_dx
		if DEBUG:print self.nx_sig_spots*self.sharp_img_dx
		if DEBUG:print 'spot_dx=',self.spot_dx
		if DEBUG:print 'resolution=',resolution
		if DEBUG:print 'nbars=',self.nbars
		if DEBUG:print self.nbars*(4*resolution+2)*self.spot_dx
		if DEBUG:print ''
		
		self.spots=self.mkSpots(staff_width_for_centering)
		self.occupied_spots=[]
		
		sig_idx=9
		self.sig_idx=sig_idx
		
		self.unlock_sig_spots()
		self.apply_sig(sig_idx)
		self.lock_sig_spots()
		
		#Reqs spots; here in case SHOW_STAFF=0
		x0y0=self.FindSpotByIdx(self.xoffset,self.H/2-14)
		x1y1=self.FindSpotByIdx(self.xoffset,self.H/2-6)
		self.scan_xmin=x1y1.xc
		self.scan_tlcx=int(self.scan_xmin)
		self.scan_ymin=x0y0.yc
		x1y1=self.FindSpotByIdx(self.xidx_last_spot()-1,self.H/2+14)
		self.scan_ymax=x1y1.yc
		self.scan_xmax=self.size.width
		
		
		self.mousePressed=self.pressCB
		self.mouseReleased=self.releaseCB
		self.mouseMoved=self.moveCB
		self.mouseDragged=self.dragCB
		
		self.setFocusable(True)
		self.addKeyListener(self)
		
		#self.keyPressed=self.keyPressCB
		#self.keyReleased=self.keyReleaseCB
		#self.keyTyped=self.keyTypeCB
		#self.setFocusTraversalKeysEnabled(False)
		
		self.CTRL_DOWN=False
		self.drag_visitor=None
		self.tlcxy=None
		self.lrcxy=None
		self.copy_rect=java.awt.Rectangle()
		self.copy_struct=[]
		self.crosshair_cursor=java.awt.Cursor(java.awt.Cursor.CROSSHAIR_CURSOR)
		self.default_cursor=java.awt.Cursor(java.awt.Cursor.DEFAULT_CURSOR)
		self.updateUI()
		
		#print dir(self)
		self.requestDefaultFocus()
		
		#
		popup_action_listener=PopupActionListener(self,self.actionCB)
		actions=['Delete','QuarterNote','HalfNote','WholeNote','QuarterRest','HalfRest','WholeRest']
		self.action_menu=JPopupMenu('Actions')
		for aidx in range(len(actions)):
			item=JMenuItem(actions[aidx])
			item.addActionListener(popup_action_listener)
			self.action_menu.add(item)

		item=JMenuItem('QuarterNote')
		item.addActionListener(popup_action_listener)
		self.action_menu.add(item)
		
		self.right_mouse_down_position=None
		
	def copyCB(self):
		if DEBUG:print 'copyCB'
		
		min_xidx=1E7
		min_yidx=0
		max_xidx=0
		max_yidx=self.H
		
		selected_spots=[]
		for spot in self.spots:
			if self.copy_rect.contains(spot.xc,spot.yc):
				selected_spots.append(spot)

		for spot in selected_spots:
			if spot.xidx<min_xidx:min_xidx=spot.xidx
			if spot.xidx>max_xidx:max_xidx=spot.xidx
		
		self.copy_struct=[]
		for yidx in range(min_yidx,max_yidx):
			row=[]
			for xidx in range(min_xidx,max_xidx):
				spot=self.FindSpotByIdx(xidx,yidx)
				if not spot:row.append(None)
				elif not spot.occupied:row.append(None)
				else:
					#NEED:somehow copy accidentals
					t=Tile(self.hostname,spot.visitors[0].img_dir,spot.visitors[0].img_fname,spot.visitors[0].duration,spot.xc,spot.yc)
					row.append(t)
			self.copy_struct.append(row)
		
	def pasteCB(self):
		if DEBUG:print 'pasteCB'
		if not self.tlcxy:
			print 'no tlcxy'
			return
		if len(self.copy_struct)==0:
			print 'no copy_struct'
			return
		
		print 'self.paste_point=',self.tlcxy
		occupied=False#arg to GetNearestSpot ... rethink soon!
		spot=self.GetNearestSpot(self.tlcxy[0],self.tlcxy[1])
		if not spot:
			print 'abort: failed to get spot'
			return
			
		min_xidx=spot.xidx
		min_yidx=0
		max_xidx=spot.xidx+len(self.copy_struct[0])
		max_yidx=self.H
		
		for yidx in range(min_yidx,max_yidx):
			for xidx in range(min_xidx,max_xidx):
				try:
					target=self.FindSpotByIdx(xidx,yidx)
					if not target:continue
					if not self.copy_struct[yidx][xidx-spot.xidx]:continue#None for unoccupied spots in copy_struct
					try:
						target.TakeVisitor(self.copy_struct[yidx][xidx-spot.xidx])
						self.occupied_spots.append(target)
						#dc = wx.ClientDC(self)
						#target.render(dc)
						#print 'copied'
					except Exception,e:
						#print 'copy failure'
						print yidx,xidx-spot.xidx,len(self.copy_struct),len(self.copy_struct[0]),e
					
				except Exception,e:
					print 'pasteCB Exception: ',e
					pass
				
		#print 'self.copy_struct=',self.copy_struct
		self.copy_struct=[]
		self.updateUI()

	def cutCB(self):
		if DEBUG:print 'copyCB'
		
		min_xidx=1E7
		min_yidx=0
		max_xidx=0
		max_yidx=self.H
		
		selected_spots=[]
		for spot in self.spots:
			if self.copy_rect.contains(spot.xc,spot.yc):
				selected_spots.append(spot)

		for spot in selected_spots:
			if spot.xidx<min_xidx:min_xidx=spot.xidx
			if spot.xidx>max_xidx:max_xidx=spot.xidx
		
		self.copy_struct=[]
		for yidx in range(min_yidx,max_yidx):
			row=[]
			for xidx in range(min_xidx,max_xidx):
				spot=self.FindSpotByIdx(xidx,yidx)
				if not spot:row.append(None)
				elif not spot.occupied:row.append(None)
				else:
					#NEED:somehow copy accidentals
					#t=Tile(self.hostname,spot.visitors[0].img_dir,spot.visitors[0].img_fname,spot.visitors[0].duration,spot.xc,spot.yc)
					t=spot.ReleaseVisitor()
					row.append(t)
			self.copy_struct.append(row)
		self.updateUI()	

	def FindSpotByIdx(self,xidx,yidx):
		for spot in self.spots:
			if spot.xidx==xidx:
				if spot.yidx==yidx:
					return spot

	def GetNearestSpot(self,x,y):
		target=None
		rmin=1000.
		for spot in self.spots:
			r=math.sqrt(pow(math.fabs(x-spot.xc),2)+pow(math.fabs(y-spot.yc),2))
			if r<rmin:
				rmin=r
				target=spot
		return target	


	def keyPressed(self,e):
		if DEBUG:print 'keyCB',e.getKeyCode()#,e.getKeyChar()
		if e.getKeyCode()==java.awt.event.KeyEvent.VK_CONTROL:self.CTRL_DOWN=True
		elif e.getKeyCode()==67:#C
			if self.CTRL_DOWN:
				if DEBUG:print 'calling copyCB'
				self.copyCB()
		elif e.getKeyCode()==86:#V
			if self.CTRL_DOWN:
				if DEBUG:print 'calling pasteCB'
				self.pasteCB()
		elif e.getKeyCode()==88:#X
			if self.CTRL_DOWN:
				if DEBUG:print 'calling cutCB'
				self.cutCB()
		else:
			print e.getKeyCode()#,e.getKeyChar()
		
	def keyReleased(self,e):
		if DEBUG:print 'keyReleaseCB'
		if e.getKeyCode()==java.awt.event.KeyEvent.VK_CONTROL:self.CTRL_DOWN=False
		pass

	def keyTyped(self,e):
		#print 'keyTypeCB'
		pass	
	
	def dragCB(self,e):
		#if DEBUG:print 'dragCB'
		if self.action_menu.isVisible():
			#hilight button
			#self.action_menu.isVisible()
			self.lrcxy=None
			print 'need hilight menu item'
			return
		
		if self.drag_visitor:
			pass#self.updateUI()
		else:
			self.lrcxy=(e.getX(),e.getY())
		
		#Either way:		
		self.updateUI()
	
	def actionCB(self,e):

		if DEBUG:print 'actionCB',e.getSource().getText()

		if not self.right_mouse_down_position:return
		spot=self.GetNearestSpot(self.right_mouse_down_position.x,self.right_mouse_down_position.y)

		if not spot:return
		elif spot.islocked():return
		
		#1. Delete whatever's there:
		if spot and spot.isoccupied():
			tile2delete=spot.ReleaseVisitor()
			del(tile2delete)
			self.updateUI()
		
		action=e.getSource().getText()
		if action=='Delete':pass
		elif action=='QuarterNote':
			spot.TakeVisitor(Tile(self.hostname,self.img_dir,"notehead-2.png",'1',spot.xc,spot.yc))
		elif action=='HalfNote':
			spot.TakeVisitor(Tile(self.hostname,self.img_dir,"notehead-1.png",'2',spot.xc,spot.yc))
		elif action=='WholeNote':
			spot.TakeVisitor(Tile(self.hostname,self.img_dir,"notehead-0.png",'4',spot.xc,spot.yc))
		elif action=='QuarterRest':
			spot.TakeVisitor(Tile(self.hostname,self.img_dir,"r4.png",'1',spot.xc,spot.yc))
		elif action=='HalfRest':
			spot.TakeVisitor(Tile(self.hostname,self.img_dir,"r2.png",'2',spot.xc,spot.yc))
		elif action=='WholeRest':
			spot.TakeVisitor(Tile(self.hostname,self.img_dir,"r1.png",'4',spot.xc,spot.yc))
		
			
		self.action_menu.setVisible(False)
		self.right_mouse_down_position=None
		self.updateUI()
		
	def show_action_menu(self,e):
		if DEBUG:print 'show_action_menu'
		#self.action_menu.grabFocus()
		self.action_menu.show(e.getComponent(),e.getX(), e.getY());

	def pressCB(self,e):
		
		if e.getButton()==java.awt.event.MouseEvent.BUTTON3:
			self.right_mouse_down_position=self.getMousePosition()
			self.show_action_menu(e)
			return
			
		self.grabFocus()
		self.lrcxy=None
		if DEBUG:print 'pressCB'
		self.tlcxy=(e.getX(),e.getY())
		#print self.tlcxy
		self.setCursor(self.crosshair_cursor)
		
		target_spot=None
		rmin=1000
		for spot in self.spots:
			if spot.rect.contains(e.getX(),e.getY()):
				r=math.sqrt(pow(math.fabs(e.getX()-spot.xc),2)+pow(math.fabs(e.getY()-spot.yc),2))
				if r<rmin and spot.isoccupied():
					rmin=r
					target_spot=spot
		
		if target_spot:
			self.drag_visitor=target_spot.ReleaseVisitor()
			print self.drag_visitor
					
		
	def releaseCB(self,e):
		
		if self.action_menu.isVisible():
			self.action_menu.setVisible(False)
			self.lrcxy=None
			self.setCursor(self.default_cursor)
			return
			
		self.grabFocus()
		self.setCursor(self.default_cursor)
		
		if DEBUG:print 'releaseCB'
		
		if not self.drag_visitor:
			self.lrcxy=(e.getX(),e.getY())
			if DEBUG:print self.lrcxy
		
		else:
			target_spot=None
			rmin=1000
			for spot in self.spots:
				if spot.rect.contains(e.getX(),e.getY()):
					r=math.sqrt(pow(math.fabs(e.getX()-spot.xc),2)+pow(math.fabs(e.getY()-spot.yc),2))
					if r<rmin and not spot.isoccupied():
						rmin=r
						target_spot=spot
			if target_spot:
				target_spot.TakeVisitor(self.drag_visitor)
		
		self.drag_visitor=None#lost to oblivion if not released over vacant spot!
		self.updateUI()
		
	def moveCB(self,e):
		#print 'moveCB'
		
		pass
		
	def check_if_barline(self,xidx):
		if xidx==self.xoffset:return True
		for bidx in range(self.nbars):
			if xidx==self.xoffset+bidx*(self.tempo[0]*self.resolution+1):return True
		if xidx==self.xidx_last_spot():return True

	def xidx_last_spot(self):
		#1 clef
		#2 sig spots
		#3 bars*tempo*resolution
		return self.xoffset+(self.nbars)+self.nbars*self.tempo[0]*self.resolution

	def mkSpots(self,staff_width_for_centering):
		if DEBUG:print 'mkSpots'
		
		offset=int((self.getSize().width-staff_width_for_centering)/2)
		if offset<0:offset=0
		
		if DEBUG:print 'self.size=',self.getSize()
		if DEBUG:print 'staff_width_for_centering=',staff_width_for_centering
		if DEBUG:print 'offset=',offset
		
		spots=[]
		
		tnotes=[

			{'ly':"f'''"	,'midi':89	,'sharp':False, 'flat':False},
			{'ly':"e'''"	,'midi':88	,'sharp':False, 'flat':False},
			{'ly':"d'''"	,'midi':86	,'sharp':False, 'flat':False},
			{'ly':"c'''"	,'midi':84	,'sharp':False, 'flat':False},

			{'ly':"b''"		,'midi':83	,'sharp':False, 'flat':False},
			{'ly':"a''"		,'midi':81	,'sharp':False, 'flat':False},
			{'ly':"g''"		,'midi':79	,'sharp':False, 'flat':False},
			{'ly':"f''"		,'midi':77	,'sharp':False, 'flat':False},

			{'ly':"e''"		,'midi':76	,'sharp':False, 'flat':False},
			{'ly':"d''"		,'midi':74	,'sharp':False, 'flat':False},
			{'ly':"c''"		,'midi':72	,'sharp':False, 'flat':False},
			{'ly':"b'"		,'midi':71	,'sharp':False, 'flat':False},

			{'ly':"a'"		,'midi':69	,'sharp':False, 'flat':False},
			{'ly':"g'"		,'midi':67	,'sharp':False, 'flat':False},
			{'ly':"f'"		,'midi':65	,'sharp':False, 'flat':False},
			{'ly':"e'"		,'midi':64	,'sharp':False, 'flat':False},

			{'ly':"d'"		,'midi':62	,'sharp':False, 'flat':False},
			{'ly':"c'"		,'midi':60	,'sharp':False, 'flat':False},
			{'ly':"b"		,'midi':59	,'sharp':False, 'flat':False},
			{'ly':"a"		,'midi':57	,'sharp':False, 'flat':False},
			
			{'ly':"g"		,'midi':55	,'sharp':False, 'flat':False},#H/2-1 (first space above H/2)
			
		]
		
		#----------------------------------H/2 Unoccupied--------------------------------  H/2
		
		
		bnotes=[
			{'ly':"f'"		,'midi':65	,'sharp':False, 'flat':False},#H/2+1 (first space below H/2)

			{'ly':"e'"		,'midi':64	,'sharp':False, 'flat':False},
			{'ly':"d'"		,'midi':62	,'sharp':False, 'flat':False},
			{'ly':"c'"		,'midi':60	,'sharp':False, 'flat':False},
			{'ly':"b"		,'midi':59	,'sharp':False, 'flat':False},

			{'ly':"a"		,'midi':57	,'sharp':False, 'flat':False},
			{'ly':"g"		,'midi':55	,'sharp':False, 'flat':False},
			{'ly':"f"		,'midi':53	,'sharp':False, 'flat':False},
			{'ly':"e"		,'midi':52	,'sharp':False, 'flat':False},

			{'ly':"d"		,'midi':50	,'sharp':False, 'flat':False},
			{'ly':"c"		,'midi':48	,'sharp':False, 'flat':False},
			{'ly':"b,"		,'midi':47	,'sharp':False, 'flat':False},
			{'ly':"a,"		,'midi':45	,'sharp':False, 'flat':False},

			{'ly':"g,"		,'midi':43	,'sharp':False, 'flat':False},
			{'ly':"f,"		,'midi':41	,'sharp':False, 'flat':False},
			{'ly':"e,"		,'midi':40	,'sharp':False, 'flat':False},
			{'ly':"d,"		,'midi':38	,'sharp':False, 'flat':False},

			{'ly':"c,"		,'midi':36	,'sharp':False, 'flat':False},
			{'ly':"b,,"		,'midi':35	,'sharp':False, 'flat':False},
			{'ly':"a,,"		,'midi':33	,'sharp':False, 'flat':False},
			{'ly':"g,,"		,'midi':31	,'sharp':False, 'flat':False},

			{'ly':"f,,"		,'midi':29	,'sharp':False, 'flat':False},
			{'ly':"e,,"		,'midi':28	,'sharp':False, 'flat':False},
			{'ly':"d,,"		,'midi':26	,'sharp':False, 'flat':False},
			{'ly':"c,,"		,'midi':24	,'sharp':False, 'flat':False},

		]
		
		tidx=len(tnotes)-1
		amline=False
		amledger=False
		
		#Top notes (H/2-1 -> up)
		for yidx in range(self.H/2-1,max(0,self.H/2-1-len(tnotes)),-1):
			note=tnotes[tidx]
			
			if False:pass
			elif tidx>len(tnotes)-1-4 and amline==True:amledger=True
			elif tidx>len(tnotes)-15 and amline==True:amledger=False
			elif amline==True:amledger=True
			
			
			for xidx in range(self.xidx_last_spot()):
				if xidx==0:
					spot=Spot(self.hostname,offset,xidx,yidx,math.fabs(self.sig_idx),self.treble_clef_img_dx,self.spot_dy,amline,amledger,note)
					spots.append(spot)
		
					if tidx==11:
						t=Tile(self.hostname,self.img_dir,"treble_clef.png",'0',spot.xc,spot.yc)
						spot.TakeVisitor(t)
						spot.lock()
					else:spot.lock()
		
				elif xidx>0 and xidx<=self.nx_sig_spots:
					spot=Spot(self.hostname,offset,xidx,yidx,math.fabs(self.sig_idx),self.sharp_img_dx,self.spot_dy,amline,amledger,note)
					spots.append(spot)
				
				elif self.check_if_barline(xidx):
					spot=Spot(self.hostname,offset,xidx,yidx,math.fabs(self.sig_idx),self.spot_dx,self.spot_dy,amline,amledger,note)
					spot.lock()
					spots.append(spot)
					
				else:
					spot=Spot(self.hostname,offset,xidx,yidx,math.fabs(self.sig_idx),self.spot_dx,self.spot_dy,amline,amledger,note)
					spots.append(spot)
				
				
			if amline==False:amline=True
			else:amline=False
			amledger=False
			tidx-=1
		
			
		
		#Now for bottom notes (H/2+1 -> down)
		tidx=0
		amline=False
		amledger=False
		
		for yidx in range(self.H/2+1,min(self.H,self.H/2+len(bnotes))):
			
			note=bnotes[tidx]
			
			if False:pass
			elif tidx<4 and amline==True:amledger=True
			elif tidx<14 and amline==True:amledger=False
			elif amline==True:amledger=True
			
			for xidx in range(self.xidx_last_spot()):
				
				if xidx==0:
					spot=Spot(self.hostname,offset,xidx,yidx,math.fabs(self.sig_idx),self.treble_clef_img_dx,self.spot_dy,amline,amledger,note)
					spots.append(spot)
					if yidx==self.H/2+10:
						spot.TakeVisitor(Tile(self.hostname,self.img_dir,"bass_clef.png",'0',spot.xc,spot.yc))
						spot.lock()
					else:spot.lock()
					
				elif xidx>0 and xidx<=self.nx_sig_spots:
					spot=Spot(self.hostname,offset,xidx,yidx,math.fabs(self.sig_idx),self.sharp_img_dx,self.spot_dy,amline,amledger,note)
					spots.append(spot)
					
				elif self.check_if_barline(xidx):
					spot=Spot(self.hostname,offset,xidx,yidx,math.fabs(self.sig_idx),self.spot_dx,self.spot_dy,amline,amledger,note)
					spot.lock()
					spots.append(spot)
					
				else:
					spot=Spot(self.hostname,offset,xidx,yidx,math.fabs(self.sig_idx),self.spot_dx,self.spot_dy,amline,amledger,note)
					spots.append(spot)
				
			if amline==False:amline=True
			else:amline=False
			amledger=False
			tidx+=1
		
		return spots

	
	def mksigs(self):
		if DEBUG:print 'mksigs'
		sigs={
			'-7':{
				'majkey':'C Flat Major',
				'minkey':'A Flat Minor',
				'flatlist':['B','E','A','D','G','C','F'],
				'sharplist':[],
				'sigkey':'-7',
				'sig_coords':[(1,4),(2,1),(3, 5),(4,2),(5,6),(6,3),(7,7)]
			},
			'-6':{
				'majkey':'G Flat Major',
				'minkey':'E Flat Minor',
				'flatlist':['B','E','A','D','G','C'],
				'sharplist':[],
				'sigkey':'-6',
				'sig_coords':[(1,4),(2,1),(3, 5),(4,2),(5,6),(6,3)]
			},
			'-5':{
				'majkey':'D Flat Major',
				'minkey':'B Flat Minor',
				'flatlist':['B','E','A','D','G'],
				'sharplist':[],
				'sigkey':'-5',
				'sig_coords':[(1,4),(2,1),(3, 5),(4,2),(5,6)]
			},
			'-4':{
				'majkey':'A Flat Major',
				'minkey':'F Minor',
				'flatlist':['B','E','A','D'],
				'sharplist':[],
				'sigkey':'-4',
				'sig_coords':[(1,4),(2,1),(3, 5),(4,2)]
			},
			'-3':{
				'majkey':'E Flat Major',
				'minkey':'C Minor',
				'flatlist':['B','E','A'],
				'sharplist':[],
				'sigkey':'-3',
				'sig_coords':[(1,4),(2,1),(3, 5)]
			},
			'-2':{
				'majkey':'B Flat Major',
				'minkey':'G Minor',
				'flatlist':['B','E'],
				'sharplist':[],
				'sigkey':'-2',
				'sig_coords':[(1,4),(2,1)]
			},
			'-1':{
				'majkey':'F Major',
				'minkey':'D Minor',
				'flatlist':['B'],
				'sharplist':[],
				'sigkey':'-1',
				'sig_coords':[(1,4)]
			},
			'0':{
				'majkey':'C Major',
				'minkey':'A Minor',
				'flatlist':[],
				'sharplist':[],
				'sigkey':'0',
				'sig_coords':[]
			},
			'1':{
				'majkey':'G Major',
				'minkey':'E Minor',
				'flatlist':[],
				'sharplist':['F'],
				'sigkey':'1',
				'sig_coords':[(1,0)]
			},
			'2':{
				'majkey':'D Major',
				'minkey':'B Minor',
				'flatlist':[],
				'sharplist':['F','C'],
				'sigkey':'2',
				'sig_coords':[(1,0),(2,3)]
			},
			'3':{
				'majkey':'A Major',
				'minkey':'F Sharp Minor',
				'flatlist':[],
				'sharplist':['F','C','G'],
				'sigkey':'3',
				'sig_coords':[(1,0),(2,3),(3,-1)]
			},
			'4':{
				'majkey':'E Major',
				'minkey':'C Sharp Minor',
				'flatlist':[],
				'sharplist':['F','C','G','D'],
				'sigkey':'4',
				'sig_coords':[(1,0),(2,3),(3,-1),(4,2)]
			},
			'5':{
				'majkey':'B Major',
				'minkey':'G Sharp Minor',
				'flatlist':[],
				'sharplist':['F','C','G','D','A'],
				'sigkey':'5',
				'sig_coords':[(1,0),(2,3),(3,-1),(4,2),(5,5)]
			},
			'6':{
				'majkey':'F Sharp Major',
				'minkey':'D Sharp Minor',
				'flatlist':[],
				'sharplist':['F','C','G','D','A','E'],
				'sigkey':'6',
				'sig_coords':[(1,0),(2,3),(3,-1),(4,2),(5,5),(6,1)]
			},
			'7':{
				'majkey':'C Sharp Major',
				'minkey':'A Sharp Minor',
				'flatlist':[],
				'sharplist':['F','C','G','D','A','E','B'],
				'sigkey':'7',
				'sig_coords':[(1,0),(2,3),(3,-1),(4,2),(5,5),(6,1),(7,4)]
			},
		}
		return sigs
			
	def apply_sig(self,sig_coord_idx):
		
		if DEBUG:print 'apply_sig',sig_coord_idx
		
		#This repaints both toolbar and menu-over-panel:
		#rect2refresh=wx.Rect(0,0,800,600)
		#self.parent.RefreshRect(rect2refresh,True)
		#self.parent.Update()
		
		sig_idx=sig_coord_idx-7
		"""
		sigs=[
				{'sig_coords':[(1,4),(2,1),(3, 5),(4,2),(5,6),(6,3),(7,7)]},#-7
				{'sig_coords':[(1,4),(2,1),(3, 5),(4,2),(5,6),(6,3)]},#-6
				{'sig_coords':[(1,4),(2,1),(3, 5),(4,2),(5,6)]},#-5
				{'sig_coords':[(1,4),(2,1),(3, 5),(4,2)]},#-4
				{'sig_coords':[(1,4),(2,1),(3, 5)]},#-3
				{'sig_coords':[(1,4),(2,1)]},#-2
				{'sig_coords':[(1,4)]},#-1
				{'sig_coords':[]},#+0
				{'sig_coords':[(1,0)]},#+1
				{'sig_coords':[(1,0),(2,3)]},#+2
				{'sig_coords':[(1,0),(2,3),(3,-1)]},#+3
				{'sig_coords':[(1,0),(2,3),(3,-1),(4,2)]},#+4
				{'sig_coords':[(1,0),(2,3),(3,-1),(4,2),(5,5)]},#+5
				{'sig_coords':[(1,0),(2,3),(3,-1),(4,2),(5,5),(6,1)]},#+6
				{'sig_coords':[(1,0),(2,3),(3,-1),(4,2),(5,5),(6,1),(7,4)]},#+7
			]
		sig_coords=sigs[sig_coord_idx]['sig_coords']
		"""
		
		sig_coords=self.sigs[`sig_idx`]['sig_coords']
		
		#print sig_coords
		#sys.exit()
		
		if sig_idx<0:
			img_fname="flat.png"
			isflat=True
			issharp=False
		elif sig_idx==0:
			img_fname=""
			isflat=False
			issharp=False
		else:
			img_fname="sharp.png"
			isflat=False
			issharp=True
		
		#dc = wx.ClientDC(self)
		#self.PrepareDC(dc)
		
		#Erase current keysig: (both clefs)
		for yidx in range(0,self.H):
			for xidx in range (1,self.xoffset):
				spot=self.FindSpotByIdx(xidx,yidx)
				if not spot:
					#print 'no spot @ ',yidx,xidx,' H/2=',self.H/2
					continue
				if not spot.occupied:continue
				#rect2refresh=wx.Rect(spot.xc-spot.visitors[0].w2,spot.yc-spot.visitors[0].h2,spot.xc+spot.visitors[0].w2,spot.yc+spot.visitors[0].h2)
				rval=spot.ReleaseVisitor()
				if rval:
					#self.myparent.updateUI()
					#self.super__updateUI()
					print 'would be myparent.updateUI()'

				#	self.RefreshRect(rect2refresh, True)
					self.updateUI()
				
				#spot.render(dc)
		
		#Erase keysig settings for notes: (both clefs)	
		for yidx in range(0,self.H):
			for xidx in range (self.xoffset,self.xidx_last_spot()):
				spot=self.FindSpotByIdx(xidx,yidx)
				if not spot:continue
				spot.note['flat']=False
				spot.note['sharp']=False
				
		#Apply to treble clef sig spots:		
		for yidx in range(self.H/2-15,self.H/2-5):
			for xidx in range (1,self.xoffset):
				for xy in sig_coords:
					if xidx==xy[0] and yidx==self.H/2-15+xy[1]+1:
						spot=self.FindSpotByIdx(xidx,yidx)
						spot.TakeVisitor(Tile(self.hostname,self.img_dir,img_fname,'0',spot.xc,spot.yc))
						#spot.render(self.getGraphics())
						
		#Apply to treble clef note spots:		
		for yidx in range(self.H/2-15,self.H/2-5):
			for xidx in range (1,self.xoffset):
				for xy in sig_coords:
					if xidx==xy[0] and yidx==self.H/2-15+xy[1]+1:
						ylist=[]
						if not isflat and not issharp:ylist=[]
						else:ylist=[yidx-7,yidx,yidx+7]
						for yyidx in ylist:
							if yyidx>self.H/2:continue
							if yyidx<0:continue
							for xxidx in range(self.xoffset,self.xidx_last_spot()):
								try:
									sspot=self.FindSpotByIdx(xxidx,yyidx)
									sspot.note['flat']=isflat
									sspot.note['sharp']=issharp
								except Exception,e:
									#print xxidx,yyidx,e
									pass
									
		#Apply to bass clef sig spots:
		for yidx in range(self.H/2+5,self.H/2+15):
			for xidx in range (1,self.xoffset):
				for xy in sig_coords:
					if xidx==xy[0] and yidx==self.H/2+5+xy[1]+3:
						spot=self.FindSpotByIdx(xidx,yidx)
						spot.TakeVisitor(Tile(self.hostname,self.img_dir,img_fname,'0',spot.xc,spot.yc))
						#spot.render(self.getGraphics())
						
		
		#Apply to bass clef note spots:		
		for yidx in range(self.H/2+5,self.H/2+15):
			for xidx in range (1,self.xoffset):
				for xy in sig_coords:
					if xidx==xy[0] and yidx==self.H/2+5+xy[1]+3:
						ylist=[]
						if not isflat and not issharp:ylist=[]
						else:ylist=[yidx-7,yidx,yidx+7]
						for yyidx in ylist:
							if yyidx<self.H/2:continue
							if yyidx>self.H:continue
							for xxidx in range(self.xoffset,self.xidx_last_spot()):
								try:
									sspot=self.FindSpotByIdx(xxidx,yyidx)
									sspot.note['flat']=isflat
									sspot.note['sharp']=issharp
								except Exception,e:
									#print xxidx,yyidx,e
									pass
		
	def FindSpotByIdx(self,xidx,yidx):
		for spot in self.spots:
			if spot.xidx==xidx:
				if spot.yidx==yidx:
					return spot
	
	def setKeySig(self,menu_str):

		sig_idx=self.keysigs.index(menu_str)
		
		self.unlock_sig_spots()
		self.apply_sig(sig_idx)
		self.lock_sig_spots()
		self.sig_idx=sig_idx
		
		#update staff lines
		
		self.updateUI()
		#self.myparent.updateUI()
		#self.super__updateUI()
		#print 'would be myparent.updateUI()'
		
	def unlock_sig_spots(self):
		for xidx in range(1,self.xoffset):
			for yidx in range(0,self.H):
				try:self.FindSpotByIdx(xidx,yidx).unlock()
				except Exception,e:
					pass
					#print xidx,yidx,e
				
	def lock_sig_spots(self):
		if DEBUG:print 'lock_sig_spots'
		for xidx in range(1,self.xoffset):
			for yidx in range(0,self.H):
				spot=self.FindSpotByIdx(xidx,yidx)
				if not spot:continue
				spot.lock()

	def paintComponent(self,g):
		
		if DEBUG:print 'Staff.paintComponent',time.time(),self.getSize()
		
		if self.size!=self.getSize():
			print 'need staff recompute'
			#if have notes on staff, just re-center
			#else:rebuild something
			self.size=self.getSize()
		
		#FROM:scan_test
		self.super__paintComponent(g)

		if self.SHOW_STAFF:
			self.drawMeasureBars(g)
			for spot in self.spots:
				spot.render(g)
		
		#g.setColor(java.awt.Color.RED)
		#g.drawLine(self.scan_tlcx,self.scan_tlcy,self.scan_tlcx,self.scan_lrcy)
		
		if self.drag_visitor:
			#paint img under mouse
			#print self.getMousePosition()
			g.drawImage(self.drag_visitor.img,self.getMousePosition().x-self.drag_visitor.w2,self.getMousePosition().y-self.drag_visitor.h2,self)

		if self.tlcxy!=None and self.lrcxy!=None and not self.drag_visitor:
			g.setColor(java.awt.Color.ORANGE)
			if self.tlcxy[0]<self.lrcxy[0] and self.tlcxy[1]<self.lrcxy[1]:
				self.copy_rect.setRect(self.tlcxy[0],self.tlcxy[1],self.lrcxy[0]-self.tlcxy[0],self.lrcxy[1]-self.tlcxy[1])
				g.drawRect(self.tlcxy[0],self.tlcxy[1],self.lrcxy[0]-self.tlcxy[0],self.lrcxy[1]-self.tlcxy[1])
			elif self.tlcxy[0]<self.lrcxy[0] and self.tlcxy[1]>self.lrcxy[1]:
				self.copy_rect.setRect(self.tlcxy[0],self.lrcxy[1],self.lrcxy[0]-self.tlcxy[0],self.tlcxy[1]-self.lrcxy[1])
				g.drawRect(self.tlcxy[0],self.lrcxy[1],self.lrcxy[0]-self.tlcxy[0],self.tlcxy[1]-self.lrcxy[1])
			elif self.tlcxy[0]>self.lrcxy[0] and self.tlcxy[1]>self.lrcxy[1]:
				self.copy_rect.setRect(self.lrcxy[0],self.lrcxy[1],self.tlcxy[0]-self.lrcxy[0],self.tlcxy[1]-self.lrcxy[1])
				g.drawRect(self.lrcxy[0],self.lrcxy[1],self.tlcxy[0]-self.lrcxy[0],self.tlcxy[1]-self.lrcxy[1])
			elif self.tlcxy[0]>self.lrcxy[0] and self.tlcxy[1]<self.lrcxy[1]:
				self.copy_rect.setRect(self.lrcxy[0],self.tlcxy[1],self.tlcxy[0]-self.lrcxy[0],self.lrcxy[1]-self.tlcxy[1])
				g.drawRect(self.lrcxy[0],self.tlcxy[1],self.tlcxy[0]-self.lrcxy[0],self.lrcxy[1]-self.tlcxy[1])
				
		
	def drawMeasureBars(self,g):
		if DEBUG:print 'drawMeasureBars'
		g.setColor(java.awt.Color.BLACK)
		
		#Draw TOP measure bars:
		x0y0=self.FindSpotByIdx(0,self.H/2-14)
		x1y1=self.FindSpotByIdx(0,self.H/2-6)
		g.drawLine(int(x0y0.xc-x0y0.dx/2),int(x0y0.yc),int(x1y1.xc-x1y1.dx/2),int(x1y1.yc))
		
		x0y0=self.FindSpotByIdx(self.xoffset,self.H/2-14)
		x1y1=self.FindSpotByIdx(self.xoffset,self.H/2-6)
		if self.check_if_barline(x1y1.xidx):
			g.drawLine(int(x0y0.xc),int(x0y0.yc),int(x1y1.xc),int(x1y1.yc))
			self.scan_xmin=x1y1.xc
			self.scan_ymin=x0y0.yc
			
		for bidx in range(1,self.nbars):#self.xoffset+1+bidx*self.tempo[0]*self.resolution+1
			x0y0=self.FindSpotByIdx(self.xoffset+bidx*(self.tempo[0]*self.resolution+1),self.H/2-14)
			x1y1=self.FindSpotByIdx(self.xoffset+bidx*(self.tempo[0]*self.resolution+1),self.H/2-6)
			if self.check_if_barline(x1y1.xidx):
				g.drawLine(int(x0y0.xc),int(x0y0.yc),int(x1y1.xc),int(x1y1.yc))
		
		x0y0=self.FindSpotByIdx(self.xidx_last_spot()-1,self.H/2-14)
		x1y1=self.FindSpotByIdx(self.xidx_last_spot()-1,self.H/2-6)
		self.scan_xmax=x1y1.xc
		g.drawLine(int(x0y0.xc+x0y0.dx/2),int(x0y0.yc),int(x1y1.xc+x1y1.dx/2),int(x1y1.yc))
		
		
		#Draw BOTTOM measure bars:
		x0y0=self.FindSpotByIdx(0,self.H/2+6)
		x1y1=self.FindSpotByIdx(0,self.H/2+14)
		g.drawLine(int(x0y0.xc-x0y0.dx/2),int(x0y0.yc),int(x1y1.xc-x1y1.dx/2),int(x1y1.yc))

		x0y0=self.FindSpotByIdx(self.xoffset,self.H/2+6)
		x1y1=self.FindSpotByIdx(self.xoffset,self.H/2+14)
		g.drawLine(int(x0y0.xc),int(x0y0.yc),int(x1y1.xc),int(x1y1.yc))
		
		for bidx in range(self.nbars):
			x0y0=self.FindSpotByIdx(self.xoffset+bidx*(self.tempo[0]*self.resolution+1),self.H/2+6)
			x1y1=self.FindSpotByIdx(self.xoffset+bidx*(self.tempo[0]*self.resolution+1),self.H/2+14)
			g.drawLine(int(x0y0.xc),int(x0y0.yc),int(x1y1.xc),int(x1y1.yc))
		
		x0y0=self.FindSpotByIdx(self.xidx_last_spot()-1,self.H/2+6)
		x1y1=self.FindSpotByIdx(self.xidx_last_spot()-1,self.H/2+14)
		self.scan_ymax=x1y1.yc
		g.drawLine(int(x0y0.xc+x0y0.dx/2),int(x0y0.yc),int(x1y1.xc+x1y1.dx/2),int(x1y1.yc))

	
	def take_pyld(self,pyld):
		if DEBUG:print 'take_pyld'
		note_images=[
			'notehead-0.png',
			'notehead-1.png',
			'notehead-2.png',
		]
		
		for nidx in range(1):
			spot_idx=int(random.random()*len(self.spots))
			#if nidx==0:spot_idx=len(self.spots)-1
			spot=self.spots[spot_idx]
			#print spot
			tile=Tile(pyld.hostname,pyld.img_dir,pyld.image_names[0],'4',spot.xc,spot.yc)
			#tile=Tile(self.hostname,self.img_dir,note_images[2],'4',spot.xc,spot.yc)
			
			if not spot.islocked():
				spot.TakeVisitor(tile)
				self.occupied_spots.append(spot)
				if DEBUG:print 'bingo',spot.xc,spot.yc
			
			if random.random()<0.5:return
			
			xidx=spot.xidx
			yidx=spot.yidx
			spot1=self.GetSpotByIdx(xidx,yidx+2)
			#print spot1
			if not spot1:continue
			pyld=Pyld(pyld.hostname)
			tile=Tile(pyld.hostname,pyld.img_dir,pyld.image_names[0],'4',spot1.xc,spot1.yc)
			if not spot1.islocked():
				spot1.TakeVisitor(tile)
				self.occupied_spots.append(spot1)
				if DEBUG:print 'bingo',spot1.xc,spot1.yc
			
			if random.random()<0.5:return
			xidx=spot.xidx
			yidx=spot.yidx
			spot1=self.GetSpotByIdx(xidx,yidx-2)
			#print spot1
			if not spot1:continue
			pyld=Pyld(pyld.hostname)
			tile=Tile(pyld.hostname,pyld.img_dir,pyld.image_names[0],'4',spot1.xc,spot1.yc)
			if not spot1.islocked():
				spot1.TakeVisitor(tile)
				self.occupied_spots.append(spot1)
				if DEBUG:print 'bingo',spot1.xc,spot1.yc
			
	def GetSpotByIdx(self,xidx,yidx):
		for spot in self.spots:
			#if not spot.occupied:continue
			if spot.xidx==xidx:
				if spot.yidx==yidx:
					return spot
		return None

	def clear(self):
		if DEBUG:print 'clear'
		for spot in self.spots:
			x=spot.ReleaseVisitor()
		
	def GetRHNotes(self):
		if DEBUG:self.frame.debug_panel.append('GetRHNotes')
		#rval="\t\t\t"
		rval=""
		xmin=self.xoffset
		xmax=self.xidx_last_spot()
		t_elapsed=0
		dt=1./self.tempo[0]
		
		bag_of_notes=[]
		xoffset=self.xoffset
		
		num_col_skipped=0
		
		for xidx in range(xmin,xmax):
			t_elapsed+=dt
			col_group=[]
			
			for yidx in range(0,self.H/2):
				
				spot=self.FindSpotByIdx(xidx,yidx)
				
				if not spot:continue
				
				elif spot.islocked():
					num_col_skipped+=1
					continue
				
				elif spot.occupied:
					
					#convention: any rest supercededs notes this column
					if spot.visitors[0].amrest==True:
						col_group=[{'note':spot.visitors[0].ly,'duration':spot.visitors[0].duration,'xidx':xidx-xoffset}]
						bag_of_notes.append(col_group[len(col_group)-1])
						break
						
					elif spot.accidental!=False:
						#print 'accidental work to spot: ',spot.xidx, spot.yidx,spot.accidental
						if spot.accidental=='es':
							#if not flat by sig -> flat
							if not spot.note['flat']:
								#print 'making flat'
								#col_group.append({'note':spot.note['ly'][:1]+'es'+spot.note['ly'][1:],'duration':spot.visitors[0].duration})
								col_group.append({'note':`spot.note['midi']`,'duration':spot.visitors[0].duration,'xidx':xidx-xoffset})
								bag_of_notes.append(col_group[len(col_group)-1])
								
						elif spot.accidental=='!':
							#if sharp or flat -> natural
							if spot.note['flat'] or spot.note['sharp']:
								#print 'making natural'
								#col_group.append({'note':spot.note['ly'][:1]+''+spot.note['ly'][1:],'duration':spot.visitors[0].duration})
								col_group.append({'note':`spot.note['midi']`,'duration':spot.visitors[0].duration,'xidx':xidx-xoffset})
								bag_of_notes.append(col_group[len(col_group)-1])
								
						elif spot.accidental=='is':
							#if not sharp by sig -> sharp
							if not spot.note['sharp']:
								#print 'making sharp'
								#col_group.append({'note':spot.note['ly'][:1]+'is'+spot.note['ly'][1:],'duration':spot.visitors[0].duration})
								col_group.append({'note':`spot.note['midi']`,'duration':spot.visitors[0].duration,'xidx':xidx-xoffset})
								bag_of_notes.append(col_group[len(col_group)-1])
								
						
					
					elif spot.note['sharp']==True:
						#rval+=spot.note['ly'][:1]+'is'+spot.note['ly'][1:]+spot.visitors[0].duration
						#col_group.append({'note':spot.note['ly'][:1]+'is'+spot.note['ly'][1:],'duration':spot.visitors[0].duration})
						col_group.append({'note':`spot.note['midi']+1`,'duration':spot.visitors[0].duration,'xidx':xidx-xoffset})
						bag_of_notes.append(col_group[len(col_group)-1])
						
					elif spot.note['flat']==True:
						#rval+=spot.note['ly'][:1]+'es'+spot.note['ly'][1:]+spot.visitors[0].duration
						#col_group.append({'note':spot.note['ly'][:1]+'es'+spot.note['ly'][1:],'duration':spot.visitors[0].duration})
						col_group.append({'note':`spot.note['midi']-1`,'duration':spot.visitors[0].duration,'xidx':xidx-xoffset})
						bag_of_notes.append(col_group[len(col_group)-1])
					else:
						#rval+=spot.note['ly']+'4 '
						#col_group.append({'note':spot.note['ly'],'duration':spot.visitors[0].duration})
						self.frame.debug_panel.append('adding note ...')
						col_group.append({'note':`spot.note['midi']`,'duration':spot.visitors[0].duration,'xidx':xidx-xoffset})
						self.frame.debug_panel.append('note added to col_group')
						bag_of_notes.append(col_group[len(col_group)-1])
						self.frame.debug_panel.append('note added to bag_of_notes')
			
			"""			
			if len(col_group)==0:continue
			elif len(col_group)==1:
				rval+=col_group[0]['note']+":"+col_group[0]['duration']+' '
			else:
				rval+="<"
				for cidx in range(len(col_group)):
					rval+=col_group[cidx]['note']
					if cidx<len(col_group)-1:rval+=' '
				rval+=">"+":"+col_group[0]['duration']+' '
				
		#rval+="\n"
		#return rval
			"""
		self.frame.debug_panel.append('returning bag_of_notes')
		return bag_of_notes
	

	def GetLHNotes(self):
		if DEBUG:self.frame.debug_panel.append('GetLHNotes')
		#rval="\t\t\t"
		rval=""
		xmin=self.xoffset
		xmax=self.xidx_last_spot()
		t_elapsed=0
		dt=1./self.tempo[0]
		
		bag_of_notes=[]
		xoffset=self.xoffset
		
		for xidx in range(xmin,xmax):
			t_elapsed+=dt
			col_group=[]
			for yidx in range(self.H/2+1,self.H):
				spot=self.FindSpotByIdx(xidx,yidx)
				if not spot:continue
				if spot.occupied:
					
					#convention: any rest supercededs notes this column
					if spot.visitors[0].amrest==True:
						col_group=[{'note':spot.visitors[0].ly,'duration':spot.visitors[0].duration,'xidx':xidx-xoffset}]
						bag_of_notes.append(col_group[len(col_group)-1])
						break
					
					elif spot.accidental!=False:	
						#NEED: this section from above
						pass
						
					elif spot.note['sharp']==True:
						#rval+=spot.note['ly'][:1]+'is'+spot.note['ly'][1:]+spot.visitors[0].duration
						#col_group.append({'note':spot.note['ly'][:1]+'is'+spot.note['ly'][1:],'duration':spot.visitors[0].duration})
						col_group.append({'note':`spot.note['midi']+1`,'duration':spot.visitors[0].duration,'xidx':xidx-xoffset})
						bag_of_notes.append(col_group[len(col_group)-1])
						
					elif spot.note['flat']==True:
						#rval+=spot.note['ly'][:1]+'es'+spot.note['ly'][1:]+spot.visitors[0].duration
						#col_group.append({'note':spot.note['ly'][:1]+'es'+spot.note['ly'][1:],'duration':spot.visitors[0].duration})
						col_group.append({'note':`spot.note['midi']-1`,'duration':spot.visitors[0].duration,'xidx':xidx-xoffset})
						bag_of_notes.append(col_group[len(col_group)-1])
						
					else:
						#rval+=spot.note['ly']+'4 '
						#col_group.append({'note':spot.note['ly'],'duration':spot.visitors[0].duration})
						col_group.append({'note':`spot.note['midi']`,'duration':spot.visitors[0].duration,'xidx':xidx-xoffset})
						self.frame.debug_panel.append('note added to col_group')
						bag_of_notes.append(col_group[len(col_group)-1])
						self.frame.debug_panel.append('bag_of_notes')
			"""			
			if len(col_group)==0:continue
			elif len(col_group)==1:
				rval+=col_group[0]['note']+":"+col_group[0]['duration']+' '
			else:
				rval+="<"
				for cidx in range(len(col_group)):
					rval+=col_group[cidx]['note']
					if cidx<len(col_group)-1:rval+=' '
				rval+=">"+":"+col_group[len(col_group)-1]['duration']+' '
			"""	
		#rval+="\n"
		#return rval
		self.frame.debug_panel.append('returning bag_of_notes')
		return bag_of_notes

if __name__=='__main__':
	f=JFrame('Staff',visible=False)
	hostname='./'
	staff=GStaff(f,hostname,800,4,4,100)
	staff.take_pyld(Pyld(staff.hostname))
	
	f.add(staff)
	f.pack()
	f.setSize(800,600)
	f.setIconImage(staff.treble_clef_img)
	f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	#print dir(staff)
	f.setVisible(1)
	

