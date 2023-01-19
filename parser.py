
# #### Test file: points :  point ; waterways : Polyline ; natural : Polygon

def parser(_input,_output):
    import struct

    shapes=['Null','Point','','Polyline','','Polygon','','',
            'MultiPoint','','','','','','','','','','','','',
            '','','','','','','','','','','MultiPatch']
    try:
        fr = open(_input, 'rb')#Read this file    
        _file = fr.read(-1)
        h=8 #Record header
        s=100+h #start
        File_Type=struct.unpack("i",_file[32:36])[0]#Shape Type in header
        print('File Type: %s \n' %shapes[File_Type] )
        try:
            fw=open(_output,'w')#Write to this file
            print("Data has been saved in " +_output)

            while True:
                try:
                    
                    Shape_Type=struct.unpack("i",_file[s:s+4])[0]#Shape type in record
                    fw.write(shapes[Shape_Type]+'\n')
                    
                    ###NULL###
                    if(Shape_Type==0):#point
                        fw.write(shapes[Shape_Type])
                        fw.write("This file is NULL!")
                            
                    ###point####
                    if(Shape_Type==1):#point 
                        
                        X_Points=(struct.unpack("d",_file[s+4:s+12])[0])
                        Y_Points=(struct.unpack("d",_file[s+12:s+20])[0])
                        s+=28
                        fw.write("---X---points---Y---"+'\n')
                        fw.write(str(X_Points)+' '+' '+str(Y_Points)+'\n')
                        
                    ###polygon and polyline####
                    if(Shape_Type==3 or Shape_Type ==5):#polygon and polyline
                        NumParts=struct.unpack("i",_file[s+36:s+40])[0] #NumParts
                        NumPoints=struct.unpack("i",_file[s+40:s+44])[0] #NumPoints
                        fw.write('Parts : '+str(NumParts)+' '+' '+'Points : '+str(NumPoints)+'\n')
                        p=s+(44+4*NumParts)
                        Parts=(struct.unpack("i",_file[s+44:p])[0])
                        fw.write('Parts number : '+str(Parts)+'\n')
                        fw.write("---X---points---Y---")

                        for i in range(0,NumPoints*16,16):#Points #+1?
                            n=s+(44+4*NumParts)+i
                            X_Points=(struct.unpack("d",_file[n:n+8])[0])
                            Y_Points=(struct.unpack("d",_file[n+8:n+16])[0])
                            fw.write('\n')
                            fw.write(str(X_Points)+' '+' '+str(Y_Points)+'\n')
                        fw.write("---------------------- \n")
                        s=(n+24)

                                             
                    ###Multipoint###
                    if(Shape_Type==8):
                        NumParts=struct.unpack("i",_file[s+36:s+40])[0] #NumPoints

                        for i in range(0,NumPoints*16,16):
                            n=s+40+i
                            X_Points=(struct.unpack("d",_file[n:n+8])[0])
                            Y_Points=(struct.unpack("d",_file[n+8:n+16])[0])
                            fw.write('\n')
                            fw.write(str(X_Points)+' '+' '+str(Y_Points)+'\n')
                        fw.write("---------------------- \n")
               
                    ####Multipatch####
                    parts=['Triangle Strip','Triangle Fan',' Outer Ring',' Inner Ring','First Ring','Ring']
                    if(Shape==31):
                        NumParts=struct.unpack("i",_file[s+36:s+40])[0] #NumParts
                        NumPoints=struct.unpack("i",_file[s+40:s+44])[0] #NumPoints
                        fw.write('Parts : '+str(NumParts)+' '+' '+'Points : '+str(NumPoints)+'\n')
                        #print(NumPoints)

                        for i in range(0,NumParts):#Part 
                            W=s+44+(4*i)+4
                            Parts=(struct.unpack("i",_file[W-4:W])[0])
                            fw.write('Parts number : '+str(Parts)+'\n')
                            #print(Parts)

                        for j in range(0,NumParts):#PartType
                            X=W+(4*j)+4
                            PartType=(struct.unpack("i",_file[X-4:X])[0])
                            fw.write('Part Type : '+parts[PartType]+'\n')
                            
                        fw.write("\n" +"------X------points------Y------")
                        for k in range(0,NumPoints):#Points
                            Y=X+(16*k)+16
                            
                            X_Points=(struct.unpack("d",_file[Y-16:Y-8])[0])
                            Y_Points=(struct.unpack("d",_file[Y-8:Y])[0])
                            
                            fw.write('\n')
                            fw.write(str(X_Points)+' '+' '+str(Y_Points)+'\n')
                        fw.write("----------------------------- \n")

                        Z_min=(struct.unpack("d",_file[Y:Y+8])[0])
                        Z_max=(struct.unpack("d",_file[Y+8:Y+16])[0])
                        
                        fw.write('\n'+ "Z min :"+str(Z_min)+' '+' '+"Z max :"+str(Z_max)+'\n')

                        for n in range(0,NumPoints):
                            Z=Y+16+(8*n)+8
                            Z_arr=(struct.unpack("d",_file[Z-8:Z])[0])
                            fw.write("Z array :"+str(Z_arr)+'\n')
                        fw.write("---------------------- \n")
                        #s=(Z+8) #if optional values are NOT available

                        M_min=(struct.unpack("d",_file[Z:Z+8])[0])
                        M_max=(struct.unpack("d",_file[Z+8:Z+16])[0])

                        for m in range(0,NumPoints):
                            V=Z+16+(8*m)+8
                            M_arr=(struct.unpack("d",_file[V-8:V])[0])
                        s=(V+8)
                        fw.write("========================== \n")
                  
                except:
                    break     
        except IOError:
             print('Error While Saving the data!')
    except IOError:
        print('Error While Opening the file!')


parser( r"C:\Users\tarek\Parser_Data/Camb3D_Bldg_Active_MP.shp", r"C:\Users\tarek\Parser_Data\test.txt")







