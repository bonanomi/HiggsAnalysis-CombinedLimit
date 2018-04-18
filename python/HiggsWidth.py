from HiggsAnalysis.CombinedLimit.PhysicsModel import *

 
### This is the base python class to study the Higgs width
 
class Higgswidth(PhysicsModel):
    def __init__(self):
        self.mHRange = []
        self.GGsmfixed = False
        self.is2l2nu = False
        self.poiMap = []
        self.pois = {}
        self.verbose = False
        self.xsec= 1.0 
        self.xsec_vbf= 1.0 
        self.m= 200. 
        self.w= 10. 
    def setModelBuilder(self, modelBuilder):
        PhysicsModel.setModelBuilder(self,modelBuilder)
        self.modelBuilder.doModelBOnly = False
 
    def getYieldScale(self,bin,process):
        if process == "ggH_sonl": return "ggH_s_func"
        elif process == "ggH_bonl": return "ggH_b_func"
        elif process == "ggH_sand": return "ggH_sbi_func"
        if process == "qqH_sonl": return "qqH_s_func"
        elif process == "qqH_bonl": return "qqH_b_func"
        elif process == "qqH_sand": return "qqH_sbi_func"
        #elif process in ["ggH","qqH","ttH","WH","ZH","VH"]: return "CMS_zz4l_mu"
        else:
            return 1
           
    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po == "GGsmfixed":
                print "Will fix CMS_zz4l_GGsm to 1 and float mu"
                self.GGsmfixed = True
            if po == "is2l2nu":
                print "Will consider cards in 2l2nu style (separated S, B, S+B+I)"
                self.is2l2nu = True
            if po == "muAsPOI":
                print "Will combine all ZZ cards"
                self.isCombine = True
            if po.startswith("m="): 
                self.m = float(po.replace("m=",""))
                print "mass = ",self.m
            if po.startswith("w="): 
                self.w = float(po.replace("w=",""))
                print "width = ",self.w
           
    def setXsec(self):
#        marr = [200 , 300 ,400 ,500 ,600 ,700 ,800 ,900 ,1000 ,1500 ,2000 ,2500 ,3000];
        marr = [300 ,400 ,500 ,600 ,700 ,800 ,900 ,1000 ,1500 ,2000 ,2500 ,3000];

	## GGF Cross-Section
        XSec100 = [0.00960252, 0.0176147, 0.0172144, 0.0121598, 0.00997052, 0.00723416, 0.00698813, 0.0054009, 0.00193455, 0.000556375, 0.000189043, 6.72087e-05]
        XSec010 = [0.0659359, 0.208345, 0.206409, 0.139248, 0.108503, 0.0774346, 0.0731695, 0.0557424, 0.0196021, 0.00540282, 0.00177042, 6.72087e-05]
        XSec001 = [0.127286, 0.422868, 0.418509, 0.281284, 0.217461, 0.155051, 0.14615, 0.112064, 0.039561, 0.00540282, 0.00177042, 6.72087e-05]
        #XSec010 = [0.0659359, 0.208345, 0.206409, 0.139248, 0.108503, 0.0774346, 0.0731695, 0.0557424, 0.0196021, 0.00540282, 0.00177042, 0.000599182]
        #XSec001 = [0.127286, 0.422868, 0.418509, 0.281284, 0.217461, 0.155051, 0.14615, 0.112064, 0.039561, 0.0107575, 0.00351486, 0.00119645]

	## VBF Cross-Section
        XSec100_vbf = [0.00287243, 0.0036309, 0.00362422, 0.00521962, 0.00604965, 0.00507774, 0.00587514, 0.00699234, 0.00608269, 0.00205446, 0.00311864, 0.00168995]
        XSec010_vbf = [0.0217257, 0.0328555, 0.0352548, 0.0532355, 0.0621021, 0.0537883, 0.0612105, 0.0757539, 0.0641665, 0.0208263, 0.0319856, 0.00168995]
        XSec001_vbf = [0.0426389, 0.0653835, 0.0701999, 0.106933, 0.123089, 0.13, 0.120946, 0.15687, 0.129265, 0.0208263, 0.0319856, 0.001689995]
        #XSec010_vbf = [0.0217257, 0.0328555, 0.0352548, 0.0532355, 0.0621021, 0.0537883, 0.0612105, 0.0757539, 0.0641665, 0.0208263, 0.0319856, 0.0169707]
        #XSec001_vbf = [0.0426389, 0.0653835, 0.0701999, 0.106933, 0.123089, 0.13, 0.120946, 0.15687, 0.129265, 0.0416394, 0.0638276, 0.0335741]

        for index in range(len(marr)):
		if self.m == marr[index]:
	  		if self.w == 100:
	  			self.xsec = XSec100[index]
	  			self.xsec_vbf = XSec100_vbf[index]
	  		elif self.w == 10:
	  			self.xsec = XSec010[index]
	  			self.xsec_vbf = XSec010_vbf[index]
	  		elif self.w == 0.1:
	  			self.xsec = XSec001[index]
	  			self.xsec_vbf = XSec001_vbf[index]
			else:
				raise RuntimeError, "Don't know this mass, width %f, %f" %(self.m, self.w)
	print "xsec: ", self.xsec, self.xsec_vbf

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        if self.modelBuilder.out.var("r"):
            print "have r inside"
        else:
            self.modelBuilder.doVar("r[1,0,10000]")
        if self.modelBuilder.out.var("fvbf"):
            print "have fvbf inside"
        else:
            self.modelBuilder.doVar("fvbf[0,0,1]")
        if self.is2l2nu:
            #self.modelBuilder.doVar("CMS_zz4l_GGsm[1.,0.,50.]")
            #self.modelBuilder.doVar("CMS_zz4l_mu[1.,0.,1000.]")
            #self.modelBuilder.doVar("CMS_widthH_kbkg[1.,0.,2.]")
            self.setXsec()
            self.modelBuilder.factory_( "expr::CMS_zz2l2nu_mu(\"@0*(1-@1)*0.0673*0.2*2/1000./%f\", r,fvbf)" %(self.xsec))
            self.modelBuilder.factory_( "expr::CMS_zz2l2nu_mu_vbf(\"@0*@1*0.0673*0.2*2/1000./%f\", r,fvbf)" %(self.xsec_vbf))
            poi = "r"            
       

        self.modelBuilder.factory_( "expr::ggH_s_func(\"@0-sqrt(@0)\", CMS_zz2l2nu_mu)")
        self.modelBuilder.factory_(  "expr::ggH_b_func(\"1-sqrt(@0)\", CMS_zz2l2nu_mu)")
        self.modelBuilder.factory_(  "expr::ggH_sbi_func(\"sqrt(@0)\", CMS_zz2l2nu_mu)")

        self.modelBuilder.factory_( "expr::qqH_s_func(\"@0-sqrt(@0)\", CMS_zz2l2nu_mu_vbf)")
        self.modelBuilder.factory_(  "expr::qqH_b_func(\"1-sqrt(@0)\", CMS_zz2l2nu_mu_vbf)")
        self.modelBuilder.factory_(  "expr::qqH_sbi_func(\"sqrt(@0)\", CMS_zz2l2nu_mu_vbf)")


	self.modelBuilder.doSet("POI",poi)


       
higgswidth = Higgswidth()
 
