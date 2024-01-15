from ultralytics import YOLO
import cv2
import cvzone
import math
import RoyalRushFunction  # Make sure this is available

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Load YOLO model
model = YOLO('code\last.pt')

# Class names for the playing cards
classnames = ['10C', '10D', '10H', '10S',
              '2C', '2D', '2H', '2S',
              '3C', '3D', '3H', '3S',
              '4C', '4D', '4H', '4S',
              '5C', '5D', '5H', '5S',
              '6C', '6D', '6H', '6S',
              '7C', '7D', '7H', '7S',
              '8C', '8D', '8H', '8S',
              '9C', '9D', '9H', '9S',
              'AC', 'AD', 'AH', 'AS',
              'JC', 'JD', 'JH', 'JS',
              'KC', 'KD', 'KH', 'KS',                                           
              'QC', 'QD', 'QH', 'QS']

while True:
    # Capture frame from webcam
    success, img = cap.read()

    # Perform object detection using YOLO
    results = model(img, stream=True)

    # Initialize list to store recognized playing cards
    hand = []

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            # Draw rectangle around the detected card
            cvzone.cornerRect(img, (x1, y1, w, h))

            # Display class name and confidence level
            conf = round(float(box.conf[0]), 2)
            cls = int(box.cls[0])
            cvzone.putTextRect(img, f'{classnames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            # If confidence is above 0.5, add the card to the hand
            if conf > 0.5:
                hand.append(classnames[cls])

    # Remove duplicate cards from the hand
    hand = list(set(hand))

    # If five cards are detected, determine the poker hand
    if len(hand) == 5:
        poker_hand_results = RoyalRushFunction.find_poker_hand(hand)
        poker_hand = RoyalRushFunction.POKER_HAND_RANKS[poker_hand_results]

        # Display the determined poker hand
        cvzone.putTextRect(img, f'Your Hand: {poker_hand}', (300, 75), scale=3, thickness=5)

    # Display the processed image
    cv2.imshow("Image", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
