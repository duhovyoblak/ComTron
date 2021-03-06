#==============================================================================
# ComTron class GUI
#------------------------------------------------------------------------------
#
#    
#    
#
#    
#    
#
#------------------------------------------------------------------------------
from siqo_lib   import journal
#from neuron     import Neuron
#from layer      import Layer
from comTron    import ComTron

#from matplotlib.figure                 import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits                      import mplot3d

import numpy             as np
import matplotlib.pyplot as plt
import tkinter           as tk

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

_WIN            = '1680x1050'
_DPI            = 100

_FIG_W          = 0.8
_FIG_H          = 1.0

_SC_RED         = 1.4

_BTN_AXE_W      = 0.81
_BTN_AXE_H      = 0.03

_BTN_VAL_W      = 0.81
_BTN_VAL_H      = 0.10

_BTN_DIS_W      = 0.1
_BTN_DIS_H      = 0.025

#==============================================================================
# class ComTronGui
#------------------------------------------------------------------------------
class ComTronGui:
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, comTron):
        "Create and show GUI for ComTron"

        journal.I( 'ComTronGui constructor...', 10 )
        
        #----------------------------------------------------------------------
        # Data source
        
        self.comTron = comTron
        self.title   = self.comTron.name
        
        self.axes    = {1:'Scatter', 2:'Quiver', 3:'3D projection'}
        self.actAxe  = 1
        
        self.keyX = 'lay'
        self.keyY = 'pos'
        self.keyU = 'reAct'
        self.keyV = 'imAct'
        
        #----------------------------------------------------------------------
        # Ziskanie realnych dat na zobrazenie z podkladoveho priestoru
        
        dat  = self.comTron.getPlotData()
        self.meta    = dat['meta']
        self.data    = dat['data']
        self.reScale()
        
        #----------------------------------------------------------------------
        # Create output window
        win = tk.Tk()
        win.title(self.title)
        win.geometry(_WIN)
        win.resizable(False,False)
        win.update()
        self.w = win.winfo_width()
        self.h = win.winfo_height()
        
        #----------------------------------------------------------------------
        # Create layout

        self.fig = plt.figure(figsize=(self.w*_FIG_W/100, self.h*_FIG_H/100), dpi=_DPI)
        self.ax = self.fig.add_subplot(1,1,1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=win)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=self.w*0.0, y=self.h*0.0)
        
        self.fig.canvas.callbacks.connect('button_press_event', self.on_click)

        #----------------------------------------------------------------------
        # Axes type buttons setup
        
        self.butAxeMap = tk.IntVar()
        
        self.butAx1 = tk.Radiobutton(win, text='Scatter chart', variable=self.butAxeMap, value=1, command=self.onButAxe)
        self.butAx1.place(x=self.w * _BTN_AXE_W, y = self.h * (_BTN_AXE_H + 0 * _BTN_DIS_H) )

        self.butAx2 = tk.Radiobutton(win, text='Quiver chart',  variable=self.butAxeMap, value=2, command=self.onButAxe)
        self.butAx2.place(x=self.w * _BTN_AXE_W, y = self.h * (_BTN_AXE_H + 1 * _BTN_DIS_H) )

        self.butAx3 = tk.Radiobutton(win, text='3D projection', variable=self.butAxeMap, value=3, command=self.onButAxe)
        self.butAx3.place(x=self.w * _BTN_AXE_W, y = self.h * (_BTN_AXE_H + 2 * _BTN_DIS_H) )

        self.butAx1.select()
        
        #----------------------------------------------------------------------
        # Value U buttons setup
        
        self.butValMapU = tk.IntVar()

        i = 0
        for key in self.meta['points'].keys():
            
            # Zobrazim iba udaje typu data
            if self.meta['points'][key]['typ'] == 'dat':
                self.butU = tk.Radiobutton(win, text="{} [{}]".format(key, self.meta['points'][key]['dim']), variable=self.butValMapU, value=i, command=self.onButValU)
                self.butU.place(x=self.w * _BTN_VAL_W, y = self.h * (_BTN_VAL_H + (i+15) * _BTN_DIS_H))
                i += 1

        self.butU.select()
        self.butValMapU.set(self.keyU)

        #----------------------------------------------------------------------
        # Value V buttons setup
        
        self.butValMapV = tk.IntVar()

        i = 0
        for key in self.meta['points'].keys():

            # Zobrazim iba udaje typu data
            if self.meta['points'][key]['typ'] == 'dat':
                self.butV = tk.Radiobutton(win, text="{} [{}]".format(key, self.meta['points'][key]['dim']), variable=self.butValMapV, value=i, command=self.onButValV)
                self.butV.place(x=self.w * (_BTN_VAL_W + _BTN_DIS_W), y = self.h * (_BTN_VAL_H + (i+15) * _BTN_DIS_H))
                i += 1

        self.butV.select()
        self.butValMapV.set(self.keyV)

        #----------------------------------------------------------------------
        # Initialisation
        
        self.show()   # Initial drawing
        journal.O( 'ComTronGui created for space {}'.format(self.title), 10 )

        win.mainloop()       # Start listening for events

    #==========================================================================
    # Tools for figure setting
    #--------------------------------------------------------------------------
    def reScale(self):
        "Re-scale all data vectors for better understability"
        
        journal.I( 'ComTronGui {} reScale...'.format(self.title), 10 )
        for key, lst in self.data['points'].items():
            
            # Preskalujem len nie-identifikatory
            if self.meta['points'][key]['typ'] != 'id':
            
                pL = list(lst)  # Urobim si kopiu listu na pokusy :-)
                pL.sort()
                
                # Najdem vhodny koeficient
                c = ('x', 1e+12)
                if pL[-1]-pL[0] > 1e-12 : c = ('p', 1e+12)
                if pL[-1]-pL[0] > 1e-09 : c = ('n', 1e+09)
                if pL[-1]-pL[0] > 1e-06 : c = ('??', 1e+06)
                if pL[-1]-pL[0] > 1e-03 : c = ('m', 1e+03)
                if pL[-1]-pL[0] > 1e+00 : c = ('',  1e+00)
                if pL[-1]-pL[0] > 1e+03 : c = ('K', 1e-03)
                if pL[-1]-pL[0] > 1e+06 : c = ('M', 1e-06)
                if pL[-1]-pL[0] > 1e+09 : c = ('G', 1e-09)
                if pL[-1]-pL[0] > 1e+12 : c = ('T', 1e-12)
                
                # Preskalujem udaje
                for i in range(len(lst)): lst[i] = lst[i] * c[1]
                self.meta['points'][key]['unit' ] = c[0] + self.meta['points'][key]['unit' ]
                self.meta['points'][key]['coeff'] = c[1]
            
                journal.M( 'ComTronGui {} Data list {} was re-scaled by {:e} with preposition {}'.format(self.title, key, c[1], c[0]), 10 )
                
        journal.O( 'ComTronGui {} reScale done'.format(self.title), 10 )
    
    #--------------------------------------------------------------------------
    def getDataLabel(self, key):
        "Return data label for given data's key"
        
        return "${}$ [{}{}]".format(key, self.meta['points'][key]['unit'], 
                                         self.meta['points'][key]['dim' ])
    
    #--------------------------------------------------------------------------
    def getValByGrid(self, gv, key):
        "Return rescaled value for given grid's value and data's key"
        
        gl = self.meta['points']['g'+key]['max'] - self.meta['points']['g'+key]['min']
        vl = self.meta['points'][    key]['max'] - self.meta['points'][    key]['min']
        
        return (gv/gl) * vl * self.meta['points'][key]['coeff']
    
    #--------------------------------------------------------------------------
    def getDataSlice(self):
        "Return a slice of data for given setup"
        
        journal.I( "ComTronGui {} getDataSlice will use ".format(self.title), 10 )

        # Priradim aktualne listy 
        
        x = list( self.data['points'][self.keyX] )
        y = list( self.data['points'][self.keyY] )
        u = list( self.data['points'][self.keyU] )
        v = list( self.data['points'][self.keyV] )

        # Konvertujem do np-array
        X = np.array(x)
        journal.M( "ComTronGui {} getDataSlice X dimension is {} in <{:.3}, {:.3}>".format(self.title, self.meta['points'][self.keyX]['dim'], X.min(), X.max()), 10 )

        Y = np.array(y)
        journal.M( "ComTronGui {} getDataSlice Y dimension is {} in <{:.3}, {:.3}>".format(self.title, self.meta['points'][self.keyY]['dim'], Y.min(), Y.max()), 10 )

        U = np.array(u)
        journal.M( "ComTronGui {} getDataSlice U dimension is {} in <{:.3}, {:.3}>".format(self.title, self.meta['points'][self.keyU]['dim'], U.min(), U.max()), 10 )

        V = np.array(v)
        journal.M( "ComTronGui {} getDataSlice V dimension is {} in <{:.3}, {:.3}>".format(self.title, self.meta['points'][self.keyV]['dim'], V.min(), V.max()), 10 )


        journal.O( "ComTronGui {} getDataSlice return 4 x {} data points".format(self.title, len(x)), 10 )
        
        return (X, Y, U, V)
        
    #==========================================================================
    # GUI methods
    #--------------------------------------------------------------------------
    def show(self):
        "Show network according to given parameters"
        
        journal.I( 'ComTronGui {} show {}'.format(self.title, self.axes[self.actAxe]), 10 )
        
        # Odstranenie vsetkych axes
        while len(self.fig.axes)>0: self.fig.axes[0].remove()
        
        # Vytvorenie rezu udajov na zobrazenie
        (X, Y, U, V) = self.getDataSlice()
    
        # Priprava novych axes

        if self.actAxe == 1:
            
            self.ax = self.fig.add_subplot(1,1,1)
            self.ax.set_title("{}".format( self.axes[self.actAxe]), fontsize=14)
            self.ax.grid(True)
            self.ax.set_xlabel( self.getDataLabel(self.keyX) )
            self.ax.set_ylabel( self.getDataLabel(self.keyY) )
            
            # Vykreslenie neuronov
            sctr = self.ax.scatter( x=X, y=Y, c=U, cmap='RdYlBu_r')
            self.fig.colorbar(sctr, ax=self.ax)
            
            # Vykreslenie vazieb medzi neuronmi
            self.showArrows()
           
        elif self.actAxe == 2:
            
            self.ax = self.fig.add_subplot(1,1,1)
            self.ax.set_title("Amplitude's phase in <0, 2Pi>", fontsize=14)
            self.ax.grid(True)
            self.ax.set_xlabel( self.getDataLabel(self.keyX) )
            self.ax.set_ylabel( self.getDataLabel(self.keyY) )
            self.ax.quiver( X, Y, U, V )

            # Vykreslenie vazieb medzi neuronmi
            self.showArrows()
            
        elif self.actAxe == 3:
            
            self.ax = self.fig.add_subplot(1,1,1, projection='3d')
            self.ax.set_title("Phi angle as phi = omega*t - abs(k*r) in [rad]", fontsize=14)
            self.ax.grid(True)
            self.ax.set_xlabel( self.getDataLabel(self.keyX) )
            self.ax.set_ylabel( self.getDataLabel(self.keyY) )
            
            # Reduction z-axis 
            a = U.min()
            b = U.max()
            
            if abs(a) > abs(b): 
                vMax = a * _SC_RED
                vMin = b
            else              : 
                vMax = b * _SC_RED
                vMin = a
                
            if a * b > 0: vMin = vMin / _SC_RED
            else        : vMin = vMin * _SC_RED
                
            self.ax.set_zlim(vMin, vMax)
            
            surf = self.ax.plot_trisurf( X, Y, U, linewidth=0.2, cmap='RdYlBu_r', antialiased=False)
            self.fig.colorbar(surf, ax=self.ax)
        
        # Vykreslenie noveho grafu
        self.fig.tight_layout()
        self.canvas.draw()
    
        journal.O( 'ComTronGui {} show done'.format(self.title), 10 )
        
    #--------------------------------------------------------------------------
    def showArrows(self):
        "Show arrows between neurons"
        
        shp = self.data['arrows']['shape']
        col = self.data['arrows']['color']
        
        # prejdenm vstky target neurony
        for id, arrs in self.data['arrows']['data'].items():
            
            # prejdem vsetky sipky pre source neurony
            for arr in arrs:
                
                self.ax.arrow( arr['x'], arr['y'], arr['dx'], arr['dy'], shape=shp, color=col )


    #--------------------------------------------------------------------------
    def onButAxe(self):
        "Resolve radio buttons selection for active Axe of figure"
        
        self.actAxe = self.butAxeMap.get() # get integer value for selected button
        self.show()
    
    #--------------------------------------------------------------------------
    def onButValU(self):
        "Resolve radio buttons selection for active U Value in plot"
        
        self.actValU = self.butValMapU.get() # get integer value for selected button
        self.show()
    
    #--------------------------------------------------------------------------
    def onButValV(self):
        "Resolve radio buttons selection for active V Value in plot"
        
        self.actValV = self.butValMapV.get() # get integer value for selected button
        self.show()
    
    #--------------------------------------------------------------------------
    def on_click(self, event):
        "Print information about mouse-given position"
        
        if event.inaxes is not None:
            
            x = float(event.xdata)
            y = float(event.ydata)

            # Ziskanie nastavenia grafu
            valX = self.values[self.actValX]
            valY = self.values[self.actValY]
            valS = self.values[self.actValS]
            
            x = x                                  / self.meta['points'][valX]['coeff']
            y = y                                  / self.meta['points'][valY]['coeff']
            s = self.getValByGrid(self.sVal, valS) / self.meta['points'][valS]['coeff']
            
            pos = {'x':0, 'y':0, 'z':0, 't':0}
            pos[valX] = x
            pos[valY] = y
            pos[valS] = s
            
            id = self.comTron.getIdFromPos(pos)
            self.comTron.printCell(id)
            
        else:
            print('Clicked ouside axes bounds but inside plot window')
    
    #--------------------------------------------------------------------------

#------------------------------------------------------------------------------
print('ComTron class GUI ver 0.14')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
