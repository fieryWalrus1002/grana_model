# To Do list:
- work on the overlap 
- seriously, work on the overlap
- does the camera scaling alter the physics? 
    - do we need to scale the object movement?
    - we are already saving the scale information, so we can use it to calculate the appropriate position updates for body posiiont. Sprites
    seem to be working already.DOes this mean it isn't a problem?
- The drawing of circles for particles is not working
- wrap particle into the other objects types, have one place to store all their data. Dataclasses for each object type? then a dict of those?

# Done:
- okay so what if whne we create the ObjectData class object, it had some function that returned an iterable object that we could just iterate through for instantiation. 
- spawner doesn't actually spawn anything right now. GOtta work on the way it feeds information from object_data to the PSIIStructure class to instanatiate objects.

# Ideas:
Re: verifying object areas, 9-30-21:
    - In our Biochem paper, Table 3 we estimated 285 nm^2 for a C2S2 particle.
    - A quick search leads to the powerpoint that has a scale bar.
    - also the protein structures that Roma send you should be in scale.
    - IN the TIPS paper (Fig. 1) we estimated that in the stacked area (your red circle) PSII occupies ~50%. That is significant less than you have although we we assumed a similar density of ~1600 per um^-2. Although at that time we used C2S2 only and you use a mix I would assume that the extra sizes of the larger PSII (C2S2M2 and C2S2M) is somehow compensated for by your smaller particles (C2S, C2) that the total area occupation shouldn’t be to different.


