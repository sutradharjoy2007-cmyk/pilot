# Django User Panel Application

A modern, responsive Django web application with user authentication, profile management, and AI agent configuration.

## Features

- ✅ **KYC Verification**: Mandatory document upload (NID/Passport) and admin approval process
- ✅ **AI Agent Control**: Global toggle to enable/disable the AI agent
- ✅ **Blocked Posts**: Dynamic list to block AI responses on specific Facebook posts
- ✅ **Auto-Save**: Real-time saving of AI configuration with visual feedback
- ✅ **Email Notifications**: Automatic emails for KYC status changes (Approved/Rejected)
- ✅ **Public API**: Extended endpoints for retrieving user configuration and status
- ✅ **Subscription System**: Admin-assigned time packages (7, 15, 30 days) with auto-expiration
- ✅ **Phone Number & Business Info**: Collects contact and business details for professional profiles
- ✅ **Public Privacy Policy**: Auto-generated, theme-matched privacy policy page for each user
- ✅ **Subscription History**: Admin tracks all package changes and assignments
- ✅ **Admin Dashboard**: Custom "New Users Today" widget for quick onboarding tracking
- ✅ **Modern UI**: Polished interface with Tailwind CSS and responsive design
- ✅ **SQLite3 Database**: Lightweight and easy to set up

## Subscription System

The application includes a built-in subscription management system:

1. **Admin Assignment**: Admins can select users in the Django admin panel and assign 7, 15, or 30-day packages.
2. **Dashboard Tracking**: Users can see their active package and expiration date on the dashboard.
3. **Access Control**: Middleware automatically blocks access to the panel once the subscription expires.
4. **Expiration Handling**: Expired users are redirected to a "Package Expired" page. AI Agent is automatically disabled.
5. **History Tracking**: All package assignments are logged in the admin panel for audit purposes.

## Tech Stack

- **Backend**: Django 6.0.2
- **Database**: SQLite3
- **Frontend**: HTML, Tailwind CSS (CDN)
- **Image Handling**: Pillow

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Start Development Server

```bash
python manage.py runserver
```

### 5. Access the Application

- **Main URL**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Login**: http://127.0.0.1:8000/login/
- **Register**: http://127.0.0.1:8000/register/

## Usage

### Registration
1. Navigate to the registration page
2. Enter your email, phone number, and password
3. Click "Create Account"
4. You'll be automatically logged in and redirected to the dashboard

### Profile Management
1. Click "Profile" in the sidebar
2. Upload a profile picture
3. Enter your name, mobile number, and business information
4. Click "Save Changes"
5. **Privacy Policy**: A public link to your privacy policy is generated automatically. You can copy it to share.

### AI Agent Configuration
1. **KYC Verification**: You must be Verified to access this page.
2. **Toggle Power**: Use the switch to turn your agent On or Off.
3. **Configuration**: Enter Facebook Page ID, API Key, and System Prompt.
   - **Auto-Save**: Changes are saved automatically as you type.
4. **Blocked Posts**: Add Facebook Post IDs to prevent the AI from responding to specific posts.
5. **Webhook**: Copy the generated URL to your Facebook App settings.

### KYC Verification Process
1. Go to **Profile** and upload your NID or Passport.
2. Status will change to **Pending**.
3. Admin reviews the document in the Django Admin Panel.
4. Upon **Approval**, you receive an email and gain access to AI features.
5. If **Rejected**, you receive an email with instructions to resubmit.

### API Documentation
External services can retrieve user configuration via the public API:

**Endpoint**: `/api/user/{admin_password}/{email_prefix}/{field}/`

**Fields**:
- `ai_agent_status`: Returns `{"status": "on"}` or `{"status": "off"}`.
- `block_post_ids`: Returns `{"blocked_post_ids": ["123", "456"]}`.
- `all`: Returns full configuration including status and blocked list.

## Webhook URL Format

The webhook URL is automatically generated based on your email address:

- **Format**: `https://ftn8nbd.onrender.com/webhook-test/{email_prefix}`
- **Example**: For email `joysd2005@gmail.com`, the webhook URL will be:
  ```
  https://ftn8nbd.onrender.com/webhook-test/joysd2005
  ```

## Project Structure

```
userpanel/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── userpanel_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── templatetags/
│   │   └── admin_dashboard_extras.py
│   └── templates/
│       ├── base.html
│       └── accounts/
│           ├── register.html
│           ├── login.html
│           ├── dashboard.html
│           ├── profile.html
│           ├── ai_agent.html
│           └── privacy_policy.html
├── templates/
│   └── admin/
│       └── custom_dashboard.html
├── static/
└── media/
```

## Features in Detail

### Authentication System
- Custom user model with email as username
- Secure password hashing
- Login/logout functionality
- Protected views with login_required decorator

### Responsive Design
- Mobile-first approach
- Hamburger menu for mobile devices
- Responsive grid layouts
- Tailwind CSS for modern styling

### User Profile
- Profile picture upload with preview
- Personal information management
- One-to-one relationship with User model

### AI Agent Configuration
- Facebook Page ID storage
- AI system prompt customization
- Auto-generated webhook URL
- Copy to clipboard functionality

## Database Models

### CustomUser
- Email (unique, used for login)
- Password (hashed)

### UserProfile
- User (OneToOne)
- Name
- Profile Picture
- Mobile Number

### AIAgentConfig
- User (OneToOne)
- Facebook Page ID
- System Prompt

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (for production)
```bash
python manage.py collectstatic
```

## License

This project is open source and available for use.

## Support

For issues or questions, please refer to the walkthrough documentation.
