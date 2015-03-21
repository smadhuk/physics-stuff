#Siddhant Madhuk
#Final Project
#Physics Simulator- Gravity and Electricity
import math
from visual import *
from Tkinter import *
import tkMessageBox, Tkconstants, os, sys
import tkFileDialog
import wx
from visual.graph import *

####################Opens Files For Gravitation#############################
def openFile(filename):
    args=[]
    with open(filename, "r") as f:
        for line in f:
            line = line.replace("\n","")
            if getArgs(line)==None:
                return 
            args.append(getArgs(line))
    createBodies(args)
    
####################Opens Files For Electricity#############################

def openEMFile(filename):
    args=[]
    with open(filename, "r") as f:
        for line in f:
            line = line.replace("\n","")
            if getEMArgs(line)==None:
                return 
            args.append(getEMArgs(line))
    createParticles(args)
    
####################Creation Of Bodies and Particles#############################

def createBodies(argList):
    for args in argList:
        try:
            name1=args[0]
            pos1=args[1]
            mass1=args[2]
            radius1=args[3]
            color1=args[4]
            type1=args[5]
            name1=CelestialBody(name1,pos1,mass1,radius1,color1,type1)
        except:
            tkMessageBox.showwarning("Open file","Corrupt/Invalid File")
            return
    createScene()

def createParticles(argList):
    for args in argList:
        try:
            name1=args[0]
            pos1=args[1]
            mass1=args[2]
            radius1=args[3]
            color1=args[4]
            charge1=args[5]
            vel1=args[6]
            name1=Particle(name1,pos1,mass1,radius1,color1,charge1,vel1)
        except:
            tkMessageBox.showwarning("Open file","Corrupt/Invalid File")
            return
    createEMScene()

####################Extracts arguments from text files#############################


def getArgs(string):
    count=0
    stringPos=0
    while count<6:
        if string[stringPos]=="\"" and count==0:
            name=getName(string)
            count+=1
            stringPos+=len(name)+3
        elif string[stringPos]=="(" and count==1:
            pos=getPos(string[stringPos+1:])
            count+=1
            for i in xrange(len(string)):
                if string[i]==")":
                    stringPos=i+2
                    break
        elif count==2:
            mass,addition=getMass(string[stringPos:])
            stringPos+=addition
            count+=1
        elif count==3:
            radius,addition=getRadius(string[stringPos:])
            stringPos+=addition+1
            count+=1
        elif count==4:
            color,addition = getColor(string[stringPos:])
            count+=1
            stringPos+=addition+1
        elif count==5:
            type = getType(string[stringPos:])
            count+=1
    if type==None:
            tkMessageBox.showwarning("Open file","Try a different file")
            return
    return name,pos,mass,radius,color,type

def getEMArgs(string):
    count=0
    stringPos=0
    while count<7:
        if string[stringPos]=="\"" and count==0:
            name=getName(string)
            count+=1
            stringPos+=len(name)+3
        elif string[stringPos]=="(" and count==1:
            pos=getPos(string[stringPos+1:])
            count+=1
            for i in xrange(len(string)):
                if string[i]==")":
                    stringPos=i+2
                    break
        elif count==2:
            mass,addition=getMass(string[stringPos:])
            stringPos+=addition
            count+=1
        elif count==3:
            radius,addition=getRadius(string[stringPos:])
            stringPos+=addition+1
            count+=1
        elif count==4:
            color,addition = getColor(string[stringPos:])
            count+=1
            stringPos+=addition+1
        elif count==5:
            charge,addition = getCharge(string[stringPos:])
            if charge==None:
                tkMessageBox.showwarning("Open file","Try a different file")
                return
            count+=1
            stringPos+=addition
        elif count==6:
            vel=getVel(string[stringPos:])
            count+=1
    return name,pos,mass,radius,color,charge,vel

###################Individual Functions meant to extract certain arguments from text files###################


