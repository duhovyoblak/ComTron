#==============================================================================
# Complex neuron class
#------------------------------------------------------------------------------
#
#    
#    
#
#    
#    
#
#------------------------------------------------------------------------------
from siqo_lib   import *
from math       import sqrt, exp


#==============================================================================
# package's constants
#------------------------------------------------------------------------------


#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# class Neuron
#------------------------------------------------------------------------------
class Neuron():

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name):
        "Call constructor of Neuron and initialise it"

        self.name     = name      # unique name for neuron in Your project
        self.pos      = 0         # neuron's position in layer in net coordinates
        
        self.act      = complex() # actual   value of neuron's activation
        self.tgt      = complex() # expected value of neuron's activation
        self.err      = complex() # tgt-act  value of neuron's activation
        self.src      = []        # list of source's neurons

        journal.M( '<Neuron> {} created'.format(self.name), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"

        self.src = []

        journal.M( '<Neuron> {} ALL cleared'.format(self.name), 10)
        
    #==========================================================================
    # Tools for selecting & editing
    #--------------------------------------------------------------------------
    def getName(self):
        "Return neuron's name"
        
        return self.name

    #--------------------------------------------------------------------------
    def getPosition(self):
        "Return neuron's position in layer in net coordinates"
        
        return self.pos

    #--------------------------------------------------------------------------
    def getAct(self):
        "Return neuron's value of Activation"
        
        return self.act

    #--------------------------------------------------------------------------
    def getTgt(self):
        "Return neuron's value of Target"
        
        return self.tgt

    #--------------------------------------------------------------------------
    def getErr(self):
        "Return neuron's value of Error"
        
        return self.err

    #--------------------------------------------------------------------------
    def init(self, m=0.5, s=1):
        "Set random neuron's activation with mean and sigma value"
        
        self.act = (1, 0)

    #==========================================================================
    # 
    #--------------------------------------------------------------------------


    #==========================================================================
    # Tools for data extraction & persistency
    #--------------------------------------------------------------------------
    def getJson(self):
        "Create and return Json record for neuron"
        
        json = {'name':self.name }
        
        journal.M( '<Neuron> {} getJson created'.format(self.name), 10)
        
        return json
        
    #--------------------------------------------------------------------------
    def print(self):
        "Print neuron's properties" 
        
        print( "   {} has act={}, tgt={}, err={}".format(self.name, sel.act.re, sel.tgt.re, sel.err.re ) )
        
#------------------------------------------------------------------------------
journal.M('Neuron class ver 0.10')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
