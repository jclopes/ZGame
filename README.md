zgame
=====

TODO:
-----
- Network
  - server send world status + next round id
  - server receive user input from clients
  - clients send user input to server

- UI
  - server selection screen

- Game Logic
  - set right subscriptions to events
  - implement the input events
  - direction using vector
  - collission resolution

- Data model
  - state basic data model: field, areas, players

- Other
  - input config file: mapping file from controller to input
  - pass connection parameters on command line


Development Notes:
------------------
The game engine is a colection of systems that take care of a specific task.
The communication between systems uses a publish/subscriber queue.

For the first iteration of the game the server will be the authority of the game state and the game will work in fake realtime by having the server asking each turn what is the input from each client and then updating the game status.