def getVel(string):
    count=0
    curPos=0
    lastPos=0
    x,y,z=0,0,0
    for i in string:
        if i==")":
            endPos=string.index(i)
    while count<3:
        if string[curPos]==",":
            if count==0:
                x=float(string[1:curPos])
                lastPos=curPos+1
                curPos=lastPos
                count+=1
            elif count==1:
                y=float(string[lastPos:curPos])
                lastPos=curPos+1
                count+=1
        elif count==2 and string[curPos]==")":
            z=float(string[lastPos:curPos])
            count+=1
        curPos+=1
    return (x,y,z)    


def getCharge(string):
    try:
        for i in xrange(len(string)):
            if string[i]==",":
                endPos=i
                break
        return float(string[:endPos]),len(string[:endPos+1])
    except:
        tkMessageBox.showwarning("Open file","You are trying to open a Gravity File!")
        return None,None
        
        
def getType(string):
    for i in xrange(1,len(string)):
        if string[i]=="\"":
            endPos=i+1
            break
    try:
        return string[1:endPos-1]
    except UnboundLocalError:
        tkMessageBox.showwarning("Open file","You are trying to open a Electricity File!")
        return None
       

def getColor(string):
    endPos=0
    for i in xrange(len(string)):
        if string[i]==",":
            endPos=i
            break
    color=string[:endPos]
    rgbVal=""
    if color=='"red"':
        rgbVal=(1,0,0)
    elif color=='"green"':
        rgbVal=(0,1,0)
    elif color=='"blue"':
        rgbVal=(0,0,1)
    elif color=='"yellow"':
        rgbVal=(1,1,0)
    elif color=='"orange"':
        rgbVal=(1,0.5,0)
    elif color=='"cyan"':
        rgbVal=(0,1,1)
    elif color=='"magenta"':
        rgbVal=(1,0,1)
    elif color=='"black"':
        rgbVal=(0,0,0)
    elif color=='"white"':
        rgbVal=(1,1,1)
    return rgbVal, len(string[:endPos])

def getRadius(string):
    for i in xrange(len(string)):
        if string[i]==",":
            endPos=i
            break
    radius=float(string[:endPos])
    return radius,len(string[:endPos])
            

def getMass(string):
    for i in xrange(len(string)):
        if string[i]==",":
            endPos=i
            break
    addition=len(string[:endPos+1])
    mass=float(string[:endPos])
    return mass,addition
                        

def getPos(string):
    count=0
    curPos=0
    lastPos=0
    x,y,z=0,0,0
    for i in string:
        if i==")":
            endPos=string.index(i)
    while count<3:
        if string[curPos]==",":
            if count==0:
                x=float(string[0:curPos])
                lastPos=curPos+1
                curPos=lastPos
                count+=1
            elif count==1:
                y=float(string[lastPos:curPos])
                lastPos=curPos+1
                count+=1
        elif count==2 and string[curPos]==")":
            z=float(string[lastPos:curPos])
            count+=1
        curPos+=1
    return (x,y,z)    
    
def getName(string):
        endPos=0
        name=""
        startPos=0
        for i in xrange(1,len(string)):
            if string[i]=="\"":
                endPos=i
                break
        name=string[1:endPos]
        return name




##################Functions that open files#####################    
    
def askopenfile():
    filename = tkFileDialog.askopenfilename()
    if filename:
      return openFile(filename)

def askopenEMfile():
    filename = tkFileDialog.askopenfilename()
    if filename:
            return openEMFile(filename)

###################Classes For Planets and Particles##################


class CelestialBody(object):
    bodyList=[ ]
    centralBody=""

    def __init__(self,name,pos,mass,radius,color,type="planet"):
        self.name=name
        if type=="center":
            self.pos=vector(0,0,0)
            CelestialBody.centralBody=self
        elif type=="planet":
            self.pos=vector(pos)
        self.mass=mass
        self.radius=radius
        self.color=color
        self.type=type
        CelestialBody.bodyList.append(self)

    def __repr__(self):
        return "%r" % self.name


