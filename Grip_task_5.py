#----------------------------------------------------------IMPORTING LIBRARIES---------------------------------------------------------
import cv2
import pandas as pd



#-----------------------------------------------------------READING IMAGE--------------------------------------------------------------

img_path = 'color-image.jpg'
img = cv2.imread(img_path)



#----------------------------------------------------READING CSV FILE HAVING COLORS NAME------------------------------------------------ 

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)



#-----------------------------------------------------------INITIALIZING VARIABLES------------------------------------------------------

clicked = False
r = g = b = x_pos = y_pos = 0



#------------------------------------------------------FUNCTION FOR DETECTING THE COLOR------------------------------------------------

def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname



#--------------------------------------------FUNCTIONS FOR GETTING X,Y COORDINATES DURING DOUBLE MOUSE CLICK---------------------------

def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)



#-------------------------------------------------------------DISPLAYING IMAGE---------------------------------------------------------

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)



#----------------------------------------------------DISPLAYING THE NAME OF COLOR DETECTED---------------------------------------------

while True:

    cv2.imshow("image", img)
    if clicked:

        # cv2.rectangle(image, start point, endpoint, color, thickness)
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text to display( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # Displaying text over image
        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # Text color set to 'black' for very light colors
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()