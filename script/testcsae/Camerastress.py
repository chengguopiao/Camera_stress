#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import commands
import re
import subprocess
import os
import string
import time
import sys
import util 
import unittest

A  = util.Adb()
SM = util.SetMode()
TB = util.TouchButton()
#Written by Piao chengguo

# PATH
PATH ='/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml '
# key
PICTURE_SIZE_KEY ='| grep pref_camera_picture_size_key'
#################################

PACKAGE_NAME = 'com.intel.camera22'
ACTIVITY_NAME = PACKAGE_NAME + '/.Camera'

class CameraTest(unittest.TestCase):
    def setUp(self):
        super(CameraTest,self).setUp()
        # Delete all image/video files captured before
        #a.cmd('rm','/sdcard/DCIM/*')
        # Launch social camera
        self._launchCamera()


    def tearDown(self):
        super(CameraTest,self).tearDown()
        self._pressBack(4)




# Test case 18
    def testCapturePerectshotImage200TimesBackCamera(self):
        """
        Summary:testCaptureperfectshotimage200times: Capture perfect shot image 200 times
        Steps:  1.Launch perfectshot capture activity
		        2.Capture perfectshot image 200 times
                3.Exit  activity
        """
    #step 1
        SM.switchcamera('perfectshot')
        d.expect('perfectshot.png')
    #step 2	
        for i in range(200):
            self._checkCapturedPic()
            time.sleep(2)


# Test case 19
    def testCapturePanoramaImage200TimesBackCamera(self):
        """
        Summary:testCapturepanoramaimage200times: Capture panorama image 200 times
        Steps:  1.Launch panorama capture activity
                2.Capture panorama image 200 times
                3.Exit  activity
        """
    #step 1
        SM.switchcamera('panorama')
        d.expect('panorama.png')
    #step 2
        for i in range(200):
            self._PanoramaCapturePic()
            time.sleep(1)



# Test case 20
    def testCaptureSingleImage8M500TimesBackCamera(self):
        """
        capture single image 500 times
        8M pixels, back camera

        """
    #step 1    
        SM.setCameraSetting('single',4,2)
        assert bool(a.cmd('cat',PATH + PICTURE_SIZE_KEY).find('StandardScreen')+1)
    #step 2
        TB.switchBackOrFrontCamera('back')
    #step 3
        for i in range(500):
            self._checkCapturedPic()
            time.sleep(1)
  


# Test case 21
    def testcaseCaptureSmileImage8M500TimesBackCamera(self):
        """
        Capture Smile Image 8M 500 times back camera
        8M pixels, back camera
        """
    #step 1
        SM.setCameraSetting('smile',2,2)
        d.expect('smile.png')
    #step 2
        TB.switchBackOrFrontCamera('back')
    #step 3
        for i in range(500):
            self._checkCapturedPic()
            time.sleep(1)


# Test Case 22
    def testcaseRecord720PVideo500Times(self):

        """
        Record 720P Video 500times
        Video size 720P
        """
    #step 1
        SM.switchcamera('video')
        SM.setCameraSetting('video',3,2)
        d.expect('video.png')
    #step 2	
        for i in range (500):
            TB.takeVideo(5)
            time.sleep(1)	


# Test Case 23
    def testcaseRecord480PVideo500Times(self):
        """
        test case Record 480 Pvideo 500 times
        Video size 480P

        """
    #step 1
        SM.switchcamera('video')
        SM.setCameraSetting('video',3,1)
        d.expect('video.png')
    #step 2	
        for i in range (500):
        	TB.takeVideo(5)
        	time.sleep(1)	
        SM.setCameraSetting('video',3,2)

# Test Case 24
    def testcaseBurstImage8M200Times(self):
        """
        test case Burst Image 200 times
        8M pixels, back camera
        """

    #step 1
        SM.setCameraSetting('burstfast',2,2)
        d.expect('burst.png') 
        assert bool(a.cmd('cat',PATH + PICTURE_SIZE_KEY).find('StandardScreen')+1)
    #step 2	
        TB.switchBackOrFrontCamera('back')
    #step 3
        for i in range(200):
            self._checkCapturedPic()
            time.sleep(1)





    ############################################################################################################
    ############################################################################################################

    def _checkCapturedPic(self):
        beforeNo = A.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        TB.takePicture('single')
        afterNo = A.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo == afterNo: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')

    def _PanoramaCapturePic(self):
        beforeNo = A.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        TB.takePicture('smile')
        afterNo = A.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo == afterNo: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')
    

    def _launchCamera(self):
        d.start_activity(component = ACTIVITY_NAME)
        time.sleep(1)
        assert d(resourceId = 'com.intel.camera22:id/mode_button').wait.exists(timeout = 3000), 'Launch camera failed in 3s'

    def _pressBack(self,touchtimes):
        for i in range(1,touchtimes+1):
            d.press('back')


if __name__ =='__main__':  
    unittest.main()