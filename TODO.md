- work on the overlap 
- seriously, work on the overlap
- does the camera scaling alter the physics? 
    - do we need to scale the object movement?
    - we are already saving the scale information, so we can use it to calculate the appropriate position updates for body posiiont. Sprites
    seem to be working already.DOes this mean it isn't a problem?
- The drawing of circles for particles is not working
- wrap particle into the other objects types, have one place to store all their data. Dataclasses for each object type? then a dict of those?

Done:
- okay so what if whne we create the ObjectData class object, it had some function that returned an iterable object that we could just iterate through for instantiation. 
- spawner doesn't actually spawn anything right now. GOtta work on the way it feeds information from object_data to the PSIIStructure class to instanatiate objects.