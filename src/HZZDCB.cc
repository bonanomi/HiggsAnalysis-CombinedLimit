#include <iostream>
#include <math.h>
#include "TMath.h"

#include "../interface/HZZDCB.h"
#include "RooRealVar.h"
#include "RooRealConstant.h"

using namespace RooFit;
using namespace std; 


 RooDoubleCB_spec::RooDoubleCB_spec(){}

 RooDoubleCB_spec::RooDoubleCB_spec(const char *name, const char *title, 
		    //RooAbsReal& _x,
		    RooAbsReal& _xreco,
		    RooAbsReal& _xgen,
		    RooAbsReal& _mean,
		    RooAbsReal& _width,
		    RooAbsReal& _alpha1,
		    RooAbsReal& _n1,
		    RooAbsReal& _alpha2,
		    RooAbsReal& _n2
		    ) :
   RooAbsPdf(name,title), 
//   x("x","x",this,_x),
   xreco("xreco","xreco",this,_xreco),
   xgen("xgen","xgen",this,_xgen),
   mean("mean","mean",this,_mean),
   width("width","width",this,_width),
   alpha1("alpha1","alpha1",this,_alpha1),
   n1("n1","n1",this,_n1),
   alpha2("alpha2","alpha2",this,_alpha2),
   n2("n2","n2",this,_n2)
 { 
 } 


 RooDoubleCB_spec::RooDoubleCB_spec(const RooDoubleCB_spec& other, const char* name) :  
   RooAbsPdf(other,name), 
   //x("x",this,other.x),
   xreco("xreco",this,other.xreco),
   xgen("xgen",this,other.xgen),
   mean("mean",this,other.mean),
   width("width",this,other.width),
   alpha1("alpha1",this,other.alpha1),
   n1("n1",this,other.n1),
   alpha2("alpha2",this,other.alpha2),
   n2("n2",this,other.n2)

 { 
 } 

 double RooDoubleCB_spec::evaluate() const 
 { 
	 double x= xreco-xgen;
   double t = (x-mean)/width;
   if(t>-alpha1 && t<alpha2){
     return exp(-0.5*t*t);
   }else if(t<-alpha1){
     double A1 = pow(n1/fabs(alpha1),n1)*exp(-alpha1*alpha1/2);
     double B1 = n1/fabs(alpha1)-fabs(alpha1);
     return A1*pow(B1-t,-n1);
   }else if(t>alpha2){
     double A2 = pow(n2/fabs(alpha2),n2)*exp(-alpha2*alpha2/2);
     double B2 = n2/fabs(alpha2)-fabs(alpha2);
     return A2*pow(B2+t,-n2);
   }else{
     cout << "ERROR evaluating range..." << endl;
     return 99;
   }
   
 } 

 Int_t RooDoubleCB_spec::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* range) const 
 {
//   if (matchArgs(allVars,analVars,x)) return 1;
   if (matchArgs(allVars,analVars,xreco)) return 1;
   if (matchArgs(allVars,analVars,xgen)) return 2;
   return 0;
 }

 Double_t RooDoubleCB_spec::analyticalIntegral(Int_t code, const char* rangeName) const 
 {
 //  assert(code==1) ;
 
   double central=0;
   double left=0;
   double right=0;
 
   static const Double_t root2 = sqrt(2) ;
   static const Double_t rootPiBy2 = sqrt(atan2(0.0,-1.0)/2.0);
   Double_t xscale = root2*width;
 
   //compute gaussian contribution
	 //xiao
   //double central_low =max(x.min(rangeName),mean - alpha1*width );
   //double central_high=min(x.max(rangeName),mean + alpha2*width );
	 
   //double central_low =max(xreco.min(rangeName)-xgen,mean - alpha1*width );
   //double central_high=min(xreco.max(rangeName)-xgen,mean + alpha2*width );
   //double left_low=xreco.min(rangeName)-xgen;
   //double left_high=min(xreco.max(rangeName)-xgen,mean - alpha1*width);
   //double right_low=max(xreco.min(rangeName)-xgen,mean + alpha2*width);
   //double right_high=xreco.max(rangeName)-xgen;

   double central_low =mean - alpha1*width ;
   double central_high=mean + alpha2*width ;

   double left_low= min(-xgen*0.1,xreco.min(rangeName)-xgen);
   double left_high=mean - alpha1*width;

   double right_low=mean + alpha2*width;
   double right_high=max(xgen*0.1,xreco.max(rangeName)-xgen);

//	 cout << xgen<<endl;
//	 cout << central_low << " "<<max(xreco.min(rangeName)-xgen,mean - alpha1*width )<<endl;
//	 cout << central_high<< " "<<min(xreco.max(rangeName)-xgen,mean + alpha2*width )<<endl;
//	 cout << left_low<<" "<< xreco.min(rangeName)-xgen<<endl;
//	 cout << left_high<<" "<< min(xreco.max(rangeName)-xgen,mean - alpha1*width)<<endl;
//	 cout << right_low<<" "<<max(xreco.min(rangeName)-xgen,mean + alpha2*width)<<endl; 
//	 cout <<right_high<<" "<<xreco.max(rangeName)-xgen<<endl;

	if(code==2){
   central_low =max(xreco-xgen.max(rangeName),mean - alpha1*width );
   central_high=min(xreco-xgen.min(rangeName),mean + alpha2*width );
   left_low=xreco-xgen.max(rangeName);
   left_high=min(xreco-xgen.min(rangeName),mean - alpha1*width);
   right_low=max(xreco-xgen.max(rangeName),mean + alpha2*width);
   right_high=xreco-xgen.min(rangeName);
	}

   if(central_low < central_high) // is the gaussian part in range?
     central = rootPiBy2*width*(TMath::Erf((central_high-mean)/xscale)-TMath::Erf((central_low-mean)/xscale));
 
   //compute left tail;
   double A1 = pow(n1/fabs(alpha1),n1)*exp(-alpha1*alpha1/2);
   double B1 = n1/fabs(alpha1)-fabs(alpha1);
	//xiaom 
   //double left_low=x.min(rangeName);
   //double left_high=min(x.max(rangeName),mean - alpha1*width);

   if(left_low < left_high){ //is the left tail in range?
     if(fabs(n1-1.0)>1.e-5)
       left = A1/(-n1+1.0)*width*(pow(B1-(left_low-mean)/width,-n1+1.)-pow(B1-(left_high-mean)/width,-n1+1.));
     else
       left = A1*width*(log(B1-(left_low-mean)/width) - log(B1-(left_high-mean)/width) );
   }
 
   //compute right tail;
   double A2 = pow(n2/fabs(alpha2),n2)*exp(-alpha2*alpha2/2);
   double B2 = n2/fabs(alpha2)-fabs(alpha2);
 
 //xiaom
   //double right_low=max(x.min(rangeName),mean + alpha2*width);
   //double right_high=x.max(rangeName);
   if(right_low < right_high){ //is the right tail in range?
     if(fabs(n2-1.0)>1.e-5)
       right = A2/(-n2+1.0)*width*(pow(B2+(right_high-mean)/width,-n2+1.)-pow(B2+(right_low-mean)/width,-n2+1.));
     else
       right = A2*width*(log(B2+(right_high-mean)/width) - log(B2+(right_low-mean)/width) );
   }
     
   return left+central+right;
 
 }

