objectMap = {}

#add object to list
def addTo(object_class, object):
    if objectMap.get(object_class) == None:
        objectMap[object_class] = []
    objectMap[object_class].append(object)

#remove object from list
def removeFrom(object_class, object):
    if objectMap.get(object_class) == None:
        objectMap[object_class] = []
    else:
        objectMap[object_class].remove(object)

#find object from list
def find(object_class, objectId):
    if objectMap.get(object_class) == None:
        objectMap[object_class] = []
        return
    else:
    	  for object in objectMap[object_class]:
    	  	  if objectId == object.getId():
    	  		    return object

# Clear the ID Map
def clear(object_class):
    if object_class in objectMap:
        del objectMap[object_class]
