# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<br>

# Version History
- `0.0.x` : End-to-end Flask PoC
- `0.1.x` : GitHub Actions
- `0.2.x` : Simple Tic Tac Toe (3 x 3)
- `0.3.x` : Implement ultimate edition (9 x 9)
- `0.4.x` : Add single player mode
- `0.5.x` : Implement push notifications
- `0.6.x` : UI Revamp
- `0.7.x` : Misc Improvements
- `1.0.x` : Initial release after user-tests

<br>

# Releases
<!-- @LatestFirst -->

## [1.0.1] - 09/12/23
- UMA-40: Add pythonic logging
- UMA-57: Bolster test suite

## [1.0.0] - 09/12/23
- UMA-46: Address security vulnerabilities
- UMA-59: [BUG] Address deployment issue caused by missing .git/.project-root (`from-root` lib)
- UMA-60: Add .gif to README
- UMA-61: Create architecture diagram

## [0.7.1] - 08/12/23
- UMA-55: Fix the test step in the GitHub Actions workflow
- UMA-56: Add tests for admin and login blueprint

## [0.7.0] - 06/12/23
- UMA-32: [BUG] If winning move is placed on the last square, the game ends in draw (ultimate only)
- UMA-49: Add delay in single player mode for the computer thinking time (randomised)
- UMA-53: Refresh playable square with game reset to allow first move to be anywhere (ultimate)

## [0.6.1] - 04/12/23
- UMA-47: Add user error for invalid move
- UMA-48: Add game instruction tooltip

## [0.6.0] - 02/12/23
- UMA-37: Create star field background
- UMA-38: Restyle login screen
- UMA-39: Restyle game screen

## [0.5.3] - 28/11/23
- UMA-33: Allow for parallel games through game-specific websocket channels

## [0.5.2] - 27/11/23
- UMA-35: [BUG] Set websocket URL based on environment

## [0.5.1] - 27/11/23
- UMA-34: [BUG] Broken deployment due to missing gevent installation

## [0.5.0] - 27/11/23
- UMA-30: Add the ability to display a message from the backend via message topic
- UMA-31: Implement websocket replacement throughout game flow for both game and player modes

## [0.4.1] - 18/11/23
- UMA-29: [BUG] Computer incorrectly places in already completed outer-squares (Ultimate)

## [0.4.0] - 18/11/23
- UMA-25: Add single player option to log in
- UMA-27: In standard mode, play computer's move after user has placed
- UMA-28: In ultimate mode, play computer's move after user has placed

## [0.3.2] - 15/11/23
- UMA-18: Add replay button

## [0.3.1] - 11/11/23
- UMA-26: [BUG] Draw Game Over message displayed on first load

## [0.3.0] - 11/11/23
- UMA-17: Give the user the option of standard or ultimate tic-tac-toe
- UMA-19: Create interactive 9x9 board and allow player to make a turn
- UMA-20: Force ultimate players to play in the correct square after a move is placed
- UMA-21: Make game completable through correct outer square selection and evaluation

## [0.2.1] - 07/11/2023
- UMA-11: Allow players to make their turns
- UMA-12: Display results to each player when the game is over
- UMA-13: Apply finishing touches to 3 x 3 game and refactor

## [0.2.0] - 28/10/2023
- UMA-10: Create interactive game board

## [0.1.2] - 22/10/2023
- UMA-5: Acquire domain name and set-up on repo/platform

## [0.1.1] - 21/10/2023
- UMA-4: Set-up GitHub action to build, test, release and deploy
- UMA-5: Acquire domain name and set-up on repo/platform

## [0.1.0] - 21/10/2023
- UMA-4: Set-up GitHub action to build, test, release and deploy

## [0.0.0] - 21/10/2023
- UMA-2: Create Flask MVP
- UMA-3: Deploy to Render (with Redis)
- UMA-9: Add project version and create a CHANGELOG

<br>

[0.0.0]: https://github.com/jrsmth/ultima/releases/tag/0.0.0
[0.1.0]: https://github.com/jrsmth/ultima/compare/0.0.0...0.1.0
[0.1.1]: https://github.com/jrsmth/ultima/compare/0.1.0...0.1.1
[0.1.2]: https://github.com/jrsmth/ultima/compare/0.1.1...0.1.2
[0.2.0]: https://github.com/jrsmth/ultima/compare/0.1.2...0.2.0
[0.2.1]: https://github.com/jrsmth/ultima/compare/0.2.0...0.2.1
[0.3.0]: https://github.com/jrsmth/ultima/compare/0.2.1...0.3.0
[0.3.1]: https://github.com/jrsmth/ultima/compare/0.3.0...0.3.1
[0.3.2]: https://github.com/jrsmth/ultima/compare/0.3.1...0.3.2
[0.4.0]: https://github.com/jrsmth/ultima/compare/0.3.2...0.4.0
[0.4.1]: https://github.com/jrsmth/ultima/compare/0.4.0...0.4.1
[0.5.0]: https://github.com/jrsmth/ultima/compare/0.4.1...0.5.0
[0.5.1]: https://github.com/jrsmth/ultima/compare/0.5.0...0.5.1
[0.5.2]: https://github.com/jrsmth/ultima/compare/0.5.1...0.5.2
[0.5.3]: https://github.com/jrsmth/ultima/compare/0.5.2...0.5.3
[0.6.0]: https://github.com/jrsmth/ultima/compare/0.5.3...0.6.0
[0.6.1]: https://github.com/jrsmth/ultima/compare/0.6.0...0.6.1
[0.7.0]: https://github.com/jrsmth/ultima/compare/0.6.1...0.7.0
[0.7.1]: https://github.com/jrsmth/ultima/compare/0.7.0...0.7.1
[1.0.0]: https://github.com/jrsmth/ultima/compare/0.7.1...1.0.0
[1.0.1]: https://github.com/jrsmth/ultima/compare/1.0.0...1.0.1