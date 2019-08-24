//#ifndef HZZ2L2QROOPDFS
//#define HZZ2L2QROOPDFS

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"

class RooDoubleCB_spec : public RooAbsPdf {
public:
  RooDoubleCB_spec();
  RooDoubleCB_spec(const char *name, const char *title,
	      //RooAbsReal& _x,
	      RooAbsReal& _xreco,
	      RooAbsReal& _xgen,
	      RooAbsReal& _mean,
	      RooAbsReal& _width,
	      RooAbsReal& _alpha1,
	      RooAbsReal& _n1,
	      RooAbsReal& _alpha2,
	      RooAbsReal& _n2
	   );
  RooDoubleCB_spec(const RooDoubleCB_spec& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new RooDoubleCB_spec(*this,newname); }
  inline virtual ~RooDoubleCB_spec() { }
  Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
  Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;

protected:

  //RooRealProxy x ;
  RooRealProxy xreco;
  RooRealProxy xgen;
  RooRealProxy mean;
  RooRealProxy width;
  RooRealProxy alpha1;
  RooRealProxy n1;
  RooRealProxy alpha2;
  RooRealProxy n2;
  
  Double_t evaluate() const ;

private:

  ClassDef(RooDoubleCB_spec,1)
};
 
//#endif
