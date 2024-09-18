import pygame
import random

# 初始化 Pygame 模块，准备使用 Pygame 的各种功能
pygame.init()

# 定义游戏窗口和游戏逻辑相关的常量
WIDTH, HEIGHT = 800, 600  # 游戏窗口的宽度和高度
TILE_SIZE = 100  # 每个图块的大小
ROWS, COLS = 6, 8  # 游戏板上的行数和列数
FPS = 30  # 游戏的帧率
WHITE = (255, 255, 255)  # 白色，用于绘制
BLACK = (0, 0, 0)  # 黑色，用于绘制
BG_COLOR = (255, 255, 255)  # 背景颜色
HIGHLIGHT_COLOR = (255, 255, 0)  # 高亮颜色，用于选中的图块
WIN_COLOR = (0, 255, 0)  # 游戏成功的颜色
LOSE_COLOR = (255, 0, 0)  # 游戏失败的颜色
POINTS_PER_MATCH = 10  # 每消除一个匹配的图片获得的分数
TIME_LIMIT = 180  # 游戏时间限制（秒）
WIN_SCORE = 1500  # 获胜所需的分数

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ice Cream Party")  # 设置窗口标题

# 加载图案图片，并对图片进行缩放以适应图块大小
patterns_easy = [pygame.image.load(f"{i}.jpg") for i in range(1, 9)]
patterns_easy = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns_easy]

# 加载困难模式的图案图片，并对图片进行缩放
patterns_hard = [pygame.image.load(f"{i}.jpg") for i in range(1, 13)]
patterns_hard = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns_hard]

# 加载登录界面背景图片，并缩放至窗口大小
background_image = pygame.image.load("background4.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
# 加载游戏界面背景图片，并缩放至窗口大小
background_image2 = pygame.image.load("background5.png")
background_image2 = pygame.transform.scale(background_image2, (WIDTH, HEIGHT))

# 加载游戏结束、胜利和失败的图像，并缩放至窗口大小
game_over_image = pygame.image.load("lose3.png")
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))
you_win_image = pygame.image.load("success2.png")
you_win_image = pygame.transform.scale(you_win_image, (WIDTH, HEIGHT))
you_lose_image = pygame.image.load("time2.png")
you_lose_image = pygame.transform.scale(you_lose_image, (WIDTH, HEIGHT))

# 创建游戏板，每个位置可以有多张图片
def create_board(patterns):
    # 为每一行的每一列创建一个列表，列表中包含随机选择的图案
    return [[[random.choice(patterns) for _ in range(3)] for _ in range(COLS)] for _ in range(ROWS)]

# 自动生成
# 创建图案列表，确保每种图案的数量是3的倍数
def create_patterns(patterns, total_tiles):
    pattern_count = {pattern: total_tiles // len(patterns) for pattern in patterns}
    for pattern in patterns:
        while pattern_count[pattern] % 3 != 0:
            pattern_count[pattern] += 1
    # 返回包含每种图案正确数量的列表
    return [pattern for pattern in patterns for _ in range(pattern_count[pattern])]

# 使用简单的图案创建游戏板
board = create_board(create_patterns(patterns_easy, ROWS * COLS))

selected = []  # 存储玩家选中的图块位置

# 定义按钮区域类，用于处理按钮的绘制和点击事件
class ButtonArea:
    def __init__(self, x, y, width, height, text=""):
        self.rect = pygame.Rect(x, y, width, height)  # 按钮的位置和大小
        self.text = text  # 按钮上的文字

    def is_clicked(self):
        # 检查鼠标是否点击了按钮区域
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def draw(self, screen):
        pass
    # 目前不绘制任何内容，但可以扩展为绘制按钮的背景和文字

# 创建开始游戏和困难模式按钮区域
start_button_area = ButtonArea(WIDTH // 2 - 270, HEIGHT // 2 + 220, 200, 50, "")
difficulty_button_area = ButtonArea(WIDTH // 2 + 100, HEIGHT // 2 + 220, 200, 50, "")

# 初始化分数和倒计时
score = 0
start_time = pygame.time.get_ticks()  # 获取游戏开始的时间
timer = TIME_LIMIT  # 设置游戏时间限制

# 定义绘制分数和时间的函数
def draw_score_and_time():
    global score, timer
    # 创建字体对象，设置字体大小
    score_font = pygame.font.SysFont(None, 36)
    # 将分数和时间渲染成图像
    score_text = score_font.render(f"Score: {score}", True, BLACK)
    time_text = score_font.render(f"Time: {int(timer)}", True, BLACK)
    # 将渲染好的图像绘制到屏幕上的指定位置
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (WIDTH - 150, 10))

# 定义绘制游戏结束界面的函数
def draw_end_screen(image):
    # 将游戏结束的图像绘制到屏幕上
    screen.blit(image, (0, 0))

# 定义绘制登录界面的函数
def draw_login_screen():
    # 将背景图像绘制到屏幕上
    screen.blit(background_image, (0, 0))

# 自动生成
# 定义检查匹配的函数
def check_match():
    global score
    # 如果玩家选中了3个图块
    if len(selected) == 3:
        # 获取选中图块的图案
        tiles = [board[r][c][0] for r, c in selected]
        # 如果3个图块的图案相同
        if tiles[0] == tiles[1] == tiles[2]:
            # 消除这3个图块，并增加分数
            for r, c in selected:
                board[r][c].pop(0)
            score += POINTS_PER_MATCH * 3
            selected.clear()  # 清空选中的图块
            return True
    # 如果没有匹配，清空选中的图块
    selected.clear()
    return False

# 自动生成
# 定义重新排列图片的函数
def rearrange_tiles():
    # 遍历每一行的每一列
    for row in range(ROWS):
        for col in range(COLS):
            # 如果当前位置没有图块
            while not board[row][col]:
                # 从当前位置向下寻找有图块的位置
                found = False
                for r in range(row + 1, ROWS):
                    if board[r][col]:
                        # 将找到的图块向上移动，并清空原位置
                        board[row][col] = [board[r][col].pop(0)]
                        board[r][col] = []
                        found = True
                        break
                if not found:
                    break

# 定义绘制游戏板的函数
def draw_board():
    # 遍历每一行和每一列
    for row in range(ROWS):
        for col in range(COLS):
            # 获取当前位置的图块列表
            tile_list = board[row][col]
            # 如果列表不为空，即该位置有图块
            if tile_list:
                # 获取最上面的图块
                tile = tile_list[0]
                # 将图块绘制到屏幕上对应的位置
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))
                # 如果该位置的图块被选中（在selected列表中），绘制高亮框
                if (row, col) in selected:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

# 检查是否有可能的匹配
def check_possible_matches():
    # 创建一个字典，用于存储每种图案及其位置
    tile_positions = {}
    # 遍历游戏板上的每个位置
    for row in range(ROWS):
        for col in range(COLS):
            # 获取当前位置的第一张图块
            pattern = board[row][col][0] if board[row][col] else None
            # 如果该位置有图块
            if pattern:
                # 如果图案不在字典中，添加到字典中
                if pattern not in tile_positions:
                    tile_positions[pattern] = []
                # 将图案的位置添加到字典中
                tile_positions[pattern].append((row, col))

    # 检查每种图案的位置列表，看是否有至少3个相同的图案
    for pattern, positions in tile_positions.items():
        if len(positions) >= 3:
            # 如果有，说明有可能的匹配
            return True
    # 如果没有可能的匹配，返回False
    return False

# 定义返回按钮区域类
class ReturnButtonArea:
    def __init__(self, x, y, width, height, text):
        # 初始化按钮的位置、大小和文本
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def is_clicked(self):
        # 检查鼠标点击的位置是否在按钮上
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def draw(self, screen):
        # 绘制按钮的背景
        pygame.draw.rect(screen, WHITE, self.rect)
        # 设置字体和大小
        font = pygame.font.SysFont(None, 24)
        # 渲染按钮文本
        text_surf = font.render(self.text, True, BLACK)
        # 获取文本的矩形区域，以便居中绘制
        text_rect = text_surf.get_rect(center=self.rect.center)
        # 将文本绘制到屏幕上
        screen.blit(text_surf, text_rect)

# 创建返回按钮区域实例
return_button_area = ReturnButtonArea(WIDTH // 2 -50, HEIGHT // 2 +90, 300, 200, "Restart")

# 定义重置游戏的函数
def reset_game(difficulty):
    global board, score, start_time, timer, selected, login_screen, game_over, patterns
    # 根据难度选择图案集
    if difficulty == "easy":
        patterns = create_patterns(patterns_easy, ROWS * COLS)
    else:
        patterns = create_patterns(patterns_hard, ROWS * COLS)
    # 创建新的游戏板
    board = create_board(patterns)
    # 重置分数、计时器和选中的图块
    score = 0
    start_time = pygame.time.get_ticks()
    timer = TIME_LIMIT
    selected = []
    # 重置游戏状态
    login_screen = True
    game_over = False

# 主游戏循环
running = True
login_screen = True
game_over = False  # 控制游戏是否结束的标志
over=False  # 控制游戏是否完成一局的标志
clock = pygame.time.Clock()

while running:
    # 控制游戏循环的帧率
    clock.tick(FPS)

    # 获取当前时间
    current_time = pygame.time.get_ticks()
    # 计算已过时间
    elapsed_time = (current_time - start_time) / 1000
    # 更新倒计时
    timer = TIME_LIMIT - elapsed_time
    # 确保倒计时不会变成负数
    timer = max(timer, 0)
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 如果点击了关闭按钮，结束游戏
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 如果在登录屏幕，处理开始和难度选择按钮的点击
            if login_screen:
                if start_button_area.is_clicked():
                    reset_game("easy")
                    login_screen = False
                elif difficulty_button_area.is_clicked():
                    reset_game("hard")
                    login_screen = False
            # 如果在游戏中，处理图块的选中和返回按钮的点击
            else:
                x, y = event.pos
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if 0 <= col < COLS and 0 <= row < ROWS:
                    if board[row][col] and board[row][col][0] is not None:
                        if (row, col) not in selected:
                            selected.append((row, col))
                        if len(selected) == 3:
                            # 如果选中了3个图块，检查是否匹配
                            if check_match():
                                # 如果匹配，重新排列图块
                                rearrange_tiles()
                            else:
                                # 如果不匹配，清空选中的图块
                                selected.clear()
                        # 如果游戏已结束，处理返回按钮的点击
                    if over and return_button_area.is_clicked():
                        reset_game("easy")

    # 填充背景颜色
    # 绘制背景图片
    screen.blit(background_image2, (0, 0))
    # 如果在登录屏幕，绘制登录界面
    if login_screen:
        draw_login_screen()
        start_button_area.draw(screen)
        difficulty_button_area.draw(screen)
    # 如果游戏已结束，绘制结束界面
    elif game_over:
        draw_end_screen(game_over_image if timer <= 0 else you_win_image if score >= WIN_SCORE else you_lose_image)
        return_button_area.draw(screen)
    else:
        # 否则，绘制游戏板和分数时间
        draw_board()
        draw_score_and_time()
        # 如果分数达到胜利条件，显示胜利界面
        if timer > 0 and score >= WIN_SCORE:
            draw_end_screen(you_win_image)
            over=True
        # 检查是否所有图像都被消除
        all_tiles_removed = all(not board[row][col] for row in range(ROWS) for col in range(COLS))
        if timer>0 and all_tiles_removed:
            draw_end_screen(you_win_image)
            over = True
        # 检查是否有可能的匹配
        if timer>0 and not check_possible_matches():
            draw_end_screen(game_over_image)
            over = True
        # 检查时间是否结束
        if timer <= 0:
            draw_end_screen(you_lose_image)
            over = True

    # 更新屏幕显示
    pygame.display.flip()
