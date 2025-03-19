# Use an official lightweight Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the bot's requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot's source code into the container
COPY . .

# Set environment variables (optional, recommended to use secrets in production)
ENV DISCORD_TOKEN=${discord_token}

# Command to run the bot
CMD ["python", "main.py"]
