import cv2
from utils import SimpleFacerec, save_image, unkonwns_count
from csv_manger import get_csv, markAttendance
import datetime 
import copy
 

sfr = SimpleFacerec()
#get last i
sfr.i= unkonwns_count() + 1
sfr.load_encoding_images("images/")

########## Uncomment the line below if you wwant to use the pictures of Unkowns as Knowns for another run cycle#############
#sfr.load_encoding_images("Unknowns/")


dtString = datetime.datetime.now().strftime(' %d%b %I%p')


cap = cv2.VideoCapture(0)

width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_name = f"livestream{dtString}.mp4"

writer= cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 10, (width,height))
#creat csv file
filename=get_csv()

while True:
    ret, frame = cap.read()
    writer.write(frame)

    # Detect Faces
    face_locations, face_names  = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        markAttendance(name,filename)
        
        #adding name to frame
        clean_frame = copy.copy(frame) #kept a clean copy to save if there's unknown
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (143, 255, 255 ), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 4)
        
        
        frame_span = 60
        if name.startswith("Unknown") :
            save_image(clean_frame, name, y1-frame_span, x2+frame_span, y2+frame_span, x1-frame_span)

    cv2.imshow("Frames", frame)

    key = cv2.waitKey(1)

    if key == 32: # 32 is spaceBar ascii order
        break

cap.release()
cv2.destroyAllWindows()

