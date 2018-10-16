from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import fnmatch 

class stagex(PhysicsModel):
    "Allow different signal strength fits for the stage-x model"
    def __init__(self):
	self.POIs = ""
	self.options= ""
	self.stage0= False 
	self.muNames =[]
	self.pois = []
	self.count=0
    def setModelBuilder(self, modelBuilder):
	PhysicsModel.setModelBuilder(self, modelBuilder)
	self.modelBuilder.doModelBOnly = False
    def getYieldScale(self,bin,process):
	    if not self.DC.isSignal[process]: 
		    return 1
	    else:
		muname=""
		if self.stage0 :
			if process.startswith("ggH"):
				muname= "r_ggH"
		  	if process.startswith("VBF"):
				muname= "r_VBF"
			if process.startswith("VH"):
			  	muname= "r_VH"
			if process.startswith("TTH"):
			  	muname= "r_TTH"
		else:
			muname = "r_%s"%process
		if self.modelBuilder.out.var(muname):
			print "reclying %s" %muname
		else:
			self.modelBuilder.doVar("%s[1,0,10]" % muname)
			print "scale process %s with %s" %(process,muname)
			self.pois.append(muname)
			self.POIs=",".join(self.pois)
			self.modelBuilder.doSet("POI",self.POIs)
			print "Default parameters of interest: ", self.POIs
		return muname 
    def setPhysicsOptions(self,physOptions):
	    for po in physOptions:
		    if 'doStage0' in po: 
			    self.stage0= True
	                    print "doing stage0"
    def doParametersOfInterest(self):
	    self.POIs=",".join(self.pois)
	    print "Default parameters of interest: ", self.POIs
	    self.modelBuilder.doSet("POI",self.POIs)

stagex = stagex()