class Particle(object):
    particleList=[]

    def __init__(self,name,pos,mass,radius,color,charge,vel):
        self.vel=vel
        self.name=name
        self.pos=pos
        self.charge=charge
        self.mass=mass
        self.radius=radius
        self.color=color
        Particle.particleList.append(self)

    def __repr__(self):
        return "%r" % self.name


def displayKEGraph(body):
    f1 = gcurve(color=color.cyan)	 
    for x in arange(0, 86400,10):	
        f1.plot(pos=(x,(1.0/2)*body.mass*mag(body.name.vel)**2))	


####################functions that call vpython###################

def createScene():
    for body in CelestialBody.bodyList:
        G=6.7e-11
        centerBod=CelestialBody.centralBody
        body.name=sphere(pos=body.pos,radius=body.radius,color=body.color
                         ,make_trail=True)
        if body!=centerBod:
            dist=centerBod.name.pos-body.name.pos
            distance=mag(dist)
            body.name.vel=vector(0,0,1)*((G*(centerBod.mass)/distance))**(1.0/2)
    while True:
        G=6.7e-11
        timeChange=86400
        rate(100)
        centerBod=CelestialBody.centralBody
        for body in CelestialBody.bodyList:
            if len(CelestialBody.bodyList)>1 and body!=centerBod:
                dist=centerBod.name.pos-body.name.pos
                distance=mag(dist)
                Force=dist
                Force.dir=Force/mag(Force)
                Force.mag=(G*centerBod.mass*body.mass)/(distance**2)
                Force.vec=(Force.dir)*Force.mag
                acceleration=(Force.vec)/body.mass
                body.name.vel=body.name.vel+(acceleration*timeChange)
                body.name.pos=body.name.pos+(body.name.vel*timeChange)
                if distance<=(body.radius+centerBod.radius):
                    body.name.visible=False
                    del body.name
                    CelestialBody.bodyList.remove(body)

def createEMScene():
    for particle in Particle.particleList:
        K=9e9
        particle.name=sphere(pos=particle.pos,radius=particle.radius
                            ,color=particle.color,make_trail=True)
        particle.name.vel=vector(particle.vel)
    while True:
        rate(10000)
        for particleA in Particle.particleList:
            for particleB in Particle.particleList:
                if particleB is not particleA:
                    timeChange=1e-22
                    ForceVec=particleA.name.pos-particleB.name.pos
                    ForceDir=ForceVec/mag(ForceVec)
                    distance=mag(ForceVec)
                    ForceMag=(K*particleA.charge*particleB.charge)/(distance**2)
                    Force=ForceMag*ForceDir
                    acceleration=Force/particleA.mass
                    particleA.name.pos=particleA.name.pos+(particleA.name.vel*timeChange)
                    particleA.name.vel=particleA.name.vel+(acceleration*timeChange)

####creates 2D List#####
                    
def make2DList(rows,cols):
    a=[]
    for row in xrange(rows): a += [[0]*cols]
    return a


#########Display Menus############

def createStartMenu(canvas):
    canvas.delete(ALL)
    image = canvas.data.image
    imageSize = ( (image.width(), image.height()) )
    canvas.create_image(601/2, 452/2, image=image)

def createInstructions(canvas):
    image =canvas.data.image
    imageSize = ( (image.width(), image.height()) )
    canvas.create_image(601/2, 452/2, image=image)
         

def redrawAll(canvas):
    canvas.delete(ALL)
    if canvas.data.startMenu==True:
        createStartMenu(canvas)
        canvas.data.titleText="Force Simulator"
    elif canvas.data.instructions==True:
        createInstructions(canvas)
        
    
    
#############Initializes values################    

def init(canvas):
    canvas.data.instructions=False
    canvas.data.titleText="Force Simulator"
    canvas.data.startMenu=True
    canvas.data.editMenu=False
    canvas.data.width =1000
    canvas.data.height = 1000
    image = PhotoImage(file="Nasa.gif")
    canvas.data.image = image
    redrawAll(canvas)

#############Key Bindings for user interface###########

