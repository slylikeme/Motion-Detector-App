import cv2, time, pandas
from datetime import datetime

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

video = cv2.VideoCapture(0)  # creates the video object
time.sleep(2)  # allows webcam to initialize properly

while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # apply blur to increase accuracy

    if first_frame is None:  # fires on first loop
        first_frame = gray
        continue  # skips rest of the code on the first loop

    # compares differences between frames
    delta_frame = cv2.absdiff(first_frame, gray)

    # anything beyond a threshold of 30 difference is assigned to white
    # returns a tuple, but only need second item of tuple so [1]
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # smooth out the thresh_frame
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=3)

    # find the contours and check the area of the contours
    # make copy of threshframe, retrieve external, approximate contours
    (_, cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # filter out the conturs and keep the ones with area larger than 1000 pixels
    # Create rectangle around large contours
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # append status to status_list to track start and end
    status_list.append(status)

    # check whether last two items of list are changing; if so append datetime to times list
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    # create frames
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(100)  # time the program waits on each frame display

    if key == ord('q'):  # sets q to break out of the loop
        if status == 1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()
