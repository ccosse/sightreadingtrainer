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
from random import random

DEBUG=False

class Music:
	def __init__(self):
		self.tnotes=[

			{'ly':"f'''"	,'midi':89	,'sharp':False, 'flat':False,	'staff_region':'upper treble ledgers',	'amline':False},
			{'ly':"e'''"	,'midi':88	,'sharp':False, 'flat':False,	'staff_region':'upper treble ledgers',	'amline':True},
			{'ly':"d'''"	,'midi':86	,'sharp':False, 'flat':False,	'staff_region':'upper treble ledgers',	'amline':False},
			{'ly':"c'''"	,'midi':84	,'sharp':False, 'flat':False,	'staff_region':'upper treble ledgers',	'amline':True},

			{'ly':"b''"		,'midi':83	,'sharp':False, 'flat':False,	'staff_region':'upper treble ledgers',	'amline':False},
			{'ly':"a''"		,'midi':81	,'sharp':False, 'flat':False,	'staff_region':'upper treble ledgers',	'amline':True},
			{'ly':"g''"		,'midi':79	,'sharp':False, 'flat':False,	'staff_region':'treble clef',			'amline':False},
			{'ly':"f''"		,'midi':77	,'sharp':False, 'flat':False,	'staff_region':'treble clef',			'amline':True},

			{'ly':"e''"		,'midi':76	,'sharp':False, 'flat':False,	'staff_region':'treble clef',			'amline':False},
			{'ly':"d''"		,'midi':74	,'sharp':False, 'flat':False,	'staff_region':'treble clef',			'amline':True},
			{'ly':"c''"		,'midi':72	,'sharp':False, 'flat':False,	'staff_region':'treble clef',			'amline':False},
			{'ly':"b'"		,'midi':71	,'sharp':False, 'flat':False,	'staff_region':'treble clef',			'amline':True},

			{'ly':"a'"		,'midi':69	,'sharp':False, 'flat':False,	'staff_region':'treble clef',			'amline':False},
			{'ly':"g'"		,'midi':67	,'sharp':False, 'flat':False,	'staff_region':'treble clef',			'amline':True},
			{'ly':"f'"		,'midi':65	,'sharp':False, 'flat':False,	'staff_region':'treble clef',			'amline':False},
			{'ly':"e'"		,'midi':64	,'sharp':False, 'flat':False,	'staff_region':'treble clef',			'amline':True},

			{'ly':"d'"		,'midi':62	,'sharp':False, 'flat':False,	'staff_region':'treble clef',			'amline':False},
			{'ly':"c'"		,'midi':60	,'sharp':False, 'flat':False,	'staff_region':'lower treble ledgers',	'amline':True},
			{'ly':"b"		,'midi':59	,'sharp':False, 'flat':False,	'staff_region':'lower treble ledgers',	'amline':False},
			{'ly':"a"		,'midi':57	,'sharp':False, 'flat':False,	'staff_region':'lower treble ledgers',	'amline':True},
			
			{'ly':"g"		,'midi':55	,'sharp':False, 'flat':False,	'staff_region':'lower treble ledgers',	'amline':False},#H/2-1 (first space above H/2)
			
		]
		
		#----------------------------------H/2 Unoccupied--------------------------------  H/2
		
		
		self.bnotes=[
			{'ly':"f'"		,'midi':65	,'sharp':False, 'flat':False,	'staff_region':'upper bass ledgers',	'amline':False},#H/2+1 (first space below H/2)

			{'ly':"e'"		,'midi':64	,'sharp':False, 'flat':False,	'staff_region':'upper bass ledgers',	'amline':True},
			{'ly':"d'"		,'midi':62	,'sharp':False, 'flat':False,	'staff_region':'upper bass ledgers',	'amline':False},
			{'ly':"c'"		,'midi':60	,'sharp':False, 'flat':False,	'staff_region':'upper bass ledgers',	'amline':True},
			{'ly':"b"		,'midi':59	,'sharp':False, 'flat':False,	'staff_region':'upper bass ledgers',	'amline':False},

			{'ly':"a"		,'midi':57	,'sharp':False, 'flat':False,	'staff_region':'bass clef',				'amline':True},
			{'ly':"g"		,'midi':55	,'sharp':False, 'flat':False,	'staff_region':'bass clef',				'amline':False},
			{'ly':"f"		,'midi':53	,'sharp':False, 'flat':False,	'staff_region':'bass clef',				'amline':True},
			{'ly':"e"		,'midi':52	,'sharp':False, 'flat':False,	'staff_region':'bass clef',				'amline':False},

			{'ly':"d"		,'midi':50	,'sharp':False, 'flat':False,	'staff_region':'bass clef',				'amline':True},
			{'ly':"c"		,'midi':48	,'sharp':False, 'flat':False,	'staff_region':'bass clef',				'amline':False},
			{'ly':"b,"		,'midi':47	,'sharp':False, 'flat':False,	'staff_region':'bass clef',				'amline':True},
			{'ly':"a,"		,'midi':45	,'sharp':False, 'flat':False,	'staff_region':'bass clef',				'amline':False},

			{'ly':"g,"		,'midi':43	,'sharp':False, 'flat':False,	'staff_region':'bass clef',				'amline':True},
			{'ly':"f,"		,'midi':41	,'sharp':False, 'flat':False,	'staff_region':'bass clef',				'amline':False},
			{'ly':"e,"		,'midi':40	,'sharp':False, 'flat':False,	'staff_region':'lower bass ledgers',	'amline':True},
			{'ly':"d,"		,'midi':38	,'sharp':False, 'flat':False,	'staff_region':'lower bass ledgers',	'amline':False},

			{'ly':"c,"		,'midi':36	,'sharp':False, 'flat':False,	'staff_region':'lower bass ledgers',	'amline':True},
			{'ly':"b,,"		,'midi':35	,'sharp':False, 'flat':False,	'staff_region':'lower bass ledgers',	'amline':False},
			{'ly':"a,,"		,'midi':33	,'sharp':False, 'flat':False,	'staff_region':'lower bass ledgers',	'amline':True},
			{'ly':"g,,"		,'midi':31	,'sharp':False, 'flat':False,	'staff_region':'lower bass ledgers',	'amline':False},

			{'ly':"f,,"		,'midi':29	,'sharp':False, 'flat':False,	'staff_region':'lower bass ledgers',	'amline':True},
			{'ly':"e,,"		,'midi':28	,'sharp':False, 'flat':False,	'staff_region':'lower bass ledgers',	'amline':False},
			{'ly':"d,,"		,'midi':26	,'sharp':False, 'flat':False,	'staff_region':'lower bass ledgers',	'amline':True},
			{'ly':"c,,"		,'midi':24	,'sharp':False, 'flat':False,	'staff_region':'lower bass ledgers',	'amline':False},

		]
		self.maj_midi_intervals=[2,2,1,2,2,2,1]
		self.min_midi_intervals=[2,1,2,2,1,2,2]
	
		self.CHORD_INTERVALS={
			'Major':		[0,4,7],#[[0,4,7],[4,7,12],[7,12,16]],#[[0,4,7],[-8,-5,0],[-5,0,4]],
			'Minor':		[0,3,7],
			'Diminished':	[0,3,6],
			'Augmented':	[0,4,8],
			'Major 6':		[0,4,7,9],
			'Minor 6':		[0,3,7,9],
			'7':			[0,4,7,10],#ie. Dominant 7
			'Major 7':		[0,4,7,11],
			'Minor 7':		[0,3,7,10],
			'7 Flat 5':		[0,4,6,10],#ie. Dominant 7 Flat 5
			'7 Sharp 5':	[0,4,8,10],
			'Diminished 7':	[0,3,6,9],
			'9':			[0,4,7,10,14],
			'7 Flat 9':		[0,4,7,10,13],
			'7 Sharp 9':	[0,4,7,10,15],
			'Major 7 +9':	[0,4,7,11,14],
			'9 Flat 5':		[0,4,6,10,14],
			'11':			[0,4,7,10,14,17],
			'Augmented 11':	[0,4,7,10,14,18],
			'13':			[0,4,7,10,14,21],
			'13 Flat 9':	[0,4,7,10,13,21],
		}
		self.major_key_chords=[
				['Major 7'],
				['Minor 7'],
				['Minor 7'],
				['Major 7'],
				['7'],
				['Minor 7'],
				['Diminished'],
				['Major 7']
			]
		
		self.minor_key_chords=[
				['Minor','Minor 7','Minor 6','7 Flat 5','7','9','7 Flat 5','11','13'],
				['Diminished','Minor 6','7 Flat 5','7','9','7 Flat 5','11','13'],
				['Major','Major 7','Minor 6','7 Flat 5','7','9','7 Flat 5','11','13'],
				['Major','Major 7','Minor 6','7 Flat 5','7','9','7 Flat 5','11','13'],
				['Minor','Minor 7','Minor 6','7 Flat 5','7','9','7 Flat 5','11','13'],
				['Minor','Minor 7','Minor 6','7 Flat 5','7','9','7 Flat 5','11','13'],
				['Major','Major 7','Minor 6','7 Flat 5','7','9','7 Flat 5','11','13'],
				['Major','7','Minor 6','7 Flat 5','7','9','7 Flat 5','11','13']
			]
	
	def getStaffRegionUsingY1(self,y1):
		for tnote in self.tnotes:
			if tnote['y1']==y1:return tnote['staff_region']
		for bnote in self.bnotes:
			if bnote['y1']==y1:return bnote['staff_region']
		else:return None
	
	def getBidx(self,midi):
		for bidx in range(len(self.bnotes)):
			if self.bnotes[bidx]['midi']==midi:return bidx
			elif self.bnotes[bidx]['sharp'] and self.bnotes[bidx]['midi']+1==midi:return bidx#
			elif self.bnotes[bidx]['flat'] and self.bnotes[bidx]['midi']-1==midi:return bidx#
		if DEBUG:print 'getBidx returning None (24-65)',midi
		return None
		
	def getTidx(self,midi):
		for tidx in range(len(self.tnotes)):
			if self.tnotes[tidx]['midi']==midi:return tidx
			elif self.tnotes[tidx]['sharp'] and self.tnotes[tidx]['midi']+1==midi:return tidx#
			elif self.tnotes[tidx]['flat'] and self.tnotes[tidx]['midi']-1==midi:return tidx#
		if DEBUG:print 'getTidx returning None (55-89)',midi
		return None
	
	def getNotes(self,name,sig,minor,active_modes,active_staff_regions,*args):
		if DEBUG:print 'getNotes',name
		if len(active_modes)<1:return []
		notes=None
		min_midi=None
		max_midi=None
		if name=="Bass":
			min_midi=24
			max_midi=65
			notes=self.bnotes
		else:
			min_midi=55
			max_midi=89
			notes=self.tnotes
		
		if DEBUG:print "min_midi=",min_midi," max_midi=",max_midi
		
		ctype=active_modes[int(random()*len(active_modes))]
		if DEBUG:print "ctype=",ctype
		
		roots=None
		if minor:roots=sig['minkey_midi_roots']
		else:roots=sig['majkey_midi_roots']
		if DEBUG:print "roots=",roots
		
		key_root=None
		while key_root==None:
			key_root=roots[int(random()*len(roots))]
			
			if key_root>=min_midi and key_root<=max_midi:pass
			else:
				key_root=None
				continue
				
			if name=="Bass":
				if active_staff_regions[notes[self.getBidx(key_root)]['staff_region']]:pass
				else:key_root=None
			else:
				if active_staff_regions[notes[self.getTidx(key_root)]['staff_region']]:pass
				else:key_root=None
			
		if DEBUG:print "key_root=",key_root
		
		intervals=None
		if minor:intervals=self.min_midi_intervals
		else:intervals=self.maj_midi_intervals
		if DEBUG:print "intervals=",intervals
		
		chord_root=key_root
		relative_idx=int(random()*len(intervals))
		for ridx in range(relative_idx):
			chord_root+=intervals[ridx]
		if DEBUG:print "chord_root=",chord_root
		
		chord_key=None
		if minor:chord_key=self.minor_key_chords[relative_idx][int(random()*len(self.minor_key_chords[relative_idx]))]
		else:chord_key=self.major_key_chords[relative_idx][int(random()*len(self.major_key_chords[relative_idx]))]
		if DEBUG:print "chord_key=",chord_key
		
		chord_intervals=self.CHORD_INTERVALS[chord_key]
		if DEBUG:print "chord_intervals=",chord_intervals
		
		numnotes=None
		if ctype=="Single":numnotes=1
		elif ctype=="Double":numnotes=2
		elif ctype=="Chord":numnotes=len(chord_intervals)
		if DEBUG:print "numnotes=",numnotes
		
		rval=[]
		idx=None
		if name=="Bass":
			while idx==None:
				idx=self.getBidx(chord_root)
				if not idx:idx=self.getBidx(chord_root - 12)#both go from 0->up
				if not idx:idx=self.getBidx(chord_root - 24)#both go from 0->up
		else:
			while idx==None:
				idx=self.getTidx(chord_root)
				if not idx:idx=self.getTidx(chord_root - 12)#both go from 0->up
				if not idx:idx=self.getTidx(chord_root - 24)#both go from 0->up

		rval.append(notes[idx])
		
		if DEBUG:print "got idx=",idx
		if DEBUG:print "rval=",rval
		
		for nidx in range(1,numnotes):
			
			candidate=None
			
			if ctype=="Double":
				cidx=int(random()*len(chord_intervals))
				if cidx==0:cidx=1
			else:cidx=nidx
			
			idx=None
			if name=="Bass":
				idx=self.getBidx(chord_root+chord_intervals[cidx])
				if idx==None:idx=self.getBidx(chord_root-(12+chord_intervals[cidx]))
				if idx==None:idx=self.getBidx(chord_root+(12+chord_intervals[cidx]))
				if idx==None:continue
				
			else:
				idx=self.getTidx(chord_root+chord_intervals[cidx])
				if idx==None:idx=self.getTidx(chord_root-(12+chord_intervals[cidx]))
				if idx==None:idx=self.getTidx(chord_root+(12+chord_intervals[cidx]))
				if idx==None:continue
			
			candidate=notes[idx]
			
			if candidate['midi']>=min_midi and candidate['midi']<=max_midi:rval.append(notes[idx])
			elif candidate['midi']<min_midi:
				pass#try +12
			elif candidate['midi']>max_midi:
				pass#try -12
			
		return rval
			
	
	def getLedgerList(self,note_img_dy,midi,staff_region):
		
		ylist=[]
		direction=+1
		
		#######################################		
		#LOWER BASS LEDGERS
		#######################################		
		if staff_region=='lower bass ledgers':
			direction=+1
			
			bmax=len(self.bnotes)-1
			bidx=self.getBidx(midi)
			if not bidx:
				print 'no bidx',midi;return ylist
			bmin=bmax-10
			
			y1=self.bnotes[bidx]['y1']
			amline=self.bnotes[bidx]['amline']
			y0=None
			if amline:
				y0=y1+note_img_dy/2
				#the first in list isn't always there, depending if line or space
			else:
				y0=y1
				
			ylist.append(y0)
			for bbidx in range(bidx-1,bmin+1,-2):
				y0-=direction*note_img_dy
				#y1=self.bnotes[bbidx]['y1']
				#ylist.append(y1+note_img_dy/2)
				ylist.append(y0)
		
		#######################################		
		#UPPER BASS LEDGERS
		#######################################		
		if staff_region=='upper bass ledgers':
			direction=-1
			
			bmax=4
			bidx=self.getBidx(midi)
			if bidx==None:
				print 'no bidx',midi;return ylist
			bmin=0
			
			y1=self.bnotes[bidx]['y1']
			amline=self.bnotes[bidx]['amline']
			y0=None
			if amline:
				y0=y1+note_img_dy/2
				#the first in list isn't always there, depending if line or space
			elif bidx-1<bmax-2:
				y0=y1+note_img_dy
				
			if y0!=None:ylist.append(y0)
			
			for bbidx in range(bidx-1,bmax-3,+2):
				y0+=note_img_dy
				#y1=self.bnotes[bbidx]['y1']
				#ylist.append(y1+note_img_dy/2)
				ylist.append(y0)
		
		#######################################		
		#LOWER TREBLE LEDGERS
		#######################################		
		if staff_region=='lower treble ledgers':
			direction=+1
			
			tmax=len(self.tnotes)-1
			tidx=self.getTidx(midi)
			if not tidx:
				print 'no tidx',midi;return ylist
			tmin=tmax-4
			
			y1=self.tnotes[tidx]['y1']
			amline=self.tnotes[tidx]['amline']
			y0=None
			if amline:
				y0=y1+note_img_dy/2
				#the first in list isn't always there, depending if line or space
			else:
				y0=y1
				
			ylist.append(y0)
			for ttidx in range(tidx-1,tmin+1,-2):
				y0-=direction*note_img_dy
				#y1=self.tnotes[ttidx]['y1']
				#ylist.append(y1+note_img_dy/2)
				ylist.append(y0)
		
		#######################################		
		#UPPER TREBLE LEDGERS
		#######################################		
		if staff_region=='upper treble ledgers':
			direction=-1
			
			tmax=5
			tidx=self.getTidx(midi)
			if tidx==None:
				print 'no tidx',midi;return ylist
			tmin=0
			
			y1=self.tnotes[tidx]['y1']
			amline=self.tnotes[tidx]['amline']
			y0=None
			if amline:
				y0=y1+note_img_dy/2
				#the first in list isn't always there, depending if line or space
			elif tidx<tmax:
				y0=y1+note_img_dy
				
			if y0!=None:ylist.append(y0)
			
			for ttidx in range(tidx-1,tmax-2,+2):
				y0+=note_img_dy
				#y1=self.bnotes[ttidx]['y1']
				#ylist.append(y1+note_img_dy/2)
				ylist.append(y0)
		
		return ylist
		
		
