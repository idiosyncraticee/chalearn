#N DIMENSIONAL DYNAMIC TIME WARPING
#    USING EUCLIDEAN DISTANCE
#    EUCLIDEAN DISTANCE ASSUMES THAT ALL OF THE N-DIMENSIONS ARE EQUALLY WEIGHTED
#    nd_dtw(xn,yn)


import numpy


def nd_dtw(baseline,target,plot=False, mlpy_dtw=False): 
    #OPTIONALLY IMPORT THESE IF THE PLOTTING IS DESIRED
    
    #INITIALIZE dtw AND SIZE THE BASTARD
    #TODO: FIGURE OUT HOW TO MAKE THE INITIALIZATION INFINITY
    dtw = numpy.empty([len(baseline), len(target)])
    
    #MAKE THE 0 COLUMNS INFINITY AS PART OF THE ALGORITHM
    for i in range(1,len(baseline)):
        dtw[i][0]=9999999
    for i in range(1,len(target)):
        dtw[0][i]=9999999
        
    #MAKE THE 0,0 CELL 0 AS PART OF THE ALGORITHM
    dtw[0][0]=0
    
    dist =0
    for baselineTimeFrame in range (1,len(baseline)):
#        print "baseline="+str(baselineTimeFrame)
        for targetTimeFrame in range (1,len(target)):
            
            #GET THE EUCLIDEAN DISTANCE BETWEEN POINTS FOR THE WHOLE CHANNEL
            euclideanDistance = numpy.linalg.norm(target[targetTimeFrame]-baseline[baselineTimeFrame])
    
            #THE INITIAL GUESS FOR THE COST IS EUCLIDEAN
            #TODO: COULD SUPPORT OTHER DISTANCES
            cost = euclideanDistance
            print "Cost="+str(cost)+",Baseline["+str(baselineTimeFrame)+"]="+str(baseline[baselineTimeFrame])+",Target["+str(targetTimeFrame)+"]="+str(target[targetTimeFrame])
            
            #print "cost ="+str(cost[baselineTimeFrame][targetTimeFrame])
            minValue = min(dtw[baselineTimeFrame-1][targetTimeFrame],dtw[baselineTimeFrame][targetTimeFrame-1],dtw[baselineTimeFrame-1][targetTimeFrame-1])
            #print "cost="+str(cost)+",min="+str(minValue)
    
            #print dtw[baselineTimeFrame][targetTimeFrame]
            #print dtw[baselineTimeFrame-1][targetTimeFrame]
            #print dtw[baselineTimeFrame][targetTimeFrame-1]
            #print dtw[baselineTimeFrame-1][targetTimeFrame-1]
            
            #AS PART OF THE ALGORITHM, SUM THE COST FUNCTION AND THE MINIMUM VALUE OF THE LOWER 3 CELLS
            dtw[baselineTimeFrame][targetTimeFrame] = cost + minValue
            #print "dtw["+str(baselineTimeFrame)+"]["+str(targetTimeFrame)+"]="+str(dtw[baselineTimeFrame][targetTimeFrame])
            
            dist +=cost
            
    #OPTIONALLY ADJUST THE RANGE SO THE PLOT LOOKS BETTER
    for i in range(1,len(baseline)):
        dtw[i][0]=0
    for i in range(1,len(target)):
        dtw[0][i]=0
    for i in range(1,len(baseline)):
        dtw[i][0]=numpy.amax(dtw)
    for i in range(1,len(target)):
        dtw[0][i]=numpy.amax(dtw)
    
    #print dtw
    #WALK THE dtw ARRAY AND FIND THE PATH 
