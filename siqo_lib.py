#==============================================================================
# Siqo common library
#------------------------------------------------------------------------------
from  datetime import datetime

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_ERR            = '_ERROR_'

_E              = 2.718281828459045    # Euler number
_PI             = 3.141592653589793    # Pi number
_2PI            = 2 * _PI              # 2 * Pi

#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# Journal
#------------------------------------------------------------------------------
class SiqoJournal:
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name):
        "Call constructor of SiqoJournal and initialise it with empty data"
        
        self.name = name
        self.reset()
   
    #--------------------------------------------------------------------------
    def reset(self):
        "nastavi default parametre"
        
        self.debugLevel = 10
        self.indent     = 0

    #--------------------------------------------------------------------------
    def M(self, mess, lvl=10 ):
        "vypise spravu do terminalu"
        
        if lvl <= self.debugLevel:
            print( datetime.now().time().strftime('%H:%M:%S ') + self.indent*'|  ' + mess )
    
    #--------------------------------------------------------------------------
    def I(self, mess, lvl=10 ):
        
        self.M(  chr(691) + ' ' +  mess, lvl )
        self.indent += 1
    
    #--------------------------------------------------------------------------
    def O(self, mess, lvl=10 ):
    
        self.indent -= 1
        self.M( chr(746) + ' ' + mess, lvl )
  
#------------------------------------------------------------------------------
journal = SiqoJournal('Journal')
journal.M('Journal start')

#==============================================================================
# Journal
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
journal.M('Siqo common library ver 1.04')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
