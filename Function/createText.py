from pygame import font

def createText(X, Y, size, textColour, weight, textInfo, alignment = "l"):
        fontx = font.Font(f"./Font/Exo2-{weight}.ttf", size)
        text = fontx.render(textInfo, True, textColour)
        textRect = text.get_rect()
        if(alignment == "left" or alignment == "l"):
            textRect = (X // 2, Y // 2) # Left aligned text
        elif(alignment == "center" or alignment == "c"):
            textRect.center = (X//2, Y//2) # Centered text
        elif(alignment == "right" or alignment == "r"):
            textRect.right = (X//2, Y//2) # Right aligned text

        return text, textRect;