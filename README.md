# PBT205 Chat Application

## Overview
This project is a command-line chat application built using Python and RabbitMQ as middleware. It allows multiple users to communicate in real time through a shared chat room.

## Features
- Uses RabbitMQ as middleware
- Real-time messaging
- Multiple users supported
- Command-line interface

## Setup Instructions

### 1. Run RabbitMQ (Docker)
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

### 2. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install pika

### 3. Run the application
Terminal 1:
python3 chat.py Eva localhost

Terminal 2:
python3 chat.py Alex localhost

## Usage
Type messages and press Enter.
Type exit to quit.

## Technologies Used
- Python
- RabbitMQ
- Docker
