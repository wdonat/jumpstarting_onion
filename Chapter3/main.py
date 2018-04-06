import oneWire
import temperatureSensor
from twython import Twython

# Twitter stuff
app_key = "ToxWXdvWNNrh97l5vYPDoAjsf"
app_secret = "YpcVk6hYsLvsh7t7bxm1NCfY52stWx0tPnQDD4aXP4mfNoA1lA"
oauth_token = "2680369399-fU3uoNKwDelbpeuoUGd3tPAmrvjrM2FgvM7iDaH"
oauth_secret = "qvDkgdVJcEg1EcOj64QhPnKJGeasjJGgrsKynObq5kSMF"
twitter = Twython(app_key, app_secret, oauth_token, oauth_secret)

oneWireGpio = 19

def __main__():
    
    if not oneWire.setupOneWire(str(oneWireGpio)):
        print "Kernel module could not be inserted. Please reboot and try again."
        return -1

    # get the address of the temperature sensor
    # 	it should be the only device connected in this experiment    
    sensorAddress = oneWire.scanOneAddress()

    # instantiate the temperature sensor object
    sensor = temperatureSensor.TemperatureSensor("oneWire", { "address": sensorAddress, "gpio": oneWireGpio })
    if not sensor.ready:
        print "Sensor was not set up correctly. Please make sure that your sensor is firmly connected to the GPIO specified above and try again."
        return -1

    # check and print the temperature
    temperature = sensor.readValue()
    dataPoint = {
        "temperature": temperature
    }

    # temperature is in deg C
    # To change to deg F, add following line:
    temperature = temperature * (9.0/5.0) + 32.0
    
    # Post to Twitter
    twitter.update_status(status="Current Omega2 temperature: " + str(temperature))
    
    
if __name__ == '__main__':
    __main__()
