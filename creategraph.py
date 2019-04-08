import firebase

def send_data():
    firebaseq = firebase.FirebaseApplication('https://smart-irrigation-outer.firebaseio.com/', None)
    result = firebaseq.get('', '')

    d = {}
    for data in result:
        if data == "present":
            continue
        else:
            #print result[data]
            for key,value in result[data].items():
               if key=="output":
                   continue
               else:
                  try:
                      d[key].append(value)
                  except KeyError:
                      d[key] = [value]
    return d

def send_graph():
    d = send_data()
    l = []
    for key,value  in d.items():
        if key == "Moisture":
             continue
        elif key == "Wheater":
             continue
        l1 = []
        l1.append(key)
        for i in value:
            l1.append(i)
        l.append(l1)
    return l

def send_data_table():
   d = send_data()
   l = []
   for key,value  in d.items():
        l1 = []
        for i in value:
            l1.append(i)
        l.append(l1)
   print l
   return l

#send_data_table()
