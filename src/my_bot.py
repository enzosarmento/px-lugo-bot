import math
import random
import traceback
from abc import ABC
from typing import List

import lugo4py
from settings import get_my_expected_position

DEF_PLAYERS = [5, 4, 3, 2]


class MyBot(lugo4py.Bot, ABC):
    def on_disputing(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        """
        Método chamado quando nenhum jogador está com a posse da bola (bola disputada).
        O bot decide se vai tentar pegar a bola ou se posicionar.
        """
        try:
            me = inspector.get_me()
            ball_position = inspector.get_ball().position
            my_team = inspector.get_my_team_players()

            # Ordena os jogadores do time por proximidade da bola
            closest_players = self.get_closest_players(ball_position, my_team)
            n_catchers = 3  # Quantos jogadores tentarão pegar a bola
            catchers = closest_players[:n_catchers]
            if me in catchers:
                # Se estou entre os mais próximos, vou em direção à bola
                move_order = inspector.make_order_move_max_speed(ball_position)
            else:
                # Caso contrário, me posiciono na posição esperada
                move_order = inspector.make_order_move_max_speed(get_my_expected_position(inspector, self.mapper, self.number))

            catch_order = inspector.make_order_catch()

            return [move_order, catch_order]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_defending(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        """
        Método chamado quando um adversário está com a posse da bola.
        O bot decide se pressiona o adversário, mantém a linha defensiva ou retorna à posição esperada.
        """
        try:
            me = inspector.get_me()
            ball_pos = inspector.get_ball().position
            my_team = inspector.get_my_team_players()
            
            closest_player_to_ball = self.get_closest_players(ball_pos, my_team)[0]
            am_i_closest = (me.number == closest_player_to_ball.number)
            
            if am_i_closest:
                ball_holder = inspector.get_ball_holder()
                target_pos = ball_holder.position if ball_holder else ball_pos
                move_order = inspector.make_order_move_max_speed(target_pos)
                catch_order = inspector.make_order_catch()
                return [move_order, catch_order]
            
            if me.number in DEF_PLAYERS:
                defensive_pos = self.dynamic_defensive_position(inspector, me.number)
                move_order = inspector.make_order_move_max_speed(defensive_pos)
                return [move_order]
            else:
                expected_pos = get_my_expected_position(inspector, self.mapper, self.number)
                move_order = inspector.make_order_move_max_speed(expected_pos)
                return [move_order]
        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def on_holding(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        """
        Método chamado quando este bot está com a posse da bola.
        O bot decide se chuta ao gol, avança ou passa para um companheiro livre.
        """
        try:
            me = inspector.get_me()
            opponent_goal = self.mapper.get_attack_goal()

            if me.number in DEF_PLAYERS:
                # Zagueiros com a bola devem passar para um jogador de meio/ataque livre
                free_allies = self.get_free_allies(inspector, 600)
                
                non_defenders = [p for p in free_allies if p.number not in DEF_PLAYERS]

                if non_defenders:
                    # Passa para o jogador de meio/ataque livre mais avançado
                    side_factor = 1 if self.side == lugo4py.TeamSide.HOME else -1
                    non_defenders.sort(key=lambda p: p.position.x * side_factor, reverse=True)
                    
                    target_player = non_defenders[0]
                    kick_order = inspector.make_order_kick_max_speed(target_player.position)
                    return [kick_order]
                else:
                    # Se não houver jogadores livres, chuta para o meio do campo
                    kick_order = inspector.make_order_kick_max_speed(lugo4py.Point(x=lugo4py.specs.FIELD_WIDTH / 2, y=lugo4py.specs.FIELD_HEIGHT / 2))
                    return [kick_order]

            goal_line_x = opponent_goal.get_center().x
            x_dist = abs(me.position.x - goal_line_x)

            # Condição para chutar: perto da linha do gol e com ângulo razoável
            should_shoot = False
            if x_dist < lugo4py.GOAL_ZONE_RANGE * 1.5:
                goal_top_y = opponent_goal.get_top_pole().y
                goal_bottom_y = opponent_goal.get_bottom_pole().y
                margin = 400  # Margem para permitir chutes da lateral
                
                if (goal_bottom_y - margin) < me.position.y < (goal_top_y + margin):
                    should_shoot = True

            if should_shoot:
                my_order = inspector.make_order_kick_max_speed(self.find_best_shot_target(inspector))
                return [my_order]

            # Se estou marcado, tento passar a bola
            if self.is_marked(inspector, me, 700):
                free_players = self.get_free_allies(inspector, 600)
                if free_players:
                    # Prioriza passar para o jogador mais avançado (eixo x)
                    side_factor = 1 if self.side == lugo4py.TeamSide.HOME else -1
                    free_players.sort(key=lambda p: p.position.x * side_factor, reverse=True)

                    target_player = free_players[0]
                    kick_order = inspector.make_order_kick_max_speed(target_player.position)
                    return [kick_order]

            # Se não estou marcado ou não achei passe, continuo avançando
            my_order = inspector.make_order_move_max_speed(opponent_goal.get_center())
            return [my_order]

        except Exception as e:
            print(f'did not play this turn due to exception. {e}')
            traceback.print_exc()

    def on_supporting(self, inspector: lugo4py.GameSnapshotInspector) -> List[lugo4py.Order]:
        """
        Método chamado quando um companheiro de time está com a posse da bola.
        O bot decide se apoia o portador da bola, se posiciona para receber passe ou mantém posição defensiva.
        """
        try:
            me = inspector.get_me()
            ball_holder = inspector.get_ball_holder()
            my_team = inspector.get_my_team_players()

            # Defensores tem uma lógica própria
            if me.number in DEF_PLAYERS:
                defensive_pos = self.dynamic_defensive_position(inspector, me.number)
                move_order = inspector.make_order_move_max_speed(defensive_pos)
                return [move_order]

            # Se o goleiro do meu time está com a bola, me aproximo
            if ball_holder.number == 1:
                my_team = inspector.get_my_team_players()
                closest_players = self.get_closest_players(ball_holder.position, my_team)
                if me in closest_players[:4]:
                    move_order = inspector.make_order_move_max_speed(ball_holder.position)
                    return [move_order]

            # Se o portador da bola está marcado, o companheiro mais próximo deve dar suporte
            if self.is_marked(inspector, ball_holder, 900):
                closest_teammate = self.get_closest_players(ball_holder.position, my_team)[:2]
                for closest_player in closest_teammate:
                    if me.number == closest_player.number:
                        print("Sou jogador proximo")
                        # Eu sou o mais próximo, então devo encontrar uma posição de suporte
                        support_pos = self.find_support_position(inspector, ball_holder)
                        move_order = inspector.make_order_move_max_speed(support_pos)
                        return [move_order]

            # Caso contrário, me movo para a minha posição esperada
            move_dest = get_my_expected_position(inspector, self.mapper, self.number)
            move_order = inspector.make_order_move_max_speed(move_dest)
            return [move_order]

        except Exception as e:
            print(f'did not play this turn due to exception {e}')
            traceback.print_exc()

    def as_goalkeeper(self, inspector: lugo4py.GameSnapshotInspector, state) -> List[lugo4py.Order]:
        """
        Método chamado quando este bot é o goleiro (número 1).
        O goleiro decide se passa a bola, intercepta ou se posiciona no gol.
        """
        try:
            ball_pos = inspector.get_ball().position
            my_goal_center = self.mapper.get_defense_goal().get_center()

            if state == lugo4py.PLAYER_STATE.HOLDING_THE_BALL:
                free_players = self.get_free_allies(inspector, 800)
                if free_players:
                    side_factor = 1 if self.side == lugo4py.TeamSide.HOME else -1
                    free_players.sort(key=lambda p: p.position.x * side_factor, reverse=True)
                    target_player = free_players[0]
                    kick_order = inspector.make_order_kick_max_speed(target_player.position)
                    return [kick_order]
                else:
                    kick_order = inspector.make_order_kick_max_speed(lugo4py.Point(x=lugo4py.specs.FIELD_WIDTH / 2, y=lugo4py.specs.FIELD_HEIGHT / 2))
                    return [kick_order]

            oscillation_x = random.randint(-50, 50)
            oscillation_y = random.randint(-50, 50)

            if lugo4py.distance_between_points(my_goal_center, ball_pos) > lugo4py.specs.FIELD_WIDTH / 4:
                target_pos = lugo4py.Point(x=my_goal_center.x + oscillation_x, y=my_goal_center.y + oscillation_y)
                move_order = inspector.make_order_move_max_speed(target_pos)
                return [move_order]

            target_y = ball_pos.y
            
            if inspector.get_ball().velocity.speed > 0:
                future_ball_pos = lugo4py.Point(x=ball_pos.x, y=ball_pos.y)
                ball_speed = inspector.get_ball().velocity.speed
                ball_dir = inspector.get_ball().velocity.direction
                for _ in range(3):
                    ball_speed -= lugo4py.specs.BALL_DECELERATION
                    if ball_speed < 0: ball_speed = 0
                    future_ball_pos.x += ball_dir.x * ball_speed / 100
                    future_ball_pos.y += ball_dir.y * ball_speed / 100
                target_y = future_ball_pos.y

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
        """
        Método chamado antes do início do jogo e após um gol.
        Pode ser usado para redefinir variáveis ou estratégias.
        """
        print('getting ready')

    def is_near(self, region_origin: lugo4py.mapper.Region, dest_origin: lugo4py.mapper.Region) -> bool:
        """
        Verifica se duas regiões do campo estão próximas (usado para posicionamento).
        """
        max_distance = 2
        return abs(region_origin.get_row() - dest_origin.get_row()) <= max_distance and abs(
            region_origin.get_col() - dest_origin.get_col()) <= max_distance

    def dynamic_defensive_position(self, inspector: lugo4py.GameSnapshotInspector, player_number: int) -> lugo4py.Point:
        """
        Calcula a posição defensiva dinâmica para o jogador, baseada na posição da bola e do gol.
        """
        ball_pos = inspector.get_ball().position
        my_goal_center = self.mapper.get_defense_goal().get_center()

        defense_line_x = my_goal_center.x + (ball_pos.x - my_goal_center.x) * 0.4
        
        midfield_x = lugo4py.specs.FIELD_WIDTH / 2
        if self.side == lugo4py.TeamSide.HOME:
            defense_line_x = min(defense_line_x, midfield_x - 300)
            defense_line_x = max(defense_line_x, my_goal_center.x + 800)
        else: # AWAY
            defense_line_x = max(defense_line_x, midfield_x + 300)
            defense_line_x = min(defense_line_x, my_goal_center.x - 800)

        center_y = my_goal_center.y + (ball_pos.y - my_goal_center.y) * 0.7
        spacing = 900

        if self.side == lugo4py.TeamSide.HOME:
            offsets = {2: -1.5, 3: -0.5, 4: 0.5, 5: 1.5}
        else:  # AWAY
            offsets = {2: 1.5, 3: 0.5, 4: -0.5, 5: -1.5}

        offset = offsets.get(player_number, 0)
        pos_y = center_y + offset * spacing
        
        pos_y = max(200, min(lugo4py.specs.FIELD_HEIGHT - 200, pos_y))
        return lugo4py.Point(x=round(defense_line_x), y=round(pos_y))

    def find_best_shot_target(self, inspector: lugo4py.GameSnapshotInspector) -> lugo4py.Point:
        """
        Calcula o melhor alvo para o chute ao gol, considerando a posição do goleiro adversário.
        """
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

    def is_marked(self, inspector: lugo4py.GameSnapshotInspector, player: lugo4py.Player, dist: int) -> bool:
        """
        Verifica se um jogador está marcado por um adversário em um determinado raio de distância,
        considerando apenas os adversários à sua frente ou aos lados.
        """
        opponent_team = inspector.get_opponent_players()
        
        for opponent in opponent_team:
            distance_to_opponent = lugo4py.geo.distance_between_points(player.position, opponent.position)
            
            if distance_to_opponent <= dist:
                # Verifica se o oponente não está atrás do jogador
                is_behind = False
                tolerance = 200  # Tolerância para considerar "atrás"
                if self.side == lugo4py.TeamSide.HOME:
                    if opponent.position.x < player.position.x - tolerance:
                        is_behind = True
                else:  # AWAY
                    if opponent.position.x > player.position.x + tolerance:
                        is_behind = True
                
                if not is_behind:
                    return True
        return False

    def find_support_position(self, inspector: lugo4py.GameSnapshotInspector, ball_holder: lugo4py.Player) -> lugo4py.Point:
        """
        Encontra a melhor posição para dar suporte ao jogador com a posse de bola.
        """
        best_pos = None
        max_dist_to_opp = -1

        # Gera pontos candidatos ao redor do portador da bola
        for angle in range(0, 360, 45):
            rad = angle * 3.14159 / 180
            dist = 800
            candidate_pos = lugo4py.Point(
                x=ball_holder.position.x + dist * math.cos(rad),
                y=ball_holder.position.y + dist * math.sin(rad)
            )

            # Verifica se a posição candidata está dentro do campo
            if not (0 < candidate_pos.x < lugo4py.specs.FIELD_WIDTH and 0 < candidate_pos.y < lugo4py.specs.FIELD_HEIGHT):
                continue

            # Encontra o oponente mais próximo da posição candidata
            opponents = inspector.get_opponent_players()
            closest_opp_dist = float('inf')
            if opponents:
                for opp in opponents:
                    d = lugo4py.geo.distance_between_points(candidate_pos, opp.position)
                    if d < closest_opp_dist:
                        closest_opp_dist = d
            
            # Queremos a posição que está mais longe de qualquer oponente
            if closest_opp_dist > max_dist_to_opp:
                max_dist_to_opp = closest_opp_dist
                best_pos = candidate_pos

        if best_pos:
            return best_pos
        else:
            # Como alternativa, volta para uma posição atrás do portador da bola
            goal_direction = -1 if self.side == lugo4py.TeamSide.HOME else 1
            return lugo4py.Point(x=ball_holder.position.x + (goal_direction * 500), y=ball_holder.position.y)

    def get_closest_players(self, point: lugo4py.Point, player_list: List[lugo4py.Player]) -> List[lugo4py.Player]:
        """
        Retorna a lista de jogadores mais próximos de um ponto específico.
        """
        sortKey = lambda player: lugo4py.geo.distance_between_points(point, player.position)

        closest_players = sorted(player_list, key=sortKey)
        return closest_players

    def get_free_allies(self, inspector: lugo4py.GameSnapshotInspector, dist: int) -> List[lugo4py.Player]:
        """
        Retorna os companheiros de time que estão livres de adversários em um determinado raio de distância.
        """
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
