# 🔒 Vaultify - Secure Secret Sharing

Vaultify is a secure, one-time secret sharing web application that allows you to share sensitive information with confidence. Your secrets are encrypted, can only be viewed once, and automatically expire after a set time or number of views.

##  Features

- **End-to-End Encryption**: Your secrets are encrypted before they reach our servers
- **One-Time View**: Links can only be viewed once (configurable)
- **Automatic Expiration**: Set an expiration time for your secrets
- **No Account Needed**: Simple and straightforward to use
- **Open Source**: Transparent and verifiable security
- **Responsive Design**: Works on desktop and mobile devices

##  Quick Start

### Prerequisites

- Python 3.8+
- MongoDB
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vaultify.git
   cd vaultify
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   4.Run the key_generations script to get the encryption key.

5. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   MONGODB_URI=your_mongodb_connection_string
   SECRET_KEY=your_secret_key_here
   ```

6. Run the application:
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

7. Open your browser and visit: `http://localhost:8001`

## 🛠️ Configuration

You can customize the following settings in the `.env` file:

- `MONGODB_URI`: MongoDB connection string
- `SECRET_KEY`: Secret key for encryption
- `HOST`: Host address (default: 0.0.0.0)
- `PORT`: Port number (default: 8001)
- `DEBUG`: Debug mode (True/False)

##  Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t vaultify .
   ```

2. Run the container:
   ```bash
   docker run -d --name vaultify -p 8001:8001 --env-file .env vaultify
   ```

##  Deployment

For production deployment, refer to the [DEPLOYMENT.md](DEPLOYMENT.md) file for detailed instructions on deploying to various platforms.

## 🔧 Technologies Used

- **Backend**: FastAPI
- **Frontend**: HTML, Tailwind CSS
- **Database**: MongoDB
- **Encryption**: AES-256
- **Deployment**: Docker, Render

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- Thanks to all open-source projects that made this possible
- Special thanks to contributors who help improve this project

## 📧 Contact

Anwesha Guha

Project Link: https://github.com/Anwesha290/Vaultify
