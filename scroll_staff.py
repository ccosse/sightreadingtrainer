"""
**********************************************************

    Author          :Charles Brissac

    Email           :cdbrissac@gmail.com

    License         :GPLv3

***********************************************************
"""
import java,javax
from java import awt
from java.awt import *
from javax import swing
from javax.swing import *
import math,random,thread,time
from random import random
from mfcinstrument import *
from tile import *
from music import *

DEBUG=False


class PopupActionListener(awt.event.ActionListener):
	def __init__(self,parent,callback):
		self.callback=callback
		self.parent=parent

	def actionPerformed(self,e):
		if DEBUG:print 'actionPerformed'
		if DEBUG:print e.getSource().getText()
		self.callback(e)

class foo(java.awt.event.ActionListener):
	def __init__(self,parent,callback):
		self.parent=parent
		self.callback=callback

	def actionPerformed(self,e):
		self.callback(e)

class ScrollStaff(MFCInstrument,JPanel,awt.event.KeyListener,javax.swing.event.ChangeListener,java.awt.event.ActionListener):

	def SetTreble(self,e):
		self.TREBLE=e.getSource().getSelectedItem()
		if self.TREBLE=="None":self.TREBLE=None

	def SetBass(self,e):
		self.BASS=e.getSource().getSelectedItem()
		if self.BASS=="None":self.BASS=None

	def treble_modeCB(self,e):
		note_mode=e.getActionCommand()
		self.common_modeCB(note_mode,"TREBLE")

	def bass_modeCB(self,e):
		note_mode=e.getActionCommand()
		self.common_modeCB(note_mode,"BASS")

	def common_modeCB(self,note_mode,clef):#get rid e so callable from @init to produce 2x lists

		if DEBUG:
			print 'common_modeDB note_mode=',note_mode,' clef=',clef

		if note_mode=="Single":
			if self.active_note_modes[clef]['Single']:
				self.active_note_modes[clef]['Single']=False
			else:
				self.active_note_modes[clef]['Single']=True
		elif note_mode=="Double":
			if self.active_note_modes[clef]['Double']:
				self.active_note_modes[clef]['Double']=False
			else:
				self.active_note_modes[clef]['Double']=True
		elif note_mode=="Chord":
			if self.active_note_modes[clef]['Chord']:
				self.active_note_modes[clef]['Chord']=False
			else:
				self.active_note_modes[clef]['Chord']=True

		if DEBUG:print self.active_note_modes
		#Enable menu toggles:

		#Build active_modes list:
		active_modes=[]
		item_count=0
		if clef=='BASS':item_count=self.lh_structs_menu.getItemCount()
		elif clef=='TREBLE':item_count=self.rh_structs_menu.getItemCount()
		key=None
		for idx in range(item_count):
			if DEBUG:print 'idx=',idx#some of these are separators!
			try:

				#Never disable these guys...
				if clef=='BASS':
					if self.lh_structs_menu.getItem(idx).getLabel()=="Single":key="Single"
					elif self.lh_structs_menu.getItem(idx).getLabel()=="Double":key="Double"
					elif self.lh_structs_menu.getItem(idx).getLabel()=="Chord":key="Chord"
				elif clef=='TREBLE':
					if self.rh_structs_menu.getItem(idx).getLabel()=="Single":key="Single"
					elif self.rh_structs_menu.getItem(idx).getLabel()=="Double":key="Double"
					elif self.rh_structs_menu.getItem(idx).getLabel()=="Chord":key="Chord"

				if DEBUG:print 'key=',key

				if self.active_note_modes[clef][key]:#if enabled then setEnabled(True)

					if clef=='BASS':
						dummy=self.note_struct_subtoggles[key].index(self.lh_structs_menu.getItem(idx).getLabel())
						self.lh_structs_menu.getItem(idx).setEnabled(True)
						if self.lh_structs_menu.getItem(idx).getState():
							active_modes.append(self.lh_structs_menu.getItem(idx).getLabel())#toggled
					elif clef=='TREBLE':
						dummy=self.note_struct_subtoggles[key].index(self.rh_structs_menu.getItem(idx).getLabel())
						self.rh_structs_menu.getItem(idx).setEnabled(True)
						if self.rh_structs_menu.getItem(idx).getState():
							active_modes.append(self.rh_structs_menu.getItem(idx).getLabel())#toggled
				#else:
				#	if clef=='BASS':self.lh_structs_menu.getItem(idx).setEnabled(False)
				#	elif clef=='TREBLE':self.rh_structs_menu.getItem(idx).setEnabled(False)

			except Exception,e:pass

		if DEBUG:print 'active_modes=',active_modes
		if clef=='TREBLE':self.active_treble_modes=active_modes
		elif clef=='BASS':self.active_bass_modes=active_modes
		else:print 'wtf?'

		tooltip=""
		for idx in range(len(active_modes)):
			tooltip+='%s, '%active_modes[idx]
		if clef=='BASS':self.lh_structs_menu.setToolTipText(tooltip)
		elif clef=='TREBLE':self.rh_structs_menu.setToolTipText(tooltip)

	def bass_subtoggleCB(self,e):
		self.common_subtoggleCB("BASS",e)

	def treble_subtoggleCB(self,e):
		self.common_subtoggleCB("TREBLE",e)

	def common_subtoggleCB(self,clef,e):
		if DEBUG:print 'common_subtoggleCB',clef
		if e:
			label=e.getSource().getLabel()
			if clef=="TREBLE":
				try:
					idx=self.active_treble_modes.index(label)
					self.active_treble_modes.pop(idx)
				except:
					self.active_treble_modes.append(label)
					if DEBUG:print 'added ',label,' to active_treble_modes'
			if clef=="BASS":
				try:
					idx=self.active_bass_modes.index(label)
					self.active_bass_modes.pop(idx)
				except:
					self.active_bass_modes.append(label)
					if DEBUG:print 'added ',label,' to active_base_modes'

	def keysigCB(self,e):
		if DEBUG:print 'keysigCB: ',e.getSource().getText()
		self.SetKeySig(e)

	def active_staff_regionsCB(self,e):
		self.active_staff_regions[e.getSource().getText()]=e.getSource().getState()

	def minorCB(self,e):
		if self.MINOR:self.MINOR=False
		else:self.MINOR=True

	def __init__(self,orch,hostname,W,resolution,nbars,barwidth):

		MFCInstrument.__init__(self,'Staff',hostname,[Color.ORANGE],True)
		self.setLayout(BorderLayout())

		self.RUNNING=False
		self.CONTINUOUS_LEDGERS=False
		self.FORCE_ACCIDENTAL=False
		self.orch=orch
		self.W=W
		self.H=300
		self.resolution=resolution
		self.nbars=nbars
		self.barwidth=barwidth

		self.active_bass_modes=[]
		self.active_treble_modes=[]

		self.char_width=10#in place of spot width?
		self.staff_width_for_centering=self.nbars*(4*resolution+1)*self.char_width*3

		self.debug_panel=None

		self.xplay=int(self.W/2)

		self.dxdt=-20
		self.dt=0

		framesizeY=awt.Dimension(0,self.H)
		vfill=Box.Filler(framesizeY,framesizeY,framesizeY)
		self.add(vfill,'West')

		self.cp=JPanel()
		self.cp.setLayout(FlowLayout())
		#self.cp.setLayout(BorderLayout())

		#############################################################################
		#This matters for note generation:
		self.active_staff_regions={
			'upper treble ledgers':True,
			'treble clef':True,
			'lower treble ledgers':True,
			'upper bass ledgers':True,
			'bass clef':True,
			'lower bass ledgers':True
		}
		viewmenu=JMenu('ActiveRegions')
		view_menu_items=[
			JCheckBoxMenuItem('upper treble ledgers',self.active_staff_regions['upper treble ledgers'],actionPerformed=self.active_staff_regionsCB),
			JCheckBoxMenuItem('treble clef',self.active_staff_regions['treble clef'],actionPerformed=self.active_staff_regionsCB),
			JCheckBoxMenuItem('lower treble ledgers',self.active_staff_regions['lower treble ledgers'],actionPerformed=self.active_staff_regionsCB),
			JCheckBoxMenuItem('upper bass ledgers',self.active_staff_regions['upper bass ledgers'],actionPerformed=self.active_staff_regionsCB),
			JCheckBoxMenuItem('bass clef',self.active_staff_regions['bass clef'],actionPerformed=self.active_staff_regionsCB),
			JCheckBoxMenuItem('lower bass ledgers',self.active_staff_regions['lower bass ledgers'],actionPerformed=self.active_staff_regionsCB),
		]
		for vidx in range(len(view_menu_items)):
			viewmenu.add(view_menu_items[vidx])

		#################################################################################
		self.active_note_modes={
			"BASS":{
				"Single":True,
				"Double":False,
				"Chord":False
			},
			"TREBLE":{
				"Single":False,
				"Double":True,
				"Chord":False
			},
		}

		lh_structs_menu=JMenu('LH Structs')
		rh_structs_menu=JMenu('RH Structs')
		self.note_struct_subtoggles={
			"Single":["Single"],#,"Consecutive","Scale"
			"Double":["Double"],#["Major 2nd","Major 3rd","Pefrect 4th","Perfect 5th","6th","7th","8th","9th","10th","11th"],
			"Chord":["Chord"]#['Major','Minor','Diminished','Augmented','Major 6','Minor 6','7','Major 7','Minor 7','7 Flat 5','7 Sharp 5','Diminished 7','9','7 Flat 9','7 Sharp 9','Major 7 +9','9 Flat 5','11','Augmented 11','13','13 Flat 9']
		}


		lh_dummy=JCheckBoxMenuItem('Single',False,actionPerformed=self.bass_modeCB)
		rh_dummy=JCheckBoxMenuItem('Single',False,actionPerformed=self.treble_modeCB)
		lh_dummy.setState(True)
		#rh_dummy.setState(True)
		lh_structs_menu.add(JSeparator())
		rh_structs_menu.add(JSeparator())
		lh_structs_menu.add(lh_dummy)
		rh_structs_menu.add(rh_dummy)
		"""
		lh_structs_menu.add(JSeparator())
		rh_structs_menu.add(JSeparator())
		for idx in range(len(self.note_struct_subtoggles['Single'])):
			lh=JCheckBoxMenuItem(self.note_struct_subtoggles['Single'][idx],actionPerformed=self.bass_subtoggleCB,enabled=False)#NEED: subtoggleCB
			rh=JCheckBoxMenuItem(self.note_struct_subtoggles['Single'][idx],actionPerformed=self.treble_subtoggleCB,enabled=False)
			lh.setState(True)
			rh.setState(True)
			lh_structs_menu.add(lh)
			rh_structs_menu.add(rh)
		"""

		lh_dummy=JCheckBoxMenuItem('Double',False,actionPerformed=self.bass_modeCB)
		rh_dummy=JCheckBoxMenuItem('Double',False,actionPerformed=self.treble_modeCB)
		#lh_dummy.setState(True)
		rh_dummy.setState(True)
		lh_structs_menu.add(JSeparator())
		rh_structs_menu.add(JSeparator())
		lh_structs_menu.add(lh_dummy)
		rh_structs_menu.add(rh_dummy)
		"""
		lh_structs_menu.add(JSeparator())
		rh_structs_menu.add(JSeparator())
		for idx in range(len(self.note_struct_subtoggles['Double'])):
			lh=JCheckBoxMenuItem(self.note_struct_subtoggles['Double'][idx],actionPerformed=self.bass_subtoggleCB,enabled=False)
			rh=JCheckBoxMenuItem(self.note_struct_subtoggles['Double'][idx],actionPerformed=self.treble_subtoggleCB,enabled=True)
			lh.setState(True)
			rh.setState(True)
			lh_structs_menu.add(lh)
			rh_structs_menu.add(rh)
		"""

		lh_dummy=JCheckBoxMenuItem('Chord',False,actionPerformed=self.bass_modeCB)
		rh_dummy=JCheckBoxMenuItem('Chord',False,actionPerformed=self.treble_modeCB)
		#lh_dummy.setState(True)
		#rh_dummy.setState(True)
		lh_structs_menu.add(JSeparator())
		rh_structs_menu.add(JSeparator())
		lh_structs_menu.add(lh_dummy)
		rh_structs_menu.add(rh_dummy)
		"""
		lh_structs_menu.add(JSeparator())
		rh_structs_menu.add(JSeparator())
		for idx in range(len(self.note_struct_subtoggles['Chord'])):
			lh=JCheckBoxMenuItem(self.note_struct_subtoggles['Chord'][idx],actionPerformed=self.bass_subtoggleCB,enabled=False)
			rh=JCheckBoxMenuItem(self.note_struct_subtoggles['Chord'][idx],actionPerformed=self.treble_subtoggleCB,enabled=False)
			lh.setState(True)
			rh.setState(True)
			lh_structs_menu.add(lh)
			rh_structs_menu.add(rh)
		"""

		menubar=JMenuBar()
		menubar.add(viewmenu)
		self.lh_structs_menu=lh_structs_menu
		self.rh_structs_menu=rh_structs_menu
		menubar.add(self.lh_structs_menu)
		menubar.add(self.rh_structs_menu)

		#self.cp.add(menubar,'North')
		self.cp.add(menubar)

		#calling common_modeCB is unwieldy; also from here.
		self.active_treble_modes=['Double']#self.note_struct_subtoggles['Chord']
		self.active_bass_modes=['Single']#self.note_struct_subtoggles['Chord']

		#############################################################################

		runmenu=JMenu("Run")
		self.runB=JMenuItem("Run",actionPerformed=self.runCB)
		runmenu.add(self.runB)
		menubar.add(runmenu)

		self.scrollB=JButton('Scroll',actionPerformed=self.runCB)
		self.scrollB.setToolTipText('Start scrolling')
		#self.cp.add(self.scrollB)

		self.dxdt=-20
		self.dxdt_spinner=JSpinner(SpinnerNumberModel(-1*self.dxdt,1,99,1))
		self.dxdt_spinner.setToolTipText('Scroll rate [px/sec]')
		self.dxdt_spinner.addChangeListener(self)
		self.cp.add(self.dxdt_spinner)

		self.dtdn=50/10.
		self.dtdn_spinner=JSpinner(SpinnerNumberModel(self.dtdn*10.,1,99,1))
		self.dtdn_spinner.setToolTipText('Note delay x 10 [sec]')
		self.dtdn_spinner.addChangeListener(self)
		self.cp.add(self.dtdn_spinner)

		self.sig_idx=sig_idx=9
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

		#NEED:make radio button group:
		keysigmenu=JMenu('KeySig')
		keysig_button_group=ButtonGroup()
		for kidx in range(len(self.keysigs)):
			sel=False
			if kidx==sig_idx:sel=True
			item=JRadioButtonMenuItem(self.keysigs[kidx],actionPerformed=self.keysigCB,selected=sel)
			keysigmenu.add(item)
			keysig_button_group.add(item)
		menubar.add(keysigmenu)

		#self.keysig_cb=JComboBox(self.keysigs,actionListener=None)#keysigActionListener
		#self.keysig_cb.setSelectedIndex(self.sig_idx)
		#self.cp.add(self.keysig_cb)

		self.MINOR=False
		#self.cp.add(JCheckBox('Minor Key',self.MINOR,actionPerformed=self.minorCB))

		special_menu=JMenu("Special")
		minor_checkbox=JCheckBoxMenuItem("Use Minor",self.MINOR,actionPerformed=self.minorCB)
		special_menu.add(minor_checkbox)
		menubar.add(special_menu)

		"""
		self.note_struct_types=[
			"None",
			"Single",
			"Double",
			"Chord",
			"Any"
		]

		self.bass_mode_menu=JMenu("None")
		menubar.add(self.bass_mode_menu)
		bass_button_group=ButtonGroup()
		bass_buttons=[
			JRadioButtonMenuItem("None",actionPerformed=self.bass_modeCB,selected=True),
			JRadioButtonMenuItem("Single",actionPerformed=self.bass_modeCB,selected=False),
			JRadioButtonMenuItem("Double",actionPerformed=self.bass_modeCB,selected=False),
			JRadioButtonMenuItem("Chord",actionPerformed=self.bass_modeCB,selected=False),
			JRadioButtonMenuItem("Any",actionPerformed=self.bass_modeCB,selected=False)
		]

		for idx in range(len(bass_buttons)):
			self.bass_mode_menu.add(bass_buttons[idx])
			bass_button_group.add(bass_buttons[idx])

		self.BASS=self.note_struct_types[3]
		self.bass_cb=JComboBox(self.note_struct_types,actionListener=None)
		self.bass_cb.setSelectedIndex(3)
		self.cp.add(self.bass_cb)

		self.TREBLE=self.note_struct_types[3]
		self.treble_cb=JComboBox(self.note_struct_types,actionListener=None)
		self.treble_cb.setSelectedIndex(3)
		self.cp.add(self.treble_cb)

		self.instrument_cb=JComboBox(self.instlist,actionListener=self)
		self.cp.add(self.instrument_cb)
		"""

		greenLine=BorderFactory.createLineBorder(java.awt.Color(0,200,0))
		border=BorderFactory.createTitledBorder(greenLine,'Staff')
		self.cp.setBorder(border)
		self.add(self.cp,'South')
		self.hilighted=[]

		self.tempo=[4,4]
		self.sig_idx=6
		self.nx_sig_spots=7
		self.xoffset=1+self.nx_sig_spots

		#
		self.music=Music()

		note_img_fname=hostname+'/static/sightreadingtrainer/img/'+"notehead-2.png"
		static_note_img_fname=hostname+'img/'+"notehead-2.png"

		if hostname[0:7]=='http://':
			self.img_dir="/static/sightreadingtrainer/img/"
		else:
			self.img_dir="./img/"

		if hostname[0:7]=='http://':
			self.note_img=ImageIO.read(URL(note_img_fname))

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

		else:
			self.note_img=ImageIO.read(File(static_note_img_fname))

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

		self.note_img_dx=note_img_dx=self.note_img.getWidth()
		note_img_dy=self.note_img.getHeight()
		self.note_img_dy=note_img_dy
		self.spot_dy=note_img_dy

		dy=self.dy=self.note_img_dy
		tidx=len(self.music.tnotes)-1

		from spot import *
		from tile import *

		self.spots=[]
		offset=300
		amline=False
		amledger=False

		y_max=len(self.music.tnotes)-1
		for yidx in range(y_max,-1,-1):

			tlcy=self.H/2-dy-dy/2*(y_max-yidx)
			self.music.tnotes[yidx]['y1']=tlcy
			self.music.tnotes[yidx]['yidx']=yidx
			note=self.music.tnotes[yidx]

			if False:pass
			elif yidx>len(self.music.tnotes)-1-4 and amline==True:amledger=True
			elif yidx>len(self.music.tnotes)-15 and amline==True:amledger=False
			elif amline==True:amledger=True

			for xidx in range(self.nx_sig_spots+1):
				if xidx==0:
					tlcx=offset
					spot=Spot(self.hostname,offset,xidx,tlcx,yidx,tlcy,math.fabs(self.sig_idx),self.treble_clef_img_dx,self.spot_dy,amline,amledger,note)
					self.spots.append(spot)

					if yidx==11:
						t=Tile(self.hostname,self.img_dir,"treble_clef.png",'0',spot.xc,spot.yc)
						spot.TakeVisitor(t)
						spot.lock()
					else:spot.lock()

				elif xidx>0 and xidx<=self.nx_sig_spots:
					tlcx=int(offset+self.treble_clef_img_dx+self.nx_sig_spots*self.sharp_img_dx+(xidx-1-self.nx_sig_spots)*self.sharp_img_dx)
					spot=Spot(self.hostname,offset,xidx,tlcx,yidx,tlcy,math.fabs(self.sig_idx),self.sharp_img_dx,self.spot_dy,amline,amledger,note)
					self.spots.append(spot)

			if amline==False:amline=True
			else:amline=False
			amledger=False


		tidx=0
		amline=False
		amledger=False

		for yidx in range(0,len(self.music.bnotes)):

			tlcy=self.H/2+dy+dy/2*(yidx)
			self.music.bnotes[yidx]['y1']=tlcy
			self.music.bnotes[yidx]['yidx']=len(self.music.tnotes)+yidx
			note=self.music.bnotes[yidx]

			if False:pass
			elif yidx<4 and amline==True:amledger=True
			elif yidx<14 and amline==True:amledger=False
			elif amline==True:amledger=True

			for xidx in range(self.nx_sig_spots+1):

				if xidx==0:
					spot=Spot(self.hostname,offset,xidx,offset,note['yidx'],tlcy,math.fabs(self.sig_idx),self.treble_clef_img_dx,self.spot_dy,amline,amledger,note)
					self.spots.append(spot)
					if yidx==9:
						spot.TakeVisitor(Tile(self.hostname,self.img_dir,"bass_clef.png",'0',spot.xc,spot.yc))
						spot.lock()
					else:spot.lock()

				elif xidx>0 and xidx<=self.nx_sig_spots:
					tlcx=int(offset+self.treble_clef_img_dx+self.nx_sig_spots*self.sharp_img_dx+(xidx-1-self.nx_sig_spots)*self.sharp_img_dx)
					spot=Spot(self.hostname,offset,xidx,tlcx,note['yidx'],tlcy,math.fabs(self.sig_idx),self.sharp_img_dx,self.spot_dy,amline,amledger,note)
					self.spots.append(spot)

			if amline==False:amline=True
			else:amline=False
			amledger=False
			tidx+=1

		self.unlock_sig_spots()
		self.apply_sig(sig_idx)
		self.lock_sig_spots()

		#keysigActionListener=foo(self,self.SetKeySig)
		#self.keysig_cb.actionListener=keysigActionListener

		bassActionListener=foo(self,self.SetBass)
		#self.bass_cb.actionListener=bassActionListener

		trebleActionListener=foo(self,self.SetTreble)
		#self.treble_cb.actionListener=trebleActionListener

	def unlock_sig_spots(self):
		for xidx in range(1,self.nx_sig_spots):
			for yidx in range(0,self.H):
				try:self.FindSpotByIdx(xidx,yidx).unlock()
				except Exception,e:
					pass


	def lock_sig_spots(self):
		if DEBUG:print 'lock_sig_spots'
		for xidx in range(1,self.nx_sig_spots):
			for yidx in range(0,self.H):
				spot=self.FindSpotByIdx(xidx,yidx)
				if not spot:continue
				spot.lock()

	def FindSpotByIdx(self,xidx,yidx):
		for spot in self.spots:
			if spot.xidx==xidx:
				if spot.yidx==yidx:
					return spot
		return None

	def SetKeySig(self,e):
		self.setCursor(java.awt.Cursor(java.awt.Cursor.WAIT_CURSOR))
		self.unlock_sig_spots()
		self.apply_sig(self.keysigs.index(e.getSource().getText()))
		self.lock_sig_spots()
		self.setCursor(java.awt.Cursor(java.awt.Cursor.DEFAULT_CURSOR))
		self.updateUI()

	def apply_sig(self,sig_coord_idx):
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
		"""

		sig_idx=sig_coord_idx-7
		sig_coords=self.sigs[`sig_idx`]['sig_coords']
		self.CURRENT_SIG=self.sigs[`sig_idx`]


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

		self.orch.kbd.allOff(None)
		self.orch.updateUI()
		self.hilighted=[]

		#Erase current keysig: (both clefs)
		for yidx in range(0,self.H):
			for xidx in range (1,self.nx_sig_spots+1):
				spot=self.FindSpotByIdx(xidx,yidx)
				if not spot:continue
				if not spot.occupied:continue
				rval=spot.ReleaseVisitor()
				if rval:self.updateUI()

		#Apply to treble clef sig spots:
		y_max=len(self.music.tnotes)-1
		for yidx in range(y_max,-1,-1):
			tlcy=self.music.tnotes[yidx]['y1']
			for xidx in range (1,self.nx_sig_spots+1):
				for xy in sig_coords:
					if xidx==xy[0] and yidx==xy[1]+7:
						spot=self.FindSpotByIdx(xidx,yidx)
						if spot:
							spot.TakeVisitor(Tile(self.hostname,self.img_dir,img_fname,'0',spot.xc,spot.yc))


		for note in self.music.tnotes:
			note['flat']=False
			note['sharp']=False
			for xy in sig_coords:
				flag=False#NEED:central sharp/flat authority ... given note
				if False:pass
				elif note['yidx']==xy[1]-21:flag=True
				elif note['yidx']==xy[1]-14:flag=True
				elif note['yidx']==xy[1]-7:flag=True
				elif note['yidx']==xy[1]+0:flag=True
				elif note['yidx']==xy[1]+7:flag=True
				elif note['yidx']==xy[1]+14:flag=True
				elif note['yidx']==xy[1]+21:flag=True
				if flag:
					#is it sharp or flat? (it is one of the two since sig_coord match ... but need to query spot? other way? )
					#we set sharp/flat flag here in apply_sig so when matching random notes obtained from kbd we can set it's y1
					sig=self.sigs[`sig_idx`]
					if len(sig['sharplist']):note['sharp']=True
					elif len(sig['flatlist']):note['flat']=True


		#Apply to bass clef sig spots:
		#for yidx in range(self.H/2+5,self.H/2+15):
		for yidx in range(0,len(self.music.bnotes)):
			for xidx in range (1,self.nx_sig_spots+1):
				for xy in sig_coords:
					if xidx==xy[0] and yidx==xy[1]+7:
						spot=self.FindSpotByIdx(xidx,yidx+len(self.music.tnotes))
						if spot:
							spot.TakeVisitor(Tile(self.hostname,self.img_dir,img_fname,'0',spot.xc,spot.yc))


		for note in self.music.bnotes:
			note['flat']=False
			note['sharp']=False
			for xy in sig_coords:
				flag=False
				if False:pass
				elif note['yidx']-len(self.music.tnotes)==xy[1]-21:flag=True
				elif note['yidx']-len(self.music.tnotes)==xy[1]-14:flag=True
				elif note['yidx']-len(self.music.tnotes)==xy[1]-7:flag=True
				elif note['yidx']-len(self.music.tnotes)==xy[1]+0:flag=True
				elif note['yidx']-len(self.music.tnotes)==xy[1]+7:flag=True
				elif note['yidx']-len(self.music.tnotes)==xy[1]+14:flag=True
				elif note['yidx']-len(self.music.tnotes)==xy[1]+21:flag=True
				if flag:
					#is it sharp or flat? (it is one of the two since sig_coord match ... but need to query spot? other way? )
					#we set sharp/flat flag here in apply_sig so when matching random notes obtained from kbd we can set it's y1
					sig=self.sigs[`sig_idx`]
					if len(sig['sharplist']):note['sharp']=True
					elif len(sig['flatlist']):note['flat']=True


	def actionPerformed(self,e):
		if DEBUG:print 'scroll_staff.actionPerformed: calling self.instrumentCB ...'
		self.instrumentCB(e)

	def paintComponent(self,g):
		g.setColor(awt.Color.WHITE)
		g.fillRect(0,0,2*self.W,2*self.H)
		g.setColor(awt.Color.BLACK)

		#return

		for spot in self.spots:
			spot.render(g)

		#since drawing staff/tab lines between moving notes
		#need to keep running index per string of current
		#xprogress/staff_length_for_centering
		x0=self.W/2-self.staff_width_for_centering/2
		xmax=self.W/2+self.staff_width_for_centering/2
		xprogress=[]
		for idx in range(len(self.music.tnotes)+len(self.music.bnotes)+1):
			xprogress.append(x0)


		amline=False
		amledger=False
		tidx=len(self.music.tnotes)-1
		dy=self.note_img_dy

		LEDGER_COLOR=awt.Color.GREEN

		y_max=len(self.music.tnotes)-1
		for yidx in range(y_max,-1,-1):
			y1=self.music.tnotes[yidx]['y1']+self.dy/2

			note=self.music.tnotes[yidx]
			if False:pass
			elif tidx>len(self.music.tnotes)-1-4 and amline==True:amledger=True
			elif tidx>len(self.music.tnotes)-15 and amline==True:amledger=False
			elif amline==True:amledger=True

			if amline and amledger and self.CONTINUOUS_LEDGERS:
				#print 'RED',y1
				g.setColor(LEDGER_COLOR)
				g.drawLine(min(int(xprogress[yidx]),xmax),y1,xmax,y1)
			elif amline and not amledger:
				#print 'BLACK',y1
				g.setColor(awt.Color.BLACK)
				g.drawLine(min(int(xprogress[yidx]),xmax),y1,xmax,y1)
			else:#SPACE
				pass

			if amline==False:amline=True
			else:amline=False
			amledger=False
			tidx-=1

		#Now for bottom notes (H/2+1 -> down)
		tidx=0
		amline=False
		amledger=False

		for yidx in range(0,len(self.music.bnotes)):
			y1=self.music.bnotes[yidx]['y1']+self.dy/2

			if False:pass
			elif yidx<4 and amline==True:amledger=True
			elif yidx<14 and amline==True:amledger=False
			elif amline==True:amledger=True

			if amline and amledger and self.CONTINUOUS_LEDGERS:
				#print 'RED',y1
				g.setColor(LEDGER_COLOR)
				g.drawLine(min(int(xprogress[tidx]),xmax),y1,xmax,y1)
			elif amline and not amledger:
				#print 'BLACK',y1
				g.setColor(awt.Color.BLACK)
				g.drawLine(min(int(xprogress[tidx]),xmax),y1,xmax,y1)
			else:pass

			if amline==False:amline=True
			else:amline=False
			amledger=False
			tidx+=1

		for idx in range(len(self.hilighted)):
			g.drawImage(self.note_img,int(self.hilighted[idx]['xscroll']),int(self.hilighted[idx]['y1']),self)
			if self.hilighted[idx]['isaccidental']:
				if False:pass
				elif self.hilighted[idx]['sharp']:
					g.drawImage(self.sharp_img,int(self.hilighted[idx]['xscroll']-self.sharp_img_dx),int(self.hilighted[idx]['y1']-10),self)
				elif self.hilighted[idx]['flat']:
					g.drawImage(self.flat_img,int(self.hilighted[idx]['xscroll']-self.flat_img_dx),int(self.hilighted[idx]['y1']-14),self)
				else:
					g.drawImage(self.natural_img,int(self.hilighted[idx]['xscroll']-self.natural_img_dx),int(self.hilighted[idx]['y1']-10),self)

			if True:# and self.hilighted[idx]['amline']:

				#NEED:loop over dy ltd to ledger ys
				#How for above/below are we? are we bass or treble? use staff region to define dy; use ?? to define Ndy
				#construct list-of-ledger segs here(?)
				#PROBLEM: midi is modified for sharp/flat ... so getting by midi will miss some notes
				if not self.hilighted[idx].has_key('y1'):
					print 'no y1 key'
					continue

				staff_region=self.music.getStaffRegionUsingY1(self.hilighted[idx]['y1'])
				if staff_region:

					#Getting by midi and drawing on staff, then need to acct for sharp/flat in midi:
					midi=self.hilighted[idx]['midi']
					if self.hilighted[idx]['sharp']:midi-=1
					elif self.hilighted[idx]['flat']:midi+=1

					if not self.hilighted[idx]['ylist']:
						self.hilighted[idx]['ylist']=self.music.getLedgerList(self.note_img_dy,midi,staff_region)#later:add this permanently to note{} and call locally within music when generating

					ylist=self.hilighted[idx]['ylist']

					for yidx in range(len(ylist)):
						g.setColor(awt.Color.RED)
						g.drawLine(
							int(self.hilighted[idx]['xscroll']-2),
							int(ylist[yidx]),
							int(self.hilighted[idx]['xscroll']+self.note_img_dx+2),
							int(ylist[yidx])
						)

				else:
					print 'no staff region'

			#still part of idx loop:
			self.hilighted[idx]['xscroll']+=self.dxdt*self.dt

		#don't want to pop while looping (ie above)
		for idx in range(len(self.hilighted)):
			if self.hilighted[idx]['xscroll']<x0:
				self.hilighted[idx]['ylist']=None
				popped_note=self.hilighted.pop(idx)
				if DEBUG:print `popped_note`
				break#idx max just changed.

		for idx in range(len(self.hilighted)):
			if self.hilighted[idx]['played']==2:continue
			elif self.hilighted[idx]['played']==1:
				if time.time()-self.hilighted[idx]['toff']>0:
					#MIDI NOTE OFF:
					#self.cpCB(None)

					###################################
					#RESTORE SPECIFIC KEY DEFAULT COLOR
					if DEBUG:print 'scroll_staff turning off specific key'
					self.orch.kbd.keyOff(self.orch.kbd.getKeyByMidi(self.hilighted[idx]['midi']))
					self.cpCB(None)
					###################################

					if self.keyboardChannel:
						self.keyboardChannel.noteOff(self.hilighted[idx]['midi'],80)
						self.hilighted[idx]['played']=2
					else:
						msg=ShortMessage()
						msg.setMessage(ShortMessage.NOTE_OFF,0,self.hilighted[idx]['midi'],80)
						self.rcv.send(msg,-1)
						self.hilighted[idx]['played']=2

					#NOTE RESET:
					if self.hilighted[idx]['sharp']:self.hilighted[idx]['midi']-=1
					if self.hilighted[idx]['flat']:self.hilighted[idx]['midi']+=1
					#self.hilighted[idx]['isaccidental']=0


				continue

			dx=self.hilighted[idx]['xscroll']-self.xplay
			if DEBUG:print `dx`
			if dx<10:
				if dx>-10:
					if DEBUG:print 'PLAYING NOTE'
					self.cpCB(self.hilighted[idx])
					self.orch.kbdCB(self.hilighted[idx]['midi'])

					#PLAY MIDI:
					self.send(self.hilighted[idx]['midi'],-1)
					self.hilighted[idx]['played']=1
					self.hilighted[idx]['toff']=time.time()+1.
					"""
					if self.keyboardChannel:
						self.keyboardChannel.noteOn(self.hilighted[idx]['midi'],80)
						self.hilighted[idx]['played']=1
						self.hilighted[idx]['toff']=time.time()+1.
					else:
						msg=ShortMessage()
						msg.setMessage(ShortMessage.NOTE_ON,0,self.hilighted[idx]['midi'],80)
						self.rcv.send(msg,-1)
						self.hilighted[idx]['played']=1
						self.hilighted[idx]['toff']=time.time()+1.
					"""

		g.setColor(awt.Color.RED)
		g.drawLine(self.W/2,0,self.W/2,self.H)

	def send(self,midi,tstamp):
		if self.keyboardChannel:
			if DEBUG:print 'scroll_staff.send (keyboardChannel):',midi,tstamp
			self.keyboardChannel.noteOn(midi,80)
		else:
			if DEBUG:print 'scroll_staff.send (rcv):',midi,tstamp
			msg=ShortMessage()
			msg.setMessage(ShortMessage.NOTE_ON,0,midi,80)
			self.rcv.send(msg,tstamp)

	def sendOFF(self,midi,tstamp):
		if self.keyboardChannel:
			if DEBUG:print 'scroll_staff.sendOFF (keyboardChannel):',midi,tstamp
			self.keyboardChannel.noteOff(midi,80)
		else:
			if DEBUG:print 'scroll_staff.sendOFF (rcv):',midi,tstamp
			msg=ShortMessage()
			msg.setMessage(ShortMessage.NOTE_OFF,0,midi,80)
			self.rcv.send(msg,tstamp)


	def stateChanged(self,e):
		#print 'staff.stateChanged'
		#print e.getSource().getValue()

		if e.getSource()==self.dxdt_spinner:
			self.dxdt=(-1)*e.getSource().getValue()
			if DEBUG:print self.dxdt

		elif e.getSource()==self.dtdn_spinner:
			self.dtdn=e.getSource().getValue()/10.
			if DEBUG:print self.dtdn
		else:
			print 'unknown src'

	def runThread(self,*args):
		if DEBUG:print 'staff.runThread'
		if len(args)<1:return
		msg=args[0]

		t0=time.time()
		tlast=time.time()
		self.dt=0

		tnext=t0

		while self.RUNNING:

			#keep running for smoothe updateUI; schedule time for next note.
			t=time.time()

			#################################################################
			#NEW NOTE GENERATION OCCURS HERE:

			if t>=tnext:

				common_midi=None

				snotes=None
				if len(self.active_treble_modes)==0 and len(self.active_bass_modes)>0:
					if DEBUG:print 'calling getBassNotes'
					snotes=self.music.getNotes("Bass",self.CURRENT_SIG,self.MINOR,self.active_bass_modes,self.active_staff_regions)
				elif len(self.active_bass_modes)==0 and len(self.active_treble_modes)>0:
					if DEBUG:print 'calling getTrebleNotes'
					snotes=self.music.getNotes("Treble",self.CURRENT_SIG,self.MINOR,self.active_treble_modes,self.active_staff_regions)
				elif len(self.active_treble_modes)>0 and len(self.active_bass_modes)>0:
					if random()>0.5:
						if DEBUG:print 'calling getTrebleNotes'
						snotes=self.music.getNotes("Treble",self.CURRENT_SIG,self.MINOR,self.active_treble_modes,self.active_staff_regions)
					else:
						if DEBUG:print 'calling getBassNotes'
						snotes=self.music.getNotes("Bass",self.CURRENT_SIG,self.MINOR,self.active_bass_modes,self.active_staff_regions)

				if not snotes:continue
				if len(snotes)<1:continue
				if not snotes[0]:continue

				if DEBUG:print 'snotes',snotes

				for sidx in range(len(snotes)):

					common_midi=snotes[sidx]['midi']
					if snotes[sidx]['sharp']:common_midi+=1
					elif snotes[sidx]['flat']:common_midi-=1

					note=None
					if DEBUG:print 'common_midi=',common_midi
					note=self.orch.generate('Staff',common_midi)
					note['sharp']=snotes[sidx]['sharp']
					note['flat']=snotes[sidx]['flat']

					if self.FORCE_ACCIDENTAL:
						if not note['sharp'] and not note['flat'] and not note['isaccidental']:
							note['isaccidental']=1
							if random()>0.6:
								note['sharp']=1
								note['midi']+=1
							elif random()>0.5:
								note['flat']=1
								note['midi']-=1
							elif random()>0.5:pass#natural
							else:note['isaccidental']=0#let it go ...

					if not note:self.runCB(None);return

					note['y1']=snotes[sidx]['y1']
					note['amline']=snotes[sidx]['amline']
					if DEBUG:print 'note',note,''

					#At this point, note(=kbd.note) has staff.y1 and kbd.midi ... so we're done! (just need to fix in paintComponent not to adjust for sharp/flat)
					#also, the note no longer needs/knows about sharp/flat (it's not part of kbd note struct)

					#except we need to set this:
					note['xscroll']=self.W/2+self.staff_width_for_centering/2

					#so just add the note and we're done:
					self.hilighted.append(note)

				tnext=t+self.dtdn

			#################################################################

			self.dt=t-tlast
			tlast=t
			self.updateUI()
			time.sleep(.05)

		if DEBUG:print "staff.runThread exited cleanly"

	def registerCB(self,cpCB):
		self.cpCB=cpCB

	def runCB(self,e):
		if DEBUG:print 'staff.runCB'
		if self.RUNNING==True:
			self.RUNNING=False
			self.scrollB.setText("Scroll")
			self.runB.setText("Scroll")
		else:
			self.RUNNING=True
			thread.start_new_thread(self.runThread,("this is gonna be a keeper",))
			self.scrollB.setText("Stop ")
			self.runB.setText("Stop")


	def mksigs(self):
		if DEBUG:print 'mksigs'
		sigs={
			'-7':{
				'majkey':'C Flat Major',
				'minkey':'A Flat Minor',
				'flatlist':['B','E','A','D','G','C','F'],
				'sharplist':[],
				'sigkey':'-7',
				'sig_coords':[(1,4),(2,1),(3, 5),(4,2),(5,6),(6,3),(7,7)],
				'minkey_midi_roots':[32,44,56,68,80,92,104],
				'majkey_midi_roots':[23,35,47,59,71,83,95,107]
			},
			'-6':{
				'majkey':'G Flat Major',
				'minkey':'E Flat Minor',
				'flatlist':['B','E','A','D','G','C'],
				'sharplist':[],
				'sigkey':'-6',
				'sig_coords':[(1,4),(2,1),(3, 5),(4,2),(5,6),(6,3)],
				'minkey_midi_roots':[27,39,51,63,75,87,99],
				'majkey_midi_roots':[30,42,54,66,78,90,102]
			},
			'-5':{
				'majkey':'D Flat Major',
				'minkey':'B Flat Minor',
				'flatlist':['B','E','A','D','G'],
				'sharplist':[],
				'sigkey':'-5',
				'sig_coords':[(1,4),(2,1),(3, 5),(4,2),(5,6)],
				'minkey_midi_roots':[22,34,46,58,70,82,94,106],
				'majkey_midi_roots':[25,37,49,61,73,85,97]
			},
			'-4':{
				'majkey':'A Flat Major',
				'minkey':'F Minor',
				'flatlist':['B','E','A','D'],
				'sharplist':[],
				'sigkey':'-4',
				'sig_coords':[(1,4),(2,1),(3, 5),(4,2)],
				'minkey_midi_roots':[29,41,53,65,77,89,101],
				'majkey_midi_roots':[32,44,56,68,80,92,104]
			},
			'-3':{
				'majkey':'E Flat Major',
				'minkey':'C Minor',
				'flatlist':['B','E','A'],
				'sharplist':[],
				'sigkey':'-3',
				'sig_coords':[(1,4),(2,1),(3, 5)],
				'minkey_midi_roots':[24,36,48,60,72,84,96,108],
				'majkey_midi_roots':[27,39,51,63,75,87,99]
			},
			'-2':{
				'majkey':'B Flat Major',
				'minkey':'G Minor',
				'flatlist':['B','E'],
				'sharplist':[],
				'sigkey':'-2',
				'sig_coords':[(1,4),(2,1)],
				'minkey_midi_roots':[31,43,55,67,79,91,103],
				'majkey_midi_roots':[22,34,46,58,70,82,94,106]
			},
			'-1':{
				'majkey':'F Major',
				'minkey':'D Minor',
				'flatlist':['B'],
				'sharplist':[],
				'sigkey':'-1',
				'sig_coords':[(1,4)],
				'minkey_midi_roots':[26,38,50,62,74,86,98],
				'majkey_midi_roots':[29,41,53,65,77,89,101]
			},
			'0':{
				'majkey':'C Major',
				'minkey':'A Minor',
				'flatlist':[],
				'sharplist':[],
				'sigkey':'0',
				'sig_coords':[],
				'minkey_midi_roots':[21,33,45,57,69,81,93,105],
				'majkey_midi_roots':[24,36,48,60,72,84,96,108]
			},
			'1':{
				'majkey':'G Major',
				'minkey':'E Minor',
				'flatlist':[],
				'sharplist':['F'],
				'sigkey':'1',
				'sig_coords':[(1,0)],
				'minkey_midi_roots':[28,40,52,64,76,88,100],
				'majkey_midi_roots':[31,43,55,67,79,91,103]
			},
			'2':{
				'majkey':'D Major',
				'minkey':'B Minor',
				'flatlist':[],
				'sharplist':['F','C'],
				'sigkey':'2',
				'sig_coords':[(1,0),(2,3)],
				'minkey_midi_roots':[23,35,47,59,71,83,95,107],
				'majkey_midi_roots':[26,38,50,62,74,86,98]
			},
			'3':{
				'majkey':'A Major',
				'minkey':'F Sharp Minor',
				'flatlist':[],
				'sharplist':['F','C','G'],
				'sigkey':'3',
				'sig_coords':[(1,0),(2,3),(3,-1)],
				'minkey_midi_roots':[30,42,54,66,78,90,102],
				'majkey_midi_roots':[21,33,45,57,69,81,93,105]
			},
			'4':{
				'majkey':'E Major',
				'minkey':'C Sharp Minor',
				'flatlist':[],
				'sharplist':['F','C','G','D'],
				'sigkey':'4',
				'sig_coords':[(1,0),(2,3),(3,-1),(4,2)],
				'minkey_midi_roots':[28,40,52,64,76,88,100],
				'majkey_midi_roots':[31,43,55,67,79,91,103]
			},
			'5':{
				'majkey':'B Major',
				'minkey':'G Sharp Minor',
				'flatlist':[],
				'sharplist':['F','C','G','D','A'],
				'sigkey':'5',
				'sig_coords':[(1,0),(2,3),(3,-1),(4,2),(5,5)],
				'minkey_midi_roots':[32,44,56,68,80,92,104],
				'majkey_midi_roots':[23,35,47,59,71,83,95,107]
			},
			'6':{
				'majkey':'F Sharp Major',
				'minkey':'D Sharp Minor',
				'flatlist':[],
				'sharplist':['F','C','G','D','A','E'],
				'sigkey':'6',
				'sig_coords':[(1,0),(2,3),(3,-1),(4,2),(5,5),(6,1)],
				'minkey_midi_roots':[27,39,51,63,75,87,99],
				'majkey_midi_roots':[30,42,54,66,78,90,102]
			},
			'7':{
				'majkey':'C Sharp Major',
				'minkey':'A Sharp Minor',
				'flatlist':[],
				'sharplist':['F','C','G','D','A','E','B'],
				'sigkey':'7',
				'sig_coords':[(1,0),(2,3),(3,-1),(4,2),(5,5),(6,1),(7,4)],
				'minkey_midi_roots':[22,34,46,58,70,82,94,106],
				'majkey_midi_roots':[25,37,49,61,73,85,97]
			},
		}
		return sigs
