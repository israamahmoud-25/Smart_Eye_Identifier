import datetime
import os
def get_csv(name = "attendance_data.csv"):
    if not os.path.exists(name):
        f =open(name,'w+')
        f.writelines("name,date\n")
    return name



def markAttendance(name,filename, seconds_split = 40):
    with open(f'{filename}','r+') as f:
        namedates = f.readlines()
        for i in range(len(namedates) - 1, -1, -1):
            entry = namedates[i].strip().split(',')
            if entry[0].strip() == name :
                now = datetime.datetime.now()
                date2=datetime.datetime.strptime(entry[1],'%Y-%m-%d %H:%M:%S')
                print((now-date2).seconds)
                if(now-date2).seconds > seconds_split:
                    dtString = now.strftime('%Y-%m-%d %H:%M:%S')
                    f.writelines(f'{name},{dtString},\n')
                    return
                else : 
                    return
        else : 
            now = datetime.datetime.now()
            dtString = now.strftime('%Y-%m-%d %H:%M:%S')
            f.writelines(f'{name},{dtString},\n')
            return 
        