def keyPressed(canvas,event):
    if event.keysym=="g":
        createScenario()
    elif event.keysym=="e":
        createEMScenario()
    elif event.keysym=="t":
        createBody()
    elif event.keysym=="i":
        canvas.data.image=PhotoImage(file="Instructions.gif")
        canvas.data.instructions=True
        canvas.data.startMenu=False
    elif event.keysym=="p" and canvas.data.instructions==True:
        image = PhotoImage(file="Nasa.gif")
        canvas.data.image=image
        canvas.data.instructions=False
        canvas.data.startMenu=True
    redrawAll(canvas)


###############Creates body for the test funtion##################

def createBody():
    root1=Tk()
    root1.wm_title("Body Creator")
    root1.geometry("600x150+300+300")
    label1=Label(root1,text="Name :")
    entry1=Entry(root1)
    label2=Label(root1,text="Mass(in Kg) in scientific notation(for e.g 4x10^12 is 4e12):")
    entry2=Entry(root1)
    label3=Label(root1,text="Radius(in metres) in similar scientific notation :")
    entry3=Entry(root1)
    label4=Label(root1,text="Color(red,green,blue,yellow,orange,cyan,magenta,brown,black or white):")
    entry4=Entry(root1)
    label1.grid(row=0)
    entry1.grid(row=0,column=1)
    label2.grid(row=1)
    entry2.grid(row=1,column=1)
    label3.grid(row=2)
    entry3.grid(row=2,column=1)
    label4.grid(row=3)
    entry4.grid(row=3,column=1)
    def createSimEarth():
        try:
            radius=float(entry3.get())
            earth=sphere(pos=(-4*radius,0,0),material=materials.earth,radius=6.4e6)
            body=sphere(pos=(radius,0,0),color=color.red,radius=radius)
        except:
            tkMessageBox.showwarning("Open file","Invalid Input for radius")
    def createSimSun():
        try:
            radius=float(entry3.get())
            earth=sphere(pos=(-4*radius,0,0),color=color.yellow,radius=7e8)
            body=sphere(pos=(radius,0,0),color=color.red,radius=radius)
        except:
            tkMessageBox.showwarning("Open file","Invalid Input for radius")
    button=Button(root1,text="Compare with Earth", command=createSimEarth).grid(row=4)
    button=Button(root1,text="Compare with Sun", command=createSimSun).grid(row=4,column=1)

####################Scenario Creators#######################

def createScenario():
    root3=Tk()
    label=Label(root3,text="How many Celestial Bodies do you need?(including a central body)")
    enter=Entry(root3)
    label.pack()
    enter.pack()
    def f():
        s=enter.get()
        if s.isdigit()==False or int(s)<=0 or s=="" :
            tkMessageBox.showwarning("Open file","Invalid number of Bodies")
        elif s:
            createEditor(s)
    button=Button(root3,text="Continue",command=f).pack()

def createEMScenario():
    root5=Tk()
    label=Label(root5,text="How many Particles do you need?")
    enter=Entry(root5)
    label.pack()
    enter.pack()
    def f():
        s=enter.get()
        if s.isdigit()==False or int(s)<=0 or s=="" :
            tkMessageBox.showwarning("Open file","Invalid number of Bodies")
        elif s:
            createEMEditor(s)
    button=Button(root5,text="Continue",command=f).pack()

##############CUSTOM SCROLLING CLASS- TAKEN FROM www.stackoverflow.com###########


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, height=650, width =700, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


#######################################CREATION OF EDITING SCREENS#######################################
#Create Labels, Entry Boxes and scrollbars
 
