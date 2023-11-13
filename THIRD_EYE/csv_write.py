import csv
import time
import datetime
# Open the CSV file in append mode

def write_data(data1, data2, data3):
    with open('data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        timestamp = time.time()
        dt = datetime.datetime.fromtimestamp(timestamp)
        formatted_timestamp = [dt.strftime("%Y-%m-%d %H:%M:%S")] 
                           #time
        data1 = str(data1) #status
        data2 = str(data2) #data
        data3 = str(data3) #parametres

        data1 = f"{data1}"
        data2 = f"{data2}"
        data3 = f"{data3}"

        writer.writerow([formatted_timestamp,data1, data2, data3])

for i in range(1, 6):

    write_data(i, i+1, i+3)
    print(i)
    time.sleep(1)

