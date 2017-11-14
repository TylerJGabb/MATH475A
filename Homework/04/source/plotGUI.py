import appJar as aj
import sys
import numpy as np
from numpy import *
import matplotlib.pyplot as plt

from time import sleep

app = aj.gui("HW04-475A","600x300")
app.setFont(15)
app.setSticky("ew")
app.setExpand("both")
def stop(): sys.exit(0)
app.setStopFunction(stop)

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

def press(button_name):
    if button_name == 'plot':
        makeOptimizedPlot(get_x_vec())
    else:
        name = "_".join([str(x) for x in get_x_vec()])
        plt.savefig('optimized_' + name + '.png')
        plt.close()

def update_x_label(scale_name,plot=True):
	print('blap')
	label = "label_" + scale_name
	val = 10 * (app.getScale(scale_name)/100)
	n = 3 if abs(val)*val >= 0 else 4
	new_label = scale_name + "=" + str(val)[0:n].ljust(6,' ')
	app.setLabel(label,new_label)
	if plot:
		print("PLOTTING")
		#makeOptimizedPlot(get_x_vec())
		otherFunc(5)
		sleep(0.05)

def otherFunc(x):
	print(x)

def get_x_vec():
    scale_names = ["x"+str(i) for i in range(1,7)]
    vals = [10*app.getScale(name)/100 for name in scale_names]
    return vals

def makeOptimizedPlot(x_vec):
	print(x_vec)
	plt.clf()

	fine = linspace(-10,10,200)
	f_vec = [f(x) for x in x_vec]
	lagrangian = [L(x,x_vec,f_vec) for x in fine];
	plt.plot(fine,[f(x) for x in fine],'k-',linewidth=2,label="f(x)")
	plt.plot(fine,lagrangian,label=("N="+str(6)))
	plt.plot(x_vec,f_vec,'ro',linewidth=2,label="data set");

	plt.ylim([-2,2]);
	errs = [abs(lagrangian[i] - f(fine[i])) for i in range(len(fine))]
	err = max(errs)
	i = errs.index(err)
	x = fine[i]
	lag = L(x,x_vec,f_vec)
	f_x = f(x)
	tupe = (f_x,lag)
	a = min(tupe);
	b = max(tupe);
	perc_err = 100*abs((f(x) - lag)/f_x)
	plt.plot([x,x],[a,b],'c:',label='max err='+str(perc_err)[:5]+'%',marker='d');

	name = "_".join([str(x) for x in x_vec])
	plt.legend();
	plt.show();


def setup():
	scale_names = ["x"+str(i) for i in range(1,7)]
	label_names = ["label_" + x for x in scale_names]
	colors = ['red','cyan','green','orange','yellow','pink']
	presets = np.linspace(-100,100,6)
	for i in range(6):
		label = label_names[i]
		scale = scale_names[i]
		color = colors[i]

		app.addScale(scale,i,0)
		app.setScaleIncrement(scale,1)
		app.setScaleRange(scale,-100,100,0)

		app.setScaleWidth(scale,15)
		app.setScaleLength(scale,20)
		app.setScale(scale,presets[i])
		app.setScaleChangeFunction(scale,update_x_label)

		app.addLabel(label,label,i,1)
		app.setLabelBg(label,color)

	app.addButton('save figure',press,8,0,5)
	app.addButton("plot",press,7,0,5)

setup()
[update_x_label(scale,False) for scale in ["x"+str(i) for i in range(1,7)]]
app.go()
