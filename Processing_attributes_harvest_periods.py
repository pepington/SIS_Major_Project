#Processing attributes: Harvest Periods
# The intention of this script is to assign a harvest period to each feature
#Where a year overlap exists, feture will be duplicated such that:
#feature #1 has the period between the harvest-start and year-end
#feature #2 has the period between the year-start and harvest-end
#NOTE: processing of attributes occurs within source layer

#Set a variable to the source layer (the merged feature layer with joined harvest information)
sourceLYR = QgsProject.instance().mapLayersByName('cleaned_backup2')[0]

#Start editing the layer
sourceLYR.startEditing()

#Create 2 pairs of date fields to layer
#Sea_sta, Sea_end will be the fields used by ArcGIS Online
#Sea_sta2, Sea_end2 will be used if overlap exists to store year start - harvest end dates
sourceLYR.dataProvider().addAttributes([QgsField("Sea_sta" , QVariant.Date)])
sourceLYR.dataProvider().addAttributes([QgsField("Sea_end" , QVariant.Date)])
sourceLYR.dataProvider().addAttributes([QgsField("Sea_sta2" , QVariant.Date)])
sourceLYR.dataProvider().addAttributes([QgsField("Sea_end2" , QVariant.Date)])
sourceLYR.updateFields()

#Create dictionary to translate month to a number
month_dict = {"JAN" : "01",
                "FEB" : "02",
                "MAR" : "03",
                "APR" : "04",
                "MAY" : "05",
                "JUN" : "06",
                "JUL" : "07",
                "AUG" : "08",
                "SEP" : "09",
                "OCT" : "10",
                "NOV" : "11",
                "DEC" : "12"}

#set variables for the indexes of each created field
#The next four are the fields created at beginning of script
idx_start = sourceLYR.fields().indexOf('Seas_sta')
idx_end = sourceLYR.fields().indexOf('Seas_end')
idx_start2 = sourceLYR.fields().indexOf('Sea_sta2')
idx_end2 = sourceLYR.fields().indexOf('Sea_end2')

#The next two indexes are for the joined fields
#These fields crrently have the harvest starts and ends as month strings E.G JAN, FEB etc.
idx1 = sourceLYR.fields().indexOf('Harvest_st')
idx2 = sourceLYR.fields().indexOf('Harvest_en')

#Create a list to store annual overlap features
features = []

#'for' loop, looping through each feature in the source layer
# commands after this occur to individual features until end of loop
# then returns to line 56 and moves to the next feature
# After all features run through loop, continues to next command outside the loop
for feature in sourceLYR.getFeatures():

#assign variable to attribute at idx1 (see line 46)
    attributestart = feature.attributes()[idx1]

#assign variable to attribute at idx2 (see line 47)
    attributeend = feature.attributes()[idx2]

#run start month attribute through data dictionary
#i.e. if "JUN" is the attribute for 'attributestart' data dictionary will return "06"
    attrstartnum = month_dict[attributestart]

#run end month attribute through data dictionary
    attrendnum = month_dict[attributeend]

#if the start month number returned from data dictionary is higher than end month, this means an annual overlap has occured
#E.G. plant has harvest period from NOV to FEB (11th month to 2nd month); start month is higher than end month
#If feature meets 'if' statement specification the following commands occur to feature
    if attrstartnum > attrendnum :

#Set variable for the feature's year start - harvest end, start date
        startdate1 = "2020-01-01"
#Set variable for the feature's year start - harvest end, end date
        enddate1 =  "2020-"+ attrendnum + "-29"

#Set variable for the feature's harvest start - year end, start date
        startdate2 = "2020-"+ attrstartnum + "-29"
#Set variable for the feature's harvest start - year end, end date
        enddate2 = "2020-12-29"

#Set the attribute for each of the new fields to the respective variables above
#Currently, the year start - harvest end attributes are in the fields we will use for ArcGIS Online
#Duplicated features will have harvest start - year end dates assigned to these field
        feature.setAttribute(idx_start, startdate1)
        feature.setAttribute(idx_end, enddate1)
        feature.setAttribute(idx_start2, startdate2)
        feature.setAttribute(idx_end2, enddate2)


#Add features to list to be duplicated
        features.append(feature)

#For features which have lower month start number and higher end month number
#(no overlap) assign start date to the first day of start month
# and end date as the last day in the month
    else:

#set variable for start date and end date
        startdate = "2020-"+ attrstartnum + "-01"
        enddate = "2020-" + attrendnum + "-30"

#set 'startdate' field to above start variable
        feature.setAttribute(idx_start, startdate)
#set 'enddate' field to above end variable
        feature.setAttribute(idx_end, enddate)

#update features to expect new fields
    sourceLYR.updateFeature(feature)

#loop ends and returns to run next feature through commands

#'for' loop: for each feature in list
#remember features in list are those with year overlap
# following commands occur to each feature
    for f in features:

#for duplicated features, set start date to harvest start date
        f.setAttribute(idx_start, startdate2)

#for duplicated features, set end date to year end date
        f.setAttribute(idx_end, enddate2)

#Add duplicated features to layer
    data_provider = sourceLYR.dataProvider()
    data_provider.addFeatures(features)

#finish editing
sourceLYR.commitChanges()

#All features now have harvest attributes for seas_sta and seas_end fields
#which will be called upon by ArcGIS Online
#Those with harvest seasons overlapping, have been duplicated
#The original feature has year start/harvest end dates in seas_sta/seas_end fields
#Duplicated features have harvest start/year end dates in seas_sta/seas_end fields
