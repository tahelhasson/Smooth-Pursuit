import pygame
import math

# Initialize pygame
pygame.init()

# Set screen dimensions
screen_width = 1400
screen_height = 750

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Smooth Pursuit")

# Set colors
background_color = (0, 0, 0)
gray_color = (169, 169, 169)  # Gray for the transition screen
ball_color = (255, 255, 255)  # White
ball_radius = 5

# Duration properties
durations = [2, 4, 6]  # Durations in seconds
frames_per_second = 120  # High frame rate for smooth motion
frames = [d * frames_per_second for d in durations]
speeds = [screen_width / f for f in frames]

# Obstacle properties
obstacle_colors = [(255, 0, 0), (0, 0, 0)]  # Red and black
obstacle_widths = [100, 300, 500]
obstacle_height = screen_height
obstacle_x = screen_width // 2
obstacle_y = screen_height // 2

# Time trackers
clock = pygame.time.Clock()

# Function to display instructions
def display_instructions():
    font = pygame.font.Font(None, 25)
    text_1 = font.render("wait", True, (0, 0, 0))
    screen.fill(gray_color)
    screen.blit(text_1, (screen_width // 2 - text_1.get_width() // 2, screen_height // 2))
    pygame.display.flip()

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 3000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

# Function to draw obstacles
def draw_obstacle_1(width, color, x_position):
    pygame.draw.rect(screen, color, (x_position - width // 2, 0, width, obstacle_height))

def draw_obstacle_2(width, color, x_position, y_position):
    pygame.draw.rect(screen, color, (x_position - width // 2, y_position - obstacle_height // 2, width, obstacle_height))


# Main loop for each code

def run_code_1():
    x_start = 0
    amplitude = screen_height // 16
    frequency = math.pi / (screen_width // 2)
    running = True

    while running:
        display_instructions()  # מציג את ההוראות בתחילת התוכנית

        for duration_index, duration_frames in enumerate(frames):
            speed = speeds[duration_index]

            # התחלת המסלול הרגיל (בלי מכשולים)
            time_elapsed = 0
            while time_elapsed < duration_frames:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # חישוב המיקום של הכדור לפי המהירות הרגילה
                x = x_start + time_elapsed * speed
                y = screen_height // 2 + int(amplitude * math.sin(frequency * x))
                ball_position = (int(x), int(y))

                # מלא את המסך בצבע הרקע
                screen.fill(background_color)

                # צייר את הכדור
                pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                # עדכן את המסך
                pygame.display.flip()

                # שלוט בקצב הפריימים
                clock.tick(frames_per_second)

                # עדכן את הזמן שחלף
                time_elapsed += 1

            pygame.display.flip()

            # הצגת ההוראות אחרי כל מסלול נוסף (ללא המתנה)
            display_instructions()
            pygame.display.flip()

            # הוספת מסלולים עם מכשולים
            for obstacle_color in obstacle_colors:
                for obstacle_width in obstacle_widths:
                    time_elapsed = 0
                    while time_elapsed < duration_frames:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

                        # חישוב המיקום של הכדור
                        x = x_start + time_elapsed * speed
                        y = screen_height // 2 + int(amplitude * math.sin(frequency * x))
                        ball_position = (int(x), int(y))

                        # מלא את המסך בצבע הרקע
                        screen.fill(background_color)

                        # צייר את הכדור
                        pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                        # צייר את המכשול רק אם הכדור בטווח
                        if obstacle_x - obstacle_width // 2 <= ball_position[0] <= obstacle_x + obstacle_width // 2:
                            draw_obstacle_1(obstacle_width, obstacle_color, obstacle_x)

                        # עדכן את המסך
                        pygame.display.flip()

                        # שלוט בקצב הפריימים
                        clock.tick(frames_per_second)

                        # עדכן את הזמן שחלף
                        time_elapsed += 1

                    # הצגת ההוראות אחרי סיום כל מסלול עם מכשולים
                    display_instructions()
                    pygame.display.flip()

        running = False




def run_code_2():
    running = True
    while running:
        display_instructions()  # מציג את ההוראות בתחילת התוכנית

        for duration_index, duration_frames in enumerate(frames):
            speed = speeds[duration_index]

            # Add normal path (no obstacles)
            time_elapsed = 0
            while time_elapsed < duration_frames:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Calculate ball position
                x = time_elapsed * speed
                y = screen_height // 2  # Fixed in the middle of the screen vertically
                ball_position = (int(x), int(y))

                # Fill the screen with the background color
                screen.fill(background_color)

                # Draw the ball
                pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                # Update the display
                pygame.display.flip()

                # Control the frame rate
                clock.tick(frames_per_second)

                # Update the time elapsed
                time_elapsed += 1

            # הצגת ההוראות אחרי כל מסלול רגיל (ללא מכשולים)
            display_instructions()
            pygame.display.flip()

            # Add paths with obstacles
            for obstacle_color in obstacle_colors:
                for obstacle_width in obstacle_widths:
                    time_elapsed = 0
                    while time_elapsed < duration_frames:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

                        # Calculate ball position
                        x = time_elapsed * speed
                        y = screen_height // 2  # Fixed in the middle of the screen vertically
                        ball_position = (int(x), int(y))

                        # Fill the screen with the background color
                        screen.fill(background_color)

                        # Draw the ball
                        pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                        # Draw the obstacle only if the ball is in range
                        if obstacle_x - obstacle_width // 2 <= ball_position[0] <= obstacle_x + obstacle_width // 2:
                            draw_obstacle_1(obstacle_width, obstacle_color, obstacle_x)

                        # Update the display
                        pygame.display.flip()

                        # Control the frame rate
                        clock.tick(frames_per_second)

                        # Update the time elapsed
                        time_elapsed += 1

                    # הצגת ההוראות אחרי כל מסלול עם מכשולים
                    display_instructions()
                    pygame.display.flip()

        running = False



def run_code_3():
    running = True
    while running:
        display_instructions()  # מציג את ההוראות בתחילת התוכנית

        for duration_index, duration_frames in enumerate(frames):
            speed = screen_width / duration_frames

            # Add normal path (no obstacles)
            time_elapsed = 0
            while time_elapsed < duration_frames:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Calculate ball position
                t = time_elapsed / duration_frames
                x = t * screen_width
                y = screen_height - t * screen_height  # Diagonal from bottom-left to top-right
                ball_position = (int(x), int(y))

                # Fill the screen with the background color
                screen.fill(background_color)

                # Draw the ball
                pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                # Update the display
                pygame.display.flip()

                # Control the frame rate
                clock.tick(frames_per_second)

                # Update the time elapsed
                time_elapsed += 1

            # הצגת ההוראות אחרי כל מסלול רגיל (ללא מכשולים)
            display_instructions()
            pygame.display.flip()

            # Add paths with obstacles
            for obstacle_color in obstacle_colors:
                for obstacle_width in obstacle_widths:
                    time_elapsed = 0
                    while time_elapsed < duration_frames:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

                        # Calculate ball position
                        t = time_elapsed / duration_frames
                        x = t * screen_width
                        y = screen_height - t * screen_height  # Diagonal from bottom-left to top-right
                        ball_position = (int(x), int(y))

                        # Fill the screen with the background color
                        screen.fill(background_color)

                        # Draw the ball
                        pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                        # Draw the obstacle only if the ball is in range
                        if obstacle_x - obstacle_width // 2 <= ball_position[0] <= obstacle_x + obstacle_width // 2 and \
                           screen_height // 2 - obstacle_height // 2 <= ball_position[1] <= screen_height // 2 + obstacle_height // 2:
                            draw_obstacle_2(obstacle_width, obstacle_color, obstacle_x, screen_height // 2)

                        # Update the display
                        pygame.display.flip()

                        # Control the frame rate
                        clock.tick(frames_per_second)

                        # Update the time elapsed
                        time_elapsed += 1

                    # הצגת ההוראות אחרי כל מסלול עם מכשולים
                    display_instructions()
                    pygame.display.flip()

        running = False


def run_code_4():
    running = True
    while running:
        display_instructions()  # מציג את ההוראות בתחילת התוכנית

        for duration_index, duration_frames in enumerate(frames):
            speed = screen_width / duration_frames

            # Add normal path (no obstacles)
            time_elapsed = 0
            while time_elapsed < duration_frames:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Calculate ball position (from top-left to bottom-right)
                t = time_elapsed / duration_frames
                x = t * screen_width
                y = t * screen_height  # Diagonal from top-left to bottom-right
                ball_position = (int(x), int(y))

                # Fill the screen with the background color
                screen.fill(background_color)

                # Draw the ball
                pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                # Update the display
                pygame.display.flip()

                # Control the frame rate
                clock.tick(frames_per_second)

                # Update the time elapsed
                time_elapsed += 1

            # הצגת ההוראות אחרי כל מסלול רגיל (ללא מכשולים)
            display_instructions()
            pygame.display.flip()

            # Add paths with obstacles
            for obstacle_color in obstacle_colors:
                for obstacle_width in obstacle_widths:
                    time_elapsed = 0
                    while time_elapsed < duration_frames:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

                        # Calculate ball position
                        t = time_elapsed / duration_frames
                        x = t * screen_width
                        y = t * screen_height  # Diagonal from top-left to bottom-right
                        ball_position = (int(x), int(y))

                        # Fill the screen with the background color
                        screen.fill(background_color)

                        # Draw the ball
                        pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                        # Draw the obstacle only if the ball is in range
                        if obstacle_x - obstacle_width // 2 <= ball_position[0] <= obstacle_x + obstacle_width // 2 and \
                           screen_height // 2 - obstacle_height // 2 <= ball_position[1] <= screen_height // 2 + obstacle_height // 2:
                            draw_obstacle_2(obstacle_width, obstacle_color, obstacle_x, screen_height // 2)

                        # Update the display
                        pygame.display.flip()

                        # Control the frame rate
                        clock.tick(frames_per_second)

                        # Update the time elapsed
                        time_elapsed += 1

                    # הצגת ההוראות אחרי כל מסלול עם מכשולים
                    display_instructions()
                    pygame.display.flip()

        running = False

def run_code_5():
    running = True
    while running:
        display_instructions()  # מציג את ההוראות בתחילת התוכנית

        for duration_index, duration_frames in enumerate(frames):
            speed = screen_width / duration_frames

            # Add normal path (no obstacles)
            time_elapsed = 0
            while time_elapsed < duration_frames:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Calculate ball position along a half-circle arc (radius 300)
                t = time_elapsed / duration_frames
                angle = math.pi * t  # Full half-circle (180 degrees)
                x = screen_width // 2 + 300 * math.cos(angle)  # Radius 300 for arc
                y = screen_height // 2 - 300 * math.sin(angle)  # Centering the arc
                ball_position = (int(x), int(y))

                # Fill the screen with the background color
                screen.fill(background_color)

                # Draw the ball
                pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                # Update the display
                pygame.display.flip()

                # Control the frame rate
                clock.tick(frames_per_second)

                # Update the time elapsed
                time_elapsed += 1

            # הצגת ההוראות אחרי כל מסלול רגיל (ללא מכשולים)
            display_instructions()
            pygame.display.flip()

            # Add paths with obstacles
            for obstacle_color in obstacle_colors:
                for obstacle_width in obstacle_widths:
                    time_elapsed = 0
                    while time_elapsed < duration_frames:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

                        # Calculate ball position along a half-circle arc (radius 300)
                        t = time_elapsed / duration_frames
                        angle = math.pi * t  # Full half-circle (180 degrees)
                        x = screen_width // 2 + 300 * math.cos(angle)  # Radius 300 for arc
                        y = screen_height // 2 - 300 * math.sin(angle)  # Centering the arc
                        ball_position = (int(x), int(y))

                        # Fill the screen with the background color
                        screen.fill(background_color)

                        # Draw the ball
                        pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                        # Draw the obstacle only if the ball is in range
                        if obstacle_x - obstacle_width // 2 <= ball_position[0] <= obstacle_x + obstacle_width // 2 and \
                           screen_height // 2 - obstacle_height // 2 <= ball_position[1] <= screen_height // 2 + obstacle_height // 2:
                            draw_obstacle_2(obstacle_width, obstacle_color, obstacle_x, screen_height // 2)

                        # Update the display
                        pygame.display.flip()

                        # Control the frame rate
                        clock.tick(frames_per_second)

                        # Update the time elapsed
                        time_elapsed += 1

                    # הצגת ההוראות אחרי כל מסלול עם מכשולים
                    display_instructions()
                    pygame.display.flip()

        running = False

def run_code_6():
    running = True
    while running:
        display_instructions()  # מציג את ההוראות בתחילת התוכנית

        for duration_index, duration_frames in enumerate(frames):
            speed = screen_width / duration_frames

            # Add normal path (no obstacles)
            time_elapsed = 0
            while time_elapsed < duration_frames:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Calculate ball position along a half-circle arc (radius 500)
                t = time_elapsed / duration_frames
                angle = math.pi * t  # Full half-circle (180 degrees)
                x = screen_width // 2 + 450 * math.cos(angle)  # Radius 500 for arc
                y = (screen_height // 2 + 100) - 450 * math.sin(angle)  # Centering the arc lower by 100
                ball_position = (int(x), int(y))

                # Fill the screen with the background color
                screen.fill(background_color)

                # Draw the ball
                pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                # Update the display
                pygame.display.flip()

                # Control the frame rate
                clock.tick(frames_per_second)

                # Update the time elapsed
                time_elapsed += 1

            # הצגת ההוראות אחרי כל מסלול רגיל (ללא מכשולים)
            display_instructions()
            pygame.display.flip()

            # Add paths with obstacles
            for obstacle_color in obstacle_colors:
                for obstacle_width in obstacle_widths:
                    time_elapsed = 0
                    while time_elapsed < duration_frames:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

                        # Calculate ball position along a half-circle arc (radius 500)
                        t = time_elapsed / duration_frames
                        angle = math.pi * t  # Full half-circle (180 degrees)
                        x = screen_width // 2 + 450 * math.cos(angle)  # Radius 500 for arc
                        y = (screen_height // 2 + 100) - 450 * math.sin(angle)  # Centering the arc lower by 100
                        ball_position = (int(x), int(y))

                        # Fill the screen with the background color
                        screen.fill(background_color)

                        # Draw the ball
                        pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                        # Draw the obstacle only if the ball is in range
                        if obstacle_x - obstacle_width // 2 <= ball_position[0] <= obstacle_x + obstacle_width // 2 and \
                           screen_height // 2 - obstacle_height // 2 <= ball_position[1] <= screen_height // 2 + obstacle_height // 2:
                            draw_obstacle_2(obstacle_width, obstacle_color, obstacle_x, screen_height // 2)

                        # Update the display
                        pygame.display.flip()

                        # Control the frame rate
                        clock.tick(frames_per_second)

                        # Update the time elapsed
                        time_elapsed += 1

                    # הצגת ההוראות אחרי כל מסלול עם מכשולים
                    display_instructions()
                    pygame.display.flip()

        running = False

def run_code_7():
    running = True
    while running:
        display_instructions()  # מציג את ההוראות בתחילת התוכנית

        for duration_index, duration_frames in enumerate(frames):
            speed = screen_width / duration_frames

            # Add normal path (no obstacles)
            time_elapsed = 0
            while time_elapsed < duration_frames:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Calculate ball position along a twisted "X" path
                t = time_elapsed / duration_frames
                x = screen_width * t  # X moves from 0 to screen_width
                y = screen_height - screen_height * t  # Y moves from screen_height to 0

                # Apply sinusoidal twisting
                twist_factor = math.sin(2 * math.pi * t) * 100  # 100 is the magnitude of the twist
                ball_position = (int(x + twist_factor), int(y))

                # Fill the screen with the background color
                screen.fill(background_color)

                # Draw the ball
                pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                # Update the display
                pygame.display.flip()

                # Control the frame rate
                clock.tick(frames_per_second)

                # Update the time elapsed
                time_elapsed += 1

            # הצגת ההוראות אחרי כל מסלול רגיל (ללא מכשולים)
            display_instructions()
            pygame.display.flip()

            # Add paths with obstacles
            for obstacle_color in obstacle_colors:
                for obstacle_width in obstacle_widths:
                    time_elapsed = 0
                    while time_elapsed < duration_frames:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

                        # Calculate ball position along a twisted "X" path
                        t = time_elapsed / duration_frames
                        x = screen_width * t  # X moves from 0 to screen_width
                        y = screen_height - screen_height * t  # Y moves from screen_height to 0

                        # Apply sinusoidal twisting
                        twist_factor = math.sin(2 * math.pi * t) * 100  # 100 is the magnitude of the twist
                        ball_position = (int(x + twist_factor), int(y))

                        # Fill the screen with the background color
                        screen.fill(background_color)

                        # Draw the ball
                        pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                        # Draw the obstacle only if the ball is in range
                        if obstacle_x - obstacle_width // 2 <= ball_position[0] <= obstacle_x + obstacle_width // 2 and \
                           screen_height // 2 - obstacle_height // 2 <= ball_position[1] <= screen_height // 2 + obstacle_height // 2:
                            draw_obstacle_2(obstacle_width, obstacle_color, obstacle_x, screen_height // 2)

                        # Update the display
                        pygame.display.flip()

                        # Control the frame rate
                        clock.tick(frames_per_second)

                        # Update the time elapsed
                        time_elapsed += 1

                    # הצגת ההוראות אחרי כל מסלול עם מכשולים
                    display_instructions()
                    pygame.display.flip()

        running = False

def run_code_8():
    scale_factor = 0.5
    running = True
    while running:
        display_instructions()  # מציג את ההוראות בתחילת התוכנית

        for duration_index, duration_frames in enumerate(frames):
            time_elapsed = 0
            while time_elapsed < duration_frames:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Scaled movement in center
                t = time_elapsed / duration_frames
                x = screen_width // 2 + (screen_width * scale_factor * (t - 0.5))  # Smaller X range
                y = screen_height // 2 - (screen_height * scale_factor * (t - 0.5))  # Smaller Y range

                # Apply sinusoidal twisting
                twist_factor = math.sin(2 * math.pi * t) * (50 * scale_factor)  # Smaller twist
                ball_position = (int(x + twist_factor), int(y))

                screen.fill(background_color)
                pygame.draw.circle(screen, ball_color, ball_position, ball_radius)
                pygame.display.flip()
                clock.tick(frames_per_second)
                time_elapsed += 1

            # הצגת ההוראות אחרי כל מסלול רגיל (ללא מכשולים)
            display_instructions()
            pygame.display.flip()

            # Add paths with obstacles
            for obstacle_color in obstacle_colors:
                for obstacle_width in obstacle_widths:
                    time_elapsed = 0
                    while time_elapsed < duration_frames:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False

                        t = time_elapsed / duration_frames
                        x = screen_width // 2 + (screen_width * scale_factor * (t - 0.5))
                        y = screen_height // 2 - (screen_height * scale_factor * (t - 0.5))

                        twist_factor = math.sin(2 * math.pi * t) * (50 * scale_factor)
                        ball_position = (int(x + twist_factor), int(y))

                        screen.fill(background_color)
                        pygame.draw.circle(screen, ball_color, ball_position, ball_radius)

                        if obstacle_x - obstacle_width // 2 <= ball_position[0] <= obstacle_x + obstacle_width // 2:
                            draw_obstacle_2(obstacle_width, obstacle_color, obstacle_x, obstacle_y)

                        pygame.display.flip()
                        clock.tick(frames_per_second)
                        time_elapsed += 1

                    # הצגת ההוראות אחרי כל מסלול עם מכשולים
                    display_instructions()
                    pygame.display.flip()

        running = False


# Main execution starts here
run_code_6()