#==============================================================================
# Complex perceptron class
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
from neuron     import Neuron
from layer      import Layer


#==============================================================================
# package's constants
#------------------------------------------------------------------------------


#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# class ComTron
#------------------------------------------------------------------------------
class ComTron():

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name):
        "Call constructor of ComTron and initialise it"

        journal.I( '<ComTron> {} constructor...'.format(name), 10 )
        
        self.name     = name   # unique name for ComTron in Your project 
        self.inFile   = ''     # input   [ { 'in':'', 'tgt':int, 'dat':[ {'cat':int  } ]            } ]
        self.outFile  = ''     # output  [ { 'in':'', 'tgt':int, 'out':[ {'tgt':float} ], 'win':tgt } ]
        self.layers   = []     # network of neurons as a list of layers      


        journal.O( '<ComTron> {} created'.format(self.name), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"

        self.inFile   = ''
        self.outFile  = ''
        
        for layer in self.layers: layer.clear()

        journal.M( '<ComTron> {} ALL cleared'.format(self.name), 10)
        
    #==========================================================================
    # Tools for selecting & editing
    #--------------------------------------------------------------------------
    def getName(self):
        "Return ComTron's name"
        
        return self.name

    #==========================================================================
    # Tools for net initialisation
    #--------------------------------------------------------------------------
    def createNet(self, layersSize ):
        "Create net as list of layers and resolve neuron connections"
        
        journal.I( '<ComTron> {} createNet...'.format(self.name), 10)

        #----------------------------------------------------------------------
        # Create list of layers
        self.clear()
        
        pos = 0
        for size in layersSize:
            self.layers.append( Layer( 'Layer {}'.format(str(pos)), pos, size ) )
            pos += 1

        #----------------------------------------------------------------------
        
        journal.O( '<ComTron> {} created net of {} layers'.format(self.name, str(pos)), 10)

    #==========================================================================
    # 
    #--------------------------------------------------------------------------


    #==========================================================================
    # Tools for data extraction & persistency
    #--------------------------------------------------------------------------
    def setIOFile(self, name):
        "Set name for Input/Output json file"
        
        self.inFile  = name+'.json'
        self.outFile = name+'_out.json'

        journal.M( '<ComTron> {} setIOFile to {} / {}'.format(self.name, self.inFile, self.outFile), 10)

    #--------------------------------------------------------------------------
    def getJson(self):
        "Create and return Json record for ComTron"
        
        json = {'name':self.name }
        
        journal.M( '<ComTron> {} getJson created'.format(self.name), 10)
        
        return json
        
    #--------------------------------------------------------------------------
    def getPlotData(self):
        "Create and return numpy arrays for plotting data"
        
        #----------------------------------------------------------------------
        # Metadata section
        meta = { 
                 'id'    :{'dim':'string' , 'unit':'', 'coeff':1 },
                 'lay'   :{'dim':'#'      , 'unit':'', 'coeff':1, 'min':0, 'max':0 },
                 'pos'   :{'dim':'#'      , 'unit':'', 'coeff':1, 'min':0, 'max':0 },
                 
                 'reAct' :{'dim':'Act.re' , 'unit':'', 'coeff':1},
                 'imAct' :{'dim':'Act.im' , 'unit':'', 'coeff':1},
                 'abAct' :{'dim':'Act.abs', 'unit':'', 'coeff':1},

                 'reTgt' :{'dim':'Tgt.re' , 'unit':'', 'coeff':1},
                 'imTgt' :{'dim':'Tgt.im' , 'unit':'', 'coeff':1},
                 'abTgt' :{'dim':'Tgt.abs', 'unit':'', 'coeff':1},
                 
                 'reErr' :{'dim':'Err.re' , 'unit':'', 'coeff':1},
                 'imErr' :{'dim':'Err.im' , 'unit':'', 'coeff':1},  
                 'abErr' :{'dim':'Err.abs', 'unit':'', 'coeff':1},  
               }
        
        #----------------------------------------------------------------------
        # Data section
        data = { 'id'   :[], 'lay'  :[], 'pos'  :[],
                 'reAct':[], 'imAct':[], 'abAct':[],
                 'reTgt':[], 'imTgt':[], 'abTgt':[],
                 'reErr':[], 'imErr':[], 'abErr':[]  }
        
        toret = { 'meta':meta, 'data':data }
        
        i = 0
        for lay in self.layers:
            for neu in lay.neurons:
            
                toret['data']['id'   ].append( neu.getName()             )
                toret['data']['lay'  ].append( lay.getPosition()         )
                toret['data']['pos'  ].append( neu.getPosition()         )
            
                toret['data']['reAct'].append( neu.getAct().real         )
                toret['data']['imAct'].append( neu.getAct().imag         )
                toret['data']['abAct'].append( abs(neu.getAct())         )

                toret['data']['reTgt'].append( neu.getTgt().real         )
                toret['data']['imTgt'].append( neu.getTgt().imag         )
                toret['data']['abTgt'].append( abs(neu.getTgt())         )

                toret['data']['reErr'].append( neu.getErr().real         )
                toret['data']['imErr'].append( neu.getErr().imag         )
                toret['data']['abErr'].append( abs(neu.getErr())         )

                i +=1
        
        #----------------------------------------------------------------------
        # Aggregation section
        
        pLay = list(toret['data']['lay'])
        pLay.sort()
        pPos = list(toret['data']['pos'])
        pPos.sort()
        
        toret['meta']['lay']['min'] = pLay[ 0]
        toret['meta']['lay']['max'] = pLay[-1]
        toret['meta']['pos']['min'] = pPos[ 0]
        toret['meta']['pos']['max'] = pPos[-1]
        
        journal.M( '<ComTron> {} getPlotData created {} records'.format(self.name, i), 10)
        return toret

    #--------------------------------------------------------------------------
    def print(self):
        "Print ComTron's properties"
        
        print( "<ComTron> {} consists of {} layers".format(self.name, len(self.layers) )   )
        print( "-----------------------------------------------------------------------" )
        for layer in self.layers: layer.print()
        print( "=======================================================================" )
        
#------------------------------------------------------------------------------
journal.M('ComTron class ver 0.11')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
