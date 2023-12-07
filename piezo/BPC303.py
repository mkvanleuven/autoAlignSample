import piezo.benchtop_piezo_controller as bpc
from ctypes import (
    create_string_buffer,
    c_int,
    c_short
)
from piezo.utils import (
    c_word
)
from time import sleep
import sys


class BPC303:
    
    def __init__(self, stage) -> None:
        if bpc.TLI_BuildDeviceList() == 0:
            num_devs = int(bpc.TLI_GetDeviceListSize())
        receive_buffer = create_string_buffer(bytes(" " * 250, "utf-8"))
        buffer_size = bpc.c_dword(250)
        bpc.TLI_GetDeviceListByTypeExt(receive_buffer, buffer_size, c_int(71))

        serial_nos = receive_buffer.value.decode("utf-8").strip().split(',')
        
        #self.serial = create_string_buffer(bytes(serial_nos[stage], "utf-8"))
        self.serial = 'None'
        for device in serial_nos:
            cur_serial_no = create_string_buffer(bytes(device, "utf-8"))
            # print(cur_serial_no.value.decode())
            if cur_serial_no.value.decode() == stage: 
                self.serial = cur_serial_no
    #           print(self.serial.value.decode("utf-8").strip().split(','))
                if bpc.PBC_Open(self.serial) == 0:
                    print(f'opened BPC303 {stage} successfully')
                else:
                    print(f'could not open BPC303 {stage}')
                    raise ValueError('Open unsuccessful')
                #milliseconds = c_int(100)
                #sleep(1)
                #bpc.PBC_StartPolling(self.serial, milliseconds)
                milliseconds = c_int(100)
                for channel in range(1,bpc.PBC_GetNumChannels(self.serial)+1):
                    if bpc.PBC_IsChannelValid(self.serial,channel):
                        bpc.PBC_StartPolling(self.serial, channel, milliseconds)
                        #print(f'Polling on channel {channel}', end='\r')
                        if bpc.PBC_SetPositionControlMode(self.serial, channel, 1) == 0:
                            #sleep(1)
                            bpc.PBC_RequestPositionControlMode(self.serial, channel)
                            ControlMode = bpc.PBC_GetPositionControlMode(self.serial, channel)
                            #print(kpz.PZ_CloseLoop)
                            #print(f'Control_mode:{ControlMode}, Channel:{channel}')
                            #print(f'Connected to channel {channel} on control mode {ControlMode}', end='\r')
                            #bpc.PBC_SetZero(self.serial, channel)
                            self.loop_mode = 'open'
                            #sleep(1)
                            #print(f'Zeroing channel {channel}', end='\r')
                            #self.set_voltage(channel, 0)
                            #bpc.PBC_SetZero(self.serial, channel)
                            #print(f'Channel {channel} initialised')
                    else:
                        print(f'could not home channel {channel}')

                #if bpc.PBC_Enable(self.serial) != 0:
                #    print('Enable not successful')
                self._numChannels = bpc.PBC_GetNumChannels(self.serial)
                print(f"Connected to {self._numChannels} channels.")
                sleep(1)
        
        self.zero()
            
        if self.serial == 'None':
            print(f'could not find device {stage}')
            raise ValueError('No such device found')
    
    def zero(self) -> None:
        i = 1
        while i < self._numChannels + 1:
            #print(f'Zeroing channel {i}')
            self.set_voltage(i, 0)
            i += 1
        print(f'{i - 1} channels zeroed')

    def close(self) -> None:
        bpc.PBC_StopPolling(self.serial)
        bpc.PBC_Close(self.serial)
        # if self.loop_mode == 'closed':
        #     self.Strain_G.close()
        
    # def set_loop_mode(self, loop_mode):
    #     sleep(1)
    #     if loop_mode == "open":
    #         if kpz.PCC_SetPositionControlMode(self.serial, 1) == 0:
    #             sleep(1)
    #             print("Control mode set: Open")
    #             self.loop_mode = 'open'
    #             return 0
    #     elif loop_mode == "closed":
    #         if Strain_gauge == 'None':
    #             print('No Strain gauge serial number entered')
    #             return 1
    #         self.set_hub_analogue_input(self.hub_channel)
    #         sleep(1)
    #         self.Strain_G = ksg.KSG101(Strain_gauge)
    #         sleep(1)
    #         self.Strain_G.set_hub_analogue_output(self.hub_channel)
    #         sleep(1)
    #         if kpz.PCC_SetPositionControlMode(self.serial, 4) == 0:
    #             sleep(1)
    #             print("Control mode set: Closed")
    #             self.loop_mode = 'closed'
    #             return 0
    #     else:
    #         print("Loop mode not recognised")
    #         return 1
            
    # def set_position(self, position): # Sets position in closed loop mode
    #     pos = int(position * 653.55)
    #     kpz.PCC_RequestPositionControlMode(self.serial)
    #     ControlMode = kpz.PCC_GetPositionControlMode(self.serial)
    #     if ControlMode == 2:
    #         if kpz.PCC_SetPosition(self.serial, c_word(pos)) == 0:
    #             #sleep(1)
    #             #print(f"Position set to {position}")
    #             pass
    #         else:
    #             print(f"failed to set position")
    #     else:
    #         print("Couldn't set position: control mode not closed")
        
    # def get_position(self):
    #     #sleep(1)
    #     kpz.PCC_RequestPositionControlMode(self.serial)
    #     ControlMode = kpz.PCC_GetPositionControlMode(self.serial)
    #     #print(f'control mode:{ControlMode}')
    #     if ControlMode == 2:
    #         pos = kpz.PCC_GetPosition(self.serial)
    #         pos_ksg = self.Strain_G.get_reading()
    #         return pos_ksg #/327.67
    #     else:
    #         print("Couldn't set position: control mode not closed")            

    def set_voltage(self, channel, voltage) -> None: #sets voltage as a percentage of max voltage
        bpc.PBC_RequestPositionControlMode(self.serial, channel)
        ControlMode = bpc.PBC_GetPositionControlMode(self.serial, channel)
        pos = c_short(int(self.convert_pc_to_pos(voltage)))
        if ControlMode == 1:
            if bpc.PBC_SetOutputVoltage(self.serial, channel, pos) == 0:
                print(f"Voltage set to {voltage}% of max voltage on channel {channel}")
                pass
            else:
                print("failed to set voltage")
        else:
            print("Mode not correct for voltage setting")
            
    def get_voltage(self, channel) -> float:
        bpc.PBC_RequestPositionControlMode(self.serial, channel)
        ControlMode = bpc.PBC_GetPositionControlMode(self.serial, channel)
        if ControlMode == 1:
            bpc.PBC_RequestOutputVoltage(self.serial, channel)
            pos = bpc.PBC_GetOutputVoltage(self.serial, channel)
            return self.convert_pos_to_pc(pos)
        else:
            print("Mode not correct for voltage setting")
            
    def get_maxVoltage(self, channel) -> float:
        
        bpc.PBC_RequestPositionControlMode(self.serial, channel)
        ControlMode = bpc.PBC_GetPositionControlMode(self.serial, channel)
        if ControlMode == 1:
            bpc.PBC_RequestMaxOutputVoltage(self.serial, channel)
            pos = bpc.PBC_GetMaxOutputVoltage(self.serial, channel)
            return pos
        else:
            print("Mode not correct for voltage setting")
            
    def set_maxVoltage(self, channel, volts) -> None:
        maxi = volts *10
        bpc.PBC_RequestPositionControlMode(self.serial, channel)
        ControlMode = bpc.PBC_GetPositionControlMode(self.serial, channel)
        if ControlMode == 1:
            if maxi == 750:
                bpc.PBC_SetMaxOutputVoltage(self.serial, channel, maxi)
        else:
            print("Mode not correct for voltage setting")  
            
    def convert_pc_to_pos(self, percentage) -> float:
        return percentage / 100 * 32767
     
    def convert_pos_to_pc(self, pos) -> float:
        return pos/32767 * 100

    # def set_hub_analogue_input(self, channel):
    #     self.hub_channel = channel
    #     if channel == 1:
    #         kpz.PCC_SetHubAnalogInput(self.serial,kpz.AnalogueCh1)
    #     elif channel == 2:
    #         if kpz.PCC_SetHubAnalogInput(self.serial,kpz.AnalogueCh2)== 0:
    #             print("Hub channel set to 2")
    #     elif channel == 3:
    #         kpz.PCC_SetHubAnalogInput(self.serial,kpz.ExtSignalSMA)
            
# def start_sim():
#     kpz.TLI_InitializeSimulations()
    
# def stop_sim():
#     kpz.TLI_UninitializeSimulations()