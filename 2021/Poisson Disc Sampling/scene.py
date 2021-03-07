from manim import *
from math import cos, sin, pi, sqrt
import random
import numpy

DEFAULT_FONT = "Open Sans"
DEFAULT_BACKGROUND_COLOR = "#000015"

#This scene is the introduction part, not much is happening in here
class Introduction(Scene):
    def construct(self):
        self.camera.background_color = DEFAULT_BACKGROUND_COLOR # Set the background color to a very dark blue
    
        title_text = Text("Poission Disc Sampling", font=DEFAULT_FONT) # define top text and font
        title_text.to_edge(UP) # place it to the top of the screen

        bottom_label = Text("Bridson's algorithm", font =DEFAULT_FONT, color=ORANGE)
        bottom_label.scale_in_place(0.7)
        bottom_label.to_edge(DOWN)

        self.play(
            Write(title_text),
            Write(bottom_label)
        )

        self.wait(3) # This number is going to change according to the lenght of audio file

        self.play(
            FadeOut(title_text),
            FadeOut(bottom_label)
        )


# This scene is the part which that i am gonna explain how this algorithm works and try to visualize the process
class Demonstration(Scene):
    def construct(self):
        self.camera.background_color = DEFAULT_BACKGROUND_COLOR
        mapRectangle = Rectangle(height=6, width=10, color=GREEN,fill_opacity=0.2, fill_color=GREEN)
        
        randomDots = [Dot(numpy.array([random.random()*10-5,random.random()*6-3,0])) for i in range (100)]
        minDistance = 0.5
        self.play(DrawBorderThenFill(mapRectangle), run_time=1.5)
        for i in randomDots:
            self.play(GrowFromCenter(i), run_time=0.1)
        rect = []
        VGroup()
        for i in randomDots:
            for j in randomDots:
                if (i is not j) and self.getDistance(i, j) < minDistance:
                    twoDotGroup = VGroup(i,j)
                    rect.append(Circle(color=RED, fill_opacity=0.2))
                    rect[-1].surround(twoDotGroup)
                    

        self.play(*[ShowCreation(i) for i in rect])
        
        self.wait(6)
        self.play(
            *[FadeOut(i) for i in randomDots],
            *[FadeOut(i) for i in rect]
        )
        self.play()

    def getDistance(self, a, b):
        relativeDistancex = a.get_coord(0) - b.get_coord(0)
        relativeDistancey = a.get_coord(1) - b.get_coord(1)

        distance = relativeDistancex**2 + relativeDistancey**2
        return sqrt(distance)



class RandomSampling(Scene):
    def construct(self):
        self.camera.background_color = DEFAULT_BACKGROUND_COLOR
        mapRectangle = Rectangle(height=6, width=10, color=GREEN,fill_opacity=0.2, fill_color=GREEN)
        self.add(mapRectangle)
        self.play(ApplyMethod(mapRectangle.shift, DOWN/2))

        titleLabel = Text("Random Sampling", font=DEFAULT_FONT)
        titleLabel.to_edge(UP)
        self.play(Write(titleLabel))
        # Yes, i am hard coding this scene's dots, but i will show a few dots just to prove my point
        # i hope it won't be such pain to implement
        initDot = Dot(numpy.array([1,1.5,0]))
        
        initCircle = Circle(color=WHITE, fill_opacity=0.2, fill_color=GRAY)
        
        initCircle.move_to(initDot.get_center())
       

        self.play(FadeIn(initDot),run_time=0.3)
        self.play(ShowCreation(initCircle), runn_time=0.3)
        
        self.testDots = [[initDot, True]]
        circles = [initCircle]
        for i in range(20):
            self.testDots.append([Dot(numpy.array([random.random()*10-5, random.random()*6-3.5,0])), True])
            self.play(FadeIn(self.testDots[-1][0]), run_time=0.3)
            circles.append(Circle(color=WHITE, fill_opacity=0.2, fill_color=GRAY))
            circles[-1].move_to(self.testDots[-1][0].get_center())
            self.play(ShowCreation(circles[-1]), run_time=0.3)
            valid = False
            for i in self.testDots[:-1]:
                if i[1]:
                    theLine = Line(i[0].get_center(), self.testDots[-1][0].get_center(), stroke_width=3)
                    self.play(ShowCreation(theLine), run_time=0.1)


                    if self.distance(self.testDots[-1][0], i[0]) > 2:
                        valid = True
                    
                    else:
                        self.play(FadeOut(VGroup(self.testDots[-1][0], circles[-1],theLine)), run_time=0.2)
                        self.testDots[-1][1] = False
                        break
                    
                    self.play(FadeOut(theLine), run_time=0.1)
            
            if valid is False:
                self.testDots.pop()
                    
        
        self.wait(2)
        #self.play(FadeOut(VGroup(*circles, *[self.testDots[i][0] for i in range(len(self.testDots)) if self.testDots[i][1]])))
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    def distance(self, a,b):
        distancex = a.get_center()[0] - b.get_center()[0]
        distancey = a.get_center()[1] - b.get_center()[1]
        return sqrt(distancex**2 + distancey**2)


