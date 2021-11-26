# import os
# import ftplib
# import csv
# import datetime
# import pyodbc
# import dateutil.parser
# from sys import exit

# user='1105loads'
# passwd='xYMTVTnH'
# dirfolder = '/reports/2021/loadtrack'
# server = 'ftp.truckertools.com'


# today= datetime.datetime.now()

# class DateConversion:
#     def __init__(self, dt):
#         self.dt = dt
#         # self.delta = delta

#     def dateconvertionISO8601(self,delta_param):
#         delta = datetime.timedelta(days=delta_param)
#         updated_dt = str(self.dt+delta)
#         yourdate = str(dateutil.parser.parse(updated_dt))
#         converted_date = yourdate[:yourdate.find('.',1)]
#         return converted_date

# conn = pyodbc.connect(

# "Driver={SQL Server Native Client 11.0};"
# "Server=RT-TABDB;"
# "Database=McLeodTMS;"
# "Trusted_Connection=no;"
# "UID=SuperUser;"
# "PWD=Sm00thy!!@RTS;"
# )

# class truckertool_integration(DateConversion):
#     def __init__(self, conn, dt):
#         self.conn = conn
#         super().__init__(dt)

#     def insert_truckertool_daily_integration(self,conn,load_number,start_date,cancelled,not_a_mobile_phone,to_be_tracked,tracked,consistently_tracked,assigned,late_assignment,ELD_load):




#         query = f"insert into [McLeodTMS].[dbo].[Reed_TruckerTools_Daily] values('{load_number}','{start_date}','{cancelled}','{not_a_mobile_phone}','{to_be_tracked}','{tracked}','{consistently_tracked}','{assigned}','{late_assignment}','{ELD_load}','{DateConversion.dateconvertionISO8601(self,-3)}', '{DateConversion.dateconvertionISO8601(self,0)}')"
#         cursor = conn.cursor()
#         cursor.execute(query)

#         conn.commit()
#         cursor.close()


# class grab_file(truckertool_integration):
#     def __init__(self,user, passwd, dirfolder, server,conn, dt):
#         self.user = user
#         self.passwd = passwd
#         self.dirfolder = dirfolder
#         self.server = server
#         truckertool_integration.__init__(self,conn, dt)

#     def grabFile(self):
#         ftp = ftplib.FTP(self.server)
#         ftp.login(user= self.user, passwd=self.passwd)
#         ftp.cwd(self.dirfolder)
#         filename = sorted(ftp.nlst(), key=lambda x: ftp.voidcmd(f"MDTM {x}"))[-1]
#         os.chdir("\\\\rt-tabapp\\ReedTMS_ETL\\TruckerToolsAPI\\FTPdownloadsDaily")
#         if os.path.exists(filename):
#             print('break')
#             exit()
#         localfile = open(filename, 'wb')
#         ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
#         ftp.quit()
#         localfile.close()
#         with open(filename,'r') as csv_file:
#             csv_reader = csv.reader(csv_file)
#             for line in csv_reader:
#                 if 'Daily Loadtrack Stats Report' not in line[0] and 'Load Number' not in line[0]:
#                     # if line[8]:
#                     #     line[8] = int(line[8][:-1])/100
#                     # if line[10]:
#                     #     line[10] = int(line[10][:-1])/100
#                     # if line[0]:
#                     #     line[0] = line[0].replace("'","")
#                     truckertool_integration.insert_truckertool_daily_integration(self, conn, line[0],line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[14])




# def main():
#     main_run = grab_file(user, passwd, dirfolder, server, conn, today)
#     main_run.grabFile()

# if __name__ == "__main__":
#     main()
