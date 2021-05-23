import random, time, pygame, sys
from pygame.locals import *

fps = 60
windowwidth = 640
windowheight = 480
boxsize = 21 #kích thước box chơi game
boardwidth = 10 #chiều rộng box thành 10 ô
boardheight = 20
blank = '.'
#thời gian giữ phím di chuyển
movesidewaysFREQ = 0.15
movedownFREQ = 0.1

#khoảng cách các lề khối box đến lề cửa sổ
Xmargin = int((windowwidth - boardwidth * boxsize) / 2) 
TopMargin = windowheight - (boardheight * boxsize) - 5

#color để tạo khối
white = (255,255,255)
gray = (185,185,185)
black = (0,0,0)
red = (155,0,0)
lightred = (175,20,20)
green = (0,155,0)
lightgreen = (20,175,20)
blue = (0,0,155)
lightblue = (20,20,175)
yellow = (155,155,0)
lightyellow = (175,175,20)

bordercolor = blue
BGcolor = black
textcolor = white
textshadowcolor = gray
colors = (blue,green,red,yellow)
lightcolors = (lightblue,lightgreen, lightred, lightyellow)
assert len(colors) == len(lightcolors) #mỗi màu phải có màu nhạt

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....','.....','..OO.','.OO..','.....'],['.....','..O..','..OO.','...O.','.....']]
Z_SHAPE_TEMPLATE = [['.....','.....','.OO..','..OO.','.....'],['.....','..O..','.OO..','.O...','.....']]
I_SHAPE_TEMPLATE = [['..O..','..O..','..O..','..O..','.....'],['.....','.....','OOOO.','.....','.....']]
O_SHAPE_TEMPLATE = [['.....','.....','.OO..','.OO..','.....']]
J_SHAPE_TEMPLATE = [['.....','.O...','.OOO.','.....','.....'],['.....','..OO.','..O..','..O..','.....'],['.....','.....','.OOO.','...O.','.....'],['.....','..O..','..O..','.OO..','.....']]
L_SHAPE_TEMPLATE = [['.....','...O.','.OOO.','.....','.....'],['.....','..O..','..O..','..OO.','.....'],['.....','.....','.OOO.','.O...','.....'],['.....','.OO..','..O..','..O..','.....']]
T_SHAPE_TEMPLATE = [['.....','..O..','.OOO.','.....','.....'],['.....','..O..','..OO.','..O..','.....'],['.....','.....','.OOO.','..O..','.....'],['.....','..O..','.OO..','..O..','.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,'Z': Z_SHAPE_TEMPLATE,'J': J_SHAPE_TEMPLATE,'L': L_SHAPE_TEMPLATE,'I': I_SHAPE_TEMPLATE,'O': O_SHAPE_TEMPLATE,'T': T_SHAPE_TEMPLATE} #lưu trữ hình dạng các khối

def main():
    global FPSCLOCK, displaysurf, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((windowwidth, windowheight))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetris Game')

    showTextScreen('Tetris game')
    while True: 
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
        else:
            pygame.mixer.music.load('tetrisc.mid')
        pygame.mixer.music.play(-1, 0.0)
        runGame() #game sẽ được xử lý bởi hàm runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')


def runGame():
    #setup biến để bắt đầu trò chơi
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece() #các piece có thể xoay theo ý người chơi
    nextPiece = getNewPiece()

    while True:
        if fallingPiece == None:
            #khi fallingPiece rơi hết,đẩy nextPiece vào fallingPiece,tạo random new nextPiece
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return #khi bảng bị lấp đầy gameover quay lại rungame()

        checkForQuit()
        for event in pygame.event.get(): #vòng lặp xử lý sự kiện

            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing game
                    displaysurf.fill(BGcolor)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused') # pause until a key press
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            elif event.type == KEYDOWN:
                #di chuyển mảng sang trái,phải
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                #xoay mảng(nếu thỏa mãn)
                elif (event.key == K_UP or event.key == K_SPACE):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif (event.key == K_q): #xoay hướng khác
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                #làm mảng rơi nhanh hơn
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                #làm mảnh rơi luôn xuống
                elif event.key == K_LSHIFT or event.key == K_RSHIFT:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, boardheight):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        #di chuyển bằng cách giữ phím
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > movesidewaysFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > movedownFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        #để mảnh rơi tự nhiên
        if time.time() - lastFallTime > fallFreq:
            if not isValidPosition(board, fallingPiece, adjY=1):
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        #in mọi thứ ra màn hình
        displaysurf.fill(BGcolor)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(fps)


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Đi qua hàng đợi sự kiện để tìm kiếm sự kiện KEYUP.
    # Lấy các sự kiện KEYDOWN để xóa chúng khỏi hàng đợi sự kiện.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # hiển thị chữ Tetris game,gameover
    # Hiện chữ ra giữa màn hình đến khi bấm phím bất kì
    # đổ bóng cho chữ
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, textshadowcolor)
    titleRect.center = (int(windowwidth / 2), int(windowheight / 2))
    displaysurf.blit(titleSurf, titleRect)

    # vẽ chữ
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, textcolor)
    titleRect.center = (int(windowwidth / 2) - 3, int(windowheight / 2) - 3)
    displaysurf.blit(titleSurf, titleRect)

    # vẽ chữ bấm    phím bất kì để bắt đầu và chơi lại
    pressKeySurf, pressKeyRect = makeTextObjs('Press any key to play.', BASICFONT, textcolor)
    pressKeyRect.center = (int(windowwidth / 2), int(windowheight / 2) + 100)
    displaysurf.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP): # nhận sự kiện keyup
        if event.key == K_ESCAPE:
            terminate() # chấm dứt sự kiện key up khi bấm ESC
        pygame.event.post(event) # đặt các đối tượng sự kiện KEYUP khác trở lại


def calculateLevelAndFallFreq(score):
    # Dựa trên điểm số, trả về cấp độ của người chơi
    # tốc độ rơi ở mỗi cấp
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    # trả về một mảnh mới ngẫu nhiên trong một vòng quay và màu sắc ngẫu nhiên
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(boardwidth / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # mảnh rơi từ phía trên của bảng
                'color': random.randint(0, len(colors)-1)}
    return newPiece


def addToBoard(board, piece):
    # điền vào bảng dựa trên vị trí, hình dạng và vòng quay của mảnh
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != blank:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # tạo và trả về cấu trúc dữ liệu bảng trống mới
    board = []
    for i in range(boardwidth):
        board.append([blank] * boardheight)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < boardwidth and y < boardheight


def isValidPosition(board, piece, adjX=0, adjY=0):
    # trả về True nếu mảnh nằm trong bảng và không va chạm
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == blank:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != blank:
                return False
    return True

def isCompleteLine(board, y): #kiểm tra các dòng đã hoàn thành
    for x in range(boardwidth):
        if board[x][y] == blank:
            return False
    return True


def removeCompleteLines(board): # loại bỏ các dòng đã hoàn thành
    #di chuyển mọi thứ phía trên chúng xuống và trả về số dòng hoàn chỉnh
    numLinesRemoved = 0
    y = boardheight - 1 #bắt đầu y ở cuối bảng
    while y >= 0:
        if isCompleteLine(board, y):
            # Xóa dòng và kéo các box xuống một dòng.
            for pullDownY in range(y, 0, -1):
                for x in range(boardwidth):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Đặt dòng trên cùng thành trống.
            for x in range(boardwidth):
                board[x][0] = blank
            numLinesRemoved += 1
            # các dòng kèo xuống mà cũng hoàn thành thì nó cũng bị xóa
        else:
            y -= 1 # kiểm tra dòng tiếp theo 
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    # Chuyển đổi tọa độ xy đã cho của bảng thành xy
    # tọa độ của vị trí trên màn hình.
    return (Xmargin + (boxx * boxsize)), (TopMargin + (boxy * boxsize))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # vẽ một ô duy nhất (mỗi mảnh tetromino có bốn ô) tại tọa độ xy trên bảng. Hoặc, nếu pixelx & pixely được chỉ định, vẽ các tọa độ pixel được lưu trữ trong pixelx & pixely (cái này được sử dụng cho phần "Tiếp theo")
    if color == blank:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(displaysurf, colors[color], (pixelx + 1, pixely + 1, boxsize - 1, boxsize - 1))
    pygame.draw.rect(displaysurf, lightcolors[color], (pixelx + 1, pixely + 1, boxsize - 4, boxsize - 4))


def drawBoard(board):
    # vẽ đường viền xung quanh bảng
    pygame.draw.rect(displaysurf, bordercolor, (Xmargin - 3, TopMargin - 7, (boardwidth * boxsize) + 8, (boardheight * boxsize) + 8), 5)

    # tô nền của bảng   
    pygame.draw.rect(displaysurf, BGcolor, (Xmargin, TopMargin, boxsize * boardwidth, boxsize * boardheight))
    # vẽ các ô riêng lẻ trên bảng
    for x in range(boardwidth):
        for y in range(boardheight):
            drawBox(x, y, board[x][y])


def drawStatus(score, level):
    # in điểm ra màn hình
    scoreSurf = BASICFONT.render('Score: %s' % score, True, textcolor)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (windowwidth - 150, 20)
    displaysurf.blit(scoreSurf, scoreRect)

    # in level ra mành hình
    levelSurf = BASICFONT.render('Level: %s' % level, True, textcolor)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (windowwidth - 150, 50)
    displaysurf.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        #  nếu pixelx & pixely chưa được chỉ định, hãy sử dụng vị trí được lưu trữ trong cấu trúc dữ liệu mảnh
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # vẽ từng khối tạo nên mảnh ghép
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != blank:
                drawBox(None, None, piece['color'], pixelx + (x * boxsize), pixely + (y * boxsize))


def drawNextPiece(piece):
    # in ra chữ 'next'
    nextSurf = BASICFONT.render('Next:', True, textcolor)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (windowwidth - 120, 80)
    displaysurf.blit(nextSurf, nextRect)
    # vẽ ra mảnh rơi tiếp theo
    drawPiece(piece, pixelx=windowwidth-120, pixely=100)


if __name__ == '__main__':
    main()