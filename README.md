# autoAlignSample/
Image collection and analysis code to optimise the position of a Thorlabs BPC303 benchtop piezo controller using image 
feedback from a Teledyne Prime BSI Express sCMOS camera. Python wrapper for Thorlab's Kinesis communication protocol 
for the BPC303 benchtop piezo controller based on [ekarademir's thorlabs_kinesis](https://github.com/ekarademir/thorlabs-kinesis/) bindings. This code is being 
used by the Imperial College London EXSS group for increasing integration time in temperature measurements of plasmonic 
nanostructures.

# Installation
To be able to run this code, some dependancies are required. They are not difficult to install, but I will outline here 
how to do so. If you prefer a video tutorial, check out [this video](https://youtu.be/oFDtj0EP-r8) I made showing how to download the 
dependencies.

We begin with Thorlabs' Kinesis software, which is required to control the piezo stage. The installer can be downloaded 
[here](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=0). Do not modify the default installation location, if you do, you will have to change it in 
`benchtop_stepper_motor.py` and `benchtop_piezo_controller.py` yourself. The code has only been tested using Kinesis 
64-Bit Software for 64-Bit Windows, so I cannot promise support for any 32-Bit software. No SDK is required.

Secondly, to be able to use the camera, PVCAM drivers are required. I cannot send the download link directly, however it 
is possible to submit a form to get the `/download` link from [here](https://www.photometrics.com/support/download/pvcam/). I do not believe the SDK is required to use 
this code. 

Before the Python wrapper can be installed, Visual Studio C++ Build Tools is required. To do this, download 
and install Visual Studio from [here](https://visualstudio.microsoft.com/), I recommend the Community edition, however it will not matter. This should 
bring you into the Visual Studio Installer, where you scroll down to the "Desktop & Mobile" tab. Ensure "Desktop 
development with C++" is selected, and install.

The final step is to install the Python wrapper for PVCAM, which can be downloaded [here](https://github.com/Photometrics/PyVCAM). Download the GitHub repo 
and unzip it. Use a terminal to navigate to the installed folder, and run the command `python setup.py install`. This 
assumes you have Python installed, but I doubt you would be using this code if that were not the case.

If you have any issues, feel free to contact me and I may try to assist, but I cannot promise anything. Good luck with 
the code, thanks for downloading!
# Docs
## camera/
### PBSI.createCam
`PBSI.createCam()`

Searches connected devices on serial ports for a valid camera, and creates a camera object if one can be found.
<pre>
Parameters:
    None
</pre>
<pre>
Returns:
    out : pyvcam Camera
        Detected camera object.
</pre>

### PBSI.openCam
`PBSI.openCam(camera)`

Opens connection to a camera.
<pre>
Parameters:
    camera : pyvcam Camera
        Camera object to open connection to.    
</pre>
<pre>
Returns:
    None
</pre>

### PBSI.closeCam
`PBSI.closeCam(camera)`

Closes connection to a camera.
<pre>
Parameters:
    camera : pyvcam Camera
        Camera object to close connection to.    
</pre>
<pre>
Returns:
    None
</pre>

### PBSI.generateFrame
`PBSI.generateFrame(camera, exposure_time)`

Generates an image with specified camera and exposure time.
<pre>
Parameters:
    camera : pyvcam Camera
        Camera object to take image with.
    exposure_time : int
        Exposure length of image to be taken in ms.
</pre>
<pre>
Returns:
    out : ndarray
        2D NumPy array with shape equal to camera sensor dimensions in px representing pixel intensity values.
</pre>

### PBSI.getGain
`PBSI.getGain(camera)`

Gets gain index of camera.
<pre>
Parameters:
    camera : pyvcam Camera
        Camera object to get gain index of.    
</pre>
<pre>
Returns:
    out : int
        Gain index of specified camera.
</pre>

### PBSI.setGain
`PBSI.setGain(camera, gain_index)`

Sets gain index of camera.
<pre>
Parameters:
    camera : pyvcam Camera
        Camera object to get gain index of.   
    gain_index : int
        Value to set camera gain index to.
</pre>
<pre>
Returns:
    None
</pre>

### photometry.mostCommon
`photometry.mostCommon(list)`

Gets most common value from a NumPy array. Works with ndarrays.
<pre>
Parameters:
    list : ndarray
        Array of values to get most common value of.
</pre>
<pre>
Returns:
    out : int
        Most common value of input array.
</pre>

### photometry.subtractBackground
`photometry.subtractBackground(image)`

Subtracts image background based on most common pixel value.
<pre>
Parameters:
    image : ndarray
        Image from camera.
</pre>
<pre>
Returns:
    out : ndarray
        Background subtracted image.
</pre>

### photometry.getPeakIntensity
`photometry.getPeakIntensity(image)`

Gets highest intensity value in the image.
<pre>
Parameters:
    image : ndarray
        Image from camera.
</pre>
<pre>
Returns:
    out : float
        Maximum intensity value in image.
</pre>

### photometry.getPeakIndex
`photometry.getPeakIndex(image)`

Gets position of highest intensity value in the image.
<pre>
Parameters:
    image : ndarray
        Image from camera.
</pre>
<pre>
Returns:
    out : array
        NumPy array of the average position where the peak intensity occurs.
</pre>

### photometry.step
`photometry.step(image, startIndex, dir, threshold)`

Stepper function to travel from a starting point in a given direction until an intensity threshold condition is 
reached.
<pre>
Parameters:
    image : ndarray
        Image from camera.
    startIndex : array
        Position to begin stepping from.
    dir : array
        Direction to step in.
    threshold : 
        Intensity threshold condition as a fraction of the peak.
</pre>
<pre>
Returns:
    out : array
        First position where the stepper function reaches the threshold condition.
</pre>

### photometry.getBbox
`photometry.getBbox(image, center, frac)`

Gets the bounding box of a spot based on the stepper function.
<pre>
Parameters:
    image : ndarray
        Image from camera.
    center : array
        Position to begin stepping from, assumed to be spot center.
    frac : array
        Intensity threshold condition as a fraction of the peak.
</pre>
<pre>
Returns:
    out : ndarray
        NumPy array containing the top left and bottom right positions of the bounding box respectively.
</pre>

### photometry.getSpotDiameter
`photometry.getSpotDiameter(bbox)`

Gets the bounding box of a spot based on the stepper function.
<pre>
Parameters:
    bbox : ndarray
        Bounding box of spot.
</pre>
<pre>
Returns:
    out : float
        Approximate spot diameter based on the mean of vertical and horizontal axes.
</pre>


## piezo/
### utils
Supporting code to use Thorlabs' original C bindings in python.

### benchtop_piezo_controller
Supporting code to use Thorlabs' original C bindings in python.

### benchtop_stepper_motor
Supporting code to use Thorlabs' original C bindings in python.

### BPC303.BPC303
`BPC303.BPC303(serial_no)`

Piezo controller object. Calling this class automatically searches connected devices on serial ports for a valid 
controller, and creates the object if one is found.
<pre>
Parameters:
    serial_no : str
        Serial number of piezo controller to connect to.
</pre>
<pre>
Returns:
    None
</pre>

### BPC303.BPC303.zero
`BPC303.BPC303.zero()`

Sets piezo controller to the zero position on all channels.
<pre>
Parameters:
    None
</pre>
<pre>
Returns:
    None
</pre>

### BPC303.BPC303.close
`BPC303.BPC303.close()`

Closes connection to the piezo controller.
<pre>
Parameters:
    None
</pre>
<pre>
Returns:
    None
</pre>

### BPC303.BPC303.set_voltage
`BPC303.BPC303.set_voltage(channel, voltage)`

Sets voltage of specified channel on the piezo controller.
<pre>
Parameters:
    channel : int
        Channel value (1, 2, 3).
    voltage : float
        Voltage as a percentage of the maximum value.
</pre>
<pre>
Returns:
    None
</pre>

### BPC303.BPC303.get_voltage
`BPC303.BPC303.get_voltage(channel)`

Gets voltage of specified channel on the piezo controller.
<pre>
Parameters:
    channel : int
        Channel value (1, 2, 3).
</pre>
<pre>
Returns:
    out : float
        Voltage as a percentage of the maximum value.
</pre>

### BPC303.BPC303.get_maxVoltage
`BPC303.BPC303.get_maxVoltage(channel)`

Gets maximum allowed voltage of specified channel on the piezo controller.
<pre>
Parameters:
    channel : int
        Channel value (1, 2, 3).
</pre>
<pre>
Returns:
    out : float
        Maximum allowed voltage of channel.
</pre>

### BPC303.BPC303.set_maxVoltage
`BPC303.BPC303.set_maxVoltage(channel, volts)`

Sets maximum allowed voltage of specified channel on the piezo controller.
<pre>
Parameters:
    channel : int
        Channel value (1, 2, 3).
</pre>
<pre>
Returns:
    None
</pre>

### BPC303.BPC303.convert_pos_to_pc
`BPC303.BPC303.convert_pos_to_pc(pos)`

Converts position of piezo to percentage of maximum value. Inverse function of `convert_pc_to_pos`.
<pre>
Parameters:
    pos : float
        Value of absolute piezo position.
</pre>
<pre>
Returns:
    out : float
        Piezo position as a percentage of the maximum value.
</pre>

### BPC303.BPC303.convert_pc_to_pos
`BPC303.BPC303.convert_pc_to_pos(percentage)`

Converts position of piezo to percentage of maximum value. Inverse function of `convert_pos_to_pc`.
<pre>
Parameters:
    percentage : float
        Piezo position as a percentage of the maximum value.
</pre>
<pre>
Returns:
    out : float
        Value of absolute piezo position.
</pre>

### dither.dither
`dither.dither(piezo, channel, dV, camera, num_iter, exposure_time)`

Main dithering function. Moves the piezo channel either way by `dV * num_iter`.
<pre>
Parameters:
    piezo : BPC303.BPC303
        Piezo object.
    channel : int
        Channel index to dither.
    dV : float
        Voltage increment between dither positions.
    camera : camera.cam
        Camera object.
    num_iter : int
        How many intensity measurements to make either side of the original position.
    exposure_time : float
        Exposure time per measurement.
</pre>
<pre>
Returns:
    V_array : array
        Array of voltage values where intensity measurements taken.
    I_array : array
        Array of intensity values of each measurement.
</pre>

### dither.correctChannel
`dither.correctChannel(piezo, channel, dV, camera, num_iter, exposure_time)`

Uses `dither.dither` to correct the position of the sample based on what voltage value gives the highest intensity 
reading.

<pre>
Parameters:
    piezo : BPC303.BPC303
        Piezo object.
    channel : int
        Channel index to dither.
    dV : float
        Voltage increment between dither positions.
    camera : camera.cam
        Camera object.
    num_iter : int
        How many intensity measurements to make either side of the original position.
    exposure_time : float
        Exposure time per measurement.
</pre>
<pre>
Returns:
    None
</pre>

### dither.threePointDither
`dither.threePointDither(piezo, channel, dV, camera, exposure_time)`

Uses Lagrange interpolation to estimate the position of highest intensity with a quadratic approximation to the 
Gaussian profile. This method only uses three intensity measurements, hence it is much faster but less accurate than
`dither.correctChannel`.

<pre>
Parameters:
    piezo : BPC303.BPC303
        Piezo object.
    channel : int
        Channel index to dither.
    dV : float
        Voltage increment between dither positions.
    camera : camera.cam
        Camera object.
    exposure_time : float
        Exposure time per measurement.
</pre>
<pre>
Returns:
    None
</pre>