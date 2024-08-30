# Visitor-Insight
Machine Learning, Facial Recognition, Real-Time Notification Systems

– Developed a Machine Learning-based system for advanced visitor recognition by encoding facial features for accurate identification.

– Implemented real-time notification delivery to alert users immediately upon visitor detection


## Features

- **Automatic Entry:** Recognized visitors within allowed timings are granted entry automatically.
- **Time-Based Heuristics:** Visitors can be categorized based on their relationship with the homeowner, with different rules for entry.
- **Real-Time Notifications:** Homeowners receive notifications via Telegram for unknown visitors or visitors outside of allowed timings.
- **Dynamic Database:** New visitors can be added to the system in real-time, with the facial recognition model retrained automatically.
- **Robust Facial Recognition:** The system uses KNN for accurate and efficient face recognition.

## Technologies Used

- **IoT:** The system uses a webcam as an IoT sensor to capture visitor images.
- **Machine Learning:** KNN is employed for real-time facial recognition, with support for real-time model updates.
- **Telegram API:** Notifications are sent to the homeowner via Telegram, allowing for remote management.

## Usage
- The system captures images of visitors when they approach the door.
- Recognized visitors within allowed timings are granted entry automatically.
- For unknown visitors or visitors outside allowed timings, the homeowner is notified via Telegram to decide whether to allow entry.
- New visitors can be added to the system through the Telegram interface, with the model updated in real-time.

## Future Enhancements
- Extend the system for use in office spaces, banks, and toll plazas.
- Implement priority-based entry for different visitor categories.
- Integrate with other IoT devices for enhanced security features.
