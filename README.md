
# **Daily Journal App** 📝

## **Overview** 🌟

The **Daily Journal App** is a web-based journaling platform built with **Streamlit** and **Firebase**. It offers a private, secure, and user-friendly environment where individuals can log in, create, and review journal entries. The app focuses on ensuring privacy, accessibility, and an easy-to-navigate experience.

## **Features** ✨

* **User Authentication** 🔒 with Firebase
* **Create Journal Entries** ✍️ (with title and content)
* **View Past Entries** 📜
* **Mobile-Optimized Design** 📱
* **Real-Time Database** with **Firebase Firestore** 📂
* **Logout Functionality** 🚪

## **Tech Stack** 💻

* **Frontend**: Streamlit
* **Backend**: Firebase (Authentication & Firestore)
* **Language**: Python

## **Installation** ⚙️

To install the required dependencies, run:

```bash
pip install streamlit firebase-admin
```

## **How It Works** 🚀

1. **Login**: Users sign up or log in using Firebase Authentication 🔑.
2. **Create Journal Entries**: Users can easily write and save their journal entries with a title and content ✨.
3. **View Entries**: Past journal entries are displayed in an organized manner 📚.
4. **Logout**: Securely log out of the app to protect your data 🔐.

## **Firebase Configuration** 🔑

Make sure to set up a **Firebase** project and integrate the service account credentials into the app for authentication and database operations.

## **Steps to Set Up Firebase** 🔧

1. Go to the Firebase Console: [https://console.firebase.google.com](https://console.firebase.google.com)
2. Create a new project (or use an existing one).
3. Enable **Firebase Authentication** (Email/Password method).
4. Set up **Firestore Database** for storing journal entries.
5. Create a **Service Account** for Firebase Admin SDK and download the JSON file.
6. Add the downloaded JSON file in your project for authentication.

## **Running the App** 🚀

After setting up the Firebase configuration, run the app with:

```bash
streamlit run journal_app.py
```

## **Future Enhancements** 🔮

* **Text Analysis**: Sentiment analysis to better understand journaling moods 💬
* **Daily Prompts**: Encourage consistent journaling with daily writing prompts 🌅
* **Data Export**: Export journal entries as PDFs or text files 📥

## **Contributing** 🤝

Contributions are welcome! Feel free to fork this repository, create a branch, and submit a pull request.

