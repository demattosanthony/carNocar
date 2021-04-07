 # High Point University Undergraduate Research Project 
 By: Anthony DeMattos
 
 ## Abstract
 
 ## Scripts for data collection, labeling, and detection
 
 ### set_coords.py
     Description: 
        Scipt to set the coordinates of each parking space withing a given image. Will load a openCV window with 
        the image passed in and wait for four mouse clicks (top left, top right, bottom left, bottom right) to set 
        coordinates of one spot, then will wait for the next four and so on until the program is quit. If you 
        accidently press the wrong coordinate just press 'u' to undo.
        
     Command Line Arguments:
        --spot : Allows you to update coordinates of just one parking space, just pass in the spot_id
        --img : Path of image that you want to label the coordinates of each parking space
      
      Output:
         Will create a coords.txt file, which stoores the location of every parking space with a unique id in a Json format
         
### data_labeler.py 
      Description:
         Script to loop through each parking space, that was set in coords.txt. Will create a new cropped image 
         and allow you to label the image as a car or open space. Each cropped image will pop up one at a time 
         and wait for you to press 'c' for car or 'o' for open. You can also press 'q' to not label the image
         and move to the next. 

      Command Line Arguments:
         --img : The path of the image which you are looking to label each parking space
        
      Output: 
          If 'c' is pressed - will put the cropped image in the car data folder
          If 'o' is pressed - will put the cropped image in the open data folder
          If 'q' is pressed - will do nothing and move to next image
          
 ### get_clip.py
      Description:
          Script for data collection that uses python schedule to get image every 45 minutes. Run with nohup to run
          in the background until machine is shut down or restarted. 
          
      Output:
          Will store image (named as timestamp of time and day collected) in the data folder

### detect.py
      Description:
          Program to run trained pytorch model on either live video or passed in image. Uses python threading for live 
          video in order to be as real time as possible. Will use each parking space coordinate from coords.txt and pass
          it throught the model for the predicted output.
          
      Command Line Arguments:
          --live : defaults to True to show live video, can set to false to run model on image instead
          --img : path to image that you want to run model on
          
      Output:
          Will show OpenCV window with green rectangles around predicted open spaces and red rectangles around predicted
          spaces that contain cars. 
          
## Training
