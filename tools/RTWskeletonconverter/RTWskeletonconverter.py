# ===================================================================================
#                            RTWskeletonconverter.py                                |
# ===================================================================================
#                                                                                   |
# Programmer:     Sandy Wilson (KnightErrant)                                       |
#                                                                                   |
# Creation Date:  15 June  2009                                                     |
# Revision Dates: 15 June  2009 - Just finishing off the User Interface.            |
#                                                                                   |
# ----------------------------------------------------------------------------------|
#                                                                                   |
#    A (sort of) object oriented converter of the RTW skeletons to ASCII .txt files |
# and back again to binary.                                                         |
#                                                                                   |
# ===================================================================================

# GUI stuff and system dialogs.
from tkinter              import *                     # This is for the main GUI.
from tkinter.filedialog   import askopenfilename       # Replace old filechoose with the system one.
from tkinter.filedialog   import asksaveasfilename     # Added this to allow user to confirm save name.
from tkinter.filedialog   import askdirectory
from tkinter.messagebox   import showinfo              # Used for the info button help dialogs. 
from tkinter.messagebox   import askokcancel           # Used for proceed or exit in reorderbones.
from tkinter.messagebox   import askyesno              # Used for GOM's skeleton or my skeleton in importstandardhumanskeleton.

# General and simple dialogs.                          
from tkinter.dialog       import Dialog                # Used to make simple dialogs.
from tkinter.simpledialog import askinteger            # Used to get FPS value in animmerge.
from tkinter.simpledialog import askfloat              # Used to get scaling factor for the skeleton when exporting.

# Imports.
import array                                           # The 1D array class, has fast reads and writes for binary files.
import struct                                          # This is for reading and writing binary files. It packs and unpacks the data.
import math                                            # Need this trig functions to do quat to euler conversions.
import copy                                            # copy is used to make deepcopy so we don't get just references.
import os
import os.path                                         # Needed for full filename path splitting.

# ===================================================================================
#                            File operations.                                       |
# ===================================================================================
def iseof( fidin ) :
    val                    = fidin.read( 1 )
    if val == '' :
        return True

    # Rewind the file 1 byte.
    fidin.seek( -1, 1 )                 
    return False

# ===================================================================================
#                            Getters for binary files.                              |
# ===================================================================================

# -----------------------------------------------------------------------------------
def getbyte( fidin ) :
    (thebyte,)             = struct.unpack( 'b', fidin.read(1) ) # 'b' is signed byte.
    return thebyte

# -----------------------------------------------------------------------------------
def getubyte( fidin ) :
    (thebyte,)             = struct.unpack( 'B', fidin.read(1) ) # 'B' is unsigned byte.
    return thebyte

# -----------------------------------------------------------------------------------
def getshort( fidin ) :
    (theshort,)            = struct.unpack( 'h', fidin.read(2) ) # 'h' is signed short.
    return theshort

# -----------------------------------------------------------------------------------
def getushort( fidin ) :
    (theshort,)            = struct.unpack( 'H', fidin.read(2) ) # 'H' is unsigned short.
    return theshort

# -----------------------------------------------------------------------------------
def getint( fidin ) :
    (theint,)              = struct.unpack( 'i', fidin.read(4) ) # 'i' is signed int.
    return theint

# -----------------------------------------------------------------------------------
def getuint( fidin ) :
    (theint,)              = struct.unpack( 'I', fidin.read(4) ) # 'I' is unsigned int.
    return theint

# -----------------------------------------------------------------------------------
def getfloat( fidin ) :
    (thefloat,)            = struct.unpack( 'f', fidin.read(4) ) # 'f' is float.
    return thefloat

# -----------------------------------------------------------------------------------
def getstring( fidin, nchar ) :
    thestring              = fidin.read( nchar )           # Direct binary string read.
    return thestring

# -----------------------------------------------------------------------------------
def getszstring( fidin ) :
    curpos                 = fidin.tell()                  # Save current position.
    for ii in range( 1000 ) :
        thebyte            = getbyte( fidin )
        if ( thebyte == 0 ) : break

    nchar                  = ii
    fidin.seek( curpos, 0 )
    thestring              = fidin.read( nchar )           # Direct binary string read.
    strstring              = thestring.decode()
    return strstring

# -----------------------------------------------------------------------------------
def gobblebytes( fidin ) :
    curpos                 = fidin.tell()                  # Save current position.
    thebytes               = array.array( 'B' )
    for ii in range( 1000 ) :
        thebyte            = getubyte( fidin )
        if ( ( thebyte >= 97 ) and ( thebyte <= 122 ) ) or ( thebyte == 65 ) : 
            fidin.seek( -1, 1 )                            # Back up the one byte.
            break
        else :
            thebytes.append( thebyte )

    return thebytes 

# -----------------------------------------------------------------------------------
def gobblenullbytes( fidin ) :
    nullbytes              = array.array( 'B' )
    for ii in range( 1000 ) :
        thebyte            = getubyte( fidin )
        if ( thebyte == 0 ) :
            nullbytes.append( thebyte )
        else:
            fidin.seek( -1, 1 )
            break

    return nullbytes


# ===================================================================================
#                            Putters for binary files.                              |
# ===================================================================================

# -----------------------------------------------------------------------------------
def putbyte( thebyte, fidout ) :
    fidout.write( struct.pack( 'b', thebyte ) )            # 'b' is signed byte.
    return  

# -----------------------------------------------------------------------------------
def putubyte( thebyte, fidout ) :
    fidout.write( struct.pack( 'B', thebyte ) )            # 'B' is unsigned byte.
    return  

# -----------------------------------------------------------------------------------
def putshort( theshort, fidout ) :
    fidout.write( struct.pack( 'h', theshort ) )           # 'h' is signed short.
    return  

# -----------------------------------------------------------------------------------
def putushort( theshort, fidout ) :
    fidout.write( struct.pack( 'H', theshort ) )           # 'H' is unsigned short.
    return  

# -----------------------------------------------------------------------------------
def putint( theint, fidout ) :
    fidout.write( struct.pack( 'i', theint ) )             # 'i' is signed int.
    return  

# -----------------------------------------------------------------------------------
def putuint( theint, fidout ) :
    fidout.write( struct.pack( 'I', theint ) )             # 'I' is unsigned int.
    return  

# -----------------------------------------------------------------------------------
def putfloat( thefloat, fidout ) :
    fidout.write( struct.pack( 'f', thefloat ) )           # 'f' is float.
    return  

# -----------------------------------------------------------------------------------
def putstring( thestring, fidout ) :
    fidout.write( thestring )
    return  

# -----------------------------------------------------------------------------------
def putzerobytes( n, fidout ) :
    for ii in range(n) :
        putubyte( 0, fidout )
    return  


# ===================================================================================
#                            Formatters.                                            |
# ===================================================================================


# -----------------------------------------------------------------------------------
#    Strips trailing \0's. (Mete's fault.)  Used for fixed length comments that     |
# have null bytes padding them out to a fixed byte length.                          |
# -----------------------------------------------------------------------------------
def zipstrip( string ) :
    nch                    = len( string )
    for ii in range( nch ) :
        (val,)             = struct.unpack( 'b', string[ii] ) # Read each byte and break on a null.
        if val == 0 :
            break

    stripstring            = string[0:ii]

    return stripstring

