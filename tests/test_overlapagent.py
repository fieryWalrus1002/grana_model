import unittest
import pymunk
import pyglet
from time import process_time

from grana_model.objectdata import ObjectData
from grana_model.spawner import Spawner
from grana_model.overlapagent import OverlapAgent, ExpandingCircle
from grana_model.collisionhandler import CollisionHandler


class TestOverlapAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.space = pymunk.Space()
        cls.object_list, _ = Spawner(
            object_data=ObjectData(
                pos_csv_filename="082620_SEM_final_coordinates.csv"
            ),
            spawn_type="psii_only",
            shape_type="complex",
            space=cls.space,
            batch=pyglet.graphics.Batch(),
            num_particles=0,
            num_psii=200,
        ).setup_model()

        cls.collision_handler = CollisionHandler(cls.space)

    def create_agent(cls) -> OverlapAgent:
        overlap_agent = OverlapAgent(
            time_limit=10,
            object_list=cls.object_list,
            area_strategy=ExpandingCircle,
            collision_handler=cls.collision_handler,
            space=cls.space,
        )
        overlap_agent._update_space()

        return overlap_agent

    def test_object_list_length(self):
        self.assertEqual(len(self.object_list), 200)

    def test_if_strategy_gives_list(self):
        overlap_agent = self.create_agent()
        zone_list = overlap_agent.area_strategy.get_next_zone()
        self.assertTrue(type(zone_list) == list)

    def test_zone_lists_size1(self):
        overlap_agent = self.create_agent()
        zone_list_a = overlap_agent.area_strategy.get_next_zone()
        zone_list_b = overlap_agent.area_strategy.get_next_zone()
        self.assertTrue(len(zone_list_a) < len(zone_list_b))

    def test_zone_lists_size2(self):
        overlap_agent = self.create_agent()
        zone_list_a = overlap_agent.area_strategy.get_next_zone()
        zone_list_b = overlap_agent.area_strategy.get_next_zone()
        self.assertFalse(len(zone_list_a) > len(zone_list_b))

    def test_expanding_circle_zone_length(self):
        overlap_agent = self.create_agent()
        iter_length = sum(1 for _ in overlap_agent.area_strategy)
        self.assertEqual(5, iter_length)

    # def test_overlap_reduction(self):
    #     overlap_agent = self.create_agent()
    #     overlap_results = overlap_agent.run()
    #     overlap_reduction_percent = (
    #         (overlap_results[1] - overlap_results[-1])
    #         / (overlap_agent.time_limit * 5)
    #         * 100
    #     )
    #     print(f"overlap reduction of {overlap_reduction_percent}%")
    #     self.assertTrue(overlap_reduction_percent > 0)

    # def test_time_left(self):
    #     overlap_agent = self.create_agent()
    #     overlap_agent.run()
    #     self.assertEqual(overlap_agent.time_left, 0)

    def test_action_time(self):
        overlap_agent = self.create_agent()
        overlap_agent.time_limit = 10

        projected_time = 0.04553125 * overlap_agent.time_limit * 5

        t1 = process_time()

        overlap_results = overlap_agent.run()

        overlap_reduction_percent = (
            (overlap_results[2] - overlap_results[-1])
            / (overlap_agent.time_limit * 5)
            * 100
        )

        t2 = process_time()

        elapsed_time = t2 - t1
        delta_time = abs(elapsed_time - projected_time)
        print(
            f"projected vs elapsed time: {projected_time} vs {elapsed_time}, for a total change of {delta_time} and a reduction of {overlap_reduction_percent}%"
        )

        self.assertTrue(abs(delta_time) < (0.2 * projected_time))


unittest.main()