class Acknowledgement(Scene):
    def construct(self):
        self.camera.background_color = DEFAULT_BACKGROUND_COLOR
        
        poissonPaper = ImageMobject("poissionPaper.png")
        
        self.play(FadeIn(poissonPaper))
        self.wait(7)
        self.play(FadeOut(poissonPaper))

        self.wait()
        thecodingtrain = ImageMobject("tct.png")
        thecodingtrain.move_to(3*RIGHT+DOWN).scale(2)

        thecodingtrainVideo = ImageMobject("thecodingtrainVideo.jpg")
        thecodingtrainVideo.scale_in_place(0.5)
        thecodingtrainVideo.move_to(3*RIGHT+2*UP)

        sebastianlague = ImageMobject("sl.png")
        sebastianlague.move_to(3*LEFT+DOWN).scale(2)

        sebastianlagueVideo = ImageMobject("sebastianlagueVideo.jpg")
        sebastianlagueVideo.scale_in_place(0.5)
        sebastianlagueVideo.move_to(3*LEFT+2*UP)
        self.play(FadeIn(thecodingtrainVideo), FadeIn(sebastianlagueVideo))
        self.play(FadeIn(thecodingtrain), FadeIn(sebastianlague))

        self.wait(11)

        self.play(
            FadeOut(thecodingtrain),
            FadeOut(thecodingtrainVideo),
            FadeOut(sebastianlague),
            FadeOut(sebastianlagueVideo)
        )
        self.wait(0.2)

