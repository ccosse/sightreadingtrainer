import java,os
from java import awt
from javax import swing
from javax.swing import JLabel,JPanel,JSlider,JScrollPane,JEditorPane,JScrollPane,ImageIcon,JComboBox
from java.awt import FlowLayout,BorderLayout,Dimension

DEBUG=0
HELP_TEXT="""
<center>
<table width="600" cellspacing="0" cellpadding="5px" border="0x" bgcolor="#000000" align="center">
    <thead>
        <tr>
            <th bgcolor="#ffffff" style="text-align: center;" scope="col">
            <p><span style="font-size: large;"><span style="font-family: Tahoma;"><span style="color: rgb(0, 51, 0);">MIDI Sight Reader</span></span></span><span style="color: rgb(0, 51, 0);"><span style="font-size: xx-large;"><span style="font-family: Comic Sans MS;"> <br />
            </span></span></span></p>
            <p><span style="font-size: small;"><span style="font-family: Arial;"><span style="color: rgb(0, 51, 0);"><span style="font-style: italic;">An Interactive Java Applet by Charles B. Coss&eacute</span></span></span></span></p>
            <p><a title="MIDI Sight Reader - Click To Launch Java Applet - Requires jdk-1.6" href="http://new.asymptopia.org/static/MFC/MFC.html"> 	<img width="620" height="361" alt="" src="http://www.asymptopia.org/static/MFC/img/MIDI_SightReader_3.3b.png" /></a></p>
            <p style="text-align: justify;"><span style="font-family: Arial;"><span style="font-size: small;">MIDI Sight Reader is an online music application inspired by its predecessor, the original MidiFlashCard system. The application scrolls both piano notes and guitar tablature.&nbsp; </span></span><span style="font-size: small;">Notes are played </span><span style="font-size: small;">for audio confirmation as they pass under the centerline on the window.&nbsp; The scrolling staffs drive a keyboard model and a guitar neck model. The guitar and keyboard can drive each other as well, for interactive exploration of the correspondence between the two instruments.&nbsp; The 3 components, staff, keyboard and guitar, can be independently added and removed from the top down, so many combinations of layout can be achieved.&nbsp; Subsequent versions will focus on implementing more sophisticated music generation capabilities.</span></p>
            <p style="text-align: center;"><span style="background-color: rgb(255, 102, 0);">NOTE: Ubuntu Linux Breaks Java Midi in Applets!</span></p>
            </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td bgcolor="#ffffff">
            <p style="text-align: center;"><span style="font-size: small;"><strong><em><span style="color: rgb(255, 0, 0);">Note</span></em></strong><em><span style="color: rgb(255, 0, 0);">: </span></em></span><strong><span style="font-size: small;"><em><span style="color: rgb(255, 0, 0);">You need </span></em></span></strong><span style="font-size: small;"><em><span style="color: rgb(255, 0, 0);"><a href="http://java.sun.com/javase/downloads/index.jsp"><strong>jdk-1.6</strong></a></span><strong><span style="color: rgb(255, 0, 0);"> browser plugin b/c applet compiled with 1.6</span></strong></em></span><span style="color: rgb(255, 0, 0);"> </span></p>
            <p style="text-align: center;"><span style="font-size: small;"><em><strong><span style="color: rgb(255, 0, 0);">Note: You need to restart your browser when switching between versions </span></strong></em></span></p>
            <p style="text-align: center;">&nbsp;</p>
            <p style="text-align: center;"><span style="font-size: large;"><strong><span style="font-family: Comic Sans MS;">latest online development applet </span></strong></span><span style="font-size: x-large;"><span style="font-family: Comic Sans MS;"><strong><span style="font-size: x-large;"><a href="http://new.asymptopia.org/static/MFC/MFC.html"><span style="font-size: large;">here</span></a></span></strong></span></span></p>
            <meta http-equiv="content-type" content="text/html; charset=utf-8">
            <h1 style="font-size: 1.4em; background-color: transparent; color: rgb(0, 0, 0); font-weight: 700; margin: 0px 5px 0px 0px; text-align: center;"><span style="font-family: 'Comic Sans MS';"><strong><span style="font-size: medium;">&nbsp;</span><span style="font-size: large;">download MFC-3.4.jar&nbsp;</span><a style="background-color: transparent; color: rgb(0, 0, 255);" href="http://new.asymptopia.org/download"><span style="font-size: large;">here</span></a></strong></span>&nbsp;</h1>
            <h2 style="text-align: center;"><span style="font-family: Comic Sans MS;">&nbsp;<span style="font-size: small;">original LaTeX midi flashcard system </span><a href="http://new.asymptopia.org/download"><span style="font-size: small;">here</span></a></span></h2>
            <p style="text-align: left;">&nbsp;</p>
            <center><span style="font-family: Comic Sans MS;">             </span><br />
            </center>
            <p><span style="font-family: Comic Sans MS;"><strong><span style="font-size: large;">Updated</span></strong>: 08/10/2013</span></p>
            <p style="text-align: left;"><span style="color: rgb(0, 51, 102);"><strong><span style="font-size: large;"><span style="font-family: Comic Sans MS;">Current&nbsp;Version</span></span></strong></span><span style="font-family: Comic Sans MS;">: 3.4</span></p>
            <p style="text-align: left;"><span style="font-family: Comic Sans MS;">CHANGES 3.4: Bug fix to rendering of bass cleff key signatures ... they were being rendered one half space too low!</span>&nbsp; Then went on to fully implement the various available note structures (Single,Double,Chord) in both clefs.&nbsp;</p>
            <p style="text-align: left;">&nbsp;</p>
            <p><strong><span style="color: rgb(51, 51, 153);"><span style="font-size: large;"><span style="font-family: Comic Sans MS;">Recommended usages</span></span></span></strong><span style="font-family: Comic Sans MS;">: </span></p>
            <p style="text-align: justify;"><span style="font-family: Comic Sans MS;">1. Use with real piano/guitar ... same way as <a href="http://new.asymptopia.org/download">original</a> MidiFlashCard&nbsp;System<br />
            </span></p>
            <p style="text-align: justify;"><span style="font-family: Comic Sans MS;">2. Plug in 2 mouses and use one for LH and one for RH (LeftHand, RightHand); play keyboard in application.&nbsp; This seems to work pretty well ... next best thing to real piano, and keeps LH associated with bass cleff and RH associated with treble clef.</span></p>
            <p style="text-align: justify;"><span style="font-family: Comic Sans MS;">3. In the absence of an actual piano (on an airplane, for example), just mimic proper RH/LH playing technique using your desk (or tray table). Get synchronized with the incoming notes; imagine that playing your desk is causing the keyboard widget to illuminate. Use headphones for better focus. Adjust your monitor so your boss can't see.<br />
            </span></p>
            <p>&nbsp;</p>
            <p style="text-align: justify;"><span style="font-size: large;"><strong><span style="color: rgb(255, 102, 0);"><span style="font-family: Comic Sans MS;">Things to know</span></span></strong></span><span style="font-family: Comic Sans MS;">: First, use the View menu (top menubar) to rearrange the 3 main components, keyboard, guitar and staff to your liking. By default all are toggled &quot;on&quot;. Toggle all off, then re-add them in any order. Components will be added from top to bottom. You can display all, some or none of the components.</span></p>
            <span style="font-family: Comic Sans MS;">             <br />
            </span>
            <p style="text-align: justify;"><span style="font-size: large;"><strong><span style="color: rgb(255, 153, 0);"><span style="font-family: Comic Sans MS;">The Staff widget</span></span></strong></span><span style="font-family: Comic Sans MS;"> has two tabbed-panes, ScrollStaff and ScrollTab. The ScrollStaff shows a grand staff which can be set to any key signature. Pushing the <b>Scroll</b> button causes notes to be added on the right side of the staff lines and scroll to the left. The key signature is separate and stays fixed. Notes are played as they pass under the centerline. The scrolling speed and delay between notes is configured using the 2x spin-control widgets. The instrument sound to use can be configured from the staff control area as well.</span></p>
            <span style="font-family: Comic Sans MS;">             <br />
            </span>
            <p style="text-align: justify;"><span style="font-size: large;"><strong><span style="color: rgb(128, 0, 128);"><span style="font-family: Comic Sans MS;">The ScrollTab</span></span></strong></span><span style="font-family: Comic Sans MS;"> tabbed-pane shows a scrolling guitar tab widget. The guitar model has 6 strings and 24 frets. Random (string,fret) notes chosen and put on the scroller. When the fretnumber passes under the centerline then the not plays.</span></p>
            <span style="font-family: Comic Sans MS;">             <br />
            </span>
            <p style="text-align: justify;"><span style="font-size: large;"><strong><span style="color: rgb(128, 0, 0);"><span style="font-family: Comic Sans MS;">All 3x widgets</span></span></strong></span><span style="font-family: Comic Sans MS;"> are interconnected: Pressing a piano note will cause the possible corresponding notes on the guitar to be hilighted, and the 2x staff models drive both instruments simultaneously.</span></p>
            <p><span style="font-family: Comic Sans MS;">             <br />
            </span></p>
            <p style="text-align: justify;"><span style="color: rgb(255, 102, 0);"><strong><span style="font-size: large;"><span style="font-family: Comic Sans MS;">Brief History</span></span></strong></span><span style="font-family: Comic Sans MS;">: First came the original MidiFlashCard System (MFC). MFC reached to version 1.0.3, but had several dependencies: Jython, MikTex/LaTeX, Java, Ghostview, and ImageMagick -- too many!&nbsp; This new version depends only on jdk-1.6.&nbsp; But the decision to make this in pure Java was taken for the reason that it can run as an applet -- namely that the javax.sound.midi package works in all browsers when carefully compiled into an applet.&nbsp; That's about as minimal of an installation as you could hope for on an application such as this.&nbsp; So, over the past year I have developed a few v2.X experiments (try one <a href="http://www.asymptopia.org/static/MFC/MFC.html">here</a>) ... and the best aspects of those are provided in the foundation of the current v3.0 implementation, which has been renamed to &quot;MIDI&nbsp;Sight Reader&quot;, as it is entirely new code and has very little in common, aside from the concept, with the original.&nbsp; So, there are more features to come, but this is the basic foundation application.&nbsp; It is now in a state at which it can be useful, so give it a try ...<br />
            </span></p>
            <p>&nbsp;</p>
            <p><strong><span style="color: rgb(255, 0, 255);"><span style="font-family: Comic Sans MS;">ToDo</span></span></strong><span style="font-family: Comic Sans MS;">: Add some brains to the thing ...</span></p>
            <span style="font-family: Comic Sans MS;">                          </span>
            <p><strong><span style="color: rgb(51, 153, 102);"><span style="font-family: Comic Sans MS;">Hopefully Coming Soon</span></span></strong><span style="font-family: Comic Sans MS;">: Video Tour and Video Tutorial</span></p>
            <p><span style="color: rgb(255, 102, 0);"><strong><span style="font-family: 'Comic Sans MS';">Needed:</span></strong></span> <span style="font-family: 'Comic Sans MS';">Venture Capitalist to advance this, and several other applications.</span></p>
            </meta>
            </td>
        </tr>
    </tbody>
</table>
<br />
<center><br />
<p>&nbsp;</p>
</center> </center>
<p>&nbsp;</p>
"""
class HelpPanel(JPanel):
	def __init__(self):
		
		JPanel.__init__(self,BorderLayout())
		self.editor=JEditorPane()
		self.editor.setEditable(0)
		#self.editor.setContentType('text/html')
		self.editor.setContentType('text/html')
		sp=JScrollPane(self.editor,
			JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
			JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED)
		self.add(sp,'Center')
		
		#html="<html><h1>Test</h1></html>"
		#self.editor.setText(html)
		#self.lines='HELP'
		self.editor.setText(HELP_TEXT)
		
	def append(self,line):
		self.lines="%s\n%s"%(self.lines,line)
		self.editor.setText(self.lines)
	
