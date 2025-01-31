import requests   
# this lets us send post request, get requests, put request whaterver it may be

BASE = "http://127.0.0.1:5000/" # definng waht our base url is gonna be


#data = [{"likes": 2000, "name": "funnyclips","views": 80000}, 
       #{"likes": 50000, "name": "movie","views": 500000},
       # {"likes": 23000, "name": "tutorial","views": 96000}]

#for i in range(len(data)):

   # response = requests.put(BASE + "video/" + str(i), data[i])   #means we want to send a get request to the url that is BASE + "Helloworld"  # we are sending information through request, {"likes": 10}
                                                                    
   # print(response.json())  # .json()  becuase we dont want it to look like response object instead be actual information# .json() method does it for us 

      
#input()     #press any key to pass
response = requests.patch(BASE + "video/2", {"views" : 99, "likes":101})
print(response.json())






