# 🚀 Deploying Vaultify to Render.com

This guide will help you deploy your Vaultify application to Render.com.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **MongoDB Atlas Account**: For the database (free tier available)
3. **Render.com Account**: Free tier available

## 🗄️ Step 1: Set Up MongoDB Atlas

### 1.1 Create MongoDB Atlas Cluster
1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free account
3. Create a new cluster (M0 Free tier)
4. Choose your preferred cloud provider and region

### 1.2 Configure Database Access
1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Create a username and password (save these!)
4. Set privileges to "Read and write to any database"

### 1.3 Configure Network Access
1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (0.0.0.0/0)

### 1.4 Get Connection String
1. Go to "Database" in the left sidebar
2. Click "Connect"
3. Choose "Connect your application"
4. Copy the connection string
5. Replace `<password>` with your actual password
6. Add `?retryWrites=true&w=majority` at the end

## 🔑 Step 2: Generate Encryption Key

Run this command to generate a secure encryption key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Save this key - you'll need it for the environment variables.

## 🌐 Step 3: Deploy to Render

### 3.1 Connect Your Repository
1. Go to [Render.com](https://render.com)
2. Sign up/Login with your GitHub account
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository

### 3.2 Configure the Service
- **Name**: `vaultify` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3.3 Set Environment Variables
Add these environment variables in Render:

| Variable | Value | Description |
|----------|-------|-------------|
| `MONGODB_URI` | `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority` | Your MongoDB connection string |
| `ENCRYPTION_KEY` | `your-generated-key-here` | The encryption key you generated |
| `ENVIRONMENT` | `production` | Set to production mode |

### 3.4 Deploy
1. Click "Create Web Service"
2. Render will automatically build and deploy your app
3. Wait for the build to complete (usually 2-5 minutes)

## 🔧 Step 4: Verify Deployment

### 4.1 Check Health Endpoint
Visit: `https://your-app-name.onrender.com/health`

You should see:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000+00:00"
}
```

### 4.2 Test the Application
1. Visit your app URL: `https://your-app-name.onrender.com`
2. Create a test secret
3. Copy the generated link
4. Open the link in an incognito window
5. Verify the secret is displayed correctly

## 🛠️ Troubleshooting

### Common Issues:

#### 1. Build Fails
- Check that all dependencies are in `requirements.txt`
- Ensure Python version compatibility
- Check build logs in Render dashboard

#### 2. Database Connection Fails
- Verify MongoDB Atlas network access allows all IPs
- Check connection string format
- Ensure database user has correct permissions

#### 3. App Crashes on Start
- Check environment variables are set correctly
- Verify encryption key is properly formatted
- Check application logs in Render dashboard

#### 4. Static Files Not Loading
- Ensure static files are in the correct directory
- Check file permissions
- Verify static file mounting in FastAPI

### Debug Commands:

```bash
# Check if MongoDB is accessible
python -c "from pymongo import MongoClient; client = MongoClient('your-connection-string'); print(client.server_info())"

# Test encryption
python -c "from app.encryption import encrypt_secret, decrypt_secret; print(decrypt_secret(encrypt_secret('test')))"
```

## 🔒 Security Considerations

1. **Environment Variables**: Never commit sensitive data to your repository
2. **MongoDB Security**: Use strong passwords and restrict network access when possible
3. **HTTPS**: Render provides HTTPS by default
4. **Encryption**: Your encryption key should be kept secure

## 📈 Scaling

### Free Tier Limitations:
- 750 hours/month
- Sleeps after 15 minutes of inactivity
- 512MB RAM
- Shared CPU

### Upgrading:
- Consider paid plans for production use
- Add custom domains
- Enable auto-scaling
- Set up monitoring

## 🎉 Success!

Your Vaultify application is now deployed and accessible worldwide! 

**Your app URL**: `https://your-app-name.onrender.com`

Remember to:
- Monitor your application logs
- Set up alerts for downtime
- Regularly backup your MongoDB data
- Keep dependencies updated 