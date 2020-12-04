from pawns.pawn import pawn as basePawn
from direct.actor.Actor import Actor

class PandaPawn(basePawn):
    """
    the pawn known as panda containing everything that only applies to this pawn
    subclass of basePawn
    """
    def __init__(self, id, hmap):
        "initate pawn using the hmap and the id refering to the posion the pawn is at"
        basePawn.__init__(self, id, hmap)
        self.actor = self.generateActor()
        "the actor for redneering crated by generateActor func"

    def generateActor(self):
        """crates and initaiats the actor for rendering
        """
        actor = Actor("panda")
        actor.setScale(.1, .1, .1)
        return actor
