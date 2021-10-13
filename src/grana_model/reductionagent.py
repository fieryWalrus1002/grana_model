# -*- coding: utf-8 -*-
"""Overlap reduction agent

This module implements an agent that attempts to reduce overlap between objects
in the simulation, and strategies that it can follow to perform this duty. 

Example:
    $ overlap_agent = OverlapAgent(area_strategy=chosen_strategy, time_limit=1000,
        space=space)
    $ overlap_agent.run()

Todo:
    * everything. abstract strategies, coding the overlap agent, etc.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from abc import ABC, abstractmethod


class AreaStrategy(ABC):
    """abstract base class for area selection strategies."""

    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def get_iterator(self):
        return self.__iter__()

    @classmethod
    def __iter__(self):
        return NotImplemented


class OverlapAgent:
    """The overlap_agent acts to reduce overlap between objects.

    overlap_agent:
        - calls objects in successive areas (area chosen via strategy),
        one by one, with a function such as below for a certain period of time
        - call_object(object):
            1. tell object to take an action (random choice? or decide?)
            2. step simulation/refresh shape states
            3. evaluate the action effect on overlap
            4. either keep or undo action
        - agent has a limited amount of time to make improvement.
            - If rate of improvement is less than a threshold in strategy:
                1. give up trying in this area. Expand area.
                2. If all areas have already been included, simulation ends.

    Attributes:
        time_limit (int): The amount of actions allowed before the agent has to
        either expand the area or end its attempt to reduce overlap in the total
        area.
    """

    def __init__(self, time_limit, area_strategy: AreaStrategy):
        pass

    def run(self):
        pass
