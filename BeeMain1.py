from cmu_graphics import*

class PlayerBee:
    def __init__(self, x, y, color='yellow', width=50, height=50): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def drawPlayer(self):
         drawCircle(self.x + self.width/2, self.y + self.height/2, self.width/2, fill=self.color, border = 'black')

    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x1 - x0)**2 + (y1 - y0)**2)**0.5
    
    def movePlayerBee(self, targetX, targetY, speed):
        dx = targetX - self.x
        dy = targetY - self.y
        dist = self.distance(self.x, self.y, targetX, targetY)

        if dist > 0:
            if dist < speed:
                self.x = targetX
                self.y = targetY
            else:
                speedDist = speed / dist
                self.x += dx * speedDist
                self.y += dy * speedDist
    
    def gatherPollen(self, flowers, gatheredFlowers):
        for flower in flowers:
            if self.distance(self.x, self.y, flower.x, flower.y) < 30:
                if flower.pollinator and not flower.isGathered:
                    flower.isGathered = True
                    gatheredFlowers.append(flower)
    
    def growFlowers(self, flowers, gatheredFlowers):
        if gatheredFlowers:
            lastGatheredFlower = gatheredFlowers[-1]

            for flower in flowers:
                if (self.distance(self.x, self.y, flower.x, flower.y) < 30 and
                    not flower.pollinator and not flower.isFullyGrown):
                    lastGatheredFlower.grow()
                    flower.grow()

                    maxSize = 35
                    if lastGatheredFlower.size >= maxSize:
                        gatheredFlowers.pop()
                        flower.isFullyGrown = True

                        


            

    
    def playerOnStep(self, mouseX, mouseY, speed=8, flowers=[], gatheredFlowers=[]):
        self.movePlayerBee(mouseX, mouseY, speed)
        self.gatherPollen(flowers, gatheredFlowers)
        self.growFlowers(flowers, gatheredFlowers)

class Flowers:
    def __init__(self, x, y, color='pink', width=50, height=50, pollinator=False):
        self.x = x
        self.y = y
        self.color = color
        self.pollinator = pollinator
        self.isGathered = False
        self.pollinated = False
        self.isFullyGrown = False
        self.size = 20
        self.size2 = 10
    
    def drawFlower(self, gathered=False, gatheredX=0):
        if gathered:
            drawCircle(gatheredX, 40, self.size, fill = None, border = self.color,
                       borderWidth = 10)
        elif self.pollinator and not self.isGathered:
            drawCircle(self.x, self.y, self.size, fill = self.color)
        elif self.pollinator and self.isGathered:
            drawCircle(self.x, self.y, self.size, fill = None, border = self.color,
                       borderWidth = 10)
        elif not self.pollinator and not self.isGathered and not self.pollinated:
            drawCircle(self.x, self.y, self.size, fill=None, border=self.color, borderWidth=5)
            drawCircle(self.x, self.y, self.size2, fill=self.color)
    
    def grow(self):
        self.size += 0.5
        self.size2 += 0.5


def onAppStart(app):
    app.playerBee = PlayerBee(app.width/2 - 30, app.height/2 - 30.)

    app.flowers = [Flowers(100, 100, color='purple', pollinator=True),
                   Flowers(200, 200, color='purple', pollinator=False),
                   Flowers(100, 384, color='purple', pollinator=True),
                   Flowers(250, 200, color='purple', pollinator=True),
                   Flowers(150, 100, color='purple', pollinator=True),
                   Flowers(175, 300, color='purple', pollinator=True),
                   Flowers(374, 400, color='purple', pollinator=True),
                   Flowers(397, 190, color='purple', pollinator=False),
                   Flowers(483, 368, color='purple', pollinator=False),
                   Flowers(182, 394, color='purple', pollinator=False)
                   ]
    
    app.gatheredFlowers = []

def redrawAll(app):
    app.playerBee.drawPlayer()

    for flower in app.flowers:
        flower.drawFlower()

    for gatheredFlower in range(len(app.gatheredFlowers)):
            cx = 30 + 30 * gatheredFlower
            app.gatheredFlowers[gatheredFlower].drawFlower(gathered=True, 
                                                           gatheredX=cx)


def onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY

def onStep(app):
    app.playerBee.playerOnStep(app.mouseX, app.mouseY, flowers=app.flowers, 
                               gatheredFlowers=app.gatheredFlowers)

def main():
    runApp(width=500, height=500)

main()

