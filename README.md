zgame
=====

TODO:
-----
- Network
  - server send world status + next round id
  - server receive user input from clients
  - clients send user input to server

- UI
  - pick server screen
  - ...

- Game Logic
  - event pub/sub comonication between managers
  - implement user_input events


Development Notes:
------------------
The game engine is a colection of systems that take care of a specific task.
The communication between systems uses a publish/subscriber queue.

For the first iteration of the game the server will be the authority of the game state and the game will work in fake realtime by having the server asking each turn what is the input from each client and then updating the game status.
