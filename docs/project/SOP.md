### Standard Operating Procedure (SOP) for GreenTravel VR System Technical Setup

**1. Hardware Setup**
- 1.1. Check and Power On Hardware
    - Ensure the following hardware components are properly connected and powered on: 
        Garmin TACX Trainer: Check the tyres are making contact with the trainer wheel.
        Ride the bicycle and check the resistance is proper. (Ideally, gear combination should be preset and known)
- 1.2. Varjo XR3 Headset: Connected to the PC and placed in a safe position.
    - Connection : Power x 1 , USB 3.0 x 2, Display Port x 2, Out USB C x 2 (Out A&B in the correct slots) 
    - Open Varjo base. Ensure all base stations and headset are connected and showing up in the top corner of the Varjo Base window
    - Start SteamVR if not running already
    - Wear the headset and check if the tracking is working properly. Enable eye calibration if not active already.
- 1.3. Biopac System: All sensors connected and powered on.
    - Verify that all USB connections are secure and that the devices are recognized by the PC. (Follow Biopac / Aqcknowledge SOP)

**2. Software Initialization**
- Open the dashboard app from **source/dashboard** folder, use this page to know connection status
- 2.1. Node Server Setup
    - Navigate to the directory('source/server') containing the Node.js server script.
    - Run the server using:
```sh
node server.js
```
- Confirm that the server is running and listening on the specified port (as detailed in the GitHub documentation).
- 2.2. Biopac AcqKnowledge Setup
    - Launch AcqKnowledge on the PC.
    - Check that biofeedback sensors are detected and displaying data in real time.
- 2.3. Run Biopac script from the folder 'source/client/biopac'
```sh
python ServerToBiopac.py
```

**3. Unreal Engine 5 Setup**
- 3.1. Launch Unreal Engine
    - Open Unreal Engine 5 and load the GreenTravel VR project.
    - Wait for the project to fully load and ensure there are no errors in the console.
    - Verify that all plugins related to motion data, biofeedback, and the VR environment are enabled.
    - Ensure the VR environment is properly rendered in the Varjo XR3 headset.
- 3.2. Verify VR Environment Functionality
    - Put on the Varjo XR3 headset and check that the visuals are clear and the head tracking is responsive.
    - Use the controls to navigate through the VR environment briefly to ensure smooth performance.

**4. Connection to Bike**
- 4.1. Pedal 2 rotations to get the sensor to start transmitting data.
- 4.2. Run the python script from the 'source/client/bike' folder and make sure that the data is being transmitted
```sh
python BikeDataToServer.py
```

**5. Eye Tracking and Video Recording with Varjo Base**
- 5.1. Eye Tracking
    - Launch the Varjo Base application on the PC.
    - Navigate to Analytics Window > Enable Eyetracking.
    - Perform a calibration check to ensure the system is ready for recording.
- 5.2. Configure Video Recording
    - (Only video recording, not eye tracking) In Varjo Base, hit the video recording button:
    - (With eye tracking) Once step 5.1 is finished, an eye icon appears in the record button in the analytics window. Clicking on it enables both eye-tracking data recording and video capture.

**6. Final Checks**
- 6.1. Network and Data Flow Verification
    - Ensure the Node.js server is running and that data from Biopac and motion sensors is being received without interruption.
    - Check the Dashboard App to verify that all data streams are active.
    - Verify that the Varjo XR3 headset is connected, and all necessary software components are running smoothly.
- 6.2. Prepare for Data Recording
    - Double-check that all software (Node server, Unreal Engine, Varjo Base, and AcqKnowledge) is active and functioning correctly.
    - Ensure there is enough storage space available for the video and eye-tracking data.

**7. Shutting Down the System**
- 7.1. Close Applications Safely
    - Stop data recording in Varjo Base and save all recorded files to the designated folder.
    - Exit Unreal Engine and ensure that no errors are reported during the shutdown process.
    - Terminate the Node.js server by closing the terminal or command prompt.
- 7.2. Power Down Hardware
    - Power off the Varjo XR3 headset, and Biopac system.
    - Disconnect all USB connections if necessary and store the equipment safely.