def createEditor(numberOfBods):
    entriesList=[ ]
    argsList=[ ]
    root2=Tk()
    root2.wm_title("Scenario Editor")
    root2.geometry("650x700+0+0")
    separator = VerticalScrolledFrame(root2)
    separator.grid()
    labelC=Label(separator.interior,text="This is where you will assign the body for the center of the system.")
    labelCN=Label(separator.interior,text="Name(Central Body):")
    entryCN=Entry(separator.interior)
    labelCM=Label(separator.interior,text="Mass(in Kg) in scientific notation(for e.g 4x10^12 is 4e12):")
    entryCM=Entry(separator.interior)
    labelCR=Label(separator.interior,text="Radius(in metres) in similar scientific notation :")
    entryCR=Entry(separator.interior)
    labelCC=Label(separator.interior,text="Color(red,green,blue,yellow,orange,cyan,magenta,brown,black or white):")
    entryCC=Entry(separator.interior)
    labelC.grid(row=0)
    entryCN.grid(row=1,column=1)
    labelCN.grid(row=1)
    entryCM.grid(row=2,column=1)
    labelCM.grid(row=2)
    entryCR.grid(row=3,column=1)
    labelCR.grid(row=3)
    entryCC.grid(row=4,column=1)
    labelCC.grid(row=4)
    labelP=Label(separator.interior,text="This is where you will input the data for the rest of the bodies")
    labelP.grid(row=5)
    startRow=6
    addition=8
    maxRow=0
    print 
    for rowNum in xrange(int(numberOfBods)-1):
        startLabel=Label(separator.interior,text="(Planet Number %d):" % (rowNum+1))
        labelN=Label(separator.interior,text="Name(Planet Number %d):" % (rowNum+1))
        entryN=Entry(separator.interior)
        labelM=Label(separator.interior,text="Mass(Planet Number %d):" % (rowNum+1))
        entryM=Entry(separator.interior)
        labelRad=Label(separator.interior,text="Rho(In Metres)(Planet Number %d):" % (rowNum+1))
        labelPhi=Label(separator.interior,text="Phi(In Degrees)(Planet Number %d):" % (rowNum+1))
        labelTheta=Label(separator.interior,text="Theta(In Degrees)(Planet Number %d" %(rowNum+1))
        entryRad=Entry(separator.interior)
        entryPhi=Entry(separator.interior)
        entryTheta=Entry(separator.interior)
        labelR=Label(separator.interior,text="Radius(Planet Number %d):" % (rowNum+1))
        entryR=Entry(separator.interior)
        labelCol=Label(separator.interior,text="Color(red,green,blue,yellow,orange,cyan,magenta,brown,black or white)(Planet Number %d):" % (rowNum+1))
        entryCol=Entry(separator.interior)
        startLabel.grid(row=startRow+rowNum*addition)
        labelN.grid(row=startRow+rowNum*addition+1)
        entryN.grid(row=startRow+rowNum*addition+1,column=1)
        labelM.grid(row=startRow+rowNum*addition+2)
        entryM.grid(row=startRow+rowNum*addition+2,column=1)
        labelR.grid(row=startRow+rowNum*addition+3)
        entryR.grid(row=startRow+rowNum*addition+3,column=1)
        labelCol.grid(row=startRow+rowNum*addition+4)
        entryCol.grid(row=startRow+rowNum*addition+4,column=1)
        labelRad.grid(row=startRow+rowNum*addition+5)
        entryRad.grid(row=startRow+rowNum*addition+5,column=1)
        labelPhi.grid(row=startRow+rowNum*addition+6)
        entryPhi.grid(row=startRow+rowNum*addition+6,column=1)
        labelTheta.grid(row=startRow+rowNum*addition+7)
        entryTheta.grid(row=startRow+rowNum*addition+7,column=1)
        if startRow+rowNum*addition+7>maxRow:
            maxRow=startRow+rowNum*addition+7
        entriesList.append((entryN,entryRad,entryPhi,entryTheta,entryM,entryR,entryCol))
    def showArgs():
        centerArgs='"'+entryCN.get()+'"'+","+"(0,0,0)"+","+entryCM.get()+","+entryCR.get()+","+'"'+entryCC.get()+'"'+","+'"center"'
        argsList.append(centerArgs)
        colorList=['"red"','"green"','"blue"','"yellow"','"orange"'
                   ,'"cyan"','"magenta"','"brown"','"black"','"white"']
        def save():
            file_opt = options = {}
            options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
            options['initialfile'] = 'MyGravitySim.txt'
            options['parent'] = root2
            filename = tkFileDialog.asksaveasfilename(**file_opt)
            if filename:
                return saveFile(filename,argsList)
        for planet in entriesList:
            try:
                color='"'+planet[6].get()+'"'
                if color not in colorList:
                    tkMessageBox.showwarning("Open file","Invalid Input for color")
                    color=None
                    break
                name='"'+planet[0].get()+'"'
                Phi=(float(planet[2].get())/360)*math.pi*2
                Theta=(float(planet[3].get())/360)*math.pi*2
                x=str(float(planet[1].get())*math.sin(Phi)*math.cos(Theta))
                y=str(float(planet[1].get())*math.sin(Phi)*math.sin(Theta))
                z=str(float(planet[1].get())*math.cos(Phi))
                mass=planet[4].get()
                radius=planet[5].get()
                color='"'+planet[6].get()+'"'
                addition=name+","+"("+x+","+y+","+z+")"+","+mass+","+radius+","+color+","+'"'+"planet"+'"'
                argsList.append(addition)
            except:
                tkMessageBox.showwarning("Open file","Invalid Input(s)")
        save()
    saveBut=Button(separator.interior,text="Save this Scenario!", command=showArgs)
    saveBut.grid(row=maxRow+1)


def createEMEditor(numberOfParticles):
    entriesList=[ ]
    argsList=[ ]
    root4=Tk()
    root4.wm_title("Scenario Editor")
    root4.geometry("650x700+0+0")
    labelP=Label(root4,text="This is where you will input the data for all the particles")
    labelP.grid(row=0)
    startRow=1
    addition=12
    maxRow=0
    separator = VerticalScrolledFrame(root4)
    separator.grid()
    for rowNum in xrange(int(numberOfParticles)):
        startLabel=Label(separator.interior,text="(Particle Number %d):" % (rowNum+1))
        labelN=Label(separator.interior,text="Name(Particle Number %d):" % (rowNum+1))
        entryN=Entry(separator.interior)
        labelM=Label(separator.interior,text="Mass(Particle Number %d):" % (rowNum+1))
        entryM=Entry(separator.interior)
        labelRad=Label(separator.interior,text="Rho(In Metres)(Particle Number %d):" % (rowNum+1))
        labelPhi=Label(separator.interior,text="Phi(In Degrees)(Particle Number %d):" % (rowNum+1))
        labelTheta=Label(separator.interior,text="Theta(In Degrees)(Particle Number %d):" %(rowNum+1))
        entryRad=Entry(separator.interior)
        entryPhi=Entry(separator.interior)
        entryTheta=Entry(separator.interior)
        labelR=Label(separator.interior,text="Radius(Particle Number %d):" % (rowNum+1))
        entryR=Entry(separator.interior)
        labelCol=Label(separator.interior,text="Color(red,green,blue,yellow,orange,cyan,magenta,brown,black or white)(Particle Number %d):" % (rowNum+1))
        entryCol=Entry(separator.interior)
        labelCharge=Label(separator.interior,text="Enter charge (Particle Number %d):" % (rowNum+1))
        entryCharge=Entry(separator.interior)
        labelXVel=Label(separator.interior,text="X Component of velocity (Particle Number %d):" %(rowNum+1))
        labelYVel=Label(separator.interior,text="Y Component of velocity (Particle Number %d):" %(rowNum+1))
        labelZVel=Label(separator.interior,text="Z Component of velocity (Particle Number %d):" %(rowNum+1))
        entryXVel=Entry(separator.interior)
        entryYVel=Entry(separator.interior)
        entryZVel=Entry(separator.interior)
        startLabel.grid(row=startRow+rowNum*addition)
        labelN.grid(row=startRow+rowNum*addition+1)
        entryN.grid(row=startRow+rowNum*addition+1,column=1)
        labelM.grid(row=startRow+rowNum*addition+2)
        entryM.grid(row=startRow+rowNum*addition+2,column=1)
        labelR.grid(row=startRow+rowNum*addition+3)
        entryR.grid(row=startRow+rowNum*addition+3,column=1)
        labelCol.grid(row=startRow+rowNum*addition+4)
        entryCol.grid(row=startRow+rowNum*addition+4,column=1)
        labelCharge.grid(row=startRow+rowNum*addition+5)
        entryCharge.grid(row=startRow+rowNum*addition+5,column=1)
        labelRad.grid(row=startRow+rowNum*addition+6)
        entryRad.grid(row=startRow+rowNum*addition+6,column=1)
        labelPhi.grid(row=startRow+rowNum*addition+7)
        entryPhi.grid(row=startRow+rowNum*addition+7,column=1)
        labelTheta.grid(row=startRow+rowNum*addition+8)
        entryTheta.grid(row=startRow+rowNum*addition+8,column=1)
        labelXVel.grid(row=startRow+rowNum*addition+9)
        entryXVel.grid(row=startRow+rowNum*addition+9,column=1)
        labelYVel.grid(row=startRow+rowNum*addition+10)
        entryYVel.grid(row=startRow+rowNum*addition+10,column=1)
        labelZVel.grid(row=startRow+rowNum*addition+11)
        entryZVel.grid(row=startRow+rowNum*addition+11,column=1)
        if startRow+rowNum*addition+11>maxRow:
            maxRow=startRow+rowNum*addition+11
        entriesList.append((entryN,entryRad,entryPhi,entryTheta,entryM,entryR,entryCol,entryCharge,entryXVel,entryYVel,entryZVel))
    def showArgs():
        colorList=['"red"','"green"','"blue"','"yellow"','"orange"'
                   ,'"cyan"','"magenta"','"brown"','"black"','"white"']
        def save():
            file_opt = options = {}
            options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
            options['initialfile'] = 'MyELectricSim.txt'
            options['parent'] = root4
            filename = tkFileDialog.asksaveasfilename(**file_opt)
            if filename:
                return saveFile(filename,argsList)
        for particle in entriesList:
            try:
                color='"'+particle[6].get()+'"'
                if color not in colorList:
                    tkMessageBox.showwarning("Open file","Invalid Input for color")
                    color=None
                    break
                    color=None
                name='"'+particle[0].get()+'"'
                Phi=(float(particle[2].get())/360)*math.pi*2
                Theta=(float(particle[3].get())/360)*math.pi*2
                x=str(float(particle[1].get())*math.sin(Phi)*math.cos(Theta))
                y=str(float(particle[1].get())*math.sin(Phi)*math.sin(Theta))
                z=str(float(particle[1].get())*math.cos(Phi))
                mass=particle[4].get()
                radius=particle[5].get()
                color='"'+particle[6].get()+'"'
                charge=particle[7].get()
                xvel=particle[8].get()
                yvel=particle[9].get()
                zvel=particle[10].get()
                addition=name+","+"("+x+","+y+","+z+")"+","+mass+","+radius+","+color+","+charge+","+"("+xvel+","+yvel+","+zvel+")"
                argsList.append(addition)
                if entriesList.index(particle)==len(entriesList)-1:
                    save()
            except:
                tkMessageBox.showwarning("Open file","Invalid Input(s)")
    saveBut=Button(separator.interior,text="Save this Scenario!", command=showArgs)
    saveBut.grid(row=maxRow+1)
    root4.mainloop()



#########File Savers
def saveFile(filename,passedArgs):
    adder=""
    for arg in passedArgs:
        adder+=arg+"\n"
    adder.strip()
    with open(filename, "w") as f:
        f.write(adder)
    

def run():
    root=Tk()
    root.wm_title("Physics Simulator")
    canvas = Canvas(root, width=601, height=452)
    class Struct: pass
    canvas.data=Struct()
    init(canvas)
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open Gravity File", command=askopenfile)
    filemenu.add_command(label="Open EM File", command=askopenEMfile)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    root.config(menu=menubar)
    redrawAll(canvas)
    canvas.pack()
    root.mainloop()

######Run Function#######
run()