class GridScale(MovingCameraScene):
    def construct(self):
        SQUARE_POINTS = numpy.array([
            [-1,-1,0],
            [1,-1,0],
            [1,1,0],
            [-1,1,0]
        ])
        self.camera.background_color = DEFAULT_BACKGROUND_COLOR
        grid = NumberPlane()
        grid.scale(0.7)
        
        self.play(ShowCreation(grid),run_time=3,lag_ratio=0.1)
        line = Line(numpy.array([0,-0.2,0]), numpy.array([0.7,-0.2,0]))
        theBrace =Brace(line, UP)
        questionMark = Text("?")
        questionMark.scale_in_place(0.6)
        questionMark.next_to(theBrace, UP, buff=0.1)
        xCharacter = Text("x")
        xCharacter.scale_in_place(0.6)
        xCharacter.next_to(theBrace, UP, buff=0.1)
        self.play(FadeIn(theBrace), FadeIn(questionMark))
        self.wait()
        self.play(Transform(questionMark, xCharacter))
        self.camera.frame.save_state()
        self.play(self.camera_frame.animate.set_width(6), run_time=3)
        self.wait()
        self.play(Restore(self.camera_frame))
        self.wait()

        self.play(FadeOut(VGroup(xCharacter,questionMark, theBrace, grid)))
        self.wait(1)
        
        square = Polygon(*SQUARE_POINTS)
        self.play(ShowCreation(square))
        textAboveTheCell = Text("This is a cell from our grid", color=BLUE, font=DEFAULT_FONT).scale(0.5).move_to(1.5*UP)

        line = Line(numpy.array([1,1,0]), numpy.array([-1,-1,0]))
        self.play(ShowCreation(line),Write(textAboveTheCell))
        theDot = Dot(numpy.array([1,1,0]))
       
        self.play(FadeIn(theDot), run_time=0.5)
        
        radius = Text("r").move_to(numpy.array([-0.12,0.12,0])).scale(0.7)
        self.play(Write(radius))
        

        x1 = Text("x", color=BLUE).move_to(numpy.array([0,-1.25,0])).scale(0.7)
        x2 = Text("x", color=BLUE).move_to(numpy.array([1.25,0,0])).scale(0.7)
        self.play(Write(x1),Write(x2))
        
        question = Text("Solve for x:", font=DEFAULT_FONT, color=GREEN).move_to(3.3*UP+4.4*LEFT).scale(1.4)
        hint = Text("Remember, radius is the minimum distance between two points", font=DEFAULT_FONT, color=BLUE).move_to(2.6*UP+2*LEFT).scale(0.4)
        self.play(Write(question), Write(hint))
        self.play(FadeOut(textAboveTheCell))

        group = VGroup(square, line, theDot, radius, x1, x2)
        self.play(group.animate.to_edge(UP+RIGHT, buff=0.5))

        eq1 = Tex(r"$r^{2}= x^{2} +x^{2}$").move_to(LEFT+UP)
        eq2 = Tex(r"$2x^{2} = r^{2}$").move_to(LEFT)
        eq3 = Tex(r"$x = \frac{r}{\sqrt{2}}$").move_to(LEFT+DOWN)

        self.play(Write(eq1)) 
        self.play(Write(eq2))
        self.play(Write(eq3))
        
        eureka = Rectangle(color=GREEN)
        eureka.surround(eq3)
        self.play(ShowCreation(eureka))
        self.wait(2)
        self.play(
            FadeOut(VGroup(
                eureka,eq1,eq2,eq3,question,hint,group
            ))
        )
        
class FirstStep(Scene):
    def construct(self):
        self.camera.background_color = DEFAULT_BACKGROUND_COLOR
        textBottom = Text("because it is not nice to find a predictable point position in this randomized region.", font=DEFAULT_FONT).scale(0.5).to_edge(DOWN)
        text = Text("Our initial point is the center of screen but we are not adding this to our pointList", font=DEFAULT_FONT).scale(0.5).next_to(textBottom, UP)
        

        theDot = Dot(radius=0.04)
        bagel = Annulus(inner_radius=1, outer_radius=2, fill_opacity=0.2, fill_color=GREEN_D)
        innerCircle = Circle(color=GREEN)
        outerCircle = Circle(color=GREEN).scale(2)
        self.play(GrowFromCenter(VGroup(theDot,bagel, innerCircle, outerCircle)))

        theLine = Line(ORIGIN, 2*RIGHT)
        fakeLine = Line(ORIGIN, RIGHT)
        innerBrace = Brace(fakeLine,DOWN).scale(0.8)
        outerBrace = Brace(theLine,UP).scale(0.8)
        r = Text("r",color=BLUE).scale(0.6).next_to(innerBrace,DOWN)
        r2 = Text("2r",color=BLUE).scale(0.6).next_to(outerBrace,UP)
        spawnPointText = Text("first spawn point", color=GREEN, font=DEFAULT_FONT).scale(0.2).next_to(theDot, UP, buff=0.4)
        self.play(ShowCreation(VGroup(theLine,innerBrace,outerBrace,r,r2,)),Write(spawnPointText))

        self.play(Write(text))
        self.play(Write(textBottom))

        candidateDot = Dot(numpy.array([-1.15,1.15,0]),radius=0.04)
        textCandidate = Text("a candidate", color=BLUE, font=DEFAULT_FONT).scale(0.4).next_to(candidateDot, UP)
        self.play(FadeIn(candidateDot),Write(textCandidate))
        self.play(FadeOut(spawnPointText))
        self.wait(12)
        self.play(FadeOut(VGroup(theLine,innerBrace,outerBrace,r,r2,text,textBottom)))

