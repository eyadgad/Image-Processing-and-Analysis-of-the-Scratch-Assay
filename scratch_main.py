
import matplotlib.pyplot as plt
import numpy as np
import cv2,os
import skimage as sk
import imageio
from scipy.stats import linregress
        
def scratch_process(imagepath,all_parameters=False,save_results=False,print_results=False,plot_resluts=False,coeffients=False,gif=False,report=False):
    time_list=[]
    area_list=[]
    if all_parameters:#make all parameters True
        save_results=True
        print_results=True
        plot_resluts=True
        coeffients=True
        gif=True
        report=True
    if gif:
        bin,ent,inp=[],[],[]
    images=os.listdir(imagepath)
 
    for time,image in enumerate(images):
        img=cv2.imread(os.path.join(imagepath,image),0)
        entropy_img = sk.filters.rank.entropy(img, sk.morphology.disk(3))
        thresh = sk.filters.threshold_otsu(entropy_img)
        _, binary_img = cv2.threshold(entropy_img, thresh, 255, cv2.THRESH_BINARY)
        scratch_area = np.sum(binary_img == 0)
        #print(binary_img.shape,type(binary_img))
        #print(entropy_img.shape,type(entropy_img))
        time_list.append(time)
        area_list.append(scratch_area)
        if gif:
            inp.append(img)
            bin.append(binary_img)
            ent.append(entropy_img)

        if save_results:

            #create entropy and binary subfolders in results folder if they don't exist in the working directory

            if not os.path.exists(os.path.join('./results','entropy')):
                os.makedirs(os.path.join('./results','entropy'))
            if not os.path.exists(os.path.join('./results','binary')):
                os.makedirs(os.path.join('./results','binary'))
       
            #save the entropy images and binary images using imwrite
            cv2.imwrite(os.path.join('./results','entropy',image),entropy_img)
            cv2.imwrite(os.path.join('./results','binary',image),binary_img)
        
        if print_results:
            #print the results
            print('Time:',time, "hr  ")
            print('Image:',image)    
            print('Scratch Area:',scratch_area, "pix\N{SUPERSCRIPT TWO}")
            print('\n')
    

      
              
    if plot_resluts:
        #plot the results showing the data points and the line of best fit
        plt.plot(time_list,area_list,'ro')
        slope, intercept, r_value, p_value, std_err = linregress(time_list,area_list)
        plt.plot(time_list,slope*np.array(time_list)+intercept)
        plt.xlabel('Time (hr)')
        plt.ylabel("Scratch area (pix\N{SUPERSCRIPT TWO})")
        plt.title('Scratch Area vs Time')
        plt.savefig("./scratch_results.png")
        plt.close()
    
    if coeffients:
        #linregrress for the plot of time vs area
        slope, intercept, r_value, p_value, std_err = linregress(time_list, area_list)
        print("Y = {:.2f}X + {:.2f}".format(slope,intercept))
        print("R\N{SUPERSCRIPT TWO} = {:.2f}".format(r_value**2))
        print("Standard error= {:.2f}".format(std_err))
        print("P-value= {:.2f}".format(p_value))
        print("\n")
    
    if report:
        #create a report of the results
        report_file=open("./scratch_report.txt","w+")
        report_file.write("Y = {:.2f}X + {:.2f}".format(slope,intercept))
        report_file.write("\n")
        report_file.write("R\N{SUPERSCRIPT TWO} = {:.2f}".format(r_value**2))
        report_file.write("\n")
        report_file.write("Standard error= {:.2f}".format(std_err))
        report_file.write("\n")
        report_file.write("P-value= {:.2f}".format(p_value))
        report_file.write("\n")
        report_file.close()
    if gif:
        #create a gif of the input images
        imageio.mimsave('./results/input_animation.gif',inp) 
        #create a gif of the binary images 
        imageio.mimsave('./results/binary_animation.gif',bin)
        #create a gif of the entropy images
        imageio.mimsave('./results/entropy_animation.gif',ent)
        
    
        

    return time_list,area_list

   


#main
if __name__ == "__main__":
    time_list,area_list=scratch_process("./images",all_parameters=True)
    #print(time_list,area_list)
