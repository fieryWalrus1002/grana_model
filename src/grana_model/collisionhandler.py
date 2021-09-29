# collision handler
class CollisionHandler:
    def __init__(self, space):
        self.space = space
        self.collision_handler = self.space.add_collision_handler(1, 1)
        self.collision_handler.begin = self.__coll_begin
        self.collision_handler.pre_solve = self.__pre_solve
        self.collision_handler.post_solve = self.__post_solve
        self.collision_handler.separate = self.__separate

    def __coll_begin(self, arbiter, space, data):
        # set_ = arbiter.contact_point_set

        print("coll_begin")
        return True

    def __separate(self, arbiter, space, data):
        print("coll_separate")

    def __post_solve(self, arbiter, space, data):
        print("coll_post_solve")

    def __pre_solve(self, arbiter, space, data):
        set_ = arbiter.contact_point_set
        print(f"coll_presolve: {set_.points[0].distance}")
        # We want to update the collision normal to make the bounce direction
        # dependent of where on the paddle the ball hits. Note that this
        # calculation isn't perfect, but just a quick example.
        # set_ = arbiter.contact_point_set
        # if len(set_.points) > 0:
        #     player_shape = arbiter.shapes[0]
        #     width = (player_shape.b - player_shape.a).x
        #     delta = (player_shape.body.position - set_.points[0].point_a).x
        #     normal = Vec2d(0, 1).rotated(delta / width / 2)
        #     set_.normal = normal
        #     set_.points[0].distance = 0
        # arbiter.contact_point_set = set_
        # print(set_.points[0].distance)
        return True
