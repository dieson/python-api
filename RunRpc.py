import xmlrpclib
import json
import sys

myIP = 'localhost'
if len(sys.argv) >=2:
  myIP = sys.argv[1]
  
server = xmlrpclib.ServerProxy("http://" + myIP + ":8008")
cpuPercent = server.get_cpu()
print (cpuPercent)
print(server.keep_alive())
print(server.run_job(json.dumps({'productName':'neocutest', 'suiteName':'getAllDevice', 'suiteType': 1,
                                'sutIp':'10.21.1.214',  'testResultId': 'testResult'})))
