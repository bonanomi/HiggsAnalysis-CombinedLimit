from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import fnmatch 

class stagex(PhysicsModel):
    "Allow different signal strength fits for the stage-x model"
    def __init__(self):
	self.POIs = ""
	self.options= ""
	self.stage0= False
	self.SingleVH= False 
	self.stxs0= False
	self.rvrf= False 
	self.singlemu= False 
	self.splitHad= False 
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
		  	elif "WHori" in process :
				muname= "r_WH"
				if self.SingleVH:
					muname= "r_VH"
			elif "ZHori" in process :
				muname = "r_ZH"
				if self.SingleVH:
					muname = "r_VH"
		  	elif "VBFori" in process :
				muname= "r_VBF"
		  	elif process.startswith("VBF") :
				muname= "r_VBF"
			elif process.startswith("WH"): 
			  	muname= "r_WH"
				if self.SingleVH:
					muname = "r_VH"
			elif process.startswith("ZH"):
			  	muname= "r_ZH"
				if self.SingleVH:
					muname = "r_VH"
			elif process.startswith("TTH"):
			  	muname= "r_TTH"
			elif process.startswith("TH"):
			  	muname= "r_TTH"
			elif process.startswith("BBH"):
			  	muname= "r_ggH"
			elif process.startswith("VH"):
			  	muname= "r_VH"
			if self.splitHad:	
				if ("VHori" in process):
				 	muname= "r_VH_Had"
			        elif (process.startswith("VH") and (not "VBFori" in process)):
			  	        muname= "r_VH_Had"
				if "Lep" in process:
				 	muname= "r_VH_Lep"

		elif self.stxs0 :
			if process.startswith("ggH"):
				muname= "r_ggH"
		  	elif "WHori" in process :
				muname= "r_qqH"
			elif "ZHori" in process :
				muname= "r_qqH"
		  	elif "VBFori" in process :
				muname= "r_qqH"
		  	elif process.startswith("VBF") :
				muname= "r_qqH"
			elif "Had" in process: 
				muname= "r_qqH"
			elif "Lep" in process: 
				muname= "r_VH_Lep"
			elif process.startswith("TTH"):
			  	muname= "r_TTH"
			elif process.startswith("TH"):
			  	muname= "r_TTH"
			elif process.startswith("BBH"):
			  	muname= "r_ggH"
			elif process.startswith("VH"):
			  	muname= "r_qqH"

		elif self.singlemu:
			muname = "r"
		elif self.rvrf:
		  	if ("ZH" in process or "WH" in process or "VBF" in process):
				muname= "rv"
		  	elif ("ggH" in process or "BBH" in process or "TH" in process):
				muname= "rf"
		else:
			muname = "r_%s"%process
			if process.startswith("BBH"):
			  	muname= "r_ggH_0j_10_200"
			if process.startswith("TH"):
			  	muname= "r_TTH"
			muname = muname.replace("WH_Had", "VH_Had")
			muname = muname.replace("ZH_Had", "VH_Had")
			muname = muname.replace("ZH_Lep", "VH_Lep")
			muname = muname.replace("WH_Lep", "VH_Lep")	
			muname = muname.replace("_WHori","") 
			muname = muname.replace("_ZHori", "")
			muname = muname.replace("_VBFori","") 
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
		    if 'stxs0' in po: 
			    self.stxs0= True
	                    print "doing STXS stage0"	                    
		    if 'SingleVH' in po:
			    self.SingleVH= True
			    print "merging WH, ZH in VH"
		    if 'singlemu' in po: 
			    self.singlemu= True
	                    print "doing single mu"
		    if 'rvrf' in po: 
			    self.rvrf= True
	                    print "doing rvrf"
		    if 'splitHad' in po: 
			    self.splitHad= True
	                    print "Splitting had and lep VH"

    def doParametersOfInterest(self):
	    self.POIs=",".join(self.pois)
	    print "Default parameters of interest: ", self.POIs
	    self.modelBuilder.doSet("POI",self.POIs)

stagex = stagex()