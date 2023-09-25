import os, sys
from fcntl import ioctl
import pygame
import random

maxSCORE = 0

RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

pygame.font.init()

s_width = 800
s_height = 700
play_width = 300 
play_height = 600 
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

S = [['.....','.....','..00.','.00..','.....'],
     ['.....','..0..','..00.','...0.','.....']]

Z = [['.....','.....','.00..','..00.','.....'],
     ['.....','..0..','.00..','.0...','.....']]

I = [['..0..','..0..','..0..', '..0..','.....'],
     ['.....','0000.','.....','.....','.....']]

O = [['.....','.....','.00..','.00..','.....']]

J = [['.....','.0...','.000.','.....','.....'],
     ['.....','..00.','..0..','..0..','.....'],
     ['.....','.....','.000.','...0.','.....'],
     ['.....','..0..','..0..','.00..', '.....']]

L = [['.....','...0.','.000.','.....','.....'],
     ['.....','..0..','..0..','..00.','.....'],
     ['.....','.....','.000.','.0...', '.....'],
     ['.....','.00..','..0..','..0..', '.....']]

T = [['.....','..0..','.000.','.....','.....'],
     ['.....','..0..','..00.','..0..','.....'],
     ['.....','.....','.000.','..0..','.....'],
     ['.....','..0..','.00..','..0..','.....'],
     ]
P = [['.....','..0..','.000.','..0..','.....']]

formatos = [S, Z, I, O, J, L, T ,P]
shape_colors = [(255, 60, 60), (255, 150, 60), (255, 255, 50), (160, 255, 128), (0, 180, 255), (166, 120, 255), (140, 220, 255) , (255,150,220)]

class Piece(object):
    linhas = 20  
    colunas = 10  
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[formatos.index(shape)]
        self.rotation = 0  

def criar_grade(locked_positions={}):
    grid = [[(255, 255, 255) for x in range(10)] for x in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (255, 255, 255)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    global formatos, shape_colors
    return Piece(5, 0, random.choice(formatos))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))
 
def draw_main_menu(size,color,surface):
    font = pygame.font.SysFont('comicsans', size, bold=False)
    font_title = pygame.font.SysFont('comicsans', 2*size, bold=True)
    
    title = "T E T R I S"
    text1 = "Pressione Espaço para Jogar"
    text2 = "Pressione Esc para Sair"
    label1 = font.render(text1,1,color)
    label2 = font.render(text2,1,color)
    label_title = font_title.render(title,1,color)
    
    x1 = s_width / 2 - label1.get_width() / 2
    x2 = s_width / 2 - label2.get_width() / 2
    xt = s_width / 2 - label_title.get_width() / 2
    y1 = s_height /2 - label1.get_height() + label_title.get_height()
    y2 = s_height /2 - label2.get_height() + label1.get_height() + label_title.get_height()+ 10
    yt = s_height /2 - label_title.get_height()
    surface.blit(label_title, (xt,yt))
    
    surface.blit(label1, (x1,y1))
    surface.blit(label2, (x2, y2))
         
def desenhar_grade(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30),
                         (sx + play_width, sy + i * 30))  
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + play_height))        

def eu_que_fiz(entrada):
	if entrada == 1:
		return 0x79
	elif entrada == 2:
		return 0x24
	elif entrada == 3:
		return 0x30
	elif entrada == 4:
		return 0x19
	elif entrada == 5:
		return 0x12
	elif entrada == 6:
		return 0x02
	elif entrada == 7:
		return 0x78
	elif entrada == 8:
		return 0x00
	elif entrada == 9:
		return 0x10
	else:
		return 0x40
	return 0x40
    	
    	
def clear_rows(grid, locked, score, maxSCORE, fd):
	ioctl(fd, WR_L_DISPLAY)
	inc = 0
	for i in range(len(grid) - 1, -1, -1):
		row = grid[i]
		#Limpar se não tem pixels vazios na linha
		if (255, 255, 255) not in row:
			inc += 1
			ind = i
			score += 1;
			if score > maxSCORE:
				maxSCORE = score
			data = 0x00000000
			data = data + eu_que_fiz(score);
			data = data + 0x40404000
			retval = os.write(fd, data.to_bytes(4, 'little'))
			print(score)
			
			for j in range(len(row)):
				try:
					del locked[(j, i)]
				except:
					continue               
	if inc > 0:
		for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
			x, y = key
			if y < ind:
				newKey = (x, y + inc)
				locked[newKey] = locked.pop(key)


def draw_right_side(shape, surface,score):
    #ver próximo formato
    font = pygame.font.SysFont('comicsans', 30)
    
    label = font.render('Próximo formato', 1, (255, 255, 255))
    
    sx = top_left_x + play_width 
    sy = s_height / 2
    l  = (s_width - play_width) / 2
    x = sx + l/2 
    x_line = sx + l/2 -2.5*block_size
    format = shape.shape[shape.rotation % len(shape.shape)]
    
    for i, line in enumerate(format):
        row = list(line)  
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (x_line + j * block_size, sy + i * block_size, block_size, block_size), 0)
    for i in range(6):
        pygame.draw.line(surface, (64, 64, 64), (x_line, sy + i * block_size),
                         (x_line + 6*block_size, sy + i * block_size))
        for j in range(6):
            pygame.draw.line(surface, (64, 64, 64), (x_line + j * block_size, sy),
                             (x_line + j * block_size, sy + 6*block_size))
    surface.blit(label, (x- label.get_width()/2, sy - block_size))
    
    # ver pontuação
    #label1 = font.render("PONTUAÇÃO", 1, (255, 255, 255))
    #label2 = font.render(score, 1, (255, 255, 255))
    
    #surface.blit(label1, (x- label1.get_width()/2, sy + 5*block_size))
    #surface.blit(label2, (x- label2.get_width()/2, sy + 6*block_size))

def desenhar_pontuacao(surface,score) :
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    font = pygame.font.SysFont('comicsans', 30)
    label1 = font.render("PONTUAÇÃO", 1, (255, 255, 255))
    label2 = font.render(str(score[0]), 1, (255, 255, 255))
    surface.blit(label1, (sx + 35, sy + 150))
    surface.blit(label2, (sx + 70, sy + 180))

def desenhar_janela(surface):
    surface.fill((64, 64, 64))
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('T E T R I S', 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)      
    desenhar_grade(surface, 20, 10)
    pygame.draw.rect(surface, (100, 100, 100), (top_left_x, top_left_y, play_width, play_height), 5)

def main():
 	# testando
    fd = os.open(sys.argv[1], os.O_RDWR)
    
    
    global grid
    score = 0
    locked_positions = {}  
    grid = criar_grade(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_speed = 0.27
        ioctl(fd, RD_PBUTTONS) #edit
        inputBOTAO = os.read(fd, 4) #edit
        grid = criar_grade(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        	

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
                
            if int.from_bytes(inputBOTAO, 'little') == 7:
            	current_piece.x -= 1
            	if not valid_space(current_piece, grid):
            			current_piece.x += 1
            if int.from_bytes(inputBOTAO, 'little') == 11:
            	current_piece.x += 1
            	if not valid_space(current_piece, grid):
            			current_piece.x -= 1
            if int.from_bytes(inputBOTAO, 'little') == 14:
            	# rotacionar formato
                current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                if not valid_space(current_piece, grid):
                	current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
            

        #saindo do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
                
            	
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotacionar formato
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # acelerar queda
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)
   
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
      
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            clear_rows(grid, locked_positions, score, maxSCORE, fd)

        desenhar_janela(win)
        draw_right_side(next_piece, win,score)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False
            
    draw_text_middle("VOCÊ PERDEU : " + str(Score[0]), 40, (0, 0, 0), win)
    pygame.display.update()
    os.close(fd)
    pygame.time.delay(2000)

def main_menu():
    clk = 0;
    run = True
    color = (0,0,0)
    while run:
        if clk % 501 == 500 :
            color = random.choice(shape_colors)
        win.fill(color)
        draw_main_menu(60,(255,255,255),win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    main()
                elif  event.key == pygame.K_ESCAPE :
                    run = False
        clk+=1            
    pygame.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('T E T R I S')

main_menu()