# -----------------------------------------------------------------------------------
#    Format float into a string with nfield.ndecimal fixed output.                  |
# -----------------------------------------------------------------------------------
def formatfloat( x, nfield, ndecimal ) :

    formatstring           = '%+' + str( nfield ) + '.' + str( ndecimal ) + 'f'

    xstr                   = formatstring % x
    return xstr       

# -----------------------------------------------------------------------------------
#    Splits a full path name into path, filename with no extension, and extension.  |
# -----------------------------------------------------------------------------------
def splitpath( fullfilename ) :

    ( fpath, ftemp )       = os.path.split( fullfilename )
    ( fname, fext  )       = os.path.splitext( ftemp )

    fileparts              = [ fpath, fname, fext ]
    return fileparts

# -----------------------------------------------------------------------------------
#                            getDragonImage()                                       |
# -----------------------------------------------------------------------------------
#                                                                                   |
#    RGB representation of the dragon logo.                                         |
#                                                                                   |
# -----------------------------------------------------------------------------------
def getDragonImage() :
    stringarray            = []
    stringarray.append(  "{#000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #000000 #000000 #000000 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #000000 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #3c00fe #000000 #fe8040 #000000 #3c00fe #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #3c00fe #000000 #fe0080 #000000 #3c00fe #000000 #0000fe #0000fe #3c00fe #3c00fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #fe8040 #000000 #3c00fe #3c00fe #3c00fe #0000fe #0000fe #3c00fe #0000fe #0000fe #0000fe #0000fe #80007f #000000 #000000 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #000000 #3c00fe #3c00fe #3c00fe #3c00fe #0000fe #0000fe #3c00fe #0000fe #0000fe #0000fe #000000 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #000000 #3c00fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #000000 #3c00fe #3c00fe #0000fe #0000fe #0000fe #0000fe #0000fe #3c00fe #0000fe #000000 #fe8040 #fe0080 #fe0080 #fe0080 #fe0080 #fe0080 #fe8040 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe0080 #fe8040 #000000 #3c00fe #0000fe #0000fe #0000fe #0000fe #0000fe #3c00fe #000000 #fe8040 #80007f #fe0080 #fe0080 #000000 #fe0080 #fe0080 #fe8040 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #000000 #0000fe #0000fe #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe0080 #fe8040 #000000 #000000 #0000fe #0000fe #0000fe #0000fe #3c00fe #000000 #fe0080 #fe8040 #fe0080 #000000 #0000fe #000000 #fe8040 #fe0080 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fefe80 #000000 #0000fe #000000 #000000 #0000fe #0000fe #0000fe #3c00fe #0000fe #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #80007f #fe0080 #fe8040 #fe8040 #000000 #0000fe #0000fe #0000fe #3c00fe #000000 #fe8040 #fe8040 #80007f #000000 #3c00fe #000000 #fe8040 #fe0080 #000000 #0000fe #000000 #000000 #000000 #fefef0 #fefef0 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fefe80 #000000 #000000 #000000 #fefe80 #000000 #3c00fe #3c00fe #3c00fe #0000fe #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fefef0 #fefef0 #0000fe #000000 #000000 #fe0080 #fe8040 #fe8040 #000000 #000000 #000000 #000000 #000000 #000000 #fe0080 #fe8040 #fe0080 #000000 #000000 #fe8040 #000000 #3c00fe #000000 #fe8040 #fe8040 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fefe80 #fefe80 #fefe80 #000000 #fefe80 #fefe80 #000000 #000000 #000000 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fefef0 #000000 #3c00fe #3c00fe #0000fe #000000 #000000 #80007f #fe0080 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #000000 #000000 #000000 #fe8040 #fe8040 #000000 #fefef0 #fefef0 #0000fe #0000fe #000000 #000000 #000000 #000000 #000000 #fefef0 #fefef0 #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #000000 #fefe80 #fefe80 #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #fe8040 #fe8040 #fefef0 #fefef0 #0000fe #0000fe #000000 #000000 #000000 #fe0080 #80007f #fe0080 #fe0080 #80007f #fe0080 #000000 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #000000 #000000 #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #fe8040 #fe0080 #fe8040 #fe8040 #000000 #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fefe80 #fefe80 #fefe80 #000000 #802e00 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #fe8040 #80007f #fe8040 #fe8040 #000000 #3c00fe #000000 #fe8040 #fe8040 #fe8040 #000000 #000000 #000000 #000000 #000000 #000000 #3c00fe #3c00fe #000000 #000000 #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #fe0080 #000000 #000000 #0000fe #000000 #fe8040 #fe8040 #80007f #fe8040 #fe8040 #fe8040 #fe8040 #fefef0 #fefef0 #3c00fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fefe80 #fefe80 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #0000fe #0000fe #0000fe #000000 #0000fe #000000 #fe8040 #80007f #fe8040 #fe8040 #000000 #000000 #fefef0 #fefef0 #000000 #fe8040 #fe8040 #fe8040 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #fe0080 #fe8040 #fe8040 #fe0080 #fe0080 #fe0080 #000000 #000000 #fe8040 #fe8040 #fe8040 #000000 #000000 #000000 #000000 #0000fe #0000fe #3c00fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #802e00 #fefe80 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #000000 #000000 #000000 #0000fe #0000fe #000000 #fe8040 #fe8040 #fe8040 #000000 #3c00fe #3c00fe #3c00fe #0000fe #3c00fe #000000 #fe8040 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #000000 #000000 #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #80007f #fe0080 #000000 #000000 #000000 #0000fe #0000fe #0000fe #fefef0 #fefef0 #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fefe80 #802e00 #fefe80 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #000000 #0000fe #0000fe #000000 #80007f #fe8040 #000000 #3c00fe #3c00fe #3c00fe #000000 #000000 #000000 #000000 #fe8040 #fe8040 #000000 #000000 #000000 #000000 #000000 #000000 #80007f #000000 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #fe8040 #fe0080 #fe8040 #80007f #fe8040 #fe0080 #80007f #fe0080 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #3c00fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #000000 #000000 #3c00fe #000000 #fe8040 #fe8040 #000000 #3c00fe #000000 #000000 #ffff00 #ffff00 #ffff00 #000000 #fe8040 #fe8040 #000000 #ffff00 #ffff00 #ffff00 #ffff00 #ffff00 #80007f #ffff00 #000000 #000000 #fe8040 #fe8040 #fe8040 #000000 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #80007f #fe0080 #fe0080 #fe0080 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #000000 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #802e00 #fefe80 #802e00 #802e00 #fefe80 #fefe80 #802e00 #fefe80 #000000 #000000 #fe8040 #fe8040 #fe8040 #000000 #ffff00 #ffff00 #80007f #ffff00 #ffff00 #000000 #fe0080 #fe8040 #000000 #ffff00 #ffff00 #ffff00 #80007f #ffff00 #ffff00 #ffff00 #80007f #ffff00 #000000 #fe8040 #000000 #3c00fe #0000fe #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #80007f #fe00ac #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #000000 #fefe80 #fefe80 #802e00 #fefe80 #802e00 #fefe80 #802e00 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #fefe80 #000000 #fe8040 #fe8040 #000000 #80007f #ffff00 #ffff00 #ffff00 #ffff00 #000000 #fe8040 #fe8040 #fe0080 #000000 #80007f #80007f #fe8040 #fe8040 #fe8040 #ffff00 #ffff00 #ffff00 #ffff00 #fefe80 #000000 #000000 #3c00fe #000000 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #80007f #fe0080 #fe0080 #fe00ac #000000 #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #000000 #000000 #fefe80 #fefe80 #802e00 #fefe80 #802e00 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #000000 #ffff00 #ffff00 #ffff00 #ffff00 #ffff00 #000000 #fe8040 #fe0080 #fe8040 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #80007f #fe8040 #fe8040 #fe8040 #80007f #ffff00 #fefe80 #000000 #000000 #fe8040 #fe8040 #fe8040 #000000 #fe8040 #80007f #fe8040 #fe8040 #fe0080 #fe0080 #80007f #000000 #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #000000 #fefe80 #fefe80 #fefe80 #802e00 #802e00 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #ffff00 #ffff00 #ffff00 #ffff00 #000000 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #fe0080 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #fe8040 #ffff00 #ffff00 #fefe80 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #fe0080 #80007f #fe0080 #fe00ac #000000 #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #000000 #fefe80 #fefe80 #fefe80 #802e00 #fefe80 #802e00 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #ffff00 #ffff00 #80007f #ffff00 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #fe8040 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #000000 #fe8040 #fe8040 #fe0080 #fe8040 #fefe80 #000000 #fe8040 #fe0080 #fe0080 #fe8040 #000000 #fe8040 #fe0080 #fe8040 #80007f #fe0080 #fe0080 #fe00ac #000000 #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fefe80 #fefe80 #802e00 #fefe80 #802e00 #fefe80 #fefe80 #fefe80 #000000 #ffff00 #80007f #ffff00 #ffff00 #fe8040 #fe8040 #000000 #fe8040 #80007f #fe8040 #000000 #fe8040 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #000000 #000000 #ffff00 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #000000 #fe8040 #fe8040 #000000 #0000fe #000000 #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #80007f #000000 #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #808080 #0000fe #0000fe #0000fe #000000 #fefe80 #fefe80 #000000 #fefe80 #802e00 #fefe80 #fefe80 #fefe80 #000000 #ffff00 #ffff00 #ffff00 #ffff00 #80007f #fe8040 #000000 #80007f #fe0080 #fe0080 #fe0080 #fe8040 #fe8040 #000000 #fe0080 #000000 #000000 #fefe80 #fefe80 #ffff00 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #0000fe #000000 #fe8040 #fe8040 #fe8040 #fe0080 #80007f #fe0080 #fe00ac #000000 #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #808080 #808080 #0000fe #0000fe #0000fe #0000fe #000000 #000000 #fefe80 #fefe80 #802e00 #fefe80 #fefe80 #000000 #ffff00 #ffff00 #ffff00 #ffff00 #ffff00 #fe8040 #fe8040 #fe0080 #000000 #fe0080 #fe0080 #fe0080 #fe8040 #fefe80 #fefe80 #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #fe0080 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #0000fe #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #fe00ac #000000 #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #c0bfbf #c0bfbf #808080 #0000fe #0000fe #0000fe #0000fe #000000 #000000 #fefe80 #802e00 #fefe80 #fefe80 #000000 #ffff00 #80007f #fefe80 #80007f #fe8040 #fe8040 #80007f #fe0080 #fe0080 #fe0080 #fe0080 #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #ffff00 #000000 #fe0080 #fe0080 #fe8040 #fe8040 #80007f #fe8040 #fe8040 #fe8040 #000000 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #80007f #000000 #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #808080 #808080 #c0bfbf #808080 #0000fe #0000fe #0000fe #0000fe #000000 #802e00 #802e00 #fefe80 #000000 #000000 #ffff00 #ffff00 #ffff00 #ffff00 #fe8040 #fe0080 #fe0080 #80007f #000000 #000000 #000000 #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #000000 #ffff00 #000000 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #fe8040 #fe8040 #80007f #fe8040 #fe8040 #fe0080 #80007f #fe8040 #000000 #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #808080 #c0bfbf #c0bfbf #808080 #000000 #000000 #000000 #000000 #fefe80 #fefe80 #fefe80 #000000 #000000 #ffff00 #80007f #ffff00 #ffff00 #fe8040 #fe0080 #fe0080 #000000 #0000fe #0000fe #0000fe #0000fe #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #000000 #000000 #fefe80 #fefe80 #fefe80 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #80007f #fe8040 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #80007f #fe0080 #fe0080 #000000 #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #808080 #c0bfbf #808080 #3c00fe #0000fe #000000 #000000 #000000 #000000 #000000 #0000fe #0000fe #000000 #ffff00 #ffff00 #fe8040 #80007f #fe0080 #fe0080 #000000 #0000fe #000000 #000000 #0000fe #3c00fe #000000 #fefe80 #000000 #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #000000 #fe8040 #fe8040 #fe0080 #fe8040 #fe8040 #fe0080 #80007f #fe0080 #000000 #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #808080 #c0bfbf #c0bfbf #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #ffff00 #ffff00 #fe8040 #80007f #80007f #80007f #000000 #3c00fe #000000 #ffff00 #000000 #3c00fe #000000 #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #fe8040 #fe8040 #80007f #fe8040 #fe8040 #fe8040 #000000 #fe8040 #80007f #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #fe0080 #000000 #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #ffff00 #0000fe #0000fe #808080 #c0bfbf #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #80007f #ffff00 #fe8040 #fe0080 #fe0080 #000000 #0000fe #000000 #ffff00 #ffff00 #000000 #000000 #fefe80 #fefe80 #7e1000 #7e1000 #7e1000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #fe8040 #fe8040 #000000 #000000 #000000 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #fe0080 #000000 #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #ffff00 #ffff00 #0000fe #808080 #c0bfbf #808080 #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #ffff00 #ffff00 #ffff00 #fe8040 #fe0080 #fe0080 #000000 #0000fe #000000 #fefe80 #fefe80 #fefe80 #7e1000 #fefe80 #fefe80 #fefe80 #fefe80 #7e1000 #7e1000 #7e1000 #7e1000 #7e1000 #7e1000 #fe0080 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #80007f #000000 #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fe0000 #fe0000 #ffff00 #ffff00 #c0bfbf #c0bfbf #808080 #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #ffff00 #ffff00 #fe8040 #fe0080 #80007f #000000 #0000fe #000000 #ffff00 #fefe80 #fefe80 #fefe80 #7e1000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #7e1000 #7e1000 #7e1000 #7e1000 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe0080 #fe0080 #80007f #80007f #fe0080 #000000 #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #ffff00 #ffff00 #fe0000 #fe0000 #ffff00 #c0bfbf #c0bfbf #808080 #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #ffff00 #ffff00 #80007f #fe0080 #000000 #0000fe #000000 #ffff00 #fefe80 #fefe80 #fefe80 #fefe80 #7e1000 #7e1000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #fe0080 #80007f #fe0080 #fe0080 #fe8040 #fe8040 #fe8040 #80007f #fe0080 #fe0080 #fe0080 #fe0080 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #ffff00 #ffff00 #fe0000 #fe0000 #ffff00 #c0bfbf #c0bfbf #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #3c00fe #000000 #ffff00 #fe8040 #fe8040 #80007f #000000 #0000fe #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #7e1000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #80007f #fe0080 #fe0080 #80007f #fe0080 #80007f #fe0080 #fe0080 #80007f #fe0080 #000000 #000000 #3c00fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #ffff00 #fe0000 #fe0000 #ffff00 #ffff00 #c0bfbf #808080 #808080 #0000fe #0000fe #000000 #000000 #000000 #000000 #000000 #000000 #ffff00 #ffff00 #ffff00 #80007f #fe0080 #000000 #0000fe #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #7e1000 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #000000 #fe0080 #fe0080 #fe0080 #80007f #fe0080 #fe0080 #80007f #fe0080 #fe0080 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #808080 #808080 #ffff00 #fe0000 #fe0000 #fe0000 #fe0000 #ffff00 #ffff00 #808080 #ffff00 #0000fe #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #ffff00 #fe8040 #fe8040 #fe0080 #000000 #000000 #0000fe #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #7e1000 #ffff00 #fefe80 #fefe80 #000000 #3c00fe #000000 #000000 #000000 #80007f #fe0080 #fe0080 #fe0080 #000000 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #c0bfbf #c0bfbf #c0bfbf #ffff00 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #ffff00 #fe0000 #fe0000 #000000 #000000 #000000 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #80007f #fe0080 #000000 #0000fe #000000 #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #7e1000 #ffff00 #fefe80 #000000 #3c00fe #3c00fe #0000fe #3c00fe #000000 #000000 #000000 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #c0bfbf #c0bfbf #c0bfbf #c0bfbf #ffff00 #fe0000 #fe0000 #fe0000 #fe0000 #ffff00 #ffff00 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #000000 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #fe8040 #fe0080 #80007f #000000 #0000fe #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #7e1000 #ffff00 #fefe80 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #808080 #808080 #ffff00 #ffff00 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #ffff00 #ffff00 #ffff00 #000000 #000000 #000000 #fe8040 #fe8040 #fe8040 #fe8040 #80007f #fe8040 #fe8040 #fe8040 #80007f #fe0080 #000000 #0000fe #0000fe #000000 #ffff00 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #7e1000 #ffff00 #000000 #3c00fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #808080 #ffff00 #fe0000 #fe0000 #fe0000 #fe0000 #ffff00 #ffff00 #fe0000 #ffff00 #ffff00 #000000 #fe8040 #000000 #fe8040 #fe8040 #fe8040 #80007f #80007f #fe8040 #fe0080 #000000 #fefef0 #000000 #fe8040 #fe0080 #000000 #0000fe #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #7e1000 #000000 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #808080 #fe0000 #fe0000 #fe0000 #ffff00 #808080 #808080 #ffff00 #fe0000 #ffff00 #c0bfbf #c0bfbf #000000 #000000 #000000 #000000 #000000 #000000 #000000 #fe0080 #fe0080 #000000 #000000 #fe8040 #fe0080 #fe0080 #000000 #0000fe #0000fe #000000 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #0000fe #0000fe #0000fe #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #ffff00 #808080 #ffff00 #c0bfbf #c0bfbf #ffff00 #fe0000 #fe0000 #ffff00 #808080 #c0bfbf #808080 #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #000000 #fe0080 #fe0080 #000000 #000000 #fe8040 #000000 #0000fe #0000fe #0000fe #000000 #ffff00 #fefe80 #fefe80 #fefe80 #fefe80 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #ffff00 #fe0000 #ffff00 #c0bfbf #808080 #ffff00 #ffff00 #fe0000 #ffff00 #ffff00 #808080 #c0bfbf #c0bfbf #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #0000fe #0000fe #000000 #fe8040 #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #ffff00 #fefe80 #fefe80 #fefe80 #000000 #3c00fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #ffff00 #808080 #c0bfbf #c0bfbf #ffff00 #ffff00 #ffff00 #fe0000 #ffff00 #ffff00 #808080 #808080 #c0bfbf #808080 #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #0000fe #0000fe #000000 #80007f #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #7e1000 #ffff00 #fefe80 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #808080 #c0bfbf #c0bfbf #808080 #ffff00 #fe0000 #fe0000 #fe0000 #ffff00 #ffff00 #0000fe #808080 #c0bfbf #808080 #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #fe8040 #0000fe #000000 #fe8040 #80007f #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #000000 #fefe80 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #808080 #c0bfbf #808080 #ffff00 #fe0000 #fe0000 #fe0000 #ffff00 #ffff00 #0000fe #0000fe #808080 #c0bfbf #c0bfbf #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #0000fe #0000fe #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #7e1000 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #c0bfbf #808080 #ffff00 #fe0000 #fe0000 #fe0000 #ffff00 #0000fe #0000fe #0000fe #808080 #808080 #c0bfbf #808080 #808080 #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #7e1000 #3c00fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #ffff00 #ffff00 #fe0000 #fe0000 #ffff00 #ffff00 #0000fe #0000fe #0000fe #808080 #808080 #c0bfbf #c0bfbf #c0bfbf #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #7e1000 #7e1000 #3c00fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #ffff00 #fe0000 #ffff00 #ffff00 #0000fe #0000fe #0000fe #0000fe #808080 #808080 #c0bfbf #808080 #808080 #c0bfbf #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #000000 #000000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #ffff00 #ffff00 #ffff00 #0000fe #0000fe #0000fe #808080 #808080 #808080 #c0bfbf #c0bfbf #808080 #808080 #c0bfbf #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #ffff00 #ffff00 #0000fe #0000fe #808080 #c0bfbf #808080 #c0bfbf #c0bfbf #c0bfbf #808080 #808080 #c0bfbf #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #ffff00 #0000fe #0000fe #0000fe #808080 #c0bfbf #c0bfbf #808080 #c0bfbf #808080 #c0bfbf #808080 #808080 #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #808080 #c0bfbf #c0bfbf #808080 #808080 #c0bfbf #c0bfbf #808080 #808080 #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #808080 #808093 #c0bfbf #c0bfbf #808080 #c0bfbf #808080 #0000fe #0000fe #808080 #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #0000fe #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #fe0000 #000000 }" )
    stringarray.append(  "{#808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #808080 #000000 }" )

    return stringarray

# ===================================================================================
#                            Class skeletonHeader                                   |
# ===================================================================================
class skeletonHeader( object ) :
    """ 
    Description:  skeletonHeader class for RTW skeleton files.  
                  Can read from or write the header part of a skeleton file produced 
                  from Vercingetorix's xidx.exe program.  

    Derives from: object

    Attributes:   
       .scale          
       .nbones   

    Data section: None

    Methods:      
       .__init__
       .fromfile
       .tofile
       .fromtextfile
       .totextfile
    """

    # -------------------------------------------------------------------------------
    #                        __init__()                                             |
    # -------------------------------------------------------------------------------
    def __init__( self ) :
        return

    # -------------------------------------------------------------------------------
    #                        fromfile()                                             |
    # -------------------------------------------------------------------------------
    def fromfile( self, fid ) :
        self.scale         = getfloat(  fid )
        self.nbones        = getuint(   fid )              

        return self.nbones       

    # -------------------------------------------------------------------------------
    #                        tofile()                                               |
    # -------------------------------------------------------------------------------
    def tofile( self, fid ) :
        # Header.
        putfloat( self.scale,          fid )
        putuint(  self.nbones,         fid )              

        return

    # -------------------------------------------------------------------------------
    #                        totextfile()                                           |
    # -------------------------------------------------------------------------------
    def totextfile( self, fidtxt ) :
        fidtxt.write( formatfloat( self.scale, 12, 7 ) + '\n' )
        fidtxt.write( str( self.nbones ) + '\n' )
        return

    # -------------------------------------------------------------------------------
    #                        fromtextfile()                                         |
    # -------------------------------------------------------------------------------
    def fromtextfile( self, fidtxt ) :
        line               = fidtxt.readline()
        tokens             = line.split()
        self.scale         = float( tokens[0] )
        line               = fidtxt.readline()
        tokens             = line.split()
        self.nbones        = int( tokens[0] )

        return self.nbones       

# ===================================================================================
#                            Class skeletonBoneSection                              |
# ===================================================================================
class skeletonBoneSection( object ) :
    """ 
    Description:  skeletonBoneSection class for RTW skeleton files.  
                  Can read from or write the bone section part of a skeleton file 
                  produced from Vercingetorix's xidx.exe program.  

    Derives from: object

    Attributes:   
       .nbones

    Data section: 
       .ivallist
       .bonelist
       .hierarchy

    Methods:      
       .__init__
       .fromfile
       .tofile
       .fromtextfile
       .totextfile
    """

    # -------------------------------------------------------------------------------
    #                        __init__()                                             |
    # -------------------------------------------------------------------------------
    def __init__( self, nbones  ) :

        self.nbones        = nbones
 
        return

    # -------------------------------------------------------------------------------
    #                        fromfile()                                             |
    # -------------------------------------------------------------------------------
    def fromfile( self, fid ) :

        self.ivallist      = []
        self.bonelist      = []
        self.hierarchy     = []
        for ibone in range( self.nbones ) :
            eightbytes     = array.array( 'B' )
            eightbytes.fromfile( fid, 8 )
            self.ivallist.append( eightbytes )
#            short1         = getushort( fid )
#            int1           = getint(   fid )
#            short2         = getshort( fid )
#            self.ivallist.append( [ short1, int1, short2 ] )
            bones          = array.array( 'f' )
            bones.fromfile( fid, 3 )
            self.bonelist.append( bones )
            self.hierarchy.append( getint( fid ) )

        return 

    # -------------------------------------------------------------------------------
    #                        tofile()                                               |
    # -------------------------------------------------------------------------------
    def tofile( self, fid ) :

        for ibone in range( self.nbones ) :
            self.ivallist[ibone].tofile( fid )
#            putushort( self.ivallist[ibone][0], fid )
#            putuint(   self.ivallist[ibone][1], fid )
#            putushort( self.ivallist[ibone][2], fid )
            putfloat(  self.bonelist[ibone][0], fid )
            putfloat(  self.bonelist[ibone][1], fid )
            putfloat(  self.bonelist[ibone][2], fid )
            putint(    self.hierarchy[ibone],   fid )

        return

    # -------------------------------------------------------------------------------
    #                        totextfile()                                           |
    # -------------------------------------------------------------------------------
    def totextfile( self, fidtxt ) :

        for ibone in range( self.nbones ) :
            for ii in range( 8 ) : fidtxt.write( str( self.ivallist[ibone][ii] ).rjust(3) + ' ' )
#            fidtxt.write( str( self.ivallist[ibone][0] ).rjust(5) + ' ' )
#            fidtxt.write( str( self.ivallist[ibone][1] ).rjust(5) + ' ' )
#            fidtxt.write( str( self.ivallist[ibone][2] ).rjust(5) + ' ' )
            fidtxt.write( formatfloat( self.bonelist[ibone][0], 12, 7 ) + ' ' )
            fidtxt.write( formatfloat( self.bonelist[ibone][1], 12, 7 ) + ' ' )
            fidtxt.write( formatfloat( self.bonelist[ibone][2], 12, 7 ) + ' ' )
            fidtxt.write( str( self.hierarchy[ibone] ).rjust(5) + '\n' )

        return

    # -------------------------------------------------------------------------------
    #                        fromtextfile()                                         |
    # -------------------------------------------------------------------------------
    def fromtextfile( self, fidtxt ) :

        self.ivallist      = []
        self.bonelist      = []
        self.hierarchy     = []
        for ibone in range( self.nbones ) :
            eightbytes     = array.array( 'B' )
            line           = fidtxt.readline()
            tokens         = line.split()
            for ii in range( 8 ) : eightbytes.append( int( tokens[ii] ) )
            self.ivallist.append( eightbytes )
            bones          = array.array( 'f' )
            bones.append( float( tokens[8] ) )
            bones.append( float( tokens[9] ) )
            bones.append( float( tokens[10] ) )
            self.bonelist.append( bones )
            self.hierarchy.append( int( tokens[11] ) )

#            self.ivallist.append( [ int( tokens[0] ), int( tokens[1] ), int( tokens[2] ) ] )
#            bones          = array.array( 'f' )
#            bones.append( float( tokens[3] ) )
#            bones.append( float( tokens[4] ) )
#            bones.append( float( tokens[5] ) )
#            self.bonelist.append( bones )

        return

# ===================================================================================
#                            Class skeletonAnimEntry                                |
# ===================================================================================
class skeletonAnimEntry( object ) :
    """ 
    Description:  skeletonAnimEntry class for RTW skeleton files.  
                  Can read from or write a single animation entry in the AnimSection 
                  part of a skeleton file produced from Vercingetorix's xidx.exe program.  

    Derives from: object

    Attributes:   
       .casstring
       .nullbyte
       .short
       .sixfloats
       .sigbytes
       .twentyeightbytes
       .threefloats
       .nanims
       .extranulls

    Data section: 
       .animlist
       .trailingnulls

    Methods:      
       .__init__
       .fromfile
       .tofile
       .fromtextfile
       .totextfile
    """

    # -------------------------------------------------------------------------------
    #                        __init__()                                             |
    # -------------------------------------------------------------------------------
    def __init__( self ) :

        return

    # -------------------------------------------------------------------------------
    #                        fromfile()                                             |
    # -------------------------------------------------------------------------------
    def fromfile( self, fid, filesize ) :

#        self.sixfloats     = array.array( 'f' )
#        self.sigbytes      = array.array( 'B' )
        self.twentyeightbytes = array.array( 'B' )
        self.threefloats   = array.array( 'f' )
        self.extranulls    = array.array( 'B' )
        self.trailingnulls = array.array( 'B' )
        self.animlist      = []

        self.casstring     = getszstring( fid )
        self.casstring     = self.casstring.replace( ' ', '~' )
        self.nullbyte      = getubyte(    fid )
        self.short         = getushort(   fid )
#        for ii in range( 6 ) : self.sixfloats.append(   getfloat( fid ) )
#        for ii in range( 4 ) : self.sigbytes.append(    getubyte( fid ) )
        for ii in range( 28 ) : self.twentyeightbytes.append( getubyte( fid ) )
        for ii in range( 3 ) :  self.threefloats.append( getfloat( fid ) )
        self.nanims        = getuint(     fid )
        # Check for extra nulls after the nanims entry.
        curpos             = fid.tell()
        bytesleft          = filesize - curpos
        if ( bytesleft < 140 ) :
            for ii in range( bytesleft - 14 ) :
                thebyte    = getubyte( fid )
                if ( thebyte == 0 ) : 
                    self.trailingnulls.append( thebyte )
                else:
                    fid.seek( -1, 1 )
                    break
        else:
            nullbytes      = gobblenullbytes( fid ) 
            for ii in range( len( nullbytes ) ) : self.extranulls.append( nullbytes[ii] )
        for ianim in range( self.nanims ) :
            eightbytes     = array.array( 'B' )
            threebytes     = array.array( 'B' )
            eightbytes.fromfile( fid, 8 )
            name           = getszstring( fid )
            threebytes.fromfile( fid, 3 )
            self.animlist.append( [ eightbytes, name, threebytes ] )

        # Check for extra nulls after the last entry.
        curpos             = fid.tell()
        bytesleft          = filesize - curpos
        if ( bytesleft < 140 ) :
            for ii in range( bytesleft - 14 ) :
                thebyte    = getubyte( fid )
                if ( thebyte == 0 ) : 
                    self.trailingnulls.append( thebyte )
                else:
                    fid.seek( -1, 1 )
                    break
        else:
            nullbytes      = gobblenullbytes( fid ) 
            for ii in range( len( nullbytes ) ) : self.trailingnulls.append( nullbytes[ii] )
        
        return 

    # -------------------------------------------------------------------------------
    #                        tofile()                                               |
    # -------------------------------------------------------------------------------
    def tofile( self, fid ) :

        putstring( self.casstring.encode(), fid )
        putubyte(  self.nullbyte,  fid )
        putushort( self.short,     fid )
#        self.sixfloats.tofile(     fid )
#        self.sigbytes.tofile(      fid )
        self.twentyeightbytes.tofile( fid )
        self.threefloats.tofile(   fid )

        putuint(   self.nanims,    fid )
        self.extranulls.tofile(    fid )

        for ianim in range( self.nanims ) :
            self.animlist[ianim][0].tofile( fid )
            putstring( self.animlist[ianim][1].encode(), fid )
            self.animlist[ianim][2].tofile( fid )

        self.trailingnulls.tofile(    fid )

        return

    # -------------------------------------------------------------------------------
    #                        totextfile()                                           |
    # -------------------------------------------------------------------------------
    def totextfile( self, fidtxt ) :

        fidtxt.write( self.casstring.ljust( 80 ) )
        fidtxt.write( '  ' + str( self.nullbyte ) + '  ' + str( self.short ).rjust(5) + '      ' )
#        for ii in range( 6 ) : fidtxt.write( formatfloat( self.sixfloats[ii], 8, 4 ) + ' ' )
#        for ii in range( 4 ) : fidtxt.write( str( self.sigbytes[ii] ).rjust(3) + ' ' )
        for ii in range( 28 ) :
            fidtxt.write( str( self.twentyeightbytes[ii] ).rjust(3) + ' ' )
            if ( (ii+1)%4 == 0 ) : fidtxt.write( '  ' )
        for ii in range( 3 ) : fidtxt.write( formatfloat( self.threefloats[ii], 8, 4 ) + ' ' )
        fidtxt.write( '\n' )

        fidtxt.write( str( self.nanims ).rjust(3) + '   ' )
        for ii in range( len( self.extranulls ) ) : fidtxt.write( str( self.extranulls[ii] ).rjust(1) + ' ' )

        for ianim in range( self.nanims ) :
            fidtxt.write( '\n' )
            for ii in range( len( self.animlist[ianim][0] ) ) : fidtxt.write( str( self.animlist[ianim][0][ii] ).rjust(2) + ' ' )
            fidtxt.write( self.animlist[ianim][1].ljust( 25 ) )
            for ii in range( len( self.animlist[ianim][2] ) ) : fidtxt.write( str( self.animlist[ianim][2][ii] ).rjust(2) + ' ' )

        fidtxt.write( '   ' )
        for ii in range( len( self.trailingnulls ) ) : fidtxt.write( str( self.trailingnulls[ii] ).rjust(1) + ' ' )
        fidtxt.write( '\n' )

        return

    # -------------------------------------------------------------------------------
    #                        fromtextfile()                                         |
    # -------------------------------------------------------------------------------
    def fromtextfile( self, fidtxt ) :

#        self.sixfloats     = array.array( 'f' )
#        self.sigbytes      = array.array( 'B' )
        self.twentyeightbytes = array.array( 'B' )
        self.threefloats   = array.array( 'f' )
        self.extranulls    = array.array( 'B' )
        self.trailingnulls = array.array( 'B' )
        self.animlist      = []

        # First line.
        line               = fidtxt.readline()
        tokens             = line.split()
        self.casstring     = tokens[0] 
        self.casstring     = self.casstring.replace( '~', ' ' )
        self.nullbyte      = int( tokens[1] )
        self.short         = int( tokens[2] )

        for ii in range( 3, 28+3 ) :
            self.twentyeightbytes.append( int( tokens[ii] ) )
#        self.sixfloats.append(   float( tokens[3] ) )
#        self.sixfloats.append(   float( tokens[4] ) )
#        self.sixfloats.append(   float( tokens[5] ) )
#        self.sixfloats.append(   float( tokens[6] ) )
#        self.sixfloats.append(   float( tokens[7] ) )
#        self.sixfloats.append(   float( tokens[8] ) )
#        self.sigbytes.append(    int(   tokens[9] ) )
#        self.sigbytes.append(    int(   tokens[10] ) )
#        self.sigbytes.append(    int(   tokens[11] ) )
#        self.sigbytes.append(    int(   tokens[12] ) )
        self.threefloats.append( float( tokens[31] ) )
        self.threefloats.append( float( tokens[32] ) )
        self.threefloats.append( float( tokens[33] ) )

        # Second line with the anim count, may have extra nulls.
        line               = fidtxt.readline()
        tokens             = line.split()
        ntoks              = len( tokens )
        self.nanims        = int( tokens[0] )
        for ii in range( 1, ntoks ) :
            self.extranulls.append( int( tokens[ii] ) )

        # Rest of the lines are anim entries.
        for ianim in range( self.nanims ) :
            line           = fidtxt.readline()
            tokens         = line.split()
            ntoks          = len( tokens )
            eightbytes     = array.array( 'B' )
            threebytes     = array.array( 'B' )
            trailingnulls  = array.array( 'B' )
            for ii in range( 8 ) : eightbytes.append( int( tokens[ii] ) )
            name           = tokens[8]
            for ii in range( 9, 12 ) : threebytes.append( int( tokens[ii] ) )
            self.animlist.append( [ eightbytes, name, threebytes ] )
            if ( ntoks > 12 ):
                for ii in range( 12, ntoks ) : self.trailingnulls.append( int( tokens[ii] ) )

        return

# ===================================================================================
#                            Class skeletonAnimSection                              |
# ===================================================================================
class skeletonAnimSection( object ) :
    """ 
    Description:  skeletonAnimSection class for RTW skeleton files.  
                  Can read from or write the anim section part of a skeleton file produced 
                  from Vercingetorix's xidx.exe program.  The workhorse class for this  
                  is class skeletonAnimEntry which does all the heavy lifting.

    Derives from: object

    Attributes:   
       .filesize       
       .nentries       

    Data section: 
       .entrylist

    Methods:      
       .__init__
       .fromfile
       .tofile
       .fromtextfile
       .totextfile
    """

    # -------------------------------------------------------------------------------
    #                        __init__()                                             |
    # -------------------------------------------------------------------------------
    def __init__( self ) :

        return

    # -------------------------------------------------------------------------------
    #                        fromfile()                                             |
    # -------------------------------------------------------------------------------
    def fromfile( self, fid, filesize ) :

        self.filesize      = filesize

        self.entrylist     = []
        notevenclose       = True 

        kk                 = 0
        while ( notevenclose ) :
            kk             = kk + 1
            entry          = skeletonAnimEntry()
            entry.fromfile( fid, self.filesize )
            self.entrylist.append( entry ) 

            # Check for loop termination.
            curpos         = fid.tell()
            if ( ( self.filesize - curpos ) < 20 ) :
                notevenclose = False
                self.nentries = kk

        return 

    # -------------------------------------------------------------------------------
    #                        tofile()                                               |
    # -------------------------------------------------------------------------------
    def tofile( self, fid ) :

        for ientry in range( self.nentries ) :
            self.entrylist[ientry].tofile( fid )

        return

    # -------------------------------------------------------------------------------
    #                        totextfile()                                           |
    # -------------------------------------------------------------------------------
    def totextfile( self, fidtxt ) :

        for ientry in range( self.nentries ) :
            self.entrylist[ientry].totextfile( fidtxt )

        return

    # -------------------------------------------------------------------------------
    #                        fromtextfile()                                         |
    # -------------------------------------------------------------------------------
    def fromtextfile( self, fidtxt, nentries ) :

        self.nentries      = nentries
        self.entrylist     = []
        for ientry in range( self.nentries ) :
            entry          = skeletonAnimEntry()
            entry.fromtextfile( fidtxt ) 
            self.entrylist.append( entry )

        return 

# ===================================================================================
#                            Class skeletonObject                                   |
# ===================================================================================
class skeletonObject( object ) :
    """ 
    Description:  skeletonObject class for RTW skeleton files.  
                  Can read from or write the entire skeleton file.  

    Derives from: object

    Attributes:   
       .filesize
       .zero           
       .nentries       

    Data section: 
       .header   
       .bonesection
       .animsection
       .lastfloats 
       .lastbytes  

    Methods:      
       .__init__
       .fromfile
       .tofile
       .fromtextfile
       .totextfile
    """

    # -------------------------------------------------------------------------------
    #                        __init__()                                             |
    # -------------------------------------------------------------------------------
    def __init__( self ) :

        return

    # -------------------------------------------------------------------------------
    #                        fromfile()                                             |
    # -------------------------------------------------------------------------------
    def fromfile( self, fid ) :

        # Find the filesize so you know when to quit.
        fid.seek( 0, 2 )                                   # Seek to end.
        self.filesize      = fid.tell()                    # Get the tell().
        fid.seek( 0, 0 )                                   # Seek to beginning.

        self.fourbytes     = array.array( 'B' )

        # Read the file.
        self.header        = skeletonHeader()
        nbones             = self.header.fromfile( fid )
        self.bonesection   = skeletonBoneSection( nbones )
        self.bonesection.fromfile( fid )
        self.fourbytes.fromfile( fid, 4 )
#        self.zero          = getuint( fid )
        self.animsection   = skeletonAnimSection()
        self.animsection.fromfile( fid, self.filesize )
        self.nentries      = self.animsection.nentries
        self.lastfloats    = array.array( 'f' )
        self.lastbytes     = array.array( 'B' )
        self.lastfloats.fromfile( fid, 3 )
        self.lastbytes.fromfile( fid, 2 )

        return 

    # -------------------------------------------------------------------------------
    #                        tofile()                                               |
    # -------------------------------------------------------------------------------
    def tofile( self, fid ) :

        self.header.tofile( fid )
        self.bonesection.tofile( fid )
#        putuint( self.zero,      fid )
        self.fourbytes.tofile(   fid )
        self.animsection.tofile( fid )
        self.lastfloats.tofile(  fid )
        self.lastbytes.tofile(   fid )

        return

    # -------------------------------------------------------------------------------
    #                        totextfile()                                           |
    # -------------------------------------------------------------------------------
    def totextfile( self, fidtxt ) :

        self.header.totextfile( fidtxt )
        self.bonesection.totextfile( fidtxt )
        for ii in range( 4 ) : fidtxt.write( str( self.fourbytes[ii] ).rjust(3) + ' ' )
        fidtxt.write( '\n' )
#        fidtxt.write( str( self.zero ) + '\n' )
        fidtxt.write( str( self.nentries ) + '\n' )
        self.animsection.totextfile( fidtxt )
        for ii in range( 3 ) : fidtxt.write( formatfloat( self.lastfloats[ii], 12, 7 ) + ' ' )
        for ii in range( 2 ) : fidtxt.write( str( self.lastbytes[ii] ) + ' ' )
        fidtxt.write( '\n' )

        return

    # -------------------------------------------------------------------------------
    #                        fromtextfile()                                         |
    # -------------------------------------------------------------------------------
    def fromtextfile( self, fidtxt ) :

        self.lastfloats    = array.array( 'f' )
        self.lastbytes     = array.array( 'B' )
        self.fourbytes     = array.array( 'B' )

        # Read the file.
        self.header        = skeletonHeader()
        nbones             = self.header.fromtextfile( fidtxt )
        self.bonesection   = skeletonBoneSection( nbones )
        self.bonesection.fromtextfile( fidtxt )
        line               = fidtxt.readline()
        tokens             = line.split()
#        self.zero          = int( tokens[0] ) 
        for ii in range( 4 ) : self.fourbytes.append( int( tokens[ii] ) ) 
        line               = fidtxt.readline()
        tokens             = line.split()
        self.nentries      = int( tokens[0] ) 
        self.animsection   = skeletonAnimSection()
        self.animsection.fromtextfile( fidtxt, self.nentries )
        line               = fidtxt.readline()
        tokens             = line.split()
        self.lastfloats.append( float( tokens[0] ) ) 
        self.lastfloats.append( float( tokens[1] ) ) 
        self.lastfloats.append( float( tokens[2] ) ) 
        self.lastbytes.append( int( tokens[3] ) )
        self.lastbytes.append( int( tokens[4] ) )

        return 

# ===================================================================================
#                            CONVERTERS AND THEIR INFO BUTTON HANDLERS              |
# ===================================================================================

# -----------------------------------------------------------------------------------
#                            SkeletonToTxtConverter()                               |
# -----------------------------------------------------------------------------------
def SkeletonToTxtConverter():

    fn                         = askopenfilename( title = "Select skeleton file" )
    if ( fn == '' ) :
        showinfo( "RTWskeletonconverter Warning", "No skeleton file selected. Exiting SkeletonToTxtConverter program." )
        print( "No skeleton file selected. Exiting SkeletonToTxtConverter program." )
        return

    # Open files.
    fid                    = open( fn, 'rb' )
    fntxt                  = fn + '.txt'
    fidtxt                 = open( fntxt, 'w' )

    # Convert to text.
    skeletonobj            = skeletonObject()
    skeletonobj.fromfile( fid ) 
    skeletonobj.totextfile( fidtxt )

    # Close files.
    fid.close()
    fidtxt.close()

    showinfo( 'SkeletonToTxtConverter Info', 'Conversion Complete.' )

    return

# -----------------------------------------------------------------------------------
#                            TxtToSkeletonConverter()                               |
# -----------------------------------------------------------------------------------
def TxtToSkeletonConverter():

    # Get filename to back convert.
    fn                         = askopenfilename( title = "Select .txt skeleton file to convert back to binary", filetypes = [("Skeleton .txt files", "*.txt")] )
    if ( fn == '' ) :
        showinfo( "RTWskeletonconverter Warning", "No skeleton file selected. Exiting TxtToSkeletonConverter program." )
        print( "No .txt skeleton file selected. Exiting TxtToSkeletonConverter program." )
        return

    fileparts                  = splitpath( fn )
    fnbin                      = fileparts[0] + '/' + fileparts[1] + '_modified'

    # Open files.
    fidtxt                     = open( fn, 'r' )
    fid                        = open( fnbin, 'wb' )

    # Convert to binary.
    skeletonobj            = skeletonObject()
    skeletonobj.fromtextfile( fidtxt ) 
    skeletonobj.tofile( fid )

    # Close files.
    fid.close()
    fidtxt.close()

    showinfo( 'TxtToSkeletonConverter Info', 'Conversion Complete.' )

    return

# -----------------------------------------------------------------------------------
#                         Info_SkeletonToTxtConverter()                             |
# -----------------------------------------------------------------------------------
def Info_SkeletonToTxtConverter( event = None ):

    infostring = """
    This utility is used to convert a binary RTW skeleton files unpacked by the xidx.exe
program into a ASCII text representation file with extension .txt.  This file can be 
edited in any text editor.         
    """

    showinfo( 'SkeletonToTxtConverter Help', infostring )

    return

# -----------------------------------------------------------------------------------
#                         Info_TxtToSkeletonConverter()                             |
# -----------------------------------------------------------------------------------
def Info_TxtToSkeletonConverter( event = None ):

    infostring = """
    This utility is used to back convert a text RTW skeleton file into a binary file.
Note that this utility will append _modified to the name so that the original file
will not be overwritten.
    """

    showinfo( 'TxtToSkeletonConverter Help', infostring )

    return



# ===================================================================================
#                            USER INTERFACE                                         |
# ===================================================================================



# -----------------------------------------------------------------------------------
#                            makeCommandMenu()                                      |
#    Handles the File->Exit menu command.                                           |
# -----------------------------------------------------------------------------------
def makeCommandMenu() :
    CmdBtn                 = Menubutton( mBar, text = 'File' )
    CmdBtn.pack( side = LEFT, padx = '2m' )
    CmdBtn.menu            = Menu( CmdBtn )
    CmdBtn.menu.add_command( label = 'Exit', underline = 0, command = doexit )
    CmdBtn['menu']         = CmdBtn.menu

    return CmdBtn

# -----------------------------------------------------------------------------------
#                            doexit()                                               |
# -----------------------------------------------------------------------------------
def doexit():
    try:
        os._exit( 0 )
    except SystemExit as e:
        pass

    return

# -----------------------------------------------------------------------------------
#                            makeHelpMenu()                                         |
#    Handles the Help->About menu command.                                          |
# -----------------------------------------------------------------------------------
def makeHelpMenu() :
    HelpBtn                = Menubutton( mBar, text = 'Help' )
    HelpBtn.pack( side = LEFT, padx = '2m' )
    HelpBtn.menu           = Menu( HelpBtn )
    HelpBtn.menu.add_command( label = 'About...', underline = 0, command = AboutBox )
    HelpBtn['menu']        = HelpBtn.menu
    return HelpBtn

# -----------------------------------------------------------------------------------
#                            AboutBox()                                             |
# -----------------------------------------------------------------------------------
def AboutBox():

    thisroot               = Tk()
    thisroot.title( 'About RTWskeletonconverter' )

    stringarray            = getDragonImage()

    canvas                 = Canvas( thisroot, width = 360, height = 200 )
    img                    = PhotoImage( height=64, width=64, master = thisroot )
    for ii in range( 64 ) :
        img.put( stringarray[63-ii], to = ( 0, ii ) )

    canvas.create_image( 15,  5, image = img, anchor = NW )
    canvas.create_text( 180, 20, anchor = CENTER, text = 'Version 1.0' )
    canvas.create_text( 180, 40, anchor = CENTER, text = 'Release date: 15 June 2009' )
    canvas.create_text( 180, 60, anchor = CENTER, text = 'Author: KnightErrant' )
    canvas.create_text(  10, 80, anchor = W, text = '' )
    canvas.create_text(  10,100, anchor = W, text = '   RTWskeletonconverter is a utility used to convert RTW skeletons into' )
    canvas.create_text(  10,115, anchor = W, text = 'ASCII .txt files and back again into binary files.  The text version allows' )
    canvas.create_text(  10,130, anchor = W, text = 'the user to make changes just with a text editor and then convert those' )
    canvas.create_text(  10,145, anchor = W, text = 'back.  It is used in conjunction with Vercingetorix''s xidx.exe which')
    canvas.create_text(  10,160, anchor = W, text = 'can unpack and repack the skeleton.dat file.' )                                                                         
    canvas.pack()

    root.mainloop()

    return

# ===================================================================================
#                            main()  (So to speak.)                                 |
# ===================================================================================

# Begin the GUI by calling Tk() and set the title.
root                       = Tk()
root.title( 'RTWskeletonconverter' )

# Make a menu bar.
mBar                       = Frame( root, borderwidth = 1 )
mBar.pack( fill = X )                      
CmdBtn                     = makeCommandMenu()
HelpBtn                    = makeHelpMenu()
#mBar.tk_menuBar( CmdBtn, HelpBtn )

# Make an outer frame to hold everything.
outerframe                 = Frame( root, width = 600, height = 840 )

# This frame is for the two converter buttons and their related info buttons.
xf1                        = Frame( outerframe, relief = GROOVE, borderwidth = 4, width = 280, height = 360 )
Label(  xf1, text = 'RTW Skeleton Conversion' ).place( relx = 0.25, rely=-0.003, anchor = W )

Button( xf1, text = 'Skeleton to Text Converter',   width = 25, command = SkeletonToTxtConverter         ).grid( row = 0, column = 0, padx = 18, pady = 18, sticky = NSEW )                           
Button( xf1, text = 'Text to Skeleton Converter',   width = 25, command = TxtToSkeletonConverter         ).grid( row = 1, column = 0, padx = 18, pady = 18, sticky = NSEW )

Button( xf1, text = 'Info',                         width =  5, command = Info_SkeletonToTxtConverter    ).grid( row = 0, column = 1, padx = 18, pady = 18, sticky = NSEW )                           
Button( xf1, text = 'Info',                         width =  5, command = Info_TxtToSkeletonConverter    ).grid( row = 1, column = 1, padx = 18, pady = 18, sticky = NSEW )

xf1.grid( row = 0, column = 0, rowspan = 3, padx = 15, pady = 15, sticky = NSEW )

# Pack them all up.
outerframe.pack()

# Start the message loop.
root.mainloop()
