from datetime import time
import cv2
from src.system.interface import AnnotatorInterface
from src.utils.drawer_eval import Drawer
import time
from sys import argv
import os



"""
Read the movie located at moviePath, perform the 2d pose annotation and display
Run from terminal : python demo_2d.py [movie_file_path] [max_persons_detected]
with all parameters optional.
Keep holding the backspace key to speed the video 30x
"""



def start(movie_path, max_persons):
    

    cam = cv2.VideoCapture(movie_path)
    
    ret_val, orig_image = cam.read()    

    annotator = AnnotatorInterface.build(max_persons=max_persons)    

    cap = cv2.VideoCapture(movie_path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    
    while(True):

        ret, frame = cap.read()

        if not ret:
            break
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        tmpTime = time.time()
        print(time.time)
        print(tmpTime)
        persons = annotator.update(frame)
        fps = int(1/(time.time()-tmpTime))

        poses = [p['pose_2d'] for p in persons]
        

        ids = [p['id'] for p in persons]
        frame = Drawer.draw_scene_2(frame, poses, ids, fps, cap.get(cv2.CAP_PROP_POS_FRAMES),length)
        

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        #cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(33) == ord(' '):
            curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(curr_frame + 30))    
        

            
    annotator.terminate()
    cap.release()
    cv2.destroyAllWindows()




def FallVideos(FallFilm):
    
    
    print("start frontend")
    
    for video_filename in os.listdir(FallFilm):
        
        video_filename=FallFilm+'/'+video_filename        
        default_media = video_filename
        max_persons = 1       
        start(default_media, max_persons)
           



if __name__ == "__main__":
    

    print("start frontend")

    default_media = './Film/augmented videos.fall/fall-30-cam0_Uniformfilter.mp4'
    max_persons = 1

    if len(argv) == 3:
        default_media = 0 if argv[1] == "webcam" else argv[1]
        start(default_media, int(argv[2]))
    elif len(argv) == 2:
        default_media = 0 if argv[1] == "webcam" else argv[1]
        start(default_media, max_persons)
    else:
        start(default_media, max_persons)






