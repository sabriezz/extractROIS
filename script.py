import cv2 # Opencv ver 3.1.0 used
import numpy as np

import sys
# Set recursion limit
sys.setrecursionlimit(10 ** 9)
ref_point = []

class Rect:
    x = None
    y = None
    w = None
    h = None

    def printit(self):
        print (str(self.x) + ',' + str(self.y) + ',' + str(self.w) + ',' + str(self.h))


# endclass

class dragRect:
    # Limits on the canvas
    keepWithin = Rect()
    # To store rectangle
    outRect = Rect()
    # To store rectangle anchor point
    # Here the rect class object is used to store
    # the distance in the x and y direction from
    # the anchor point to the top-left and the bottom-right corner
    anchor = Rect()
    # Selection marker size
    sBlk = 4
    # Whether initialized or not
    initialized = False

    # Image
    image = None
    inProgress = None

    # Window Name
    wname = ""

    # Return flag
    returnflag = False

    # FLAGS
    # Rect already present
    active = False
    # Drag for rect resize in progress
    drag = False
    # Marker flags by positions
    TL = False
    TM = False
    TR = False
    LM = False
    RM = False
    BL = False
    BM = False
    BR = False
    hold = False


# endclass

def init(dragObj, Img, windowName, windowWidth, windowHeight):
    # Image
    dragObj.image = Img.copy()
    dragObj.inProgress = Img.copy()

    # Window name
    dragObj.wname = windowName

    # Limit the selection box to the canvas
    dragObj.keepWithin.x = 0
    dragObj.keepWithin.y = 0
    dragObj.keepWithin.w = windowWidth
    dragObj.keepWithin.h = windowHeight

    # Set rect to zero width and height
    dragObj.outRect.x = 0
    dragObj.outRect.y = 0
    dragObj.outRect.w = 0
    dragObj.outRect.h = 0


# enddef

def resetValues(dragObj):
    dragObj.initialized = False

    # Image
    dragObj.image = None
    dragObj.inProgress = None
    # Window Name
    dragObj.wname = ""

    # FLAGS
    # Rect already present
    dragObj.active = False
    # Drag for rect resize in progress
    dragObj.drag = False
    # Marker flags by positions
    dragObj.TL = False
    dragObj.TR = False
    dragObj.BL = False
    dragObj.BR = False
    dragObj.hold = False
#enddef

def dragrect(event, x, y, flags, dragObj):
    if x < dragObj.keepWithin.x:
        x = dragObj.keepWithin.x
    # endif
    if y < dragObj.keepWithin.y:
        y = dragObj.keepWithin.y
    # endif
    if x > (dragObj.keepWithin.x + dragObj.keepWithin.w - 1):
        x = dragObj.keepWithin.x + dragObj.keepWithin.w - 1
    # endif
    if y > (dragObj.keepWithin.y + dragObj.keepWithin.h - 1):
        y = dragObj.keepWithin.y + dragObj.keepWithin.h - 1
    # endif

    if event == cv2.EVENT_LBUTTONDOWN:
        mouseDown(x, y, dragObj)
    # endif
    if event == cv2.EVENT_LBUTTONUP:
        mouseUp(x, y, dragObj)
    # endif
    if event == cv2.EVENT_MOUSEMOVE:
        mouseMove(x, y, dragObj)
    # endif
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mouseDoubleClick(x, y, dragObj)
    # endif

# enddef

def pointInRect(pX, pY, rX, rY, rW, rH):
    if rX <= pX <= (rX + rW) and rY <= pY <= (rY + rH):
        return True
    else:
        return False
    # endelseif


# enddef

def mouseDoubleClick(eX, eY, dragObj):
    if dragObj.active:

        if pointInRect(eX, eY, dragObj.outRect.x, dragObj.outRect.y, dragObj.outRect.w, dragObj.outRect.h):
            dragObj.returnflag = True
            global ref_point
            ref_point.append((dragObj.outRect.x, dragObj.outRect.y))
            ref_point.append((dragObj.outRect.x + dragObj.outRect.w, dragObj.outRect.y + dragObj.outRect.h))
            cv2.rectangle(dragObj.inProgress, (dragObj.outRect.x, dragObj.outRect.y),
                          (dragObj.outRect.x + dragObj.outRect.w,
                           dragObj.outRect.y + dragObj.outRect.h), (0, 255, 0), 2)

        # endif

    # endif


# enddef

def mouseDown(eX, eY, dragObj):
    if dragObj.active:

        if pointInRect(eX, eY, dragObj.outRect.x - dragObj.sBlk,
                       dragObj.outRect.y - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.TL = True
            return
        # endif
        if pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                       dragObj.outRect.y - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.TR = True
            return
        # endif
        if pointInRect(eX, eY, dragObj.outRect.x - dragObj.sBlk,
                       dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.BL = True
            return
        # endif
        if pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                       dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.BR = True
            return
        # endif

        if pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w / 2 - dragObj.sBlk,
                       dragObj.outRect.y - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.TM = True
            return
        # endif
        if pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w / 2 - dragObj.sBlk,
                       dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.BM = True
            return
        # endif
        if pointInRect(eX, eY, dragObj.outRect.x - dragObj.sBlk,
                       dragObj.outRect.y + dragObj.outRect.h / 2 - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.LM = True
            return
        # endif
        if pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                       dragObj.outRect.y + dragObj.outRect.h / 2 - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.RM = True
            return
        # endif

        # This has to be below all of the other conditions
        if pointInRect(eX, eY, dragObj.outRect.x, dragObj.outRect.y, dragObj.outRect.w, dragObj.outRect.h):
            dragObj.anchor.x = eX - dragObj.outRect.x
            dragObj.anchor.w = dragObj.outRect.w - dragObj.anchor.x
            dragObj.anchor.y = eY - dragObj.outRect.y
            dragObj.anchor.h = dragObj.outRect.h - dragObj.anchor.y
            dragObj.hold = True

            return
        # endif

    else:
        dragObj.outRect.x = eX
        dragObj.outRect.y = eY
        dragObj.drag = True
        dragObj.active = True
        return

    # endelseif


# enddef

def mouseMove(eX, eY, dragObj):
    if dragObj.drag & dragObj.active:
        dragObj.outRect.w = eX - dragObj.outRect.x
        dragObj.outRect.h = eY - dragObj.outRect.y
        #clearCanvasNDraw(dragObj)
        return
    # endif

    if dragObj.hold:
        dragObj.outRect.x = eX - dragObj.anchor.x
        dragObj.outRect.y = eY - dragObj.anchor.y

        if dragObj.outRect.x < dragObj.keepWithin.x:
            dragObj.outRect.x = dragObj.keepWithin.x
        # endif
        if dragObj.outRect.y < dragObj.keepWithin.y:
            dragObj.outRect.y = dragObj.keepWithin.y
        # endif
        if (dragObj.outRect.x + dragObj.outRect.w) > (dragObj.keepWithin.x + dragObj.keepWithin.w - 1):
            dragObj.outRect.x = dragObj.keepWithin.x + dragObj.keepWithin.w - 1 - dragObj.outRect.w
        # endif
        if (dragObj.outRect.y + dragObj.outRect.h) > (dragObj.keepWithin.y + dragObj.keepWithin.h - 1):
            dragObj.outRect.y = dragObj.keepWithin.y + dragObj.keepWithin.h - 1 - dragObj.outRect.h
        # endif

        #clearCanvasNDraw(dragObj)
        return
    # endif

    if dragObj.TL:
        dragObj.outRect.w = (dragObj.outRect.x + dragObj.outRect.w) - eX
        dragObj.outRect.h = (dragObj.outRect.y + dragObj.outRect.h) - eY
        dragObj.outRect.x = eX
        dragObj.outRect.y = eY
        #clearCanvasNDraw(dragObj)
        return
    # endif
    if dragObj.BR:
        dragObj.outRect.w = eX - dragObj.outRect.x
        dragObj.outRect.h = eY - dragObj.outRect.y
        #clearCanvasNDraw(dragObj)
        return
    # endif
    if dragObj.TR:
        dragObj.outRect.h = (dragObj.outRect.y + dragObj.outRect.h) - eY
        dragObj.outRect.y = eY
        dragObj.outRect.w = eX - dragObj.outRect.x
        #clearCanvasNDraw(dragObj)
        return
    # endif
    if dragObj.BL:
        dragObj.outRect.w = (dragObj.outRect.x + dragObj.outRect.w) - eX
        dragObj.outRect.x = eX
        dragObj.outRect.h = eY - dragObj.outRect.y
        #clearCanvasNDraw(dragObj)
        return
    # endif

    if dragObj.TM:
        dragObj.outRect.h = (dragObj.outRect.y + dragObj.outRect.h) - eY
        dragObj.outRect.y = eY
        #clearCanvasNDraw(dragObj)
        return
    # endif
    if dragObj.BM:
        dragObj.outRect.h = eY - dragObj.outRect.y
        #clearCanvasNDraw(dragObj)
        return
    # endif
    if dragObj.LM:
        dragObj.outRect.w = (dragObj.outRect.x + dragObj.outRect.w) - eX
        dragObj.outRect.x = eX
        #clearCanvasNDraw(dragObj)
        return
    # endif
    if dragObj.RM:
        dragObj.outRect.w = eX - dragObj.outRect.x
        #clearCanvasNDraw(dragObj)
        return
    # endif


# enddef

def mouseUp(eX, eY, dragObj):
    dragObj.drag = False
    disableResizeButtons(dragObj)
    straightenUpRect(dragObj)
    if dragObj.outRect.w == 0 or dragObj.outRect.h == 0:
        dragObj.active = False
    # endif

    clearCanvasNDraw(dragObj)


# enddef

def disableResizeButtons(dragObj):
    dragObj.TL = dragObj.TM = dragObj.TR = False
    dragObj.LM = dragObj.RM = False
    dragObj.BL = dragObj.BM = dragObj.BR = False
    dragObj.hold = False


# enddef

def straightenUpRect(dragObj):
    if dragObj.outRect.w < 0:
        dragObj.outRect.x = dragObj.outRect.x + dragObj.outRect.w
        dragObj.outRect.w = -dragObj.outRect.w
    # endif
    if dragObj.outRect.h < 0:
        dragObj.outRect.y = dragObj.outRect.y + dragObj.outRect.h
        dragObj.outRect.h = -dragObj.outRect.h
    # endif


# enddef

def clearCanvasNDraw(dragObj):
    # Draw
    dragObj.image = dragObj.inProgress.copy()
    cv2.rectangle(dragObj.image, (dragObj.outRect.x, dragObj.outRect.y),
                  (dragObj.outRect.x + dragObj.outRect.w,
                   dragObj.outRect.y + dragObj.outRect.h), (0, 255, 0), 2)
    drawSelectMarkers(dragObj.image, dragObj)



# enddef

def drawSelectMarkers(image, dragObj):
    # Top-Left
    cv2.rectangle(image, (dragObj.outRect.x - dragObj.sBlk,
                          dragObj.outRect.y - dragObj.sBlk),
                  (dragObj.outRect.x - dragObj.sBlk + dragObj.sBlk * 2,
                   dragObj.outRect.y - dragObj.sBlk + dragObj.sBlk * 2),
                  (0, 255, 0), 2)
    # Top-Rigth
    cv2.rectangle(image, (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                          dragObj.outRect.y - dragObj.sBlk),
                  (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk + dragObj.sBlk * 2,
                   dragObj.outRect.y - dragObj.sBlk + dragObj.sBlk * 2),
                  (0, 255, 0), 2)
    # Bottom-Left
    cv2.rectangle(image, (dragObj.outRect.x - dragObj.sBlk,
                          dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk),
                  (dragObj.outRect.x - dragObj.sBlk + dragObj.sBlk * 2,
                   dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk + dragObj.sBlk * 2),
                  (0, 255, 0), 2)
    # Bottom-Right
    cv2.rectangle(image, (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                          dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk),
                  (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk + dragObj.sBlk * 2,
                   dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk + dragObj.sBlk * 2),
                  (0, 255, 0), 2)

    # Top-Mid
    cv2.rectangle(image, (dragObj.outRect.x + int(dragObj.outRect.w / 2) - dragObj.sBlk,
                          dragObj.outRect.y - dragObj.sBlk),
                  (dragObj.outRect.x + int(dragObj.outRect.w / 2) - dragObj.sBlk + dragObj.sBlk * 2,
                   dragObj.outRect.y - dragObj.sBlk + dragObj.sBlk * 2),
                  (0, 255, 0), 2)
    # Bottom-Mid
    cv2.rectangle(image, (dragObj.outRect.x + int(dragObj.outRect.w / 2) - dragObj.sBlk,
                          dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk),
                  (dragObj.outRect.x + int(dragObj.outRect.w / 2) - dragObj.sBlk + dragObj.sBlk * 2,
                   dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk + dragObj.sBlk * 2),
                  (0, 255, 0), 2)
    # Left-Mid
    cv2.rectangle(image, (dragObj.outRect.x - dragObj.sBlk,
                          dragObj.outRect.y + int(dragObj.outRect.h / 2) - dragObj.sBlk),
                  (dragObj.outRect.x - dragObj.sBlk + dragObj.sBlk * 2,
                   dragObj.outRect.y + int(dragObj.outRect.h / 2) - dragObj.sBlk + dragObj.sBlk * 2),
                  (0, 255, 0), 2)
    # Right-Mid
    cv2.rectangle(image, (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                          dragObj.outRect.y + int(dragObj.outRect.h / 2) - dragObj.sBlk),
                  (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk + dragObj.sBlk * 2,
                   dragObj.outRect.y + int(dragObj.outRect.h / 2) - dragObj.sBlk + dragObj.sBlk * 2),
                  (0, 255, 0), 2)

# enddef


# Define the drag object
rectI = dragRect

# Initialize the  drag object
wName = "select ROIS"
#Select Image

image_m = cv2.imread("1.png", -1)
image = cv2.resize(image_m,(800,600))
original = image.copy()
imageWidth, imageHeight = image.shape[:2]
init(rectI, image, wName, imageWidth, imageHeight)

cv2.namedWindow(rectI.wname)
cv2.setMouseCallback(rectI.wname, dragrect, rectI)

# keep looping until rectangle finalized
while True:
    # display the image
    cv2.imshow(wName, rectI.image)
    key = cv2.waitKey(1) & 0xFF
    #quit
    if key == ord('q'):
        break
    #clear all selections
    if key == ord('c'):
        ref_point = []
        resetValues(rectI)
        init(rectI, original, wName, imageWidth, imageHeight)

print (ref_point)

# close all open windows
cv2.destroyAllWindows()
