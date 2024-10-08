##Ethan Rodriguez and Andrea Diaz
##November 2023
##Muon and Altitude Data Analysis

import matplotlib.pyplot as plt
import csv
from datetime import time, timedelta, datetime

##########################################
#####STORE ALTITUDE DATA IN ARRAY
##########################################

file_path = 'October14Flight.csv'

#initialize array
SecondsAndAltitude = []

#open numbers file
with open(file_path, 'r', newline='') as file:
    reader =csv.reader(file)

    #skips header row
    next(reader)

    #for every row
    for row in reader:
        #second element in the row (index 1)
        datetime_str = row[1]

        #tells the computer the format of the cell or how to read it
        dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
        #converts to local time 
        LocalRealTime = dt - timedelta(hours = 5)
        #grabs the altitude data
        altitude = float(row[4])

        time_sec = LocalRealTime.hour * 3600 + LocalRealTime.minute * 60 + LocalRealTime.second
        time_sec_base = time_sec - ((9*3600) + (31* 60))

        #adds them to the array
        SecondsAndAltitude.append([time_sec_base, altitude])

print("Arrays contrsucted.")

############################################
#####Creating Altitude bin array
############################################

binned_altitude = []

n = 1 #n is bin number
bin_start = 0 
bin_end = n * 60
for pair in SecondsAndAltitude:
    #If the time is in the bin 
    #add to an array, bin number, time, and altitude
    if bin_start <= pair[0] <= bin_end:
        binned_altitude.append((n, pair[0], pair[1]))
    #If the time is larger than the bin end
    elif pair[0] > bin_end:
        init = 0
        #Until I say it fits in the bin
        while init == 0:
            #go to the next bin number
            n = n+1
            #this bin's start is equal to the last bin's end
            bin_start = bin_end
            bin_end = n*60
            #if the time is in this bin add to the array
            if bin_start <= pair[0] <= bin_end:
                binned_altitude.append((n, pair[0], pair[1]))
                #init to 1 to break the loop
                init = 1
            #if the time is not in this bin, go to the next bin
            else:
                continue
print("Binned Altitude Constructed")
            
            
            
            
#########################################
#####Average ALT per Bin
#########################################

average_alt_per_bin = []  
# An's array
time_array = []
alt_array = []

# Bin initially 1
bin = 1
done = 0

while done == 0:
    # initialize final
    time_array = []
    alt_array = []
    final = 0
    # go through each item in array, and if its first element is equal to bin
    # Add to An's array
    for item in binned_altitude:
        if item[0] == bin:
            time_array.append(item[1])
            alt_array.append(item[2])
    k = len(time_array)
    
    if k == 1:
        # If only one element, append its alt to the final array
        average_alt_per_bin.append([bin,alt_array[0]])
        bin += 1
    elif k == 0:
        bin += 1
        continue
    else:
        total_time_diff = time_array[-1] - time_array[0]

        i = 0
        j = 1

        while j < k:
            weighted_average = (alt_array[i] + alt_array[j]) / 2
            weighted_average = weighted_average * ((time_array[j] - time_array[i]) / total_time_diff)

            final = final + weighted_average
            i += 1
            j += 1
        average_alt_per_bin.append([bin, final])
        bin += 1

        # Check if all bins are processed
        if bin > max(item[0] for item in binned_altitude):
            done = 1
print("Average Altitude per Bin Calculated")
print("Weighted Averages for Each Bin:", average_alt_per_bin)


###################################
######DL Data Array
###################################
# Specify the file name
file_name = "DLData.txt"

# Initialize an empty array to store the numbers
DLData = []

# Open the file in read mode
with open(file_name, 'r') as file:
    # Read each line from the file
    lines = file.readlines()

    # Convert each line to a number and add it to the array
    for line in lines:
        # Use strip() to remove leading and trailing whitespaces, and convert to float
        number = float(line.strip())
        DLData.append(number)





#########################################
##### Final Flux, Final Altitude
#########################################
Final_Altitude = []
Final_Count_rate = []

for item in average_alt_per_bin:
    bin_match = item[0]
    Final_Count_rate.append(DLData[bin_match-1])
    Final_Altitude.append(item[1])
    
x_values = Final_Altitude
y_values = Final_Count_rate


plt.scatter(x_values, y_values, label='Muon detector Data')

# Add labels and title
plt.xlabel('Altitude (m)')
plt.ylabel('Count Rate ($s^{-1}$)')
plt.title('Count Rate vs Altitude')

# Add a legend
plt.legend()

# Display the plot
plt.show()  



