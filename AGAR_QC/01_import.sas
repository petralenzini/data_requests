%include "Z://mharms/Projects/HCP-DA/QC/AGAR/SAS/00_includes.sas";

/* Prior to saving the csv file from IntraDB, add Scanner and Subject Label to the list of variables */

/* N.B. With changes made to 'importcsv' macro, no longer need to worry about moving rows with
    long strings up to the front to avoid truncation. */
/* Load AGAR QC data */
**%let csvfile="Z://mharms/Projects/HCP-DA/QC/AGAR/CSVs/AGAR_QC_2019.06.14.csv";
%let csvfile="Z://mharms/Projects/HCP-DA/QC/AGAR/CSVs/AGAR_QC_2020.11.13.csv";
%_importcsv (_sasfile=work.AGARQC,_csvfile=&csvfile);
data AGARQC;
    set AGARQC(drop=Subject rename=(Scanner=Station));  ** Default 'Subject' variable is in form of IntraDB UID;
    **where MR_date >= '06aug2012'd;
    rename MR_date = Date
        stat_snr = SNR
        stat_mean = mean
        stat_stddev = std
        AGAR_SFNR = tSNR
		Subject_Label = Subject
        ;
	if Station = 'MRC35177' then Scanner = 'Bay3';
    else if Station = 'AWP166038' then Scanner = 'Bay2';

	** Derive variables from MR_ID;
	SubjPerMRID = cats(scan(MR_ID,1,'_'),'_',scan(MR_ID,2,'_'));
	Coil = scan(MR_ID,3,'_');  ** Have to trust that Coil portion of MR_ID was entered correctly;
	ScannerPerMRID = substr(Coil,5);
	Coil = substr(Coil,1,4);
run;

** Inconsistent MR_IDs;
data inconsistent;
	set AGARQC;
	where (Scanner ne ScannerPerMRID and ScannerPerMRID ne '') or (Subject ne SubjPerMRID);
	keep MR_ID Date SeriesDesc Station Subject Scanner SubjPerMRID Coil ScannerPerMRID;
run;

/* If Subject and SubjPerMRID don't match, we have no way of knowing whether the "ABCD" or "EB" phantom was used; */
data AGARQC;
	set AGARQC;
	where Subject='AGAR_ABCD07' and SubjPerMRID='AGAR_ABCD07';
run;

proc sort data=AGARQC; by Date Coil Scanner ScanId; run;

data AGARQCAll;
    set AGARQC;
run;

/* To use a more recent, limited time series */
/*
data AGARQC;
    set AGARQCAll;
    where Date >= '01may2014'd;
run;
*/
