"""
The MIT License (MIT)

Copyright (c)2013 Rich Friedel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
##################################################
#                 !IMPORTANT!                    #
# You must have PyGame installed for this to run #
# Download: http://www.pygame.org/download.shtml #
##################################################
import random
import sys
import pygame

if not pygame.font:
    print('Warning! PyGame fonts disabled!')
else:
    pygame.font.init()

white_color = pygame.Color(255, 255, 255)
orange_color = pygame.Color(245, 123, 0)
green_color = pygame.Color(21, 115, 16)

frame_width = 802
frame_height = 152
card_width = 50

card_exposed = []
cards_position = []


def new_game():
    """
    Initializes or resets all values to their default state
    """
    global player_turns, player_tick, card_values, card_matches, cards_played

    # Set Player Up
    player_turns, player_tick = 0, 0

    # Build deck
    card_values = []
    card_values.extend(range(1, 9))
    card_values.extend(range(1, 9))
    random.shuffle(card_values)

    # Setup card lists
    card_matches = [-1, -1]
    cards_played = [-1, -1]

    # Clear the position and exposed lists
    cards_position[:] = []
    card_exposed[:] = []

    for x_pos in range(16):
        # Create card positions
        cards_position.append([[x_pos * card_width, 50], [x_pos * card_width + 50, 50], [x_pos * card_width + 50, 150],
                               [x_pos * card_width, 150]])
        # While we are at it, inject all the card exposed values
        card_exposed.append(False)


def frame():
    """
    Creates a new game surface for the game to run in
    """
    new_game()

    # Create the surface
    _game_surface = pygame.display.set_mode((frame_width, frame_height))

    # Set the title
    pygame.display.set_caption("The Memory Game")

    # Create our game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Call the keydown handler with the key code
                keydown_handler(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouseclick_handler(pygame.mouse.get_pos())

        # Draw to surface
        draw_handler(_game_surface)


# Event Handlers
def draw_handler(surface):
    # Clear surface
    surface.fill((0, 0, 0))

    # Draw the cards
    for i in range(16):
        if not card_exposed[i]:
            pygame.draw.polygon(surface, green_color, (cards_position[i]))
            pygame.draw.polygon(surface, orange_color, (cards_position[i]), 2)
        else:
            pygame.draw.polygon(surface, orange_color, (cards_position[i]), 2)
            draw_text_helper(surface, card_values[i], (i * card_width + 15, 80), 64, white_color)

    # Draw player turns
    draw_text_helper(surface, "Turns: " + str(player_turns), (5, 8), 52, white_color)

    # Draw reset instructions
    draw_text_helper(surface, "Click 'N' to start a new game", (450, 12), 36, white_color)

    pygame.display.update()


def mouseclick_handler(pos):
    """
    Invoked when the user performs a mouse click.
    """
    global player_turns, player_tick

    # This will be where the card is in the list of cards
    card_index = 0

    # Iterate through the cards
    for card in cards_position:
        # Get the click position
        if card[0][0] <= pos[0] < card[1][0] and pos[1] > 50:
            if not card_exposed[card_index]:
                # If this is the very first time selecting a card OR if this is
                # the second selection the player has made...
                if player_tick <= 1:
                    card_exposed[card_index] = True
                    cards_played[player_tick] = card_index

                    # Check to see if this is the second selection
                    if player_tick == 1:
                        # Increment the turn
                        player_turns += 1

                        # Check for match
                        if card_values[cards_played[0]] == card_values[cards_played[1]]:
                            # Take the matched cards out of play
                            card_matches.extend([cards_played[0], cards_played[1]])

                    player_tick += 1
                else:
                    if cards_played[0] not in card_matches:
                        # Flip them back over
                        card_exposed[cards_played[0]] = False
                        card_exposed[cards_played[1]] = False

                    card_exposed[card_index] = True
                    cards_played[0] = card_index
                    player_tick = 1
        else:
            card_index += 1


def keydown_handler(event_key):
    """
    Invoked when the user presses a keyboard key
    """
    if event_key == 110:
        new_game()


# Helper
def draw_text_helper(surface, value, pos, size, color, font="sans-serif"):
    _font_object = pygame.font.Font(pygame.font.match_font(font), size)
    _font_draw = _font_object.render(str(value), True, color)
    surface.blit(_font_draw, pos)


def main():
    frame()


if __name__ == '__main__':
    main()