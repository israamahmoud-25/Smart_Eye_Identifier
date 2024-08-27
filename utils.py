import face_recognition
import cv2
import os
import glob
import numpy as np
import re 

class SimpleFacerec:
    i=0
    def __init__(self):
        self.known_face_encodings = [] # instances
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = .3

    def load_encoding_images(self, images_path): # methods
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"+str(self.i)
            

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            # using np.argmin to find the closest face among other known faces
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            else:
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(name)
                self.i+=1
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        
        ##### my editing ###########

        return face_locations.astype(int), face_names

def save_image(frame,  basename, y1, x2, y2, x1 ,ext='jpg'):
    
    # setting crop ratio of the unknown face
    if x1<0:
        x1=0
    if y1<0:
        y1=0
    if y2>480:
        y2=480
    if x2>640:
        x2=640
    base_path = os.path.join('Unknowns/', basename)
    cv2.imwrite('{}.{}'.format(base_path, ext), frame[y1:y2,x1:x2])


def unkonwns_count () :
    """
    this function retrun the number of current unknown people
    
    Returns:
        num (int): The number of unknown people.
    """
    path = os.path.join(os.getcwd(), "Unknowns")
    name = sorted(os.listdir(path) , key = lambda x : int(x[7:-4]))
	# print(name)
	
    if len(name) ==  0 :
        num = -1
    else :
        num = int(re.findall(r'\d+' , name[-1])[0])

    return num
