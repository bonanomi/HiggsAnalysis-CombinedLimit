/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
  * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

//#ifndef HZZ4L_ROOHIGHMASS
//#define HZZ4L_ROOHIGHMASS

#include "RooAbsPdf.h"
#include "RooSetProxy.h"
#include "RooRealProxy.h"
#include "RooRealVar.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
#include "TH3F.h"
#include "TH1.h"
#include "RooDataHist.h"
#include "RooHistFunc.h"
using namespace RooFit;

class HZZ4L_RooHighmass : public RooAbsPdf {
protected:

 RooRealProxy mass;
// mutable RooArgSet* _normSet ; 
  RooRealProxy dbkg;
  RooRealProxy coupl;
  RooListProxy _coefList ;  //  List of funcficients
  TIterator* _coefIter ;    //! Iterator over funcficient lis
//  RooSetProxy _normSet ;  //  List of funcficients
//  TIterator* _normIter ;    //! Iterator over funcficient lis
  Double_t evaluate() const ;
public:
  HZZ4L_RooHighmass() {} ; 
  HZZ4L_RooHighmass(const char *name, const char *title,
//		       RooArgSet* _normSet,
		       RooAbsReal& _mass,
		       RooAbsReal& _dbkg,
		       RooAbsReal& _coupl,
//			const RooArgSet& innormSet,
			const RooArgList& inCoefList);
		    
  HZZ4L_RooHighmass(const HZZ4L_RooHighmass& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new HZZ4L_RooHighmass(*this,newname); }
  inline virtual ~HZZ4L_RooHighmass() {}
  
  Int_t getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* rangeName=0) const ;
  Double_t analyticalIntegral(Int_t code, const char* rangeName=0) const ;
	double nsig,nbkg;
//  const RooArgList& coefList() const { return _coefList ; }
//  const RooArgSet& normSet() const { return _normSet; }

private:

  ClassDef(HZZ4L_RooHighmass,1) // Your description goes here...
};
 
//#endif
