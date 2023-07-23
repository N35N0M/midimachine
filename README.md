# MIDI machine
Using MIDI- and track metadata to sequence a DMX rig.

## Brief
This is a project to explore the possibilities of both MIDI and DMX. 

The core idea is to use the MIDI clock on the Traktor S2MKIII to sync the DMX (lighting) rig to the music being played on the mixer.

To not keep things simple, the rig consists of: 
- Three lightbars, of 32 pixels each, that form a straight line.
- Two dragon heads, which each has two cheap LED PAR cans, and a smoke machine with LEDs.

Core goals here are:
- The rig MUST stay in sync with the music.
- The rig should ideally require very little intervention from the DJ, while still looking good.
-- To achieve this, we need to have a good set of defaults that can be used, and have just certain songs be heavily programmed for that extra oomph.
--- Since the MIDI clock is not enough, we will use an existing hack of the traktor software to expose track playtime and track name, and utilize this information.

Constraints:
- It is very impractical to test the actual rig (it occupies quite a bit of space, and smoke in the smoke machine is expensive), so we will have to rely on a simulator.
- However, the simulator is not perfect, and we will have to test on the actual rig at some point.

## Credits
The idea to inject a API client into the traktor software stems from https://github.com/ErikMinekus/traktor-api-client , 
there's only slight variations to this due to the info that I need, and that I use a Traktor S2MKIII and not a D2.