# The intention of this script is to manipulate a layer so features represent single food source types.
# Where multiple types are found, the feature will be duplicated to divide the types between features.
#NOTE: source and destination layer begin as identical shapefiles with ALL Falling Fruit Locations for Melbourne
#NOTE: source layer is where we will detect and collect features with multiple plant varieties AND
# make duplicates which represent single plant types.
#NOTE: Destination layer have these features copied into it, and multi-variety features deleted

# Assign variable to layers
sourceLYR = QgsProject.instance().mapLayersByName('Merged_locations_no_duplicates')[0]

#destination layer is where we will add duplicate features
#added features will only have one plant type
destLYR = QgsProject.instance().mapLayersByName('Merged_No_Duplicates')[0]

#create variable for the index of 'types' attribute
idx = sourceLYR.fields().indexOf('types')

#create list to store features duplicate features
features = []

#start editing layer
sourceLYR.startEditing()

#collect all features in layer,
#run 'for' loop for each feature
for feature in sourceLYR.getFeatures():

#assign variable to string attribute in field 'types'
    attribute = feature.attributes()[idx]

#remove curly brackets
    a = attribute.replace('{', '')
    b = a.replace('}', '')

#split varieties based on comma
#'.split' divides string at each comma and puts each resulting string as an entry to a list
    foo = b.split(',')

#'if' loop detects if feature meets specification
#in this case, if the list of plant types has more than one entry do following commands
#following commands only apply to features which have more than one plant variety
    if len(foo) > 1:

#using a 'for' loop loops through every entry in lists with more than one variety

        for n in foo:
#set the feature's 'types' attribute to the given list entry
            feature.setAttribute(idx, n)
#add feature to list collection to be added to back to destination layer
            features.append(feature)
# 'for' loop then repeats for following list entry, adding a new feature to duplicate collection
# Once no more entries are found, script return to first 'for' loop, looping through layer features

#once all features have been looped through, and necessary duplicate features collected in a list
#seet variable to provide data to destination layer
data_provider = destLYR.dataProvider()
#add features in collection to destination layer
data_provider.addFeatures(features)

#now that we have added duplicate features we need to delete original features with mltiple varieties
#start editing the destination layer
destLYR.startEditing()

# run a 'for' loop.
#this will loop through each feature in the destination layer
for f in destLYR.getFeatures():

#assign variable to index of 'types' field
    attr = f.attributes()[idx]

#run an 'if' command
#if script finds a comma in the 'types' string it will return its location in string
#if it doesn't find a comma it will return '-1'
#therefore, if location index is above -1, string meets criteria for if command
    if attr.find(',') > -1:

#Delete feature which meets 'if' command criteria
        destLYR.dataProvider().deleteFeatures([f.id()])


#commit changes to destination layer.
destLYR.commitChanges()
