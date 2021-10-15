import unittest
import pymunk
import pyglet

from grana_model.objectdata import ObjectData
from grana_model.spawner import Spawner
from grana_model.reductionagent import OverlapAgent, ExpandingCircle


class TestOverlapAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.object_list, _ = Spawner(
            object_data=ObjectData(
                pos_csv_filename="082620_SEM_final_coordinates.csv"
            ),
            spawn_type="psii_only",
            shape_type="complex",
            space=pymunk.Space(),
            batch=pyglet.graphics.Batch(),
            num_particles=0,
            num_psii=200,
        ).setup_model()

        cls.overlap_agent = OverlapAgent(
            time_limit=1000,
            object_list=cls.object_list,
            area_strategy=ExpandingCircle,
        )

    def test_object_list_length(self):
        self.assertEqual(len(self.object_list), 200)

    def test_if_strategy_gives_list(self):
        zone_list = self.overlap_agent.area_strategy.get_next_zone()
        self.assertTrue(type(zone_list) == list)

    def test_zone_lists_size1(self):
        zone_list_a = self.overlap_agent.area_strategy.get_next_zone()
        zone_list_b = self.overlap_agent.area_strategy.get_next_zone()

        self.assertTrue(len(zone_list_a) < len(zone_list_b))

    def test_zone_lists_size2(self):
        zone_list_a = self.overlap_agent.area_strategy.get_next_zone()
        zone_list_b = self.overlap_agent.area_strategy.get_next_zone()

        self.assertFalse(len(zone_list_a) > len(zone_list_b))

    # def test_object_generation(self):
    #     next_obj = next(self.obj_data.object_list)
    #     self.assertIsNotNone(next_obj)

    # def test_object_value_types(self):
    #     obj = next(self.obj_data.object_list)
    #     self.assertIsInstance(obj["obj_type"], str)
    #     self.assertIsInstance(obj["pos"], list)


unittest.main()
