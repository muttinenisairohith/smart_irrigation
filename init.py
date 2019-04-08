from predtemp import main
import time
if  __name__ == "__main__":
   # url = "http://dataservice.accuweather.com/currentconditions/v1/202190?apikey=iA4TijGiEYAX7jTH75YMEYIawAJIxf0Y&details=true"
   url = "http://dataservice.accuweather.com/currentconditions/v1/202190?apikey=2otXRiamt3Jp6AwO1jyCe4iNYlDIg5rY&details=true"
   port = "/dev/ttyACM0"
   while True:
        output = main(url,port)
        print output
        time.sleep(600)
