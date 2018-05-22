import cv2, funcs

cv2.namedWindow("preview")

handSpace = 0.33333333333
keyMult = 2**(1 / 12)
minF = 261.62
maxF = 523.25

vc = cv2.VideoCapture(0)

while True:

    rval, frame = vc.read()

    if frame is not None:

        frame = cv2.flip(frame, 1)
        #frame = cv2.imread('teste.png',cv2.IMREAD_COLOR)

        h, w, pix = frame.shape

        crop1, percLeft, numLeft = funcs.findHand(
            frame[0:2 * h * handSpace, 0:w * handSpace])

        crop2, percRight, numRight = funcs.findHand(
            frame[0:2 * h * handSpace, 2 * w * handSpace:w])

        frame[0:2 * h * handSpace, 0:w * handSpace] = crop1
        frame[0:2 * h * handSpace, 2 * handSpace * w:w] = crop2

        keys = [
            "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"
        ]

        if int(12 * (1 - percLeft) / keyMult) < 12:
            key = keys[int(12 * (1 - percLeft) / keyMult)]
        else:
            key = keys[11]

        instrument = "None"
        if numLeft == 2:
            instrument = "Guitar"
        if numLeft == 3:
            instrument = "Piano"
        if numLeft == 4:
            instrument = "Flute"
        if numLeft == 5:
            instrument = "Sine"

        if instrument == "None":
            key = "--"

        amplitude = 1.000001 * (1 - percRight)

        cv2.putText(frame, instrument, (225, 350), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 1)
        cv2.putText(frame, key, (225, 400), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (255, 255, 255), 2)

        cv2.circle(frame, (375, 360), int(30 * amplitude), [0, 0, 255], 1)
        cv2.circle(frame, (375, 360), int(26 * amplitude), [0, 0, 255], -1)
        cv2.circle(frame, (375, 360), int(20 * amplitude), [100, 100, 255], -1)
        cv2.circle(frame, (375, 360), int(15 * amplitude), [200, 200, 255], -1)

        cv2.imshow("preview", frame)
    #cv2.imwrite('final.png',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break
