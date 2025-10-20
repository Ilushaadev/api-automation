# Digital Library API

A platform-agnostic Flask application with authentication, RESTful API, and comprehensive CI/CD support.

## Features

- **RESTful API** with Swagger/OpenAPI documentation
- **Dual Authentication**: API Key and JWT Bearer token support
- **Configuration Management**: Environment-based configuration system
- **Docker Support**: Multi-stage builds for optimized images
- **CI/CD Ready**: GitHub Actions and Jenkins pipelines included
- **Platform Agnostic**: Easily deployable to any cloud provider or on-premise

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- Git

### Local Development

1. **Clone and setup environment:**
```bash
git clone <repository-url>
cd jenkins-demo
cp .env.example .env
```

2. **Edit `.env` file with your configuration:**
```bash
# Required: Set your API keys
API_KEY=your-api-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

3. **Install dependencies:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python app.py
```

5. **Access Swagger UI:**
Open `http://localhost:5001/swagger/` in your browser

## Configuration

The application uses environment variables for configuration. All settings can be customized via `.env` file or environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `5001` | Server port |
| `DEBUG` | `false` | Debug mode |
| `ENV` | `development` | Environment (development/production/test) |
| `API_KEY` | *Required* | API key for authentication |
| `JWT_SECRET_KEY` | *Required* | Secret key for JWT tokens |
| `JWT_EXPIRATION_HOURS` | `2` | JWT token expiration time |
| `ADMIN_USER` | `admin` | Admin username |
| `ADMIN_PASSWORD` | `password123` | Admin password |

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker CLI

```bash
# Build image
docker build -t jenkins-demo-app .

# Run container
docker run -d \
  -p 5001:5001 \
  --env-file .env \
  --name jenkins-demo-app \
  jenkins-demo-app
```

## Platform-Specific Deployment

### AWS (Elastic Container Service)

```bash
# Build for AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t jenkins-demo-app .
docker tag jenkins-demo-app:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/jenkins-demo-app:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/jenkins-demo-app:latest

# Deploy to ECS using Task Definition
```

### Google Cloud Platform (Cloud Run)

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/jenkins-demo-app
gcloud run deploy jenkins-demo-app \
  --image gcr.io/PROJECT-ID/jenkins-demo-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_KEY=xxx,JWT_SECRET_KEY=xxx
```

### Azure (Container Instances)

```bash
# Build and push to Azure Container Registry
az acr build --registry <registry-name> --image jenkins-demo-app:latest .

# Deploy to Azure Container Instances
az container create \
  --resource-group myResourceGroup \
  --name jenkins-demo-app \
  --image <registry-name>.azurecr.io/jenkins-demo-app:latest \
  --dns-name-label jenkins-demo-app \
  --ports 5001 \
  --environment-variables API_KEY=xxx JWT_SECRET_KEY=xxx
```

### Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jenkins-demo-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: jenkins-demo-app
  template:
    metadata:
      labels:
        app: jenkins-demo-app
    spec:
      containers:
      - name: app
        image: jenkins-demo-app:latest
        ports:
        - containerPort: 5001
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
```

```bash
kubectl apply -f deployment.yaml
```

### Heroku

```bash
# Login to Heroku
heroku login
heroku container:login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set API_KEY=xxx JWT_SECRET_KEY=xxx

# Deploy
heroku container:push web
heroku container:release web
```

## CI/CD

### GitHub Actions

The project includes a complete GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:
- Runs tests on every push and PR
- Performs code quality checks
- Builds multi-platform Docker images
- Runs security scans
- Publishes to GitHub Container Registry

**Setup:**
No additional setup needed - workflow runs automatically on push.

### Jenkins

The `Jenkinsfile` defines a complete pipeline with:
- Environment setup
- Linting
- Testing with coverage
- Docker image building
- Security scanning
- Automated deployment

**Setup:**
1. Create a new Pipeline job in Jenkins
2. Point to your repository
3. Configure credentials for Docker registry (if pushing images)
4. Run the pipeline

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

## API Documentation

### Authentication

Two methods are supported:

**1. API Key Authentication:**
```bash
curl -H "ApiKey: your-api-key" http://localhost:5001/books/get_books
```

**2. JWT Bearer Token:**
```bash
# Get token
curl -X POST http://localhost:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'

# Use token
curl -H "Authorization: Bearer <token>" http://localhost:5001/books/get_books
```

### Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | None | Welcome message |
| GET | `/health` | None | Health check |
| POST | `/auth/login` | None | Get JWT token |
| GET | `/books/get_books` | Required | Get all books |
| POST | `/books/add_book` | Required | Add a new book |
| GET | `/swagger/` | None | Interactive API documentation |

## Project Structure

```
jenkins-demo/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD
├── tests/                      # Test suite
├── app.py                      # Main application
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Docker Compose configuration
├── Jenkinsfile                 # Jenkins pipeline
├── .env.example                # Environment template
├── .dockerignore               # Docker ignore rules
└── README.md                   # This file
```

## Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Use strong secrets** in production - Change default passwords
3. **Enable HTTPS** when deploying to production
4. **Use secrets management** - AWS Secrets Manager, Azure Key Vault, etc.
5. **Regular updates** - Keep dependencies up to date
6. **Container scanning** - Use Trivy or similar tools

## Troubleshooting

### Application won't start
- Check that `.env` file exists and has required variables
- Verify API_KEY and JWT_SECRET_KEY are set
- Check port 5001 is not already in use

### Docker build fails
- Ensure Docker daemon is running
- Check internet connectivity for downloading dependencies
- Verify requirements.txt is valid

### Tests fail
- Set test environment variables: `API_KEY=test-api-key JWT_SECRET_KEY=test-jwt-secret`
- Check Python version is 3.11+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
