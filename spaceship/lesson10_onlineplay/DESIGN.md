# [Design Doc] Spaceship Online

## Design Sketch
### Requirement
* Multiplayer Online Game
  * Only one game is allowed 
  * User can choose to start or join the game from the main menu
### Architecture
#### Server
Server maintains a ServerWorld, which maintains objects locations and detect conflicts. It provides no drawing abilities.

Server maintains a single process queue, and one response queue for each client. A background thread reads(blocking) from the process queue, process incoming messages, and send the responses to response queues. Each incoming client connection is assigned a separate thread and a new response queue. The client thread reads from connection, and put incoming messages into server's process queue. It waits for response from response queue and reply back to the client.
#### Client
Clients maintain a local ClientWorld, which provide drawing abilities but do not update objects.

Clients use a one-thread loop to send operations to server, and wait for updated states from server. It uses the updated states to re-draw the local info.

#### Communication
Server and clients communicate through network. They exchange messages using pickle.

## Design Details
### Scenario 1: Start a new game
1. A client sends a StartGame message
2. Server checks if a World already exists (which means a game is in progress), and denys the request if so.
3. Server starts a new World
### Scenario 2: Join a game

### Scenario 3: Normal game play

### Scenario 4: Exit a game