class Validity(Scene):
    def construct(self):
        self.camera.background_color = DEFAULT_BACKGROUND_COLOR

        theDot = Dot(radius=0.04)
        bagel = Annulus(inner_radius=1, outer_radius=2, fill_opacity=0.2, fill_color=GREEN_D)
        innerCircle = Circle(color=GREEN)
        outerCircle = Circle(color=GREEN).scale(2)
        self.add(VGroup(theDot,bagel, innerCircle, outerCircle))
        cellSize=0.7
        candidateDot = Dot(numpy.array([-1.15,1.15,0]),radius=0.04)
        textCandidate = Text("a candidate", color=BLUE, font=DEFAULT_FONT).scale(0.4).next_to(candidateDot, UP)
        self.add(candidateDot,textCandidate)
        self.wait(3)
        self.squares = [Square(stroke_width=2,fill_opacity=0.3).scale(0.35/2) for i in range(25)]
        self.setSquares(candidateDot)
        self.play(FadeOut(textCandidate))
        self.play(FadeIn(VGroup(*self.squares)),run_time=2.5,lag_ratio=0.5)
        self.play(VGroup(*self.squares,candidateDot).animate.set_color(GREEN) ,run_time=2.5,lag_ratio=0.5)
        self.play(FadeOut(VGroup(*self.squares)),run_time=2.5,lag_ratio=0.5)
        self.wait(1)
        candidate2 = Dot(numpy.array([0,1.15,0]),radius=0.04)
        self.play(GrowFromCenter(candidate2), run_time=0.5)
        del self.squares
        self.squares = [Square(stroke_width=2,fill_opacity=0.3).scale(0.35/2) for i in range(25)]
        self.setSquares(candidate2)
        self.play(FadeIn(VGroup(*self.squares)),run_time=2.5,lag_ratio=0.5)
        self.play(VGroup(*self.squares,candidate2).animate.set_color(GREEN) ,run_time=2.5,lag_ratio=0.5)
        self.play(FadeOut(VGroup(*self.squares)),run_time=2.5,lag_ratio=0.5)
        self.wait(1)
        candidate3 = Dot(numpy.array([-0.5,1.15,0]),radius=0.04)
        self.play(GrowFromCenter(candidate3), run_time=0.5)
        del self.squares
        self.squares = [Square(stroke_width=2,fill_opacity=0.3).scale(0.35/2) for i in range(25)]
        self.setSquares(candidate3)
        self.play(FadeIn(VGroup(*self.squares)),run_time=2.5,lag_ratio=0.5)
        self.play(VGroup(*self.squares[:10],candidateDot).animate.set_color(GREEN) ,run_time=1,lag_ratio=0.5)
        self.play(self.squares[10].animate.set_color(RED))
        self.wait()
        self.play(FadeOut(VGroup(*self.squares)),run_time=2.5,lag_ratio=0.5)
        self.play(candidate3.animate.set_color(RED))
        self.wait(1)
        candidate4 = Dot(numpy.array([1.15,-1.15,0]),radius=0.04)
        self.play(GrowFromCenter(candidate4), run_time=0.5)
        del self.squares
        self.squares = [Square(stroke_width=2,fill_opacity=0.3).scale(0.35/2) for i in range(25)]
        self.setSquares(candidate4)
        self.play(FadeIn(VGroup(*self.squares)),run_time=2.5,lag_ratio=0.5)
        self.play(VGroup(*self.squares,candidate4).animate.set_color(GREEN) ,run_time=2.5,lag_ratio=0.5)
        self.play(FadeOut(VGroup(*self.squares)),run_time=2.5,lag_ratio=0.5)
        self.wait(1)
        candidate5 = Dot(numpy.array([-1.15,-1.15,0]),radius=0.04)
        self.play(GrowFromCenter(candidate5), run_time=0.5)
        del self.squares
        self.squares = [Square(stroke_width=2,fill_opacity=0.3).scale(0.35/2) for i in range(25)]
        self.setSquares(candidate5)
        self.play(FadeIn(VGroup(*self.squares)),run_time=2.5,lag_ratio=0.5)
        self.play(VGroup(*self.squares,candidate5).animate.set_color(GREEN) ,run_time=2.5,lag_ratio=0.5)
        self.play(FadeOut(VGroup(*self.squares)),run_time=2.5,lag_ratio=0.5)
        self.play(FadeOut(VGroup(theDot,bagel, innerCircle, outerCircle,candidateDot,candidate2, candidate3,candidate4,candidate5)))
            


    def setSquares(self, aDot):
        UPP = numpy.array([0,0.35,0])
        RIGHTT = numpy.array([0.35,0,0])
        DOWNN = -UPP
        LEFTT = -RIGHTT
        # god, im so stupid i forgot that indises start at 0 but im leaving this as is to people to see my quantifiable dumbness :(
        location = aDot.get_center()
        self.squares[13-1].move_to(location)
        theCenter = self.squares[13-1].get_center()
        #InnerLayer
        self.squares[7-1].move_to(theCenter+UPP+LEFTT)
        self.squares[8-1].move_to(theCenter+UPP)
        self.squares[9-1].move_to(theCenter+UPP+RIGHTT)
        self.squares[12-1].move_to(theCenter+LEFTT)
        self.squares[14-1].move_to(theCenter+RIGHTT)
        self.squares[17-1].move_to(theCenter+DOWNN+LEFTT)
        self.squares[18-1].move_to(theCenter+DOWNN)
        self.squares[19-1].move_to(theCenter+DOWNN+RIGHTT)

        #outerLayer
        self.squares[1-1].move_to(theCenter+2*UPP+2*LEFTT)
        self.squares[2-1].move_to(theCenter+2*UPP+LEFTT)
        self.squares[3-1].move_to(theCenter+2*UPP)
        self.squares[4-1].move_to(theCenter+2*UPP+RIGHTT)
        self.squares[5-1].move_to(theCenter+2*UPP+2*RIGHTT)

        self.squares[6-1].move_to(theCenter+UPP+2*LEFTT)
        self.squares[11-1].move_to(theCenter+2*LEFTT)
        self.squares[16-1].move_to(theCenter+DOWNN+2*LEFTT)

        self.squares[10-1].move_to(theCenter+UPP+2*RIGHTT)
        self.squares[15-1].move_to(theCenter+2*RIGHTT)
        self.squares[20-1].move_to(theCenter+DOWNN+2*RIGHTT)

        self.squares[21-1].move_to(theCenter+2*DOWNN+2*LEFTT)
        self.squares[22-1].move_to(theCenter+2*DOWNN+LEFTT)
        self.squares[23-1].move_to(theCenter+2*DOWNN)
        self.squares[24-1].move_to(theCenter+2*DOWNN+RIGHTT)
        self.squares[25-1].move_to(theCenter+2*DOWNN+2*RIGHTT)

class Examples(Scene):
    def construct(self):
        self.camera.background_color = DEFAULT_BACKGROUND_COLOR
        bottomText = Text("*number of trials = k", font=DEFAULT_FONT).scale(0.5).to_edge(DOWN)
        self.play(Write(bottomText))
        
        
        k1image = ImageMobject("image-163.png").scale(0.3).to_edge(LEFT, buff=1.5)
        k2image = ImageMobject("image-3361.png").scale(0.3).to_edge(RIGHT, buff=1.5)
        frameRectangle = Rectangle().surround(k1image, buff=1)
        frameRectangle2 = Rectangle().surround(k2image, buff=1)
        title = Text("k = 1").next_to(frameRectangle, UP).scale(0.7)
        title2 = Text("k = 2").next_to(frameRectangle2, UP).scale(0.7)
        
        
        self.play(Write(title2),Write(title))
        self.play(FadeIn(k2image),FadeIn(k1image))
        
       
        self.play(FadeIn(frameRectangle2),FadeIn(frameRectangle))

        self.wait(4)

        self.play(
            FadeOut(VGroup(frameRectangle,frameRectangle2,title,title2)), 
            FadeOut(k1image),
            FadeOut(k2image)
        )

        k30image = ImageMobject("image-42310.png").scale(0.6)
        
        frameRectangle30 = Rectangle().surround(k30image, buff=1)
        
        title30 = Text("k = 30").next_to(frameRectangle30, UP).scale(0.7)
        
        
        
        self.play(Write(title30))
        self.play(FadeIn(k30image))
        
       
        self.play(FadeIn(frameRectangle30))

        self.wait(4)

        self.play(
            FadeOut(VGroup(frameRectangle30, title30)), 
            FadeOut(k30image)
        )
        self.play(FadeOut(bottomText))

class Last(Scene):
    def construct(self):
        self.camera.background_color = DEFAULT_BACKGROUND_COLOR
        self.wait(1)

        pythonIcon = ImageMobject("python logo").scale(0.3).move_to(1.5*UP+4*LEFT)
        pythonText = Text("Python 3.9.0", font=DEFAULT_FONT).scale(2).next_to(pythonIcon, RIGHT)

        pillow = Text("from PIL import Image", font=DEFAULT_FONT, color=GREEN).to_edge(DOWN)

        
        self.play(FadeIn(pythonIcon))
        self.play(Write(pythonText))
        self.play(Write(pillow))

        self.wait(3)

        self.play(
            FadeOut(pythonIcon),
            FadeOut(pythonText),
            FadeOut(pillow)
        )
        # red gray blue green pink
        dots = [Dot().scale(7.5) for i in range(5)]

        dots[0].set_color(RED)
        dots[1].set_color(GRAY)
        dots[2].set_color(BLUE)
        dots[3].set_color(GREEN)
        dots[4].set_color("#FC0FC0")

        dots[0].to_corner(UP+LEFT)
        dots[1].next_to(dots[0], DOWN)
        dots[2].next_to(dots[1], DOWN)
        dots[3].next_to(dots[2], DOWN)
        dots[4].next_to(dots[3], DOWN)

        self.play(FadeIn(VGroup(*dots, run_time=2, lag_ratio=0.2)))
        text1 = Text("Rejected Point", font=DEFAULT_FONT).next_to(dots[0], RIGHT)
        text2 = Text("Sample Point", font=DEFAULT_FONT).next_to(dots[1], RIGHT)
        text3 = Text("Active List Point", font=DEFAULT_FONT).next_to(dots[2], RIGHT)
        text4 = Text("Valid Point", font=DEFAULT_FONT).next_to(dots[3], RIGHT)
        text41 =Text("(This color is only visible for 1 frame)", font=DEFAULT_FONT).move_to(text4.get_center()+5*RIGHT+0.1*DOWN)
        text41.scale(0.6)
        text5 = Text("Spawn Point", font=DEFAULT_FONT).next_to(dots[4], RIGHT)
        
        self.play(Write(VGroup(text1, text2, text3, text4,text41, text5)))
        
        self.wait(2)

        self.play(FadeOut(VGroup(text1,text2,text3,text4,text41,text5,*dots)))