#     path=
# (array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  8,  8,  8,  9,  9, 10, 11, 12,
#        13, 14, 15]), array([ 0,  0,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14,
#        14, 14, 15]))
    i=0
    j=0   
    xpath=[]
    ypath=[]
    while i<len(baseline)-1 and j<len(target)-1:
        print "    i="+str(i)+",j="+str(j)+",dtw[i][j]="+str(dtw[i][j])
        print "    i="+str(i)+",j="+str(j)+",dtw[i+1][j+1]="+str(dtw[i+1][j+1])
        print "    i="+str(i)+",j="+str(j)+",dtw[i][j+1]="+str(dtw[i][j+1])
        print "    i="+str(i)+",j="+str(j)+",dtw[i+1][j]="+str(dtw[i+1][j])
        if dtw[i+1][j+1] <= dtw[i][j+1] and dtw[i+1][j+1] <= dtw[i+1][j]:
            print "diag,i+1="+str(i+1)+",j+1="+str(j+1)+",dtw[i+1][j+1]="+str(dtw[i+1][j+1])
            xpath.append(i+1)
            ypath.append(j+1)
            i+=1
            j+=1
        elif dtw[i][j+1] < dtw[i+1][j]:
            print "y,i="+str(i)+",j+1="+str(j+1)+",dtw[i][j+1]="+str(dtw[i][j+1])

            xpath.append(i)
            ypath.append(j+1)
            j+=1
        elif dtw[i+1][j] < dtw[i][j+1]:
            print "x,i+1="+str(i+1)+",j="+str(j)+",dtw[i+1][j]="+str(dtw[i+1][j])

            xpath.append(i+1)
            ypath.append(j)
            i+=1
        elif dtw[i+1][j] == dtw[i][j+1]:
            print "both,i+1="+str(i+1)+",j="+str(j)+",dtw[i+1][j]="+str(dtw[i+1][j])

            xpath.append(i)
            ypath.append(j+1)
            i+=1   
                        
    path=(ypath,xpath)      
                
    #dist, cost, path = mlpy.a(x, y, dist_only=False)
    #MAKE THE COST dtw SO ITS THE SAME AS ml.dtw_std
    cost = dtw

    #path : tuple of two 1d numpy array (path_x, path_y)
    print "path"
    print path
    print "chris dist="+str(dist)
    
    if mlpy_dtw:
        import mlpy
        dist, mlpy_cost, mlpy_path = mlpy.dtw_std(baseline, target, dist_only=False)
    print "mlpy dist="+str(dist)        
    #PLOTTING FUNCTIONS
    if plot:
        print "Prepare to plot"
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
        
        if mlpy_dtw:
            f, axarr = plt.subplots(1,2)
            plot3 = axarr[1].imshow(mlpy_cost, origin='lower', cmap=cm.spectral, interpolation='nearest')
            #f.colorbar(plot3)
            
            #TODO: SUPPORT THE PATH
            plot4 = axarr[1].plot(mlpy_path[1], mlpy_path[0], 'w')
            xlim = axarr[1].set_xlim((0, mlpy_cost.shape[1]))
            ylim = axarr[1].set_ylim((0, mlpy_cost.shape[0]))
            axarr[1].set_title('mlpy.std_dtw')
        else:
            f, axarr = plt.subplots()
            


        plot1 = axarr[0].imshow(cost, origin='lower', cmap=cm.spectral, interpolation='nearest')
        f.colorbar(plot1)
        axarr[0].set_title('chris.nd_dtw')
        #TODO: SUPPORT THE PATH
        plot2 = axarr[0].plot(path[0], path[1], 'w')
        xlim = axarr[0].set_xlim((0, cost.shape[1]))
        ylim = axarr[0].set_ylim((0, cost.shape[0]))
        plt.show()


#TRY IT OUT:
#baseline = numpy.array([[1, 2, 3], [3, 4, 5], [1, 2, 3], [1, 2, 3]])
#target = numpy.array([[1, 2, 2], [3, 4, 5], [3, 4, 5], [1, 2, 2], [1, 2, 2]])
# baseline = [0,0,0,0,1,1,2,2,3,2,1,1,0,0,0,0]
# target = [0,0,1,1,2,2,3,3,3,3,2,2,1,1,0,0] 
# nd_dtw(baseline,target,plot=True,mlpy_dtw=True)