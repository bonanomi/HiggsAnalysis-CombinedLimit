from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import fnmatch 

class stagex(PhysicsModel):
    "Allow different signal strength fits for the stage-x model"
    def __init__(self):
	self.POIs = ""
	self.actth=False 
	self.acggh=False 
	self.accor=False 
	self.options= ""
	self.stage0= False 
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
				if self.acggh:
				    if "ALT" in process:
				  	muname= "r_ggH_times_x"
				    else:
				  	muname= "r_ggH_times_notx"
				else:
				 muname= "r_ggH"
		  	elif "VHori" in process :
				muname= "r_VH"
		  	elif "VBFori" in process :
				muname= "r_VBF"
		  	elif process.startswith("VBF") :
				muname= "r_VBF"
			elif process.startswith("WH"): 
			  	muname= "r_VH"
			elif process.startswith("ZH"):
			  	muname= "r_VH"
			elif process.startswith("TTH"):
				if self.actth:
				    if "ALT" in process:
				  	muname= "r_TTH_times_x"
				    else:
				  	muname= "r_TTH_times_notx"
				else:
					muname = "r_TTH"
			elif process.startswith("TH") or process.startswith("tqH"):
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
		elif self.singlemu:
			muname = "r"
		elif self.rvrf:
		  	if ("VH" in process or "VBF" in process):
				muname= "rv"
		  	elif ("ggH" in process or "BBH" in process or "TH" in process):
				muname= "rf"
		else:
			muname = "r_%s"%process
			if process.startswith("BBH"):
			  	muname= "r_ggH_0j_10_200"
			if process.startswith("TH"):
			  	muname= "r_TTH"
			muname = muname.replace("_VHori","") 
			muname = muname.replace("_VBFori","") 
		if self.actth or self.acggh:
			self.modelBuilder.doVar("r_TTH[1,0,10]" )
			self.modelBuilder.doVar("r_ggH[1,0,10]" )
			self.modelBuilder.doVar("x[0,0,1]" )
			self.modelBuilder.factory_("expr::r_TTH_times_x(\"@0*@1/2.56\", r_TTH, x)");
			self.modelBuilder.factory_("expr::r_TTH_times_notx(\"@0*(1-@1)\", r_TTH, x)");
			if self.accor:
				self.modelBuilder.factory_("expr::r_ggH_times_x(\"2.25*@0*@1\", r_TTH, x)");
				self.modelBuilder.factory_("expr::r_ggH_times_notx(\"@0*(1-@1)\", r_TTH, x)");
				self.pois.append("x,r_TTH")
			else:
				self.modelBuilder.factory_("expr::r_ggH_times_x(\"2.25*@0*@1\", r_ggH, x)");
				self.modelBuilder.factory_("expr::r_ggH_times_notx(\"@0*(1-@1)\", r_ggH, x)");
				self.pois.append("x,r_ggH,r_TTH")
		if self.modelBuilder.out.var(muname):
			print "reclying %s" %muname
		else:
			if not "times" in muname:
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
		    if 'doactth' in po: 
			    self.actth= True
	                    print "doing tth AC ttH"
		    if 'doaccor' in po: 
			    self.accor= True
	                    print "doing tth AC ttH"
		    if 'doacggh' in po: 
			    self.acggh= True
	                    print "doing tth AC ggH"
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
