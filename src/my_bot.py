import random
import traceback
from abc import ABC
from typing import List

import lugo4py
from settings import get_my_expected_position

DEF_PLAYERS = [5, 4, 3, 2]


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
            ball_pos = inspector.get_ball().position
            my_team = inspector.get_my_team_players()
            
            # Encontra o companheiro de time mais próximo da bola
            closest_player_to_ball = self.get_closest_players(ball_pos, my_team)[0]
            am_i_closest = (me.number == closest_player_to_ball.number)
            
            # LÓGICA DE DEFESA:
            # Se eu sou o mais próximo, eu pressiono o adversário com a bola.
            if am_i_closest:
                ball_holder = inspector.get_ball_holder()
                target_pos = ball_holder.position if ball_holder else ball_pos
                move_order = inspector.make_order_move_max_speed(target_pos)
                catch_order = inspector.make_order_catch()
                return [move_order, catch_order]
            
            # Se não sou o mais próximo:
            # Se eu sou um defensor, mantenho a formação dinâmica.
            if me.number in DEF_PLAYERS:
                defensive_pos = self.dynamic_defensive_position(inspector, me.number)
                move_order = inspector.make_order_move_max_speed(defensive_pos)
                return [move_order]
            
            # Se sou um atacante/meia, volto para minha posição esperada.
            else:
                expected_pos = get_my_expected_position(inspector, self.mapper, self.number)
                move_order = inspector.make_order_move_max_speed(expected_pos)
                return [move_order]
        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_holding(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        try:
            me = inspector.get_me()

            opponent_goal = self.mapper.get_attack_goal()
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
            me = inspector.get_me()
            if me.number in DEF_PLAYERS:
                defensive_pos = self.dynamic_defensive_position(inspector, me.number)
                move_order = inspector.make_order_move_max_speed(defensive_pos)
                return [move_order]
            
            move_dest = get_my_expected_position(inspector, self.mapper, self.number)
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
            ball_pos = inspector.get_ball().position
            my_goal_center = self.mapper.get_defense_goal().get_center()

            if state == lugo4py.PLAYER_STATE.HOLDING_THE_BALL:
                # Find free allies to pass the ball to
                free_players = self.get_free_allies(inspector, 800)
                if free_players:
                    # Sort players by their x position to find the one furthest down the field
                    side_factor = 1 if self.side == lugo4py.TeamSide.HOME else -1
                    free_players.sort(key=lambda p: p.position.x * side_factor, reverse=True)
                    
                    target_player = free_players[0]
                    kick_order = inspector.make_order_kick_max_speed(target_player.position)
                    return [kick_order]
                else:
                    # If no one is free, kick the ball to the center of the field
                    kick_order = inspector.make_order_kick_max_speed(lugo4py.Point(x=lugo4py.specs.FIELD_WIDTH / 2, y=lugo4py.specs.FIELD_HEIGHT / 2))
                    return [kick_order]

            # Add a small random oscillation to the target position
            oscillation_x = random.randint(-50, 50)
            oscillation_y = random.randint(-50, 50)

            # If the ball is far, the goalkeeper should stay in the center of the goal
            if lugo4py.distance_between_points(my_goal_center, ball_pos) > lugo4py.specs.FIELD_WIDTH / 4:
                target_pos = lugo4py.Point(x=my_goal_center.x + oscillation_x, y=my_goal_center.y + oscillation_y)
                move_order = inspector.make_order_move_max_speed(target_pos)
                return [move_order]

            # If the ball is closer, the goalkeeper should move to intercept it on the goal line
            target_y = ball_pos.y
            
            # Predict the ball's future y position
            if inspector.get_ball().velocity.speed > 0:
                # Simplified prediction: assume the ball will continue in a straight line for a few turns
                future_ball_pos = lugo4py.Point(x=ball_pos.x, y=ball_pos.y)
                ball_speed = inspector.get_ball().velocity.speed
                ball_dir = inspector.get_ball().velocity.direction
                for _ in range(3): # Predict 3 turns ahead
                    ball_speed -= lugo4py.specs.BALL_DECELERATION
                    if ball_speed < 0: ball_speed = 0
                    future_ball_pos.x += ball_dir.x * ball_speed / 100
                    future_ball_pos.y += ball_dir.y * ball_speed / 100
                target_y = future_ball_pos.y

            # Ensure the target y is within the goal posts
            goal_top_y = self.mapper.get_defense_goal().get_top_pole().y
            goal_bottom_y = self.mapper.get_defense_goal().get_bottom_pole().y
            target_y = max(goal_bottom_y, min(goal_top_y, target_y))

            target_pos = lugo4py.Point(x=my_goal_center.x + oscillation_x, y=target_y + oscillation_y)
            
            move_order = inspector.make_order_move_max_speed(target_pos)
            catch_order = inspector.make_order_catch()
            return [move_order, catch_order]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def getting_ready(self, snapshot: lugo4py.GameSnapshot):
        print('getting ready')

    def is_near(self, region_origin: lugo4py.mapper.Region, dest_origin: lugo4py.mapper.Region) -> bool:
        max_distance = 2
        return abs(region_origin.get_row() - dest_origin.get_row()) <= max_distance and abs(
            region_origin.get_col() - dest_origin.get_col()) <= max_distance

    def dynamic_defensive_position(self, inspector: lugo4py.GameSnapshotInspector, player_number: int) -> lugo4py.Point:
        """Calcula a posição defensiva baseada na bola, mantendo o espaçamento."""
        ball_pos = inspector.get_ball().position
        my_goal_center = self.mapper.get_defense_goal().get_center()

        # A linha de defesa se posiciona entre a bola e o gol.
        defense_line_x = my_goal_center.x + (ball_pos.x - my_goal_center.x) * 0.4
        
        midfield_x = lugo4py.specs.FIELD_WIDTH / 2
        # Limites para a linha defensiva
        if self.side == lugo4py.TeamSide.HOME:
            defense_line_x = min(defense_line_x, midfield_x - 300)
            defense_line_x = max(defense_line_x, my_goal_center.x + 800)
        else: # AWAY
            defense_line_x = max(defense_line_x, midfield_x + 300)
            defense_line_x = min(defense_line_x, my_goal_center.x - 800)

        # O centro da linha defensiva (eixo Y) segue a bola lateralmente
        center_y = my_goal_center.y + (ball_pos.y - my_goal_center.y) * 0.7
        spacing = 900  # Espaçamento lateral entre os defensores

        if player_number == 2:   # Lateral
            pos_y = center_y - spacing * 1.5
        elif player_number == 3: # Zagueiro
            pos_y = center_y - spacing * 0.5
        elif player_number == 4: # Zagueiro
            pos_y = center_y + spacing * 0.5
        elif player_number == 5: # Lateral
            pos_y = center_y + spacing * 1.5
        else:
            pos_y = center_y
        
        pos_y = max(200, min(lugo4py.specs.FIELD_HEIGHT - 200, pos_y))
        return lugo4py.Point(x=round(defense_line_x), y=round(pos_y))

    def is_in_front_of_the_opponent(self, my_player: lugo4py.Player, my_opponent: lugo4py.Player):
        if my_player.team_side == lugo4py.TeamSide.HOME:
            return my_player.position.x < my_opponent.position.x + lugo4py.PLAYER_SIZE
        return my_player.position.x > my_player.position.x - lugo4py.PLAYER_SIZE

    def find_best_shot_target(self, inspector: lugo4py.GameSnapshotInspector) -> lugo4py.Point:
        me = inspector.get_me()
        opponent_goal = self.mapper.get_attack_goal()
        goal_top_pole = opponent_goal.get_top_pole()
        goal_bottom_pole = opponent_goal.get_bottom_pole()

        goalkeeper = inspector.get_opponent_goalkeeper()

        if not goalkeeper:
            return goal_top_pole

        target_top = lugo4py.Point(x=goal_top_pole.x, y=round(goal_top_pole.y - lugo4py.BALL_SIZE))
        target_bottom = lugo4py.Point(x=goal_bottom_pole.x, y=round(goal_bottom_pole.y + lugo4py.BALL_SIZE))

        KEEPER_REACH = lugo4py.PLAYER_SIZE * 1.5
        gk_coverage_top = goalkeeper.position.y + KEEPER_REACH
        gk_coverage_bottom = goalkeeper.position.y - KEEPER_REACH

        is_top_path_clear = target_top.y > gk_coverage_top
        is_bottom_path_clear = target_bottom.y < gk_coverage_bottom

        dist_ball_to_top = lugo4py.geo.distance_between_points(me.position, target_top)
        dist_ball_to_bottom = lugo4py.geo.distance_between_points(me.position, target_bottom)

        dist_gk_to_top = lugo4py.geo.distance_between_points(goalkeeper.position, target_top)
        dist_gk_to_bottom = lugo4py.geo.distance_between_points(goalkeeper.position, target_bottom)

        score_top = (dist_gk_to_top / dist_ball_to_top) if is_top_path_clear else -1
        score_bottom = (dist_gk_to_bottom / dist_ball_to_bottom) if is_bottom_path_clear else -1

        if score_top <= 0 and score_bottom <= 0:
            return opponent_goal.get_center()
        if score_top > score_bottom:
            return target_top
        else:
            return target_bottom

    def get_closest_players(self, point: lugo4py.Point, player_list: List[lugo4py.Player]) -> List[lugo4py.Player]:
        sortKey = lambda player: lugo4py.geo.distance_between_points(point, player.position)

        closest_players = sorted(player_list, key=sortKey)
        return closest_players

    def get_free_allies(self, inspector: lugo4py.GameSnapshotInspector, dist: int) -> List[lugo4py.Player]:
        my_team = inspector.get_my_team_players()
        opponent_team = inspector.get_opponent_players()

        free_players = []
        for ally in my_team:
            is_free = True
            for opponent in opponent_team:
                distance_to_opponent = lugo4py.geo.distance_between_points(ally.position, opponent.position)
                if distance_to_opponent <= dist:
                    is_free = False

            if is_free and ally.number != 1 and ally.number != self.number:
                free_players.append(ally)

        free_players.sort(key=lambda p: (p.position.x, p.position.y))
        return free_players