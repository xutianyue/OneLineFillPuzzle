'''
EN.540.635 Software Carpentry
Final Project

Title: One Line Fill Puzzle
Description: A puzzle game where the player needs to fill the grid with one line. The player can only move in four directions: up, down, left, and right.
The game has multiple levels, and the player can select the level to play. The player can also view the rules of the game and adjust the volume.
The game also records the completion time and the number of stars the player gets based on the completion time. The player can view the completion time and stars.
The script is also able to solve the puzzles. Of course, the player can also view the answer(s) to the puzzle.
Enjoy the game!

Author: Xilei Huang, Tianyue Xu
Date: 2024-05-01
'''

import pygame
import sys
import numpy as np
import json
import copy

def draw_text(text, font, color, surface, x, y):
    '''
    Draw text on the screen
    
    *** Parameters ***
        text: str - The text to be displayed
        font: pygame.font.Font - The font of the text
        color: tuple - The color of the text
        surface: pygame.Surface - The surface to draw the text on
        x: int - The x-coordinate of the text
        y: int - The y-coordinate of the text
    
    *** Returns ***
        None
    '''
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
    
def load_game_data():
    '''Load game data from file'''
    try:
        with open('game_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("No previous game data found.")
        return {}
    except json.JSONDecodeError:
        print("Game data is corrupted.")
        return {}
        
def save_game_data(data):
    '''
    Save game data(records) to file
    
    *** Parameters ***
        data: dict - The game data to be saved
    
    *** Returns ***
        None
    '''
    if data:
        with open('game_data.json', 'w') as file:
            json.dump(data, file, indent=4)
        print("Game data saved successfully.")
    else:
        print("No game data to save.")

def draw_slider(volume):
    '''
    Draw the volume slider on the screen
    
    *** Parameters ***
        volume: float - The volume of the music
    
    *** Returns ***
        knob_rect: pygame.Rect - The rectangle of the knob
    '''
    # Calculate the knob position
    knob_x = slider_rect.x + (slider_rect.width * volume) - (knob_width // 2)
    knob_rect = pygame.Rect(knob_x, slider_rect.y - 5, knob_width, knob_height)
    # Draw the slider
    pygame.draw.rect(screen, LIGHT_PINK, slider_rect)
    # Draw the knob
    pygame.draw.rect(screen, PURPLE, knob_rect)
    return knob_rect

def adjust_volume(x):
    '''
    Adjust the volume based on the knob position
    
    *** Parameters ***
        x: int - The x-coordinate of the knob
        
    *** Returns ***
        volume: float - The volume of the music
    '''
    # Calculate the volume based on the knob position
    volume = (x - slider_rect.x) / slider_rect.width
    pygame.mixer.music.set_volume(volume)
    button_sound.set_volume(volume)
    return volume

def main_menu():
    """Main menu of the game"""
    dragging = False  # Whether the knob is being dragged
    global global_volume  
    while True:
        screen.fill(WHITE)
        draw_text("One Line Fill Puzzle", title_font, PURPLE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        # Draw buttons
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 - 50, BUTTON_WIDTH, BUTTON_HEIGHT)
        rules_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT)
        quit_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 + 150, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, LIGHT_PINK, start_button, border_radius=20)
        pygame.draw.rect(screen, LIGHT_PINK, rules_button, border_radius=20)
        pygame.draw.rect(screen, LIGHT_PINK, quit_button, border_radius=20)
        draw_text("Start", button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text("Rules", button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        draw_text("Quit", button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)

        # Draw the volume icon
        screen.blit(volume_icon, (slider_rect.left - 40, slider_rect.y - 10))

        # Draw the volume slider
        knob_rect = draw_slider(global_volume)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                button_sound.play()
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                mouse_pos = event.pos
                # Start the game
                if start_button.collidepoint(mouse_pos):
                    level_select_menu()
                # Show the rules
                elif rules_button.collidepoint(mouse_pos):
                    rules_menu()
                # Adjust the volume
                elif knob_rect.collidepoint(mouse_pos):
                    dragging = True
                # Quit the game
                elif quit_button.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    # Update the knob position
                    new_x = max(min(event.pos[0], slider_rect.right - knob_width / 2), slider_rect.left + knob_width / 2)
                    global_volume = adjust_volume(new_x)
                        
def rules_menu():
    """Rules menu of the game"""
    # Load the rules image
    rules_image = pygame.image.load('rules.jpg')
    image_rect = rules_image.get_rect()

    while True:
        screen.fill(WHITE)

        # Draw the back button
        back_button = pygame.Rect(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, LIGHT_PINK, back_button, border_radius=20)
        draw_text("Back", button_font, BLACK, screen, 10 + BUTTON_WIDTH // 2, 10 + BUTTON_HEIGHT // 2)

        # Draw the rules image
        image_x = (SCREEN_WIDTH - image_rect.width ) // 2
        image_y = (SCREEN_HEIGHT - image_rect.height ) // 2 + 20  # 20 pixels below the center
        screen.blit(rules_image, (image_x, image_y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                mouse_pos = event.pos
                if back_button.collidepoint(mouse_pos):
                    return

def level_select_menu():
    """Level select menu of the game"""
    while True:
        screen.fill(WHITE) # Clear the screen
        # Title
        draw_text("Level Select", button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8)

        # Draw the level buttons
        level_buttons = []
        for i in range(1, 26):
            # Calculate the position of the button
            col = (i - 1) % 5
            row = (i - 1) // 5
            button_x = SCREEN_WIDTH // 2 - (BUTTON_WIDTH * 5 + BUTTON_GAP * 4) // 2 + col * (BUTTON_WIDTH + BUTTON_GAP)
            button_y = 150 + row * (BUTTON_HEIGHT + BUTTON_GAP)
            
            button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(screen, LIGHT_PINK, button_rect, border_radius=20)
            draw_text(str(i), button_font, BLACK, screen, button_x + BUTTON_WIDTH // 2, button_y + BUTTON_HEIGHT // 2)
            level_buttons.append(button_rect)

            # Draw stars
            key = str(i)
            if key in levels_completed:
                stars_count = levels_completed[key]['stars']
                for j in range(stars_count):
                    star_x = button_x + (j * star_width)
                    star_y = button_y + 3 * BUTTON_HEIGHT // 4   # Stars are 3/4 down the button
                    screen.blit(star_icon, (star_x, star_y))
                    
        # Draw the back button
        back_button = pygame.Rect(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, LIGHT_PINK, back_button, border_radius=20)
        draw_text("Back", button_font, BLACK, screen, 10  + BUTTON_WIDTH // 2, 10 + BUTTON_HEIGHT // 2)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                mouse_pos = event.pos
                if back_button.collidepoint(mouse_pos):
                    main_menu()
                for i, button_rect in enumerate(level_buttons):
                    if button_rect.collidepoint(mouse_pos):
                        level = i + 1
                        play_level(level)

def fill_grid(current_grid, cursor_x, cursor_y, start_x, start_y):
    '''
    Fills the grid based on the current cursor position and the start position.
    
    *** Parameters ***
        current_grid: list - The current grid configuration
        cursor_x: int - The x-coordinate of the cursor
        cursor_y: int - The y-coordinate of the cursor
        start_x: int - The x-coordinate of the start position
        start_y: int - The y-coordinate of the start position
    
    *** Returns ***
        None
    '''
    grid_height = len(current_grid) * 50
    grid_width = len(current_grid[0]) * 50

    # Calculate the starting position of the grid
    start_x_px = (SCREEN_WIDTH - grid_width) // 2
    start_y_px = (SCREEN_HEIGHT - grid_height) // 2

    # Draw the grid
    for y, row in enumerate(current_grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(start_x_px + x * 50, start_y_px + y * 50, 50, 50)
            color = WHITE if cell == 0 else LIGHT_PINK if cell == 1 else PURPLE
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            
    # Draw the start position
    pygame.draw.rect(screen, LIGHT_PINK, (start_x_px + start_x * 50, start_y_px + start_y * 50, 50, 50))
    # Draw the cursor
    pygame.draw.rect(screen, PINK, (start_x_px + cursor_x * 50, start_y_px + cursor_y * 50, 50, 50), 3)

def draw_path(screen, pre_x, pre_y, current_grid):
    '''
    Draws the path based on previous positions and the current grid configuration.
    
    *** Parameters ***
        screen: pygame.Surface - The screen to draw the path on
        pre_x: list - The previous x-coordinates
        pre_y: list - The previous y-coordinates
        current_grid: list - The current grid configuration
    
    *** Returns ***
        None
    '''
    grid_height = len(current_grid) * 50
    grid_width = len(current_grid[0]) * 50

    start_x_px = (SCREEN_WIDTH - grid_width) // 2
    start_y_px = (SCREEN_HEIGHT - grid_height) // 2

    for i in range(len(pre_x) - 1):
        pygame.draw.line(screen, PINK,
                         (start_x_px + pre_x[i] * 50 + 25, start_y_px + pre_y[i] * 50 + 25),
                         (start_x_px + pre_x[i+1] * 50 + 25, start_y_px + pre_y[i+1] * 50 + 25), 3)

def play_level(level):
    '''
    Play the selected level
    
    *** Parameters ***
        level: int - The level to play
    
    *** Returns ***
        None
    '''
    running = True

    grid = levels[level - 1]["grid"]
    start_x, start_y = levels[level - 1]["start"]
    cursor_x, cursor_y = start_x, start_y
    pre_x = [cursor_x]
    pre_y = [cursor_y]
    # Initialize the grid
    current_grid = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    # Fill the grid based on the level configuration
    grid_fill_count = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'x':
                grid_fill_count += 1
                current_grid[y][x] = -1
    # Set the start position
    current_grid[start_y][start_x] = 1
    
    grid_fill_count = len(current_grid) * len(current_grid[0]) - grid_fill_count
    current_fill_count = 1

    start_time = pygame.time.get_ticks()  # Get the start time
    while running:
        # Draw the screen
        screen.fill(WHITE)

        draw_text(f"Level {level}", button_font, BLACK, screen, SCREEN_WIDTH // 2, 10 + BUTTON_HEIGHT // 2)

        # Draw the back button
        back_button = pygame.Rect(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, GRAY, back_button, border_radius=20)
        draw_text("Back", button_font, BLACK, screen, 10 + BUTTON_WIDTH // 2, 10 + BUTTON_HEIGHT // 2)

        # Draw the answer button
        answer_button = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - 10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, GRAY, answer_button, border_radius=20)
        draw_text("Answer", button_font, BLACK, screen, SCREEN_WIDTH - BUTTON_WIDTH // 2 - 10, 10+BUTTON_HEIGHT // 2)

        # Draw the reset button
        reset_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 10, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, GRAY, reset_button, border_radius=20)
        draw_text("Reset", button_font, BLACK, screen, SCREEN_WIDTH // 2, 10 + BUTTON_HEIGHT // 2)

        # Fill the grid
        fill_grid(current_grid, cursor_x, cursor_y, start_x, start_y)
        
        # Draw the path
        x_path = pre_x.copy()
        x_path.append(cursor_x)
        y_path = pre_y.copy()
        y_path.append(cursor_y)

        draw_path(screen, x_path, y_path, current_grid)

        # Update the screen
        pygame.display.update()

        # Check if the level is completed
        # Check if the current grid is filled
        current_fill_count = 0
        for y, row in enumerate(current_grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    current_fill_count += 1
                    
        if current_fill_count == grid_fill_count:
            end_time = pygame.time.get_ticks()  # Get the end time
            completion_time = (end_time - start_time) / 1000

            # Get the stars based on the completion time
            if completion_time <= 30:
                stars = 3
            elif completion_time <= 60:
                stars = 2
            else:
                stars = 1
        
            # Update the levels completed data
            if str(level) not in levels_completed or \
            completion_time < levels_completed[str(level)]['time']:
                levels_completed[str(level)] = {'time': completion_time, 'stars': stars}
                save_game_data(levels_completed)
                
            # Show the completion screen
            pygame.time.wait(700)
            screen.fill(WHITE)
            pygame.display.update()
            pygame.mixer.music.stop()
            # Load the congrats music
            pygame.mixer.music.load(congrats_music)
            pygame.mixer.music.play(0)  # 0 means play once
            pygame.time.wait(200)
            current_music = 'congrats'
            # Show the completion screen
            while True:
                screen.fill(WHITE)
                draw_text(f"Level {level}", button_font, BLACK, screen, SCREEN_WIDTH // 2, 10 + BUTTON_HEIGHT // 2)
                draw_text("You Win!", button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

                draw_text(f"Completion Time: {completion_time:.2f} s", button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 40)
                if stars == 3:
                    screen.blit(star_icon, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 4 + 60))
                    screen.blit(star_icon, (SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 4 + 60))
                    screen.blit(star_icon, (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 4 + 60))
                elif stars == 2:
                    screen.blit(star_icon, (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 4 + 60))
                    screen.blit(star_icon, (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 4 + 60))
                elif stars == 1:
                    screen.blit(star_icon, (SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 4 + 60))
                
                back_to_level_select_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
                replay_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 + 40, BUTTON_WIDTH, BUTTON_HEIGHT)
                next_level_button = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + 80, BUTTON_WIDTH + 10, BUTTON_HEIGHT)

                pygame.draw.rect(screen, LIGHT_PINK, back_to_level_select_button, border_radius=20)
                draw_text("Back", button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2)

                pygame.draw.rect(screen, LIGHT_PINK, replay_button, border_radius=20)
                draw_text("Replay", button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

                pygame.draw.rect(screen, LIGHT_PINK, next_level_button, border_radius=20)
                draw_text("Next", button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT // 2 + 80)

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        button_sound.play()
                        mouse_pos = event.pos
                        if back_to_level_select_button.collidepoint(mouse_pos):
                            level_select_menu()
                        if replay_button.collidepoint(mouse_pos):
                            play_level(level)

                        elif next_level_button.collidepoint(mouse_pos):
                            # If it's the last level, return to level select menu
                            if level == len(levels):
                                level_select_menu()
                            else:
                                play_level(level + 1)
                    if event.type == MUSIC_END:
                        if current_music == 'congrats':
                            # If the congrats music ends, play the background music
                            pygame.time.wait(500)
                            pygame.mixer.music.load(bg_music)
                            pygame.mixer.music.play(-1)
                            current_music = 'bg'
                            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                mouse_pos = event.pos
                
                # Return to the level select menu
                if back_button.collidepoint(mouse_pos):
                    level_select_menu()

                # Show the answer
                elif answer_button.collidepoint(mouse_pos):
                    show_answer(level)

                # Reset the grid
                elif reset_button.collidepoint(mouse_pos):
                    for y, row in enumerate(current_grid):
                        for x, cell in enumerate(row):
                            if not(x == start_x and y == start_y) and cell == 1:
                                current_grid[y][x] = 0
                    cursor_x, cursor_y = start_x, start_y
                    pre_x = [cursor_x]
                    pre_y = [cursor_y]
                    
            elif event.type == pygame.KEYDOWN:
                button_sound.play()
                # Move the cursor
                ## UP
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    # If out of bounds, do nothing
                    if cursor_y == 0:
                        continue
                    # If the cell cannot be filled, do nothing
                    if current_grid[cursor_y-1][cursor_x] == -1:
                        continue
                    # If the cell is filled and not the previous cell, do nothing
                    if current_grid[cursor_y-1][cursor_x] == 1 and (cursor_x, cursor_y-1) != (pre_x[-1], pre_y[-1]):
                        continue
                    # If the cell is the previous cell, remove the previous cell
                    if (cursor_x, cursor_y-1) == (pre_x[-1], pre_y[-1]):
                        pre_x.pop()
                        pre_y.pop()
                        # Remove the current cell
                        current_grid[cursor_y][cursor_x] = 0
                        cursor_y = max(0, cursor_y - 1)
                    else:
                        # Add the current cell to the path
                        pre_x.append(cursor_x)
                        pre_y.append(cursor_y)
                        cursor_y = max(0, cursor_y - 1)
                        current_grid[cursor_y][cursor_x] = 1
                ## DOWN
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if cursor_y == len(current_grid) - 1:
                        continue
                    if current_grid[cursor_y + 1][cursor_x] == -1:
                        continue
                    if current_grid[cursor_y + 1][cursor_x] == 1 and (cursor_x, cursor_y + 1) != (pre_x[-1], pre_y[-1]):
                        continue
                    if (cursor_x, cursor_y + 1) == (pre_x[-1], pre_y[-1]):
                        pre_x.pop()
                        pre_y.pop()
                        current_grid[cursor_y][cursor_x] = 0
                        cursor_y = min(len(current_grid) - 1, cursor_y + 1)
                    else:
                        pre_x.append(cursor_x)
                        pre_y.append(cursor_y)
                        cursor_y = min(len(current_grid) - 1, cursor_y + 1)
                        current_grid[cursor_y][cursor_x] = 1
                    
                ## LEFT
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if cursor_x == 0:
                        continue
                    if current_grid[cursor_y][cursor_x - 1] == -1:
                        continue
                    if current_grid[cursor_y][cursor_x - 1] == 1 and (cursor_x - 1, cursor_y) != (pre_x[-1], pre_y[-1]):
                        continue
                    if (cursor_x - 1, cursor_y) == (pre_x[-1], pre_y[-1]):
                        pre_x.pop()
                        pre_y.pop()
                        current_grid[cursor_y][cursor_x] = 0
                        cursor_x = max(0, cursor_x - 1)
                    else:
                        pre_x.append(cursor_x)
                        pre_y.append(cursor_y)
                        cursor_x = max(0, cursor_x - 1)
                        current_grid[cursor_y][cursor_x] = 1
                        
                ## RIGHT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if cursor_x == len(current_grid[0]) - 1:
                        continue
                    if current_grid[cursor_y][cursor_x + 1] == -1:
                        continue
                    if current_grid[cursor_y][cursor_x + 1] == 1 and (cursor_x + 1, cursor_y) != (pre_x[-1], pre_y[-1]):
                        continue
                    if (cursor_x + 1, cursor_y) == (pre_x[-1], pre_y[-1]):
                        pre_x.pop()
                        pre_y.pop()
                        current_grid[cursor_y][cursor_x] = 0
                        cursor_x = min(len(current_grid[0]) - 1, cursor_x + 1)
                    else:
                        pre_x.append(cursor_x)
                        pre_y.append(cursor_y)
                        cursor_x = min(len(current_grid[0]) - 1, cursor_x + 1)
                        current_grid[cursor_y][cursor_x] = 1
                        
                # UNDO
                elif event.key == pygame.K_z:
                    if len(pre_x) > 1:
                        current_grid[cursor_y][cursor_x] = 0
                        cursor_x = pre_x.pop()
                        cursor_y = pre_y.pop()
                # RESET
                elif event.key == pygame.K_r:
                    for y, row in enumerate(current_grid):
                        for x, cell in enumerate(row):
                            if not(x == start_x and y == start_y) and cell == 1:
                                current_grid[y][x] = 0
                    cursor_x, cursor_y = start_x, start_y
                    pre_x = [cursor_x]
                    pre_y = [cursor_y]

def fill(grid, x, y, counter, total_o, solutions):
    '''
    Fill the grid recursively
    
    *** Parameters ***
        grid: list - The grid to fill
        x: int - The x-coordinate
        y: int - The y-coordinate
        counter: int - The counter
        total_o: int - The total number of 'o's
        solutions: list - The solutions
    
    *** Returns ***
        bool - True if a solution is found, False otherwise
    '''
    if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):  # if out of bounds
        return
    if grid[x][y] != 'o':  # if not an 'o'
        return

    # Mark
    grid[x][y] = counter

    # If all 'o's are filled
    if counter == total_o:
        # Add the solution
        solutions.append(copy.deepcopy(grid))
        if len(solutions) == 3:  # Stop after finding 3 solutions
            return True
        grid[x][y] = 'o'
        return False

    # Try filling in all directions
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
        if fill(grid, x + dx, y + dy, counter + 1, total_o, solutions):
            return True

    # If no solution is found, backtrack
    grid[x][y] = 'o'
    return False

def draw_answer(solution):
    '''
    Draw the answer on the screen
    
    *** Parameters ***
        solution: list - The solution to draw
    
    *** Returns ***
        None
    '''
    # Calculate the height and width of the grid
    grid_height = len(solution) * 50
    grid_width = len(solution[0]) * 50

    # Calculate the starting position of the grid
    start_x_px = (SCREEN_WIDTH - grid_width) // 2
    start_y_px = (SCREEN_HEIGHT - grid_height) // 2

    # Draw the grid
    for y, row in enumerate(solution):
        for x, cell in enumerate(row):
            rect = pygame.Rect(start_x_px + x * 50, start_y_px + y * 50, 50, 50)
            color = LIGHT_PINK if cell != 'x' else PURPLE
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Convert the solution to a numpy array
    solution = np.array(solution)
    n_fill = solution.shape[0] * solution.shape[1] - np.sum(solution == 'x')
    for i in range(n_fill - 1):
        y, x = np.where(solution == str(i + 1))
        y_next, x_next = np.where(solution == str(i + 2))

        # Calculate the points
        points = list(zip(start_x_px + x * 50 + 25, start_y_px + y * 50 + 25))
        next_points = list(zip(start_x_px + x_next * 50 + 25, start_y_px + y_next * 50 + 25))

        # Draw the lines
        for p1, p2 in zip(points, next_points):
            pygame.draw.line(screen, PINK, p1, p2, 3)

        # Draw the circles
        if i == 0:
            pygame.draw.circle(screen, PINK, points[0], 10)

def show_answer(level):
    '''
    Show the answer to the selected level
    
    *** Parameters ***
        level: int - The level to show the answer
    
    *** Returns ***
        None
    '''
    # Load the level data
    grid = levels[level - 1]["grid"]
    start_y, start_x = levels[level - 1]["start"]

    # Calculate the total number of 'o's
    total_o = sum(row.count('o') for row in grid)

    # Find the solutions
    solutions = []
    fill(grid, start_x, start_y, 1, total_o, solutions)

    current_solution_index = 0

    running = True
    while running:
        screen.fill(WHITE)
        draw_text(f"Answer {current_solution_index + 1}", button_font, BLACK, screen, SCREEN_WIDTH // 2, 10 + BUTTON_HEIGHT // 2)

        # Draw the back button
        close_button = pygame.Rect(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, GRAY, close_button, border_radius=20)
        draw_text("Close", button_font, BLACK, screen, 10 + BUTTON_WIDTH // 2, 10 + BUTTON_HEIGHT // 2)

        # Draw the answer
        draw_answer(solutions[current_solution_index])  # Draw the answer according to the current solution index

        # Draw the left and right buttons
        left_button = pygame.Rect(SCREEN_WIDTH // 2 - 100 - BUTTON_WIDTH, SCREEN_HEIGHT // 8 * 7, BUTTON_WIDTH, BUTTON_HEIGHT)
        right_button = pygame.Rect(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 8 * 7, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, GRAY, left_button, border_radius=20)
        pygame.draw.rect(screen, GRAY, right_button, border_radius=20)
        draw_text("<", button_font, BLACK, screen, left_button.centerx, left_button.centery)
        draw_text(">", button_font, BLACK, screen, right_button.centerx, right_button.centery)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                mouse_pos = event.pos
                if close_button.collidepoint(mouse_pos):
                    current_solution_index = 0
                    #running = False
                    return
                elif left_button.collidepoint(mouse_pos):
                    current_solution_index = (current_solution_index - 1) % len(solutions)  # Switch to the previous solution
                elif right_button.collidepoint(mouse_pos):
                    current_solution_index = (current_solution_index + 1) % len(solutions)  # Switch to the next solution
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    current_solution_index = (current_solution_index - 1) % len(solutions)  # Switch to the previous solution
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    current_solution_index = (current_solution_index + 1) % len(solutions)  # Switch to the next solution
        
    
if __name__ == '__main__':
    # Initialize the game
    pygame.init()

    # Initialize the mixer
    pygame.mixer.init()

    # Load the background music
    global_volume = 0.5 # Volume
    bg_music = 'time-for-a-burger.mp3'
    pygame.mixer.music.load(bg_music)
    congrats_music = 'bonus-points.mp3'
    current_music = 'bg'

    # Set the end event for the music
    MUSIC_END = pygame.USEREVENT
    pygame.mixer.music.set_endevent(MUSIC_END)

    # Set the volume
    pygame.mixer.music.set_volume(global_volume)
    # Play the music
    pygame.mixer.music.play(-1)

    # Load the button sound
    button_sound = pygame.mixer.Sound('sound.wav')
    button_sound.set_volume(global_volume)
    
    # Set the screen size
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Set the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    PINK = (255, 199, 199)
    LIGHT_PINK = (255, 226, 226)
    PURPLE = (135, 133, 162)

    # Button settings
    BUTTON_WIDTH = 120
    BUTTON_HEIGHT = 50
    BUTTON_GAP = 30

    # Font settings
    font_path = "Komigo3D-Regular.ttf"
    # font = pygame.font.SysFont(None, 40)
    title_font_size = 70
    button_font_size = 30
    title_font = pygame.font.Font(font_path, title_font_size)
    button_font = pygame.font.Font(font_path, button_font_size)

    # Initialize the screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("One Line Fill Puzzle")

    # Load the levels
    with open('levels.json', 'r') as f:
        levels = json.load(f)
        
    levels_completed = load_game_data()
    
    volume_icon = pygame.image.load('volume_icon_32.png').convert_alpha()
    star_icon = pygame.image.load('star.png').convert_alpha()
    star_width, star_height = star_icon.get_size()
    
    # Slider settings
    slider_pos =  SCREEN_WIDTH // 2 
    slider_width = 200
    slider_height = 10
    knob_width = 20
    knob_height = 20

    slider_rect = pygame.Rect(SCREEN_WIDTH // 2 - slider_width // 2, 550, slider_width, slider_height)  # The slider rectangle 
    main_menu()

