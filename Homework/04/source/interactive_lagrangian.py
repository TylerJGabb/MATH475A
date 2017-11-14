import appJar as aj
import sys
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from time import sleep
import random

#define f(x)
f = lambda x: arctan(x)


#terms in the lagrangian
def l(i,x,x_vec):
	result = 1;
	for j in range(0,len(x_vec)):
		if j == i:
			continue
		result *= (x - x_vec[j])/(x_vec[i] - x_vec[j])
	return result


#the entire lagrangian
def L(x,x_vec,f_vec):
	result = 0;
	for i in range(0,len(x_vec)):
		result += f_vec[i]*l(i,x,x_vec)
	return result


##############################  GENERATING THE PLOT ############################
plt.ion()#turn interactive mode on
FIG = plt.figure("Slider Bar Lagrangian Plot Window")#create a global figure
AXES = FIG.add_subplot(111)#add a plot to it (because it was empty)
#and create a global axis handle
AXES.set_xlim(-10,10)
AXES.set_ylim(-2,2)
FINE = np.linspace(-10,10,200)
ARCTAN, = AXES.plot(FINE,[arctan(x) for x in FINE],'k-',label='arctan(x)')
PRESETS = linspace(-10,10,6)
PRESET_F = [arctan(x) for x in PRESETS]
SAMPLE, = AXES.plot(PRESETS,[arctan(x) for x in PRESETS],'ro',label='sample')
LAGRANGIAN, = AXES.plot(FINE,[L(x,PRESETS,PRESET_F) for x in FINE],'b-',label='lagrangian')
handles,labels = AXES.get_legend_handles_labels()
AXES.legend(handles,labels)
AXES.set_title("Move the sliders to change the polynomial")


########################### CREATING THE APPLICATION ###########################
SCALES = ['x' + str(i) for i in range(1,7)]#slider bars for each sample_x value
LABELS = ['label_' + x for x in SCALES]#labels for each slider
SCALE_TO_LABEL_MAP = {SCALES[i] : LABELS[i] for i in range(6) }
APP = aj.gui("Slider Bar Lagrangian","500x300")
def stop(): sys.exit(0)
APP.setStopFunction(stop)
APP.setSticky("nsew")
APP.setExpand("both")
APP.setFont(18)






def move_sample_randomly():
    '''
    chooses 6 points at random from FINE and uses them to generate new sample points
    these sample points are then used to reset the x and y data for SAMPLE.
    these data points are then used to develop a lagrangian polynomial that is then
    plotted and rendered via FIG.canvas.draw()
    -----THIS IS A DEVELOPERS FUNCTION-----
    '''
    sample_x = []
    while len(sample_x) < 6:
        x = random.choice(FINE)
        if x in sample_x: continue
        sample_x.append(x)
    print("sample_x =",sample_x)
    sample_y = [arctan(x) for x in sample_x]
    print("sample_y=",sample_y)
    SAMPLE.set_xdata(sample_x)
    SAMPLE.set_ydata(sample_y)

    lagrangian_y = [L(x,sample_x,sample_y) for x in FINE]
    LAGRANGIAN.set_ydata(lagrangian_y)

    FIG.canvas.draw()


def redraw_plot():
    '''
    redraws the plot with the x_values currently selected by each slider
    simmilar to move_sample_randomly() but with a functional purpose.
    checks return value from get_sample_x() and stops if it indicated duplicates
    '''
    sample_x = get_sample_x()
    if(sample_x == None): #add extra behavior later, for now just stop
        return
    #print("sample_x =",sample_x)
    sample_y = [arctan(x) for x in sample_x]
    #print("sample_y=",sample_y)
    SAMPLE.set_xdata(sample_x)
    SAMPLE.set_ydata(sample_y)

    lagrangian_y = [L(x,sample_x,sample_y) for x in FINE]
    LAGRANGIAN.set_ydata(lagrangian_y)

    FIG.canvas.draw()
    sleep(0.025)

def get_sample_x():
    '''
    goes to the sliders and says "Hey, what are your values" and returns them
    as list of floats. Checks for duplicates and makes adjustments accordingly
    to prevent division by zero in lagrangian formula. Returns none if duplicate
    found
    '''
    vals = [10*APP.getScale(name)/100 for name in SCALES]
    for val in vals:
        if(vals.count(val) > 1):
            return None
    return vals

def slider_value_changed(scale_name,setup=False):
    '''
    used as an event handler, called when the slider bar values change
    '''
    label = SCALE_TO_LABEL_MAP[scale_name]
    val = 10 * (APP.getScale(scale_name)/100)
    n = 3 if abs(val)*val >= 0 else 4
    new_label = scale_name + "=" + str(val)[0:n].ljust(6,' ')
    APP.setLabel(label,new_label)

    if not setup: redraw_plot()



def do_setup_app():
    '''
    sets up the APP gui, adding widgets and assigning event handlers accordingly
    '''
    colors = ['red','cyan','green','orange','yellow','pink']
    presets = linspace(-100,100,6)
    for i in range(6):
        scale = SCALES[i]
        label = LABELS[i]
        APP.addLabel(label,scale + "=?",i,0,1)
        APP.setLabelBg(label,colors[i])
        APP.addScale(scale,i,1,2)

        APP.setScaleIncrement(scale,1)
        APP.setScaleRange(scale,-100,100,0)
        APP.setScale(scale,presets[i])
        APP.setScaleChangeFunction(scale,slider_value_changed)
        slider_value_changed(scale,setup=True)


def main():
    do_setup_app()
    APP.go()



main()
