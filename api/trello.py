
import requests
import json


def Access_token( mail , pas):
     # return text["access_token"]
    url = 'https://proffstore.com/api/v1/token'
    client_code = "a34f65b2c464"
    payload = {"email": mail , "pass": pas }
    headers = {'Content-Type':'application/json', 'x-client-code':client_code }
    r = requests.post(url, headers=headers , data= json.dumps(payload))
    print( r.json()["access_token"] )
    return r.json()["access_token"]


def to_do_task( access_token ):

    url = 'https://proffstore.com/api/v1/user/tasks'
    client_code = "a34f65b2c464"
    #Access_Token = {"x-access-token": access_token }
    headers = {'Content-Type':'application/json', 'x-client-code':client_code ,"x-access-token": access_token }
    r = requests.get(url, headers=headers )
    print( r.json())

def order_task( access_token ):

    url = 'https://proffstore.com/api/v1/user/projects?portion=1000'
    client_code = "a34f65b2c464"
    #Access_Token = {"x-access-token": access_token }
    headers = {'Content-Type':'application/json', 'x-client-code':client_code ,"x-access-token": access_token }
    r = requests.get(url, headers=headers )
    #print( r.json())
    print ()
    return list(map(need_field, r.json()["projects"].values()))
    
    
def need_field( projects ):
    return { "id": projects["id"], "title": projects["title"] , "tasks" : list(map(need_fields_tasks , projects["tasks"]["tasks"].values()))  }

def need_fields_tasks(tasks):
    return {"id" : tasks["id"] , "title": tasks["title"] , "body": tasks["body"] , "created": tasks.get("created") , "updated": tasks.get("updated") ,
    "deadline": tasks.get("deadline") , "started": tasks.get("started") , "st_color": st_color(tasks.get("started"), tasks.get("deadline") ) }


def st_color(start , end):
    if start != None and end != None :
      hours_to_dead = (int(end[:4])-datetime.now().year)*8760+ (int(end[5:7]) - datetime.now().month)*730 + (int(end[8:10]) - datetime.now().day)*24 + (int(end[11:13]) - datetime.now().hour)

      if hours_to_dead < 24 :
       return "#ff2500"

      if hours_to_dead < 48 and hours_to_dead > 24:
       return "#e75d00"

      if hours_to_dead < 72 and hours_to_dead > 48:
       return  "#e7de00"

      if hours_to_dead > 72:
       return "#4ee700"
    else:
       return "#ffffff"

def all_index_of_freelanser( name ):
    url1 = 'https://proffstore.com/api/v1/search/'
    url2 = "?type=user"
    client_code = "a34f65b2c464"
    #Access_Token = {"x-access-token": access_token }
    headers = {'Content-Type':'application/json', 'x-client-code':client_code }
    r = requests.get(url1+name+url2, headers=headers )
    json1 = r.json()
    json2 = list(map(index_of_freelanser , json1["result"]["users"].values()))
    #print (json1)
    if len(json2) != 0:
       return json2
    else :
       print("list is empty" ) 


def  index_of_freelanser( person ):
    #print(person)
    print ({"id" : person["id"], "firstName": person["firstName"] , "lastName": person["lastName"] , "index": index(person["id"]) } )
    return ({"id" : person["id"], "firstName": person["firstName"] , "lastName": person["lastName"], "index": index(person["id"]) } )

def index(id):
    url1 = 'https://proffstore.com/api/v1/review/'
    portion="?portion=1000"
    client_code = "a34f65b2c464"
    #Access_Token = {"x-access-token": access_token }
    headers = {'Content-Type':'application/json', 'x-client-code':client_code }
    r = requests.get(url1+str(id)+portion, headers=headers )
    json1 = r.json()
    a = list(map(awerage_index , json1["reviews"].values() ))
    
    return sum(a)/len(a)

def awerage_index(indexs):
    p1 = indexs.get("parametr1")/10
    

    p2 = indexs.get("parametr2")/10
    p3 = indexs.get("parametr3")/10
    p4 = indexs.get("parametr4")/10
    p5 = indexs.get("parametr5")/10
    print(p1, p2, p3 , p4, p5)
    return p2*p1*(p5*p3*p2+p5*p3+p2)






print ("1.Access_token")
ACCESS_TOKEN = Access_token("mrkiril@ukr.net","123ss456")
print ("2. to_do_task")

#print ( order_task(ACCESS_TOKEN) )

all_index_of_freelanser("kovrova")
#order_task(ACCESS_TOKEN)

