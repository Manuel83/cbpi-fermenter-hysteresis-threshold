from modules import cbpi
from modules.core.controller import KettleController, FermenterController
from modules.core.props import Property


@cbpi.fermentation_controller
class HysteresisWithThreshold(FermenterController):

    heater_offset_min = Property.Number("Heater Offset ON", True, 0, description="Offset as decimal number when the heater is switched on. Should be greater then 'Heater Offset OFF'. For example a value of 2 switches on the heater if the current temperature is 2 degrees below the target temperature")
    heater_offset_max = Property.Number("Heater Offset OFF", True, 0, description="Offset as decimal number when the heater is switched off. Should be smaller then 'Heater Offset ON'. For example a value of 1 switches off the heater if the current temperature is 1 degree below the target temperature")
    cooler_offset_min = Property.Number("Cooler Offset ON", True, 0, description="Offset as decimal number when the cooler is switched on. Should be greater then 'Cooler Offset OFF'. For example a value of 2 switches on the cooler if the current temperature is 2 degrees above the target temperature")
    cooler_offset_max = Property.Number("Cooler Offset OFF", True, 0, description="Offset as decimal number when the cooler is switched off. Should be less then 'Cooler Offset ON'. For example a value of 1 switches off the cooler if the current temperature is 1 degree above the target temperature")
    max_threshold = Property.Number("Temperature Threshold when the automatic will switch off", True, 30, description="Min Threashold when the automatic will switch off. For example if the sensor is sending wrong data. Including max offset")
    min_threshold = Property.Number("Temperature Threashold when the automatic will switch off", True, -4, description="Min Threashold when the automatic will switch off. For example if the sensor is sending wrong data. Including min offset")
    max_threshold_exceeded = Property.Number("Max number for threshold exceeded before switch off", True, 3, description="Max number of threshold exceed before switch off the controller.")
    max_threshold_exceeded_count = Property.Number("Internal Counter", False, 0, description="Internal Threshold Counter")
    
    def stop(self):
        super(FermenterController, self).stop()

        self.heater_off()
        self.cooler_off()

    def run(self):
    
        
        while self.is_running():

            target_temp = self.get_target_temp()
            temp = self.get_temp()
            
            if temp + float(self.heater_offset_max) <= self.min_threshold:
                if max_threshold_exceeded_count >= max_threshold_exceeded:
                  self.stop()
                  continue
                self.max_threshold_exceeded_count = self.max_threshold_exceeded_count+1
            
            if temp + float(self.heater_offset_max) >= self.max_threshold:
                if max_threshold_exceeded_count >= max_threshold_exceeded:
                  self.stop()
                  continue
                self.max_threshold_exceeded_count = self.max_threshold_exceeded_count+1
                

            if temp + float(self.heater_offset_min) <= target_temp:
                self.heater_on(100)

            if temp + float(self.heater_offset_max) >= target_temp:
                self.heater_off()

            if temp >= target_temp + float(self.cooler_offset_min):
                self.cooler_on(100)

            if temp <= target_temp + float(self.cooler_offset_max):
                self.cooler_off()

            self.sleep(1)
