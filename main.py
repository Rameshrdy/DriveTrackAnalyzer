import cv2
import time

# Define the absolute paths for the cascade classifier and video source
cascade_src = r'C:\Users\ADMIN\Documents\Custom Office Templates\Speed_Detection_CV-master\dataset\cars1.xml'
video_src = r'C:\Users\ADMIN\Documents\Custom Office Templates\Speed_Detection_CV-master\dataset\video3.mp4'

# Coordinates for lines
ax1 = 70
ay = 90
ax2 = 230

bx1 = 15
by = 125
bx2 = 225

# Function to calculate speed
def Speed_Cal(time):
    try:
        Speed = (9.144 * 3600) / (time * 1000)
        return Speed
    except ZeroDivisionError:
        print(5)

# Function to calculate distance
def Distance_Cal(speed, time):
    return speed * time

# Car number, start time, video capture
i = 1
start_time = time.time()
cap = cv2.VideoCapture(video_src)
car_cascade = cv2.CascadeClassifier(cascade_src)

# Create a full-screen window
cv2.namedWindow('video', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, img = cap.read()
    if type(img) == type(None):
        break

    blurred = cv2.blur(img, ksize=(15, 15))
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 2)

    cv2.line(img, (ax1, ay), (ax2, ay), (255, 0, 0), 2)
    cv2.line(img, (bx1, by), (bx2, by), (255, 0, 0), 2)

    for (x, y, w, h) in cars:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.circle(img, (int((x + x + w) / 2), int((y + y + h) / 2)), 1, (0, 255, 0), -1)

        while int(ay) == int((y + y + h) / 2):
            start_time = time.time()
            break

        while int(ay) <= int((y + y + h) / 2):
            if int(by) <= int((y + y + h) / 2) and int(by + 10) >= int((y + y + h) / 2):
                cv2.line(img, (bx1, by), (bx2, by), (0, 255, 0), 2)
                current_time = time.time()
                elapsed_time = current_time - start_time
                Speed = Speed_Cal(elapsed_time)
                Distance = Distance_Cal(Speed, elapsed_time)
                print(f"Car Number {i} Speed: {Speed} KM/H Distance: {Distance} meters")
                i += 1
                cv2.putText(img, f"Speed: {Speed} KM/H Distance: {Distance:.2f} meters", (x, y - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                break
            else:
                cv2.putText(img, "Calculating", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                break

    cv2.imshow('video', img)

    if cv2.waitKey(33) == 27:
        break

cap.release()
cv2.destroyAllWindows()

