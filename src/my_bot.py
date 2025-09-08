import traceback
from abc import ABC
from typing import List

import lugo4py
from settings import get_my_expected_position


class MyBot(lugo4py.Bot, ABC):
    def on_disputing(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            me = inspector.get_me()
            ball_position = inspector.get_ball().position
            my_team = inspector.get_my_team_players()

            closest_players = self.get_closest_players(ball_position, my_team)
            n_catchers = 3
            catchers = closest_players[:n_catchers]
            if me in catchers:
                move_order = inspector.make_order_move_max_speed(ball_position)
            else:
                move_order = inspector.make_order_move_max_speed(get_my_expected_position(inspector, self.mapper, self.number))

            
            catch_order = inspector.make_order_catch()

            return [move_order, catch_order]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_defending(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:

            me = inspector.get_me()
            ball_position = inspector.get_ball().position
            my_team = inspector.get_my_team_players()

            closest_players = self.get_closest_players(ball_position, my_team)
            n_catchers = 3
            catchers = closest_players[:n_catchers]
            if me in catchers:
                move_order = inspector.make_order_move_max_speed(ball_position)
            else:
                move_order = inspector.make_order_move_max_speed(get_my_expected_position(inspector, self.mapper, self.number))
            catch_order = inspector.make_order_catch()

            return [move_order, catch_order]
        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_holding(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            opponent_goal = self.mapper.get_attack_goal()
            me = inspector.get_me()
            my_team = inspector.get_my_team_players()

            inspector.get_opponent_goalkeeper().position
            dist_to_goal = lugo4py.distance_between_points(me.position, opponent_goal.get_center())

            if dist_to_goal <= lugo4py.GOAL_ZONE_RANGE + lugo4py.BALL_SIZE * 4:
                my_order = inspector.make_order_kick_max_speed(self.find_best_shot_target(inspector))
                return [my_order]
            else:
                my_order = inspector.make_order_move_max_speed(opponent_goal.get_center())
                free_players = self.get_free_allies(inspector, 600)
                closest_to_goal = self.get_closest_players(opponent_goal.get_center(), my_team)
                for ally in closest_to_goal:
                    if ally in free_players:
                        position = lugo4py.Point(ally.position.x - 500, ally.position.y - 500)
                        kick_order = inspector.make_order_kick_max_speed(position)
                        return [my_order, kick_order]
                
                return [my_order]

            

        except Exception as e:
            print(f'did not play this turn due to exception. {e}')
            traceback.print_exc()

    def on_supporting(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            move_dest = get_my_expected_position(inspector, self.mapper, self.number)
            me = inspector.get_me()
            my_team = inspector.get_my_team_players()
            player_ball_holder = inspector.get_ball_holder()
            free_players = self.get_closest_players(player_ball_holder.position, my_team)
            if player_ball_holder.number == 1:
                if me in free_players[:4]:
                    move_order = inspector.make_order_move_max_speed(player_ball_holder.position)
                    return [move_order]
            move_order = inspector.make_order_move_max_speed(move_dest)
            return [move_order]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def as_goalkeeper(self, inspector: lugo4py.GameSnapshotInspector, state: lugo4py.PLAYER_STATE) -> List[lugo4py.Order]:
        try:
            position = inspector.get_ball().position

            if state == lugo4py.PLAYER_STATE.HOLDING_THE_BALL:
                free_players = self.get_free_allies(inspector, 500)
                kick_order = inspector.make_order_kick_max_speed(free_players[0].position)
                return [kick_order]
            if state != lugo4py.PLAYER_STATE.DISPUTING_THE_BALL:
                position = self.mapper.get_attack_goal().get_center()

            my_order = inspector.make_order_move_max_speed(position)

            return [my_order, inspector.make_order_catch()]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def getting_ready(self, snapshot: lugo4py.GameSnapshot):
        print('getting ready')

    def is_near(self, region_origin: lugo4py.mapper.Region, dest_origin: lugo4py.mapper.Region) -> bool:
        max_distance = 2
        return abs(region_origin.get_row() - dest_origin.get_row()) <= max_distance and abs(
            region_origin.get_col() - dest_origin.get_col()) <= max_distance
    
    def find_best_shot_target(self, inspector: lugo4py.GameSnapshotInspector) -> lugo4py.Point:

        opponent_goal = self.mapper.get_attack_goal()
        goal_top_pole = opponent_goal.get_top_pole()
        goal_bottom_pole = opponent_goal.get_bottom_pole()
        
        goalkeeper = inspector.get_opponent_goalkeeper()

        if not goalkeeper:
            return goal_top_pole

        KEEPER_REACH = lugo4py.PLAYER_SIZE * 1.5 

        gk_coverage_top = goalkeeper.position.y + KEEPER_REACH
        gk_coverage_bottom = goalkeeper.position.y - KEEPER_REACH

        top_gap = max(0, goal_top_pole.y - gk_coverage_top)
        bottom_gap = max(0, gk_coverage_bottom - goal_bottom_pole.y)

        target_pos = opponent_goal.get_center()

        if top_gap > bottom_gap:
            target_pos.y = round(goal_top_pole.y + lugo4py.BALL_SIZE)
        else:
            target_pos.y = round(goal_bottom_pole.y + lugo4py.BALL_SIZE)

        target_pos.y = max(goal_bottom_pole.y, min(goal_top_pole.y, target_pos.y))
        
        return target_pos

    def get_closest_players(self, point, player_list):

        sortKey = lambda player: lugo4py.geo.distance_between_points(point, player.position)

        closest_players = sorted(player_list, key=sortKey)
        return closest_players
    
    def get_free_allies(self, inspector: lugo4py.GameSnapshotInspector, dist):
        my_team = inspector.get_my_team_players()
        opponent_team = inspector.get_opponent_players()

        free_players = []
        for ally in my_team:
            is_free = True
            for opponent in opponent_team:
                distance_to_opponent = lugo4py.geo.distance_between_points(ally.position, opponent.position)
                if  distance_to_opponent <= dist:
                    is_free = False
            
            if is_free and ally.number != 1 and ally.number != self.number:
                free_players.append(ally)

        free_players.sort(key=lambda p: (p.position.x, p.position.y))
        return free_players