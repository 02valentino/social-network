# 🌐 Django Social Network

A social media platform built with Django featuring user profiles, friend connections, posts, comments, likes, and real-time notifications.

🌐 *Live Demo*: [web-production-46f7.up.railway.app](https://web-production-46f7.up.railway.app)

## ✨ Features

- � **User Profiles**: Custom profiles with bio, profile pictures, and personal info
- 👥 **Friend System**: Send/accept friend requests and manage connections
- 📝 **Posts**: Create posts with visibility controls (Public/Friends/Private)
- 💬 **Comments**: Comment on posts and engage with content
- ❤️ **Likes**: Like/unlike posts with real-time counters
- 🔔 **Notifications**: Real-time notifications for interactions
- 🛡️ **Moderation**: Admin tools for content and user management
- 📱 **Responsive**: Mobile-friendly design

## 🛠️ Tech Stack

- **Backend**: Django 5.2.3, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Features**: Custom User Model, Real-time Notifications, File Uploads

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone and setup**

   ```bash
   git clone <repository-url>
   cd social_network
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database setup**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Run the server**

   ```bash
   python manage.py runserver
   ```

4. **Access the app**
   - Website: `http://127.0.0.1:8000`
   - Admin: `http://127.0.0.1:8000/admin`

## 📖 How to Use

### Getting Started

1. **Sign Up**: Create your account on the welcome page
2. **Complete Profile**: Add bio, profile picture, and personal info
3. **Find Friends**: Search for users and send friend requests
4. **Create Posts**: Share content with different visibility settings
5. **Engage**: Like posts, leave comments, and stay connected


## 👤 Demo Accounts (For Testing)

Use these demo accounts to explore the platform without signing up:

| Username | Password  | Role        |
|----------|-----------|-------------|
| kevin    | demopass  | Moderator   |
| sara     | demopass  | Regular User|
| john     | demopass  | Regular User|

✅ You can:
- Log in and test features like posting, liking, commenting
- Use Kevin's account to access moderator tools
- Interact between users to simulate a live social environment


### Main Features

**📝 Creating Posts**

- Click "Create Post" from the main feed
- Choose visibility: 🌍 Public, 👥 Friends, or � Private
- Write your content and publish

**👥 Managing Friends**

- Send friend requests from user profiles
- Accept/decline requests in notifications
- View your friends list and their posts

**🔔 Notifications**

- Get real-time notifications for interactions
- Mark as read or delete notifications
- See unread count in the navigation

**🛡️ For Moderators**

- Access moderator dashboard
- Ban/unban users
- Delete inappropriate posts

## � Project Structure

```
social_network/
├── manage.py                    # Django management
├── requirements.txt             # Dependencies
├── db.sqlite3                   # Database
├── social_network/              # Main config
├── users/                       # User management
├── network/                     # Social features
├── templates/                   # HTML templates
├── static/                      # CSS/JS files
└── media/                       # User uploads
```

1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information
4. Contact the development team

---

**Built with ❤️ using Django** | Last updated: July 2025
