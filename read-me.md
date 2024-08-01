# autoAlignSample/
Image collection and analysis code to optimise the position of a Thorlabs BPC303 benchtop piezo controller using image 
feedback from a Teledyne Prime BSI Express sCMOS camera. Python wrapper for Thorlab's Kinesis communication protocol 
for the BPC303 benchtop piezo controller based on [ekarademir's thorlabs_kinesis](https://github.com/ekarademir/thorlabs-kinesis/) bindings. This code is being 
used by the Imperial College London EXSS group for increasing integration time in temperature measurements of plasmonic 
nanostructures.

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
`BPC303.BPC303.get_voltage(channel, voltage)`

Gets voltage of specified channel on the piezo controller.
<pre>
Parameters:
    channel : int
        Channel value (1, 2, 3).

</pre>
<pre>
Returns:
    voltage : float
        Voltage as a percentage of the maximum value.
</pre>