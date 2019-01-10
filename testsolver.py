import subprocess
import solver
import os


expected = ["S5QJB","FBH8P","3NG7D","CMAIP","ULSRH","N96QO","8LVYC","LOCFL","QP9CO","ONSCS","ROEGG","I4MJ9","IOBGX","25VOP", "6IAAS", "K6HFE", "SXWZ5", "E3ODK", "NWR7D", "F8WJF", "CA82P", "OOVOO", "2SJ4I", "8RKZF", "3BHDF"]
index = 0
hits = 0

list = os.listdir("samples")
list.sort()

for file in list:
  if file.endswith(".jpe"):
     result = solver.solve(os.path.join("samples/",file))
     
     if expected[index].strip() == result.strip():
       hits += 1
     else:
       print ( file+": "+expected[index]+' => '+result, end='' )  
   
     index += 1

print('hits: '+str(hits))
print('total: '+str(index))
