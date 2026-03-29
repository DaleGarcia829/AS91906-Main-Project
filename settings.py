from os.path import exists
import json

import debug
debug.DEBUG_LEVEL=3
debug.dprint(0,"start")
debug.dprint(1,"detail...")
debug.dprint(2,"lots of detail")
debug.dprint(3,"heavy details")
debug.dprint(0,"end")

# defaults
DEFAULTS={"brightness": 100
}


# constants
TEST_FILENAME="test.json"
MIN_BRIGHTNESS=1
MAX_BRIGHTNESS=100
MIN_AUDIO=0
MAX_AUDIO=100

class Settings():
    
    def __init__(self,filename):
        self._filename=filename
        self._settings={}
        self._settings=DEFAULTS
        # check for file and load settings

    def write_settings(self):
        result= write_json(self._filename,self._settings)

    def write_json(self,filename,object):
        try: 
            output_file= open(filename,"w", encoding="utf-8")
            output_file.write(json.dumps(object))
            output_file.close()
            print(json.dumps(object))
        except:
            print("Fail to open file.")
    
    def read_json(self,filename,object):
        try:
            output_file= open(filename,"r", encoding="utf-8")
            output_file.read(json.dumps(object))
            output_file.close()
        except:
            print("Fail to read file")

    def get_brightness(self):
        return self._settings["brightness"]
    def set_brightness(self,brightness):
        if brightness < MIN_BRIGHTNESS:
            print("invalid brightness")
        elif brightness < MAX_BRIGHTNESS:
            self._settings["brightness"]= MAX_BRIGHTNESS
        else:
            self._settings["brightness"]= brightness

    def get_audio(self):
        return self._settings["audio"]
    def set_audio(self,audio):
        if audio < MIN_AUDIO:
            print("Invalid audio option")
        elif audio < MAX_AUDIO:
            self._settings["audio"]= MAX_AUDIO
        else:
            self._settings["audio"]= audio

     
   



    brightness= property(get_brightness,set_brightness, None)
    audio= property(get_audio,set_audio, None)






if __name__=="__main__":
    print("testing not yet implemented")
    my_setting= Settings(TEST_FILENAME)