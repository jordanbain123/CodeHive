from cmu_graphics import*
import random
import math

class PlayerBee:
    def __init__(self, x, y, color='yellow', width=50, height=50): 
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.color = color

        self.gatheredFlowers = []
        self.collectedPollen = []
    
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
    
    def gatherPollen(self, flowers):
        maxPollen = 6
        for flower in flowers:
            if len(self.gatheredFlowers) >= maxPollen:
                break
            
            if self.distance(self.x, self.y, flower.x, flower.y) < 30:
                if flower.pollinator and not flower.isGathered:
                    flower.isGathered = True
                    self.gatheredFlowers.append(flower)
                    self.collectedPollen.append(flower.color)
    
    def drawBeePollen(self):
        for i in range(len(self.collectedPollen)):
            color = self.collectedPollen[i]
            cx = (self.x + 10) + 5 * i
            cy = self.y + 50
            drawCircle(cx, cy, 10, fill=color, border='black')


    def pollinateFlower(self, flower, isTouching):
        if flower.matchFlower in self.gatheredFlowers and isTouching:
            maxSize = 35
            if flower.size < maxSize:
                flower.matchFlower.grow()
                flower.grow()
            else:
                flower.isFullyGrown = True

    def growFlowers(self, flowers):
        if self.gatheredFlowers:
            lastGatheredFlower = None
            gFlowersReverse = self.gatheredFlowers[::-1]
            for gatheredFlower in gFlowersReverse:
                if not gatheredFlower.matchFlower:
                    lastGatheredFlower = gatheredFlower
                    break
            
            for flower in flowers:
                isTouching = self.distance(self.x, self.y, flower.x, flower.y) < 30

                if (flower.matchFlower and not flower.pollinator and not 
                    flower.isFullyGrown and self.compareColors(flower)):
                    self.pollinateFlower(flower, isTouching)
                
                elif (not flower.matchFlower and not flower.pollinator 
                      and lastGatheredFlower and isTouching):
                    flower.matchFlower = lastGatheredFlower
                    lastGatheredFlower.matchFlower = flower
                    break

                if (flower.matchFlower and flower.matchFlower.isFullyGrown 
                    and flower in self.gatheredFlowers):
                    self.gatheredFlowers.remove(flower)
                    self.collectedPollen.pop()
    
    def compareColors(self, other):
        if isinstance(other, Flowers) and self.collectedPollen:
            return other.color in self.collectedPollen
        return False
    
    
    def playerOnStep(self, mouseX, mouseY, speed=8, flowers=[]):
        self.movePlayerBee(mouseX, mouseY, speed)
        self.gatherPollen(flowers)
        self.growFlowers(flowers)

class HelperBee(PlayerBee):
    def __init__(self, x, y, color='yellow', width=50, height=50, speed=5):
        super().__init__(x, y, color, width, height)
        self.currentTarget = None
        self.speed = speed

    
    def getCurrentTarget(self):
          return self.currentTarget  #getter method
    
    def setCurrentTarget(self, target): #setter method
        self.currentTarget = target
    
    def chooseTarget(self, app, flowers):
        currTarget = self.getCurrentTarget()
        if currTarget and (currTarget.isGathered or currTarget.isFullyGrown or
                           currTarget.x < 0 or currTarget.x > app.width or
                           currTarget.y < 0 or currTarget.y > app.height):
            self.setCurrentTarget(None)

        if not self.getCurrentTarget():
            closestFlower = None
            minDist = None

            for flower in flowers:
                if not flower.isGathered or not flower.matchFlower:
                    dist = self.distance(self.x, self.y, flower.x, flower.y)
                    if minDist == None or dist < minDist:
                        minDist = dist
                        closestFlower = flower
        
            self.setCurrentTarget(closestFlower)
    
    def moveHelperBee(self):
        if self.getCurrentTarget():
            targetX = self.getCurrentTarget().x
            targetY = self.getCurrentTarget().y
            self.movePlayerBee(targetX, targetY, self.speed)
    
    def helperOnStep(self, app, flowers):
        self.chooseTarget(app, flowers)
        self.moveHelperBee()
        self.gatherPollen(flowers)
        self.growFlowers(flowers)

