### Visitor Insight

1. **Introduction**
   The Internet of Things (IoT) has significantly transformed various aspects of daily life, particularly in enhancing the security of homes and offices. Traditional security systems, which relied on physical locks and keys, faced challenges such as theft and misplacement. With the advent of technology-driven solutions, modern security systems have become more sophisticated. The "Visitor Insight" project aims to elevate home security by integrating IoT and facial recognition into a smart visitor recognition system. This system notifies homeowners through a smartphone app when someone is at their door. If the visitor is recognized and within the allowed entry timings, access is granted automatically. Otherwise, the homeowner is alerted to make a decision on whether to allow or deny entry. The system offers significant advantages over traditional methods by enabling automated access control based on time-based heuristics and providing real-time notifications.

2. **Proposed Idea**
   "Visitor Insight" automates the process of visitor recognition and door access control. The system categorizes visitors into various groups such as family members, daily visitors, and occasional guests. Family members receive unrestricted access, while daily visitors are only allowed during specific hours. Upon a visitor's approach, the system captures their image via a camera, processes it through a facial recognition algorithm, and determines the appropriate access rights. If the visitor is unrecognized, the homeowner is notified and can choose to add the new visitor to the system, which then updates its model to recognize the visitor in the future.

3. **Methodology**
   The "Visitor Insight" system operates online, utilizing real-time facial recognition to make access control decisions. After evaluating several machine learning models, including K-Nearest Neighbors (KNN) and Support Vector Machines (SVM), KNN was selected for its superior performance in real-time applications. Notifications are sent to homeowners via Telegram, and the system allows real-time updates to the visitor database.

   3.1 **Dataset**
   For face detection and recognition, multiple datasets were considered, including:
   - The Extended Yale Face Database B
   - Yale Face Dataset
   - A dataset from the Robotics Laboratory of National Cheng Kung University

   The Extended Yale Face Database B was chosen due to its suitable format and features. A subset of this dataset, comprising 10 subjects with 100 images each, was used for training and testing.

   3.2 **Data Pre-processing**
   To enhance model robustness, image augmentation techniques such as shearing and rotation were applied to images captured by a webcam. The final system builds its database in real-time using these processed webcam images.

   3.3 **Face Recognition**
   The face recognition process involves generating a 128-dimensional vector encoding that represents a person's facial features. This encoding is compared with stored encodings of registered users. If the distance between the new encoding and the closest match falls below a certain threshold, the visitor is recognized; otherwise, they are marked as unknown.

   3.4 **ML Model Analysis**
   KNN and SVM were implemented and compared using the customized dataset. Evaluation criteria included accuracy, training time, and prediction time. KNN demonstrated slightly better accuracy and faster training time, making it the preferred choice for real-time face recognition in this system.

4. **Results**
   The "Visitor Insight" system was tested in a residential setting under various scenarios:
   - **Case 1**: An unknown person attempts entry, triggering a notification.
   - **Case 2**: A recognized individual arrives outside allowed timings, prompting a notification.
   - **Case 3**: A family member arrives at any time and is granted automatic access.
   - **Case 4**: A new visitor is added to the system, updating the recognition model.

5. **Discussion and Future Work**
   While the primary focus of "Visitor Insight" is on enhancing home security, its potential applications extend to various other domains. For instance, the system could be adapted for secure access in banks, office environments, or toll plazas, utilizing license plate recognition instead of facial recognition.

6. **Conclusion**
   "Visitor Insight" successfully integrates IoT and machine learning to create an intelligent visitor recognition system that automates decision-making based on time-based heuristics. This project enhances security and convenience, laying the groundwork for future developments that could expand its applicability to other environments and applications.
