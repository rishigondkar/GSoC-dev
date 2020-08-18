#!/usr/bin/python3
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

from genericworker import *
from datetime import date, datetime
import time
#AGM related imports
import AGMModelConversion
from AGGL import *
import json

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

global_link = " "
userid = 0

class Human():
    def __init__(self,id = None,name = ""):
        self.id = id
        self.name = ""
        self.age = "Age<30"
        self.userType = "Clinician"
        self.PhysicalDep = 0
        self.CognitiveDep = 0
        self.emotionalState = "Neutral"
        self.activity = "Rest"
        self.pose = Pose3D()
        self.photo = ""
        print("TRIAL")

class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map):
        super(SpecificWorker, self).__init__(proxy_map)
        self.timer.timeout.connect(self.compute)
        self.Period = 2000
        self.timer.start(self.Period)
        self.persons = []

        self.AGMinit()
        usr = self.newHumanB()
        #time.sleep(10)
        a = str(userid)
        print("User id = ")
        print(a + str(type(a)))
        #self.deleteLink(a,"1")
        #self.updatingDSR()
        #self.updatingDSR()


    def __del__(self):
        print('SpecificWorker destructor')

    def setParams(self, params):
        #try:
        #	self.innermodel = InnerModel(params["InnerModelPath"])
        #except:
        #	traceback.print_exc()
        #	print("Error reading config params")
        return True

    def AGMinit(self):
        self.worldModel = AGMGraph()
        try:
            w = self.agmexecutive_proxy.getModel()
            self.AGMExecutiveTopic_structuralChange(w)
            # get all the list of persons
            self.getPersonList_AGM()
            print("Running")

        except:
            print("The executive is probably not running, waiting for first AGM model publication...")

    def getPersonList_AGM(self):
        src = self.worldModel
        print("Start")
        #print(src.links)
        for link in src.links:
            if link.linkType == 'interactive':
                print(link)
        #for linkSrc in list(src.links.values()):
            #print(linkSrc.linkname)
        #    print("ABC")
        #for nodeSrc in list(src.nodes.values()):
            #print(nodeSrc.sType)
            #if nodeSrc.sType == 'person':
            #   self.ui.id_list.addItem(nodeSrc.name)
            #    self.ui.int1_cb.addItem(nodeSrc.name)
            #    self.ui.int2_cb.addItem(nodeSrc.name)
            #if nodeSrc.sType == 'object':
            #    print(nodeSrc.name)
            #    self.ui.int1_cb.addItem(nodeSrc.name)
            #    self.ui.int2_cb.addItem(nodeSrc.name)
        print("True")



    @QtCore.Slot()
    def compute(self):
        global global_link
        print('SpecificWorker.compute...')
        # computeCODE
        # try:
        #   self.differentialrobot_proxy.setSpeedBase(100, 0)
        # except Ice.Exception as e:
        #   traceback.print_exc()
        #   print(e)

        # The API of python-innermodel is not exactly the same as the C++ version
        # self.innermodel.updateTransformValues('head_rot_tilt_pose', 0, 0, 0, 1.3, 0, 0)
        # z = librobocomp_qmat.QVec(3,0)
        # r = self.innermodel.transform('rgbd', z, 'laser')
        # r.printvector('d')
        # print(r[0], r[1], r[2])

        """with open('/home/rishi/robocomp/components/robocomp-viriato/components/rasaDialogs/case1/sample.json', 'r') as openfile: 
            # Reading from json file 
            json_object = json.load(openfile)


        new_link = json_object["link"]
        print(new_link)
        if new_link == global_link:
            return True
        else:
            attrs = {
                'timeStarted': str(datetime.now()),
                     }
            attrs["type"] = new_link
            a = str(userid)
            self.edgeUpdate(a, "1", new_link, attrs)
            global_link = new_link
            return True"""



    #
    # SUBSCRIPTION to edgeUpdated method from AGMExecutiveTopic interface
    #
    def AGMExecutiveTopic_edgeUpdated(self, modification):
        #
        #subscribesToCODE
        #
        pass


    #
    # SUBSCRIPTION to edgesUpdated method from AGMExecutiveTopic interface
    #
    def AGMExecutiveTopic_edgesUpdated(self, modifications):
        #
        #subscribesToCODE
        #
        pass


    #
    # SUBSCRIPTION to selfEdgeAdded method from AGMExecutiveTopic interface
    #
    def AGMExecutiveTopic_selfEdgeAdded(self, nodeid, edgeType, attributes):
        #
        #subscribesToCODE
        #
        pass


    #
    # SUBSCRIPTION to selfEdgeDeleted method from AGMExecutiveTopic interface
    #
    def AGMExecutiveTopic_selfEdgeDeleted(self, nodeid, edgeType):
        #
        #subscribesToCODE
        #
        pass


    #
    # SUBSCRIPTION to structuralChange method from AGMExecutiveTopic interface
    #
    def AGMExecutiveTopic_structuralChange(self, w):
        self.mutex.lock()
        #print("before")
        #print(type(self.worldModel), type(w))
        self.worldModel = AGMModelConversion.fromIceToInternal_model(w)
        #print("after")
        #print(type(self.worldModel), type(w))
        #print(self.worldModel)
        # fromIceToInternal(w, worldModel)
        self.mutex.unlock()


    #
    # SUBSCRIPTION to symbolUpdated method from AGMExecutiveTopic interface
    #
    def AGMExecutiveTopic_symbolUpdated(self, modification):
        #
        #subscribesToCODE
        #
        pass


    #
    # SUBSCRIPTION to symbolsUpdated method from AGMExecutiveTopic interface
    #
    def AGMExecutiveTopic_symbolsUpdated(self, modifications):
        #
        #subscribesToCODE
        #
        pass


    # =============== Methods for Component Implements ==================
    # ===================================================================

    #
    # activateAgent
    #
    def AGMCommonBehavior_activateAgent(self, prs):
        ret = bool()
        print("IT WORKED YAY AGMCommonBehavior_activateAgent")
        #
        # implementCODE
        #
        return ret


    #
    # deactivateAgent
    #
    def AGMCommonBehavior_deactivateAgent(self):
        ret = bool()
        #
        # implementCODE
        #
        return ret


    #
    # getAgentParameters
    #
    def AGMCommonBehavior_getAgentParameters(self):
        ret = ParameterMap()
        print("IT WORKED YAY AGMCommonBehavior_getAgentParameters")
        #
        # implementCODE
        #
        return ret


    #
    # getAgentState
    #
    def AGMCommonBehavior_getAgentState(self):
        ret = StateStruct()
        #
        # implementCODE
        #
        return ret


    #
    # killAgent
    #
    def AGMCommonBehavior_killAgent(self):
        #
        # implementCODE
        #
        pass


    #
    # reloadConfigAgent
    #
    def AGMCommonBehavior_reloadConfigAgent(self):
        ret = bool()
        #
        # implementCODE
        #
        return ret


    #
    # setAgentParameters
    #
    def AGMCommonBehavior_setAgentParameters(self, prs):
        ret = bool()
        #
        # implementCODE
        #
        return ret


    #
    # uptimeAgent
    #
    def AGMCommonBehavior_uptimeAgent(self):
        ret = int()
        #
        # implementCODE
        #
        return ret

    # ===================================================================
    # ===================================================================

    # function to add a person in RCIS
    def includeInRCIS(self, id_val, pose, meshName):
        print("includeInRCIS begins")
        name = "person" + str(id_val)
        mesh = meshType()
        mesh.pose.x = 0
        mesh.pose.y = 0
        mesh.pose.z = 0
        mesh.pose.rx = 1.57079632679
        mesh.pose.ry = 0
        mesh.pose.rz = 3.1415926535
        mesh.scaleX = mesh.scaleY = mesh.scaleZ = 12
        mesh.render = 0
        mesh.meshPath = "/home/robocomp/robocomp/components/robocomp-viriato/files/osgModels/" + meshName
        try:
            self.innermodelmanager_proxy.addTransform(name, "static", "root", pose)
        except:
            print("Can't create fake person name ")
            return False
        try:
            self.innermodelmanager_proxy.addMesh(name + "_mesh", name, mesh)
        except:
            print("Can't create fake person mesh")
            return False

        print("includeInRCIS ends")
        return True


    def includeInAGM(self, Id, pose, mesh):
        print("includeInAGM begins\n")
        print(Id)
        # name = "person"
        imName = "person" + str(Id)
        # personSymbolId = -1
        # idx = 0
        attribute2 = dict()
        attribute2["imName"] = imName
        attribute2["imType"] = "transform"
        attribute2["imGender"] = "male" 

        self.worldModel.addNode(0, 0, Id, "person", attribute2)

        #writing attributes to json
        json_object = json.dumps(attribute2, indent = 4) 
        with open("/home/rishi/robocomp/components/robocomp-viriato/components/trialComponent1/person_attributes.json", "w") as outfile: 
            outfile.write(json_object)

        self.worldModel.addEdge(Id, 3, "in")
        attrs = {
            'type': str("block"),
            'timeStarted': str(datetime.now()),
                 }
        print(Id)
        print(type(Id))
        self.worldModel.addEdge(1, Id, "block", attrs)

        edgeRTAtrs2 = dict()
        edgeRTAtrs2["tx"] = "0"
        edgeRTAtrs2["ty"] = "0"
        edgeRTAtrs2["tz"] = "0"
        edgeRTAtrs2["rx"] = "0"
        edgeRTAtrs2["ry"] = "0"
        edgeRTAtrs2["rz"] = "0"
        self.worldModel.addEdge(100, Id, "RT", edgeRTAtrs2)

        attribute = dict()
        attribute["collidable"] = "false"
        attribute["imName"] = imName + "_Mesh"
        attribute["imType"] = "mesh"
        meshPath = "/home/robocomp/robocomp/components/robocomp-viriato/files/osgModels/" + mesh
        attribute["path"] = str(meshPath)
        attribute["render"] = "NormalRendering"
        attribute["scalex"] = str(12)
        attribute["scaley"] = str(12)
        attribute["scalez"] = str(12)
        self.worldModel.addNode(0, 0, Id + 1, "mesh_person", attribute)
        # self.worldModel.addNode(0, 0, temp_id + 1, "personMesh")

        edgeRTAtrs = dict()
        edgeRTAtrs["tx"] = "0"
        edgeRTAtrs["ty"] = "0"
        edgeRTAtrs["tz"] = "0"
        edgeRTAtrs["rx"] = "1.570796326794"
        edgeRTAtrs["ry"] = "0"
        edgeRTAtrs["rz"] = "3.1415926535"
        # id used in addEdge should be int type
        self.worldModel.addEdge(Id, Id + 1, "RT", edgeRTAtrs)

        #self.newModel = AGMModelConversion.fromInternalToIce(self.worldModel)
        #self.agmexecutive_proxy.structuralChangeProposal(self.newModel, "gui1", "log2")
        self.updatingDSR()
        print("includeInAGM ends\n")
        return Id



    # to create a new Person Node in DSR
    def newHumanB(self):
        global userid
        print("newHuman")
        pose = Pose3D()
        pose.x = 0
        pose.y = 0
        pose.z = 0
        pose.rx = 0
        pose.ry = 0
        pose.rz = 0
        userid = self.getLatestId()
        # t = self.getLatestId()
        # print(type(t),t)
        meshname = "human01.3ds"
        scale = "12"
        rotationz = "3.1415926535"
        if self.includeInRCIS(userid, pose, meshname):
            self.includeInAGM(userid, pose, meshname)
            print(type(str(userid)))
            print(userid)
            print(type(userid))
            #self.addInteractiveLink(userid)
            #self.ui.id_list.addItem(str(userid))
            #self.ui.int1_cb.addItem(str(userid))
            #self.ui.int2_cb.addItem(str(userid))
            #self.ui.id_list.setCurrentIndex(self.ui.id_list.count() - 1)
            self.currentImagePath = ""
            # self.updatePersons()
            temp_human = Human(id=userid)
            self.persons.append(temp_human)
            #self.updateHumanInfo()

        else:
            print("error creating in RCIS")
        return userid

    def getLatestId(self):
        src = self.worldModel
        last_id = 0
        for nodeSrc in list(src.nodes.values()):
            last_id = max(last_id,int(nodeSrc.name))
            # print(nodeSrc.name)
        for link in list(src.links):
            last_id = max(last_id, int(link.a))
            last_id = max(last_id, int(link.b))
        # the latest available id that can be assigned to any node or link
        return last_id + 1
  
    def updateHumanInfo(self):
        print(int(self.ui.id_list.currentText()))
        currID = int(self.ui.id_list.currentText())
        self.load_image("")
        for human in list(self.persons):
            if human.id == currID:
                self.currentImagePath = human.photo
                self.load_image(human.photo)
                break

    def edgeUpdate(self, a, b, linkLabel='',attr=None):
        self.deleteLink(a, b)
        self.addLink(a, b, linkLabel, attr)
        self.updatingDSR()

    def addLink(self,a: str,b: str, linkLabel='',attr=None):
        self.worldModel.addEdge(a,b,'working',attr)


    def deleteLink(self,a: str,b: str):
        print(type(a),type(b))
        numberOfLinksdeleted = self.worldModel.removeEdge(a,b)
        print( str(numberOfLinksdeleted) + " links deleted")


    def updatingDSR(self):
        try:
            newModel = AGMModelConversion.fromInternalToIce(self.worldModel)
            self.agmexecutive_proxy.structuralChangeProposal(newModel, "component_name", "Log_fileName")
            w = self.agmexecutive_proxy.getModel()
            self.worldModel = AGMModelConversion.fromIceToInternal_model(w)
            print("AGM successfully updated")
        except:
            print("Exception moving in AGM")