class Flowers:
    def __init__(self, x, y, color='pink', width=50, height=50, pollinator=False):
        self.x = x
        self.y = y
        self.color = color
        self.pollinator = pollinator
        
        self.isGathered = False
        self.isFullyGrown = False
        self.matchFlower = None
        
        self.size = 20
        self.size2 = 10

        dirList = [-1, 1]
        self.dir = dirList[random.randint(0, 1)]
        self.flowerCycle = 0
        self.cx = random.randint(0, 2) * self.dir
    
    def drawFlower(self, gathered=False, gatheredX=0):
        if gathered:
            drawCircle(gatheredX, 40, self.size, fill = None, border = self.color,
                       borderWidth = 10)
        elif self.pollinator and not self.isGathered:
            drawCircle(self.x, self.y, self.size, fill = self.color)
        elif self.pollinator and self.isGathered:
            drawCircle(self.x, self.y, self.size, fill = None, border = self.color,
                       borderWidth = 10)
        elif not self.pollinator and not self.isGathered:
            drawCircle(self.x, self.y, self.size, fill=None, border=self.color, borderWidth=5)
            drawCircle(self.x, self.y, self.size2, fill=self.color)
    
    def grow(self):
        self.size += 1
        self.size2 += 1
    
    def flowerMovement(self):
        self.y -= 1
        self.flowerCycle += 1

        if self.flowerCycle % 16 == 0:
            self.flowerCycle = 0
            self.dir *= -1
        dx = -0.008333 * (self.flowerCycle ** 2) + 0.4833 * self.flowerCycle + 1
        self.x += self.dir * dx
        self.x += self.cx
    
    def flowerOnStep(self):
       self.flowerMovement()

def helperBeeGen(app, count):
    helperBees = []

    for _ in range(count):
        x = random.randint(0, app.width)
        y = random.randint(0, app.height)
        helperBee = HelperBee(x, y, speed=5)
        helperBees.append(helperBee)
    return helperBees



def onAppStart(app):
    app.playerBee = PlayerBee(app.width/2 - 30, app.height/2 - 30.)

    app.helperBees = helperBeeGen(app, 2)

    app.flowers = []

    app.background = 'lightblue'
    
    app.flowerTimer = 0 

def redrawAll(app):
    app.playerBee.drawPlayer()

    for helperBee in app.helperBees:
        helperBee.drawPlayer()

    for flower in app.flowers:
        flower.drawFlower()

    for gatheredFlower in range(len(app.playerBee.gatheredFlowers)):
            cx = 30 + 30 * gatheredFlower
            app.playerBee.gatheredFlowers[gatheredFlower].drawFlower(gathered=True, 
                                                           gatheredX=cx)

    app.playerBee.drawBeePollen()

def onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY

def onStep(app):
    app.flowerTimer += 1
    if app.flowerTimer % 40 == 0:
        newX = random.randint(0, app.width)
        newY = app.height + 20
        app.flowerTimer = 0
        boolList = [True, False]
        randomPol = boolList[random.randint(0,1)]
        colors = ['purple', 'red', 'green']
        randomCol = random.choice(colors) #https://www.w3schools.com/python/ref_random_choice.asp
        app.flowers.append(Flowers(newX, newY, color=randomCol , pollinator=randomPol))

    
    app.playerBee.playerOnStep(app.mouseX, app.mouseY, flowers=app.flowers)

    flowers = app.flowers
    for helperBee in app.helperBees:
        helperBee.helperOnStep(app, flowers)

    for flower in app.flowers:
        flower.flowerOnStep()
        if flower.y < -flower.size:
            app.flowers.remove(flower)



def main():
    runApp(width=500, height=500)

main()

