# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [broadcast.proto](#broadcast-proto)
    - [EventDebugBreakpoint](#lugo-EventDebugBreakpoint)
    - [EventDebugReleased](#lugo-EventDebugReleased)
    - [EventGameOver](#lugo-EventGameOver)
    - [EventGoal](#lugo-EventGoal)
    - [EventLostPlayer](#lugo-EventLostPlayer)
    - [EventNewPlayer](#lugo-EventNewPlayer)
    - [EventStateChange](#lugo-EventStateChange)
    - [GameEvent](#lugo-GameEvent)
    - [GameSetup](#lugo-GameSetup)
    - [StartRequest](#lugo-StartRequest)
    - [TeamColor](#lugo-TeamColor)
    - [TeamColors](#lugo-TeamColors)
    - [TeamSettings](#lugo-TeamSettings)
    - [WatcherRequest](#lugo-WatcherRequest)
  
    - [EventDebugBreakpoint.Breakpoint](#lugo-EventDebugBreakpoint-Breakpoint)
    - [GameSetup.ListeningMode](#lugo-GameSetup-ListeningMode)
    - [GameSetup.StartingMode](#lugo-GameSetup-StartingMode)
  
    - [Broadcast](#lugo-Broadcast)
  
- [health.proto](#health-proto)
    - [HealthCheckRequest](#grpc-health-v1-HealthCheckRequest)
    - [HealthCheckResponse](#grpc-health-v1-HealthCheckResponse)
  
    - [HealthCheckResponse.ServingStatus](#grpc-health-v1-HealthCheckResponse-ServingStatus)
  
    - [Health](#grpc-health-v1-Health)
  
- [physics.proto](#physics-proto)
    - [Point](#lugo-Point)
    - [Vector](#lugo-Vector)
    - [Velocity](#lugo-Velocity)
  
- [remote.proto](#remote-proto)
    - [BallProperties](#lugo-BallProperties)
    - [CommandResponse](#lugo-CommandResponse)
    - [GameProperties](#lugo-GameProperties)
    - [NextOrderRequest](#lugo-NextOrderRequest)
    - [NextTurnRequest](#lugo-NextTurnRequest)
    - [PauseResumeRequest](#lugo-PauseResumeRequest)
    - [PlayerProperties](#lugo-PlayerProperties)
    - [ResumeListeningRequest](#lugo-ResumeListeningRequest)
    - [ResumeListeningResponse](#lugo-ResumeListeningResponse)
  
    - [CommandResponse.StatusCode](#lugo-CommandResponse-StatusCode)
  
    - [Remote](#lugo-Remote)
  
- [server.proto](#server-proto)
    - [Ball](#lugo-Ball)
    - [Catch](#lugo-Catch)
    - [GameSnapshot](#lugo-GameSnapshot)
    - [JoinRequest](#lugo-JoinRequest)
    - [Jump](#lugo-Jump)
    - [Kick](#lugo-Kick)
    - [Move](#lugo-Move)
    - [Order](#lugo-Order)
    - [OrderResponse](#lugo-OrderResponse)
    - [OrderSet](#lugo-OrderSet)
    - [Player](#lugo-Player)
    - [ShotClock](#lugo-ShotClock)
    - [Team](#lugo-Team)
  
    - [GameSnapshot.State](#lugo-GameSnapshot-State)
    - [OrderResponse.StatusCode](#lugo-OrderResponse-StatusCode)
    - [Team.Side](#lugo-Team-Side)
  
    - [Game](#lugo-Game)
  
- [Scalar Value Types](#scalar-value-types)



<a name="broadcast-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## broadcast.proto



<a name="lugo-EventDebugBreakpoint"></a>

### EventDebugBreakpoint
(only available dev mode) Represents the event of having a breakpoint reached.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| breakpoint | [EventDebugBreakpoint.Breakpoint](#lugo-EventDebugBreakpoint-Breakpoint) |  | Type of the breakpoint reached. |






<a name="lugo-EventDebugReleased"></a>

### EventDebugReleased
(only available dev mode) Represents the event of having a breakpoint released.






<a name="lugo-EventGameOver"></a>

### EventGameOver
Represents the event of having the game ended.






<a name="lugo-EventGoal"></a>

### EventGoal
Represents the event of having a goal during the match


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| side | [Team.Side](#lugo-Team-Side) |  | Side of the team that changed the score.

@todo implementing the player who scored. |






<a name="lugo-EventLostPlayer"></a>

### EventLostPlayer
Represents the event of having a player disconnected from the game.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| player | [Player](#lugo-Player) |  | Player that has disconnected from the game. |






<a name="lugo-EventNewPlayer"></a>

### EventNewPlayer
Represents the event of having a new player connected to the game.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| player | [Player](#lugo-Player) |  | Player that has connected to the game. |






<a name="lugo-EventStateChange"></a>

### EventStateChange
Represents the event of having the game state changed (e.g. from Waiting to GetReady).


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| previous_state | [GameSnapshot.State](#lugo-GameSnapshot-State) |  | State of the game before the event. |
| new_state | [GameSnapshot.State](#lugo-GameSnapshot-State) |  | State of the game after the event. |






<a name="lugo-GameEvent"></a>

### GameEvent
Brings the game snapshot and the event in a specialised format.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| game_snapshot | [GameSnapshot](#lugo-GameSnapshot) |  | Game snapshot after the event has happened. |
| new_player | [EventNewPlayer](#lugo-EventNewPlayer) |  |  |
| lost_player | [EventLostPlayer](#lugo-EventLostPlayer) |  |  |
| state_change | [EventStateChange](#lugo-EventStateChange) |  |  |
| goal | [EventGoal](#lugo-EventGoal) |  |  |
| game_over | [EventGameOver](#lugo-EventGameOver) |  |  |
| breakpoint | [EventDebugBreakpoint](#lugo-EventDebugBreakpoint) |  |  |
| debug_released | [EventDebugReleased](#lugo-EventDebugReleased) |  |  |






<a name="lugo-GameSetup"></a>

### GameSetup



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| protocol_version | [string](#string) |  | Defines the communication protocol version between the players and the game server. The players also inform to the server what protocol they will use. If incompatible, the server will reject the player. |
| dev_mode | [bool](#bool) |  |  |
| start_mode | [GameSetup.StartingMode](#lugo-GameSetup-StartingMode) |  |  |
| listening_mode | [GameSetup.ListeningMode](#lugo-GameSetup-ListeningMode) |  |  |
| listening_duration | [uint32](#uint32) |  | in milliseconds |
| game_duration | [uint32](#uint32) |  |  |
| home_team | [TeamSettings](#lugo-TeamSettings) |  |  |
| away_team | [TeamSettings](#lugo-TeamSettings) |  |  |






<a name="lugo-StartRequest"></a>

### StartRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| watcher_uuid | [string](#string) |  | Not used on localhost |






<a name="lugo-TeamColor"></a>

### TeamColor



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| red | [uint32](#uint32) |  |  |
| green | [uint32](#uint32) |  |  |
| blue | [uint32](#uint32) |  |  |






<a name="lugo-TeamColors"></a>

### TeamColors



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| primary | [TeamColor](#lugo-TeamColor) |  |  |
| secondary | [TeamColor](#lugo-TeamColor) |  |  |






<a name="lugo-TeamSettings"></a>

### TeamSettings



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| name | [string](#string) |  |  |
| avatar | [string](#string) |  |  |
| colors | [TeamColors](#lugo-TeamColors) |  |  |






<a name="lugo-WatcherRequest"></a>

### WatcherRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| uuid | [string](#string) |  | Not used on localhost |





 


<a name="lugo-EventDebugBreakpoint-Breakpoint"></a>

### EventDebugBreakpoint.Breakpoint


| Name | Number | Description |
| ---- | ------ | ----------- |
| ORDERS | 0 | Breakpoint that breaks the game before each player orders set be processed during the &#34;Playing&#34; state Each player&#39;s order set will be processed at once, so the breakpoint controls the process based on players, not on orders. |
| TURN | 1 | Breakpoint that breaks the game before each player turn be processed during the &#34;Playing&#34; state |



<a name="lugo-GameSetup-ListeningMode"></a>

### GameSetup.ListeningMode


| Name | Number | Description |
| ---- | ------ | ----------- |
| TIMER | 0 | respect the timer defined by listening duration |
| RUSH | 1 | immediately after all orders |
| REMOTE | 2 | wait external remote control (dev only) |



<a name="lugo-GameSetup-StartingMode"></a>

### GameSetup.StartingMode


| Name | Number | Description |
| ---- | ------ | ----------- |
| NO_WAIT | 0 | start the game as soon as all players are connected |
| WAIT | 1 | do not start until the master watcher request (gRPC call to Broadcast service) |


 

 


<a name="lugo-Broadcast"></a>

### Broadcast
Service to be consumed by clients (e.g. frontend, app, etc) to watch the match.
The game server implements a Broadcast service. This service may help you to control or watch the game during
training sessions.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| OnEvent | [WatcherRequest](#lugo-WatcherRequest) | [GameEvent](#lugo-GameEvent) stream | Keep an open stream that publish all important events in the match. |
| GetGameSetup | [WatcherRequest](#lugo-WatcherRequest) | [GameSetup](#lugo-GameSetup) | Returns the game setup configuration. |
| StartGame | [StartRequest](#lugo-StartRequest) | [GameSetup](#lugo-GameSetup) | StartGame allows the master watcher to start the match. See the Game Server starting mode to understand how it works. |

 



<a name="health-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## health.proto



<a name="grpc-health-v1-HealthCheckRequest"></a>

### HealthCheckRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| service | [string](#string) |  |  |






<a name="grpc-health-v1-HealthCheckResponse"></a>

### HealthCheckResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| status | [HealthCheckResponse.ServingStatus](#grpc-health-v1-HealthCheckResponse-ServingStatus) |  |  |





 


<a name="grpc-health-v1-HealthCheckResponse-ServingStatus"></a>

### HealthCheckResponse.ServingStatus


| Name | Number | Description |
| ---- | ------ | ----------- |
| UNKNOWN | 0 |  |
| SERVING | 1 |  |
| NOT_SERVING | 2 |  |
| SERVICE_UNKNOWN | 3 | Used only by the Watch method. |


 

 


<a name="grpc-health-v1-Health"></a>

### Health


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Check | [HealthCheckRequest](#grpc-health-v1-HealthCheckRequest) | [HealthCheckResponse](#grpc-health-v1-HealthCheckResponse) |  |
| Watch | [HealthCheckRequest](#grpc-health-v1-HealthCheckRequest) | [HealthCheckResponse](#grpc-health-v1-HealthCheckResponse) stream |  |

 



<a name="physics-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## physics.proto



<a name="lugo-Point"></a>

### Point
Point represents one position on the cartesian plan of the game field.
The coordinates start at the left bottom corner from the top view .


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| x | [int32](#int32) |  | Distance from the Y axis to right. |
| y | [int32](#int32) |  | Distance from the X axis to up. |






<a name="lugo-Vector"></a>

### Vector
Vector represent one direction on a cartesian plan


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| x | [double](#double) |  | Coordinate X to define the vector direction. |
| y | [double](#double) |  | Coordinate Y to define the vector direction. |






<a name="lugo-Velocity"></a>

### Velocity
Velocity is a tuple with the direction (a vector) an a speed (float) values.
It defines the velocity of an object.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| direction | [Vector](#lugo-Vector) |  | Direction is a normalised vector that indicates the element direction |
| speed | [double](#double) |  | Speed of the element. |





 

 

 

 



<a name="remote-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## remote.proto



<a name="lugo-BallProperties"></a>

### BallProperties



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| position | [Point](#lugo-Point) |  |  |
| velocity | [Velocity](#lugo-Velocity) |  |  |
| holder | [Player](#lugo-Player) |  |  |






<a name="lugo-CommandResponse"></a>

### CommandResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| code | [CommandResponse.StatusCode](#lugo-CommandResponse-StatusCode) |  |  |
| game_snapshot | [GameSnapshot](#lugo-GameSnapshot) |  |  |
| details | [string](#string) |  |  |






<a name="lugo-GameProperties"></a>

### GameProperties



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| turn | [uint32](#uint32) |  |  |
| home_score | [uint32](#uint32) |  |  |
| away_score | [uint32](#uint32) |  |  |
| frame_interval | [int64](#int64) |  |  |
| shot_clock | [ShotClock](#lugo-ShotClock) |  |  |






<a name="lugo-NextOrderRequest"></a>

### NextOrderRequest







<a name="lugo-NextTurnRequest"></a>

### NextTurnRequest







<a name="lugo-PauseResumeRequest"></a>

### PauseResumeRequest







<a name="lugo-PlayerProperties"></a>

### PlayerProperties



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| side | [Team.Side](#lugo-Team-Side) |  |  |
| number | [uint32](#uint32) |  |  |
| position | [Point](#lugo-Point) |  |  |
| velocity | [Velocity](#lugo-Velocity) |  |  |






<a name="lugo-ResumeListeningRequest"></a>

### ResumeListeningRequest







<a name="lugo-ResumeListeningResponse"></a>

### ResumeListeningResponse






 


<a name="lugo-CommandResponse-StatusCode"></a>

### CommandResponse.StatusCode


| Name | Number | Description |
| ---- | ------ | ----------- |
| SUCCESS | 0 |  |
| INVALID_VALUE | 1 |  |
| DEADLINE_EXCEEDED | 2 |  |
| OTHER | 99 |  |


 

 


<a name="lugo-Remote"></a>

### Remote
The game server implements a Remote service that allows you to control the game flow.
This service may help you to control or watch the game during training sessions.
The game server only offers this service on debug mode on.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| PauseOrResume | [PauseResumeRequest](#lugo-PauseResumeRequest) | [CommandResponse](#lugo-CommandResponse) |  |
| NextTurn | [NextTurnRequest](#lugo-NextTurnRequest) | [CommandResponse](#lugo-CommandResponse) |  |
| NextOrder | [NextOrderRequest](#lugo-NextOrderRequest) | [CommandResponse](#lugo-CommandResponse) |  |
| SetBallProperties | [BallProperties](#lugo-BallProperties) | [CommandResponse](#lugo-CommandResponse) |  |
| SetPlayerProperties | [PlayerProperties](#lugo-PlayerProperties) | [CommandResponse](#lugo-CommandResponse) |  |
| SetGameProperties | [GameProperties](#lugo-GameProperties) | [CommandResponse](#lugo-CommandResponse) |  |
| ResumeListeningPhase | [ResumeListeningRequest](#lugo-ResumeListeningRequest) | [ResumeListeningResponse](#lugo-ResumeListeningResponse) |  |

 



<a name="server-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## server.proto



<a name="lugo-Ball"></a>

### Ball
Stores all ball attributes


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| position | [Point](#lugo-Point) |  | Current position |
| velocity | [Velocity](#lugo-Velocity) |  | Current velocity. It will be the exactly same velocity as the ball holder when a player is holding it. |
| holder | [Player](#lugo-Player) |  | Player that is currently holding the ball. Null if the ball is not holden. |






<a name="lugo-Catch"></a>

### Catch
Order to try to catch the ball. The player can only catch the ball when the player is touching the ball.
Only one catching order can be executed in a turn. So, if more than one player try to catch the ball in the same
turn, the first processed catch order will succeed, and the next ones will fail.






<a name="lugo-GameSnapshot"></a>

### GameSnapshot
GameSnapshot stores all game elements data.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| state | [GameSnapshot.State](#lugo-GameSnapshot-State) |  | The game state defines which phase the game is. The phase determine what the server is doing, are going to do, or what it is waiting for. |
| turn | [uint32](#uint32) |  | Turns counter. It starts from 1, but before the match starts, it may be zero. |
| home_team | [Team](#lugo-Team) |  | Store the home team elements. |
| away_team | [Team](#lugo-Team) |  | Store the away team elements. |
| ball | [Ball](#lugo-Ball) |  | Store the ball element. |
| turns_ball_in_goal_zone | [uint32](#uint32) |  | number of turns the ball is in a goal zone |
| shot_clock | [ShotClock](#lugo-ShotClock) |  | Store the shot clock to control ball possession limit |






<a name="lugo-JoinRequest"></a>

### JoinRequest
JoinRequest define the player configuration to the game.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| token | [string](#string) |  | Only used in official matches to guarantee that only one process will assume that player position (team and number). The bot process will receive this token as an argument, and must send it to the server in this message. |
| protocol_version | [string](#string) |  | Identifies the protocol version of the bot. |
| team_side | [Team.Side](#lugo-Team-Side) |  | Identify the bot&#39;s team side (Team_Home or Team_Away) |
| number | [uint32](#uint32) |  | Player&#39;s number 1-11 |
| init_position | [Point](#lugo-Point) |  | Position where the player must be set at &#34;GetReady&#34; state (at beginning of the match or after a goal) |






<a name="lugo-Jump"></a>

### Jump
Changes the goalkeepers velocity in a higher speed.
The goalkeepers may move kicker than other players when they jump, however the jump movement cannot be interrupted
after triggered. (read specs to find out the number of turns the jump lasts)


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| velocity | [Velocity](#lugo-Velocity) |  | Goalkeeper&#39;s velocity during the jump. |






<a name="lugo-Kick"></a>

### Kick
The kick order is only executed by the ball holder, and it is processed immediately.
Important: The kick velocity is summed to the current ball velocity.
The kick speed will suffer a power reduction proportionally to the player direction when the kick is not in the
same direction of the player direction. The reduction is calculated based on the angle with the player direction
using the formula `SpeedReducerFactor = 0.5 &#43; (0.5 * ((180 - ang) / 180))`
In summary, the speed will by reduced proportionally to the angle from 100% at 0 degrees until the limit of
50% at 180 degrees.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| velocity | [Velocity](#lugo-Velocity) |  | Kick velocity (it won&#39;t be necessarily the final ball velocity) |






<a name="lugo-Move"></a>

### Move
Order to ask the server to change the player velocity (direction and speed).
This order replaces the current player velocity, and the new velocity attribute will be immediately processed
in that turn. There is a limit speed to the player. The server will cap the velocity if the request is higher than
the limit.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| velocity | [Velocity](#lugo-Velocity) |  | The nex Velocity |






<a name="lugo-Order"></a>

### Order
Order to the game server. To be sent by players during the Listening phase.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| move | [Move](#lugo-Move) |  |  |
| catch | [Catch](#lugo-Catch) |  |  |
| kick | [Kick](#lugo-Kick) |  |  |
| jump | [Jump](#lugo-Jump) |  |  |






<a name="lugo-OrderResponse"></a>

### OrderResponse
Message sent to the player as a response after sending a order set to the the server.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| code | [OrderResponse.StatusCode](#lugo-OrderResponse-StatusCode) |  | Define if the order will be correctly processed. |
| details | [string](#string) |  | String message used for debugging proposes. |






<a name="lugo-OrderSet"></a>

### OrderSet
Message containing the orders the player want to send to the server in that turn.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| turn | [uint32](#uint32) |  | Turn which this order set should be processed at. |
| orders | [Order](#lugo-Order) | repeated | List of orders in the expected order of execution |
| debug_message | [string](#string) |  | String message used for debugging proposes. |






<a name="lugo-Player"></a>

### Player
Stores all player attributes


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| number | [uint32](#uint32) |  | Number of this player in its team (1-11) |
| position | [Point](#lugo-Point) |  | Current player position |
| velocity | [Velocity](#lugo-Velocity) |  | Current player velocity |
| team_side | [Team.Side](#lugo-Team-Side) |  | Team side which its playing in (it&#39;s used to speed up some readings since the player element will be in a list of players of a team) |
| init_position | [Point](#lugo-Point) |  | Default position when it&#39;s position is reset |
| is_jumping | [bool](#bool) |  | indicates the the player is jumping (goalkeepers only) |






<a name="lugo-ShotClock"></a>

### ShotClock
Stores the side of the team in attack and the time remaining holding the ball.
The team side is changed as soon a bot of the defense team catch the ball.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| team_side | [Team.Side](#lugo-Team-Side) |  | Team side of the team in attack. |
| remaining_turns | [uint32](#uint32) |  | Remaining turns the attack team may hold the ball |






<a name="lugo-Team"></a>

### Team
Stores all team elements and data.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| players | [Player](#lugo-Player) | repeated | List of player in the team |
| name | [string](#string) |  | Team name |
| score | [uint32](#uint32) |  | Team score in the present turn |
| side | [Team.Side](#lugo-Team-Side) |  | Side which the team is playing on. |





 


<a name="lugo-GameSnapshot-State"></a>

### GameSnapshot.State


| Name | Number | Description |
| ---- | ------ | ----------- |
| WAITING | 0 | The game is waiting for all players be connected. There is a configurable time limit to wait for players. After this limit expires, the match is considered over. |
| GET_READY | 1 | The game resets the players position to start the match or to restart the match after a goal. |
| LISTENING | 2 | The game is waiting for players orders. There is a configurable time window for this phase. After the time limit expires, the server will ignore the missing orders and process the ones it got. (when running on dev mode, the server may allow different behaviours) |
| PLAYING | 3 | The game is executing the players&#39; orders in the same sequence they were gotten. If the ball is NOT been holden, its velocity will be processed first. Otherwise, it position will be updated when the ball holder movement be processed. If there is no movement orders from a player, but it has speed greater than 0, it will be processed after all its orders are processed. Each player orders will be processed in the same sequence they were included in the message (e.g. first move, than kick) The ball kick is processed immediately after the order (the ball position is updated as its new velocity after the kick) |
| SHIFTING | 4 | The game interrupt the match to shift the ball possession. It happens only when the shot time is over (see shot_clock property). The ball will be given to the goalkeeper of the defense team, and the next state will &#34;listening&#34;, so the bots will not have time to rearrange before the next turn. |
| OVER | 99 | The game may be over after any phase. It can be over after Waiting if there is no players connected after the time limit for connections It can be over after GetReady or Listening if there is no enough players (e.g. connection lost) And it also can be over after Playing state if that was the last turn of the match. |



<a name="lugo-OrderResponse-StatusCode"></a>

### OrderResponse.StatusCode


| Name | Number | Description |
| ---- | ------ | ----------- |
| SUCCESS | 0 |  |
| UNKNOWN_PLAYER | 1 |  |
| NOT_LISTENING | 2 |  |
| WRONG_TURN | 3 |  |
| OTHER | 99 |  |



<a name="lugo-Team-Side"></a>

### Team.Side


| Name | Number | Description |
| ---- | ------ | ----------- |
| HOME | 0 | Team playing on the left side of field |
| AWAY | 1 | Team playing on the right side of the field |


 

 


<a name="lugo-Game"></a>

### Game
Service provided by the game service to the players (clients).

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| JoinATeam | [JoinRequest](#lugo-JoinRequest) | [GameSnapshot](#lugo-GameSnapshot) stream | JoinATeam allows the player to listen the server during the match. |
| SendOrders | [OrderSet](#lugo-OrderSet) | [OrderResponse](#lugo-OrderResponse) | SendOrders allows the player to send others to the server when the game is on listening state. |

 



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

