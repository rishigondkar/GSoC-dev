#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
#    Copyright (C) 2020 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

# \mainpage RoboComp::trialComponent1
#
# \section intro_sec Introduction
#
# Some information about the component...
#
# \section interface_sec Interface
#
# Descroption of the interface provided...
#
# \section install_sec Installation
#
# \subsection install1_ssec Software depencences
# Software dependences....
#
# \subsection install2_ssec Compile and install
# How to compile/install the component...
#
# \section guide_sec User guide
#
# \subsection config_ssec Configuration file
#
# <p>
# The configuration file...
# </p>
#
# \subsection execution_ssec Execution
#
# Just: "${PATH_TO_BINARY}/trialComponent1 --Ice.Config=${PATH_TO_CONFIG_FILE}"
#
# \subsection running_ssec Once running
#
#
#

import sys, traceback, IceStorm, time, os, copy
from termcolor import colored

# Ctrl+c handling
import signal

from PySide2 import QtCore
from PySide2 import QtWidgets

from specificworker import *


class CommonBehaviorI(RoboCompCommonBehavior.CommonBehavior):
    def __init__(self, _handler):
        self.handler = _handler
    def getFreq(self, current = None):
        self.handler.getFreq()
    def setFreq(self, freq, current = None):
        self.handler.setFreq()
    def timeAwake(self, current = None):
        try:
            return self.handler.timeAwake()
        except:
            print('Problem getting timeAwake')
    def killYourSelf(self, current = None):
        self.handler.killYourSelf()
    def getAttrList(self, current = None):
        try:
            return self.handler.getAttrList()
        except:
            print('Problem getting getAttrList')
            traceback.print_exc()
            status = 1
            return

#SIGNALS handler
def sigint_handler(*args):
    QtCore.QCoreApplication.quit()
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    params = copy.deepcopy(sys.argv)
    if len(params) > 1:
        if not params[1].startswith('--Ice.Config='):
            params[1] = '--Ice.Config=' + params[1]
    elif len(params) == 1:
        params.append('--Ice.Config=etc/config')
    ic = Ice.initialize(params)
    status = 0
    mprx = {}
    parameters = {}
    for i in ic.getProperties():
        parameters[str(i)] = str(ic.getProperties().getProperty(i))

    # Topic Manager
    proxy = ic.getProperties().getProperty("TopicManager.Proxy")
    print(proxy)
    print(type(proxy))
    obj = ic.stringToProxy(proxy)
    try:
        topicManager = IceStorm.TopicManagerPrx.checkedCast(obj)
    except Ice.ConnectionRefusedException as e:
        print(colored('Cannot connect to rcnode! This must be running to use pub/sub.', 'red'))
        exit(1)

    # Remote object connection for AGMExecutive
    try:
        proxyString = ic.getProperties().getProperty('AGMExecutiveProxy')
        try:
            basePrx = ic.stringToProxy(proxyString)
            print(basePrx)
            print(type(basePrx))
            agmexecutive_proxy = AGMExecutivePrx.uncheckedCast(basePrx)
            mprx["AGMExecutiveProxy"] = agmexecutive_proxy
            print(type(agmexecutive_proxy))
            print(type(mprx["AGMExecutiveProxy"]))
        except Ice.Exception:
            print('Cannot connect to the remote object (AGMExecutive)', proxyString)
            #traceback.print_exc()
            status = 1
    except Ice.Exception as e:
        print(e)
        print('Cannot get AGMExecutiveProxy property.')
        status = 1


    # Remote object connection for InnerModelManager
    try:
        proxyString = ic.getProperties().getProperty('InnerModelManagerProxy')
        try:
            basePrx = ic.stringToProxy(proxyString)
            innermodelmanager_proxy = InnerModelManagerPrx.uncheckedCast(basePrx)
            mprx["InnerModelManagerProxy"] = innermodelmanager_proxy
        except Ice.Exception:
            print('Cannot connect to the remote object (InnerModelManager)', proxyString)
            #traceback.print_exc()
            status = 1
    except Ice.Exception as e:
        print(e)
        print('Cannot get InnerModelManagerProxy property.')
        status = 1


    # Remote object connection for Laser
    try:
        proxyString = ic.getProperties().getProperty('LaserProxy')
        try:
            basePrx = ic.stringToProxy(proxyString)
            laser_proxy = LaserPrx.uncheckedCast(basePrx)
            mprx["LaserProxy"] = laser_proxy
        except Ice.Exception:
            print('Cannot connect to the remote object (Laser)', proxyString)
            #traceback.print_exc()
            status = 1
    except Ice.Exception as e:
        print(e)
        print('Cannot get LaserProxy property.')
        status = 1


    # Remote object connection for OmniRobot
    try:
        proxyString = ic.getProperties().getProperty('OmniRobotProxy')
        try:
            basePrx = ic.stringToProxy(proxyString)
            omnirobot_proxy = OmniRobotPrx.uncheckedCast(basePrx)
            mprx["OmniRobotProxy"] = omnirobot_proxy
        except Ice.Exception:
            print('Cannot connect to the remote object (OmniRobot)', proxyString)
            #traceback.print_exc()
            status = 1
    except Ice.Exception as e:
        print(e)
        print('Cannot get OmniRobotProxy property.')
        status = 1


    # Remote object connection for RGBD
    try:
        proxyString = ic.getProperties().getProperty('RGBDProxy')
        try:
            basePrx = ic.stringToProxy(proxyString)
            rgbd_proxy = RGBDPrx.uncheckedCast(basePrx)
            mprx["RGBDProxy"] = rgbd_proxy
        except Ice.Exception:
            print('Cannot connect to the remote object (RGBD)', proxyString)
            #traceback.print_exc()
            status = 1
    except Ice.Exception as e:
        print(e)
        print('Cannot get RGBDProxy property.')
        status = 1

    if status == 0:
        worker = SpecificWorker(mprx)
        worker.setParams(parameters)
        #print(mprx)
    else:
        print("Error getting required connections, check config file")
        sys.exit(-1)

    adapter = ic.createObjectAdapter('AGMCommonBehavior')
    adapter.add(AGMCommonBehaviorI(worker), ic.stringToIdentity('agmcommonbehavior'))
    adapter.activate()


    AGMExecutiveTopic_adapter = ic.createObjectAdapter("AGMExecutiveTopicTopic")
    agmexecutivetopicI_ = AGMExecutiveTopicI(worker)
    agmexecutivetopic_proxy = AGMExecutiveTopic_adapter.addWithUUID(agmexecutivetopicI_).ice_oneway()

    subscribeDone = False
    while not subscribeDone:
        try:
            agmexecutivetopic_topic = topicManager.retrieve("AGMExecutiveTopic")
            subscribeDone = True
        except Ice.Exception as e:
            print("Error. Topic does not exist (creating)")
            time.sleep(1)
            try:
                agmexecutivetopic_topic = topicManager.create("AGMExecutiveTopic")
                subscribeDone = True
            except:
                print("Error. Topic could not be created. Exiting")
                status = 0
    qos = {}
    agmexecutivetopic_topic.subscribeAndGetPublisher(qos, agmexecutivetopic_proxy)
    AGMExecutiveTopic_adapter.activate()

    signal.signal(signal.SIGINT, sigint_handler)
    app.exec_()

    if ic:
        try:
            ic.destroy()
        except:
            traceback.print_exc()
            status = 1
