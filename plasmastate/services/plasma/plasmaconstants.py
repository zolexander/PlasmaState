from enum import Enum

class ExtendedEnum(Enum):

    @classmethod
    def from_value(cls, value):
        for item in cls:
            if item.value == value:
                return item
        return None

    @classmethod
    def from_name(cls, name):
        try:
            return cls[name]
        except KeyError:
            return None
class PanelLocation(ExtendedEnum):
    FLOATING = 0
    DESKTOP= 1
    FULLSCREEN= 2
    TOPEDGE= 3
    BOTTOMEDGE= 4
    LEFTEDGE= 5
    RIGHTEDGE= 6
    TOPLEFTCORNER= 7
    TOPRIGHTCORNER= 8
    BOTTOMLEFTCORNER= 9
    BOTTOMRIGHTCORNER= 10
    CENTERAREA= 11

    
class PanelFormFactor(ExtendedEnum):
   PLANAR= 0
   MEDIACENTER= 1
   HORIZONTAL= 2
   VERTICAL= 3
   APPLICATION= 4

 