from javax.swing import JPanel
from java.awt import Color,BorderLayout,FlowLayout
import java,javax,javax.swing,java.awt
from javax.swing import *

DEBUG=True

class ControlPanel(JPanel):
	def __init__(self,name):
		self.name=name
		if DEBUG:print self.name
		self.W=200
		self.H=100
		self.setSize(self.W,self.H)
		self.setLayout(FlowLayout())
		
		self.add(JButton(self.name))
		
		greenLine=BorderFactory.createLineBorder(java.awt.Color(0,200,0))
		border=BorderFactory.createTitledBorder(greenLine,self.name)
		self.setBorder(border)
 
