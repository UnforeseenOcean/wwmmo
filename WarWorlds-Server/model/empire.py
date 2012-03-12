'''
Created on 27/02/2012

@author: dean@codeka.com.au
'''

from google.appengine.ext import db
#import logging
import sector


class Empire(db.Model):
    """Represents an empire, display name and whatnot.
    """
    displayName = db.StringProperty()
    user = db.UserProperty()
    state = db.IntegerProperty()

    @staticmethod
    def getForUser(user):
        result = Empire.all().filter("user", user).fetch(1, 0)
        if len(result) != 1:
            return None
        return result[0]

    class State:
        INITIAL = 1
        REGISTERED = 2
        BANNED = 3


class Colony(db.Model):
    """Represents a colony on a planet. A colony is owned by a single Empire.

    The colony is only "simulated" when a value actually changes. Normally, when we go to display
    a colony's data to the player, we take the value of lastSimulation, then run the simulation
    for all the time between lastSimulation and "now". (it's usually really basic stuff like
    "population = populationRate * (now - lastSimulation)" sort of thing). If you change a property
    on your colony, though, that'll change the various rates. So we need to run a simulation for
    eveything up to the point where the property changes, and save the new value.
    """
    planet = db.ReferenceProperty(sector.Planet)
    star = db.ReferenceProperty(sector.Star)
    sector = db.ReferenceProperty(sector.Sector)
    empire = db.ReferenceProperty(Empire)
    population = db.IntegerProperty()
    populationRate = db.FloatProperty()
    lastSimulation = db.DateTimeProperty()

    @staticmethod
    def getForEmpire(empire_model):
        query = Colony.all().filter("empire", empire_model)
        return Colony._getForQuery(query)

    @staticmethod
    def getForSector(sector_model):
        query = Colony.all().filter("sector", sector_model)
        return Colony._getForQuery(query)

    @staticmethod
    def getForStar(star_model):
        query = Colony.all().filter("star", star_model)
        return Colony._getForQuery(query)

    @staticmethod
    def _getForQuery(query):
        colonies = []
        for colony in query:
            colonies.append(colony)
        return colonies