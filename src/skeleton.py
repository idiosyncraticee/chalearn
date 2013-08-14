# PARSER FOR ANALYZING KAGGLE/CHALEARN ROUND 3 DATA
# THIS IS STILL QUITE INCOMPLETE

import scipy.io
import numpy
import sklearn
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import nd_dtw

numpy.set_printoptions(threshold='nan')

def load_challenge_data():
    
    #TURN ON PLOTTING
    plot=1
    
    #MAKE A LIST OF FILES TO ANALYZE
    # TO BEGIN WITH I'M JUST USING 2
    files = ['..\\data\\Sample00300\\Sample00300_data.mat','..\\data\\Sample00333\\Sample00333_data.mat']
    
    #INITIALIZE THE DICTIONARY
    dictionaryPixelHandArray={}
    gestures=[]
    
    #FOREACH FILE
    for file in files:
        #OPEN THE .mat MATLAB FILE
        mat = scipy.io.loadmat(file)
      
        print "Type of mat is "+str(type(mat))
        print "Type of mat[video] is "+str(type(mat['Video']))
    
        print mat['Video'].dtype     
       
        numFrames = mat['Video']['NumFrames'].item()[0][0]
        frameRate = mat['Video']['FrameRate'].item()[0][0]
        maxDepth = mat['Video']['MaxDepth'].item()[0][0]
        #LABELS ARE OF TYPE numpy.void
        labels = mat['Video']['Labels'].item()[0]
        
        #I THINK HAND IS THE 8th ELEMENT IN THE SKELETON SO I'LL SET IT TO 7
        #TODO: FIGURE THIS OUT FROM THE JointType
        hand = 7
        
        pixelHandArray=[]
    
        #MAKE A LIST OF ALL POSSIBLE GESTURES
        for label in labels:
            print "gesture = "+str(label[0][0])
            gestures.append(str(label[0][0]))
            
        for label in labels:
            
            gesture = str(label[0][0])
            startFrame = label[1][0][0]
            stopFrame = label[2][0][0]
            print "gestrure="+gesture+",startFrame="+str(startFrame)+",stopFrame="+str(stopFrame)
            #FOR WORLD COORDINATES 3 COLUMNS FOR X,Y,Z AND numFrames ROWS
            #worldHandArray = numpy.empty([stopFrame-startFrame, 3])
    
            pixelHandArray = numpy.empty(shape=(stopFrame-startFrame))
            for frame in range(startFrame,stopFrame):
                
                #ALL THE 0's CHAINED TOGETHER IS HOW TO ACCESS THE SKELETON.  I THINK ITS A BYPRODUCT OF THE MAT CONVERTER
                #THIS IS THE 20x3 ARRAY WITH THE SKELETON DATA
                #print mat['Video']['Frames'][0][0][0][frame]['Skeleton'].dtype
                #print mat['Video']['Frames'][0][0][0][frame]['Skeleton']['WorldPosition'][0][0][hand].shape
        
                #worldHandArray[frame] = mat['Video']['Frames'][0][0][0][frame-startFrame]['Skeleton']['WorldPosition'][0][0][hand]
                pixelHandArray[frame-startFrame]=mat['Video']['Frames'][0][0][0][frame-startFrame]['Skeleton']['PixelPosition'][0][0][hand][0]
                #pixelHandArray[frame-startFrame][1]=mat['Video']['Frames'][0][0][0][frame-startFrame]['Skeleton']['PixelPosition'][0][0][hand][1]
                #THE JointType WILL HAVE THE DESIGNATION ONCE THE FRAME HAS BEEN SKELETONIZED
                #print mat['Video']['Frames'][0][0][0][frame]['Skeleton']['JointType'][0][0]
                
            #print pixelHandArray
            print pixelHandArray.shape
            
            dictionaryPixelHandArray[(file,gesture)]=pixelHandArray


    #THIS PART IS JUST TESTING OUT THE GESTURES TO SEE IF THEY ARE WORKING
    for gesture in gestures:
        print gesture        
        baseline = dictionaryPixelHandArray[(files[0],gesture)]
        target = dictionaryPixelHandArray[(files[1],gesture)]
        nd_dtw.nd_dtw(baseline,target,plot=True,mlpy_dtw=True)
        print baseline.shape
        print target.shape           
                  
load_challenge_data() 