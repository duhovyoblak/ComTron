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
from siqo_lib   import journal
from math       import sqrt, exp, sin, cos, pi
from random     import seed, random


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
    def __init__(self, name, pos, context):
        "Call constructor of Neuron and initialise it"

        self.name     = name      # unique name for neuron in Your project
        self.pos      = pos       # neuron's position in layer in net coordinates
        self.srcs     = []        # list of source's neurons len = (2*context + 1)
        
        self.act      = complex() # actual   value of neuron's activation
        self.tgt      = complex() # expected value of neuron's activation
        self.err      = complex() # tgt-act  value of neuron's activation

        journal.M( '<Neuron> {} created'.format(self.name), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"

        self.srcs = []

        journal.M( '<Neuron> {} ALL cleared'.format(self.name), 10)
        
    #==========================================================================
    # Tools for selecting & editing
    #--------------------------------------------------------------------------
    def getName(self):
        "Return neuron's name"
        
        return self.name

    #--------------------------------------------------------------------------
    def getPos(self):
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
    def addSource(self, srcNeu):
        "Adding one neuron to source Neurons"
        
        if type(srcNeu) == Neuron:
            
            self.srcs.append(srcNeu)
            journal.M( '<Neuron> {} added {} as a source'.format(self.name, srcNeu.getName()), 10)

    #==========================================================================
    # 
    #--------------------------------------------------------------------------
    def annealing(self):
        
        alf = 2*pi*random()
        
        self.act = complex( cos(alf), sin(alf) )
        
        journal.M( '<Neuron> {} annealed to {}'.format(self.name, self.act), 10)

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
        
        print( "   {} has act={}, tgt={}, err={}".format(self.name, self.act, self.tgt, self.err ) )
        for src in self.srcs:
            print("   {} has source {}".format(self.name, src.getName()))
        
#------------------------------------------------------------------------------
journal.M('Neuron class ver 0.14')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
