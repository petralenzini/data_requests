%include "Z://mharms/Projects/HCP-DA/QC/AGAR/00_includes.sas";

%let QCver=ABCD_QA;
**%let QCver=FBIRN_QA;

%openpdf(_fname="&_sasdir./saspdf_plots_&QCver..pdf");

** Following syntax for setting HMTL output location no longer seems to work with SAS 9.4;
/* ods html path = "Z://mharms/Projects/HCP-DA/QC/AGAR"
	gpath="Z://mharms/Projects/HCP-DA/QC/AGAR/PNGs";
*/

ods graphics on;

data AGARQC;
    set AGARQCAll;
	where SeriesDesc contains "&QCver" and SeriesDesc not contains "flip10";
**   where Date >= '01may2014'd;
run;

/* Check for repeated scans on same date */
proc sort data=AGARQC;
    by SeriesDesc Date Coil Scanner ScanId;
run;
proc sort data=AGARQC out=AGARQCnodup dupout=AGARdup nodupkey;
    by SeriesDesc Date Coil Scanner;
run;


/* N.B. Can user the SERIES / GROUP= option, if you want to put Coil or Scanner into the same cell of the panel.
   (Need to then remove that variable from the PANELBY list
   Put all the sgpanel calls into a macro, so that I can use %if-%then-%else macros
   (Note that as of SAS9.4M5 you can use those construts in "open code"
		https://blogs.sas.com/content/sasdummy/2018/07/05/if-then-else-sas-programs)
*/
%macro runsgpanel;

%if (&QCver eq %str(FBIRN_QA)) %then %do;
    %let isFBIRNQA=1 ;
	%end;
%else %do;
    %let isFBIRNQA=0 ;
	%end;

title1 "AGAR QC: &QCver scan";
proc sgpanel data=AGARQCnodup;
    panelby SeriesDesc Coil Scanner / columns=2 rows=3;
    series x=Date y=tSNR / markers;
    series x=Date y=SNR / markers;
    %if (&isFBIRNQA) %then
        rowaxis max=500 ;;
run;
proc sgpanel data=AGARQCnodup;
    panelby SeriesDesc Coil Scanner / columns=2 rows=3;
    series x=Date y=mean / markers;
run;
proc sgpanel data=AGARQCnodup;
    panelby SeriesDesc Coil Scanner / columns=2 rows=3;
    series x=Date y=std / markers;
run;
proc sgpanel data=AGARQCnodup;
    panelby SeriesDesc Coil Scanner / columns=2 rows=3;
    series x=Date y=percentfluctuation / markers;
run;
proc sgpanel data=AGARQCnodup;
    panelby SeriesDesc Coil Scanner / columns=2 rows=3;
    series x=Date y=drift / markers;
    series x=Date y=driftfit / markers;
run;
proc sgpanel data=AGARQCnodup;
    panelby SeriesDesc Coil Scanner / columns=2 rows=3;
    series x=Date y=rdc / markers;
run;
proc sgpanel data=AGARQCnodup;
    panelby SeriesDesc Coil Scanner / columns=2 rows=3;
    series x=Date y=meanfwhmx / markers;
    series x=Date y=meanfwhmy / markers;
    series x=Date y=meanfwhmz / markers;
run;
proc sgpanel data=AGARQCnodup;
    panelby SeriesDesc Coil Scanner / columns=2 rows=3;
    series x=Date y=meanghost / markers;
    series x=Date y=meanbrightghost / markers;
run;

/* Occasionally, calculation failure of some sort results in extremely large values of BIRN_HUMAN_SFNR.
	List those cases, then exclude from the plot.
	Actually, this appears to be quite frequent for the FBIRN flip77 scans on the 64ch coil.
*/
title2 "birn_human_sfnr > 1e6";
proc print data=AGARQCnodup(where=(birn_human_sfnr > 1e6));
	var Date Coil Scanner SeriesDesc ScanID birn_human_sfnr;
run;

title2;
proc sgpanel data=AGARQCnodup(where=(birn_human_sfnr < 1e6));
    panelby SeriesDesc Coil Scanner / columns=2 rows=3;
    series x=Date y=birn_human_sfnr / markers;
    series x=Date y=birn_human_snr / markers;
    %if (&isFBIRNQA) %then
        rowaxis min=400 ;;
run;
proc sgpanel data=AGARQCnodup;
    panelby SeriesDesc Coil Scanner / columns=2 rows=3;
    series x=Date y=birn_human_mean_masked_fwhmx / markers;
    series x=Date y=birn_human_mean_masked_fwhmy / markers;
    series x=Date y=birn_human_mean_masked_fwhmz / markers;
run;

%mend runsgpanel;

%runsgpanel;

** Can use following to estimate values to use to trigger a QC warning;
/*
proc univariate data=AGARQCnodup nextrobs=10;
    var tSNR SNR std percentfluctuation drift driftfit rdc meanfwhm: meanghost meanbrightghost
        birn_human_sfnr birn_human_snr ;
    histogram;
    by SeriesDesc Coil Scanner;
run;
*/

ods graphics off;
%closepdf;

/*
proc corr data=AGARQCnodup;
    var birn_human_mean_masked_fwhm: ;
    with meanfwhm: ;
    by SeriesDesc Coil Scanner;
run;
proc corr data=AGARQCnodup;
    var tSNR SNR birn_human_sfnr birn_human_snr;
    by SeriesDesc Coil Scanner;
run;
*/


/* NOTES; THINGS TO INVESTIGATE

    See if we can add more precision to the PercentFluctuation output

    Why is RDC for the 32ch coil lower on Bay3 than Bay2, BUT only for the FBIRN scan and not the ABCD scan?
      Note that std and PercentFluctuation are higher on Bay3 than Bay2 for just the 32ch coil as well.
      SUGGESTS A PROBLEM WITH THE 32ch coil of Bay3, BUT why is it only showing up in the FBIRN scan??

    Why are the "BIRN_HUMAN" versions of SFNR and SNR slightly different from each other, just for the
      32ch and 64ch with the ABCD scan, but not the 20ch, and not for any of the coils for the FBIRN scan?
      (perhaps reflects ROI effects?)

    Why is BIRN_HUMAN_SFNR almost always screwy for the 64 ch coil?
      IF I HAD TO GUESS, probably an ROI/MASK related effect, due to the fact that a central (middle) ROI in the
      middle slice of the 64 ch coil frequently includes many voxels that aren't part of the mask.

    Why does there seem to be a bigger difference between the meanfwhm: and birn_human_mean_masked_fwhm:
      values for the FBIRN scan than the ABCD scan (as summarized by this bit of code:

proc sort data=agarqcall;
by SeriesDesc Coil Scanner;
run;

proc means data=agarqcall(where=(SeriesDesc contains "FBIRN_QA" and SeriesDesc not contains "flip10"));
var meanfwhm: birn_human_mean_masked_fwhm: ;
by SeriesDesc Coil Scanner;
run;

proc means data=agarqcall(where=(SeriesDesc contains "ABCD_QA" and SeriesDesc not contains "flip10"));
var meanfwhm: birn_human_mean_masked_fwhm: ;
by SeriesDesc Coil Scanner;
run;


*/
