WinActivate, Roblox
WinWaitActive, Roblox

WinGetPos, X, Y, W, H, Roblox
CenterX := X + W // 2
CenterY := Y + H // 2

MouseMove, %CenterX%, %CenterY%, 0
MouseDown, right
MouseMove, %CenterX%, % (CenterY + 100), 0
MouseUp, right
