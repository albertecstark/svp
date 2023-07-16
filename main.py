import math
import gsw
import numpy as np
import matplotlib.pyplot as plt
import csv

#TODO: lookup the oriinal documentation of the gsw library (TEOS-10) and find the actual diff eq used (solve general case?)

#dataset is for mariana trench, from https://www.youtube.com/watch?v=-tGusgPTSm4, pulled from dropbox in description
lat = 11
long = 142

#region setup and handelling
#read data into arrays of floats
filename = open('Flere_03Mar_1_2021.csv', 'r')
file = csv.DictReader(filename)

pressure = []
conductivity = []
temperature = []
density = []
speeds_from_dataset = []

for col in file:
    pressure.append(col['Pressure'])
    conductivity.append(col[' Conductivity'])
    temperature.append(col[' Temperature'])
    density.append(col[' Density'])
    speeds_from_dataset.append(col[' Sound_Speed'])

pressure = [float(x) for x in pressure]
conductivity = [float(x) for x in conductivity]
temperature = [float(x) for x in temperature]
density = [float(x) for x in density]
speeds_from_dataset = [float(x) for x in speeds_from_dataset]

#use this method so only have to return max index no any second derivative malarkey
#also no military submarine goes beneath 1500m, except for crush depth on some soviet ones from the cold war
#this cutoff gives us ~3700m
data_len = 500

pressure = pressure[:data_len]
conductivity = conductivity[:data_len]
temperature = temperature[:data_len]
density = density[:data_len]
speeds_from_dataset = speeds_from_dataset[:data_len]

#defining checks on input size
def check_in(a,b,c,d,e):
    if(len(a)!=len(b)!=len(c)!=len(d)!=len(e)):
        print("! mismatched input size")
        exit(0)

#generating depth list
depth =  -1 * gsw.z_from_p(pressure, lat)

#defining sound speed function
def sound_speed_deriv(conductivity, temperature, pressure, lat, long):
    practical_salinity = gsw.SP_from_C(conductivity, temperature, pressure)
    absolute_salinity = gsw.SA_from_SP(practical_salinity, pressure, long, lat)
    sound_speed_deriv = gsw.sound_speed(absolute_salinity, temperature, pressure)
    return sound_speed_deriv

speeds_calc = sound_speed_deriv(conductivity, temperature, pressure, lat, long)
#endregion

#region calculations on data
#TODO: implement proper second derivative implementation
def print_properties_data():
    LD_index = speeds_from_dataset.index(max(speeds_from_dataset))
    LD = depth[LD_index]
    BD = 0
    if LD < 60 :
        BD = 17 * math.sqrt(LD)
    else:
        BD = LD + 60
    print(f"LD_index = {LD_index}, LD = {LD} and BD = {BD} for the given data")

def print_properties_calc():
    LD_index = np.argmax(speeds_calc)
    LD = depth[LD_index]
    BD = 0
    if LD < 60 :
        BD = 17 * math.sqrt(LD)
    else:
        BD = LD + 60
    print(f"LD_index = {LD_index}, LD = {LD} and BD = {BD} for the derived data")
#endregion

#region image generation
def gen_img_svps():
    #the calculated and given data plotted
    fig, ax = plt.subplots()
    x1 = depth
    y11 = speeds_calc
    y12 = speeds_from_dataset
    ax.plot(x1,y11, "-b", label="speeds as derived from this program")
    ax.plot(x1,y12, "-r", label="speeds directly from dataset")
    ax.legend()
    plt.savefig('svp.png')

def gen_img_deviations():
    #deviation between the calculated and given data
    fig, ax = plt.subplots()
    x = depth
    y = speeds_from_dataset - speeds_calc
    ax.plot(x, y, "-r", label = "Deviation in calculated and given values")
    plt.savefig('deviation.png')

def gen_img_propagation_paths():
    #propagation paths
    #TODO propagation paths
    time = 0.00005 # "seconds"
    dt = 0.00001
    timesteps = int(time/dt)
    theta_res = 2
    values = np.zeros((theta_res, timesteps, 2))
    #values[theta step][time step][x or y], starts at 0 
    for i in range(theta_res):
        for j in range(timesteps):
            values[i][j] = 2
    print(values)


    fig, ax = plt.subplots()
    plt.savefig('paths.png')
#endregion

def main():
    check_in(pressure, conductivity, temperature, density, speeds_from_dataset)
    #print_properties_calc()
    #print_properties_data()
    #gen_img_svps()
    #gen_img_deviations()
    gen_img_propagation_paths()

if __name__ == "__main__" :
    main()