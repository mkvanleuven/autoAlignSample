import piezo.BPC303 as bpc
import time

piezo = bpc.BPC303("71281854")

#print(piezo.get_maxVoltage(1))

piezo.set_voltage(1, 50)
piezo.set_voltage(2, 50)
piezo.set_voltage(3, 50)

## header 5 2nd down