# PoC: Sistema de Pagos con REST, RabbitMQ y Kafka  
*(Compatibilidad multiplataforma: macOS, Linux y Windows)*  

## Tabla de Contenidos
- [Prerrequisitos por SO](#-prerrequisitos-por-sistema-operativo)
  - [macOS](#-macos)
  - [Linux](#-linux-ubuntudebian)
  - [Windows](#-windows-powershell-como-admin)
- [Configuración Inicial](#-configuración-inicial)
- [Entorno Python](#-entorno-python)
- [Ejecución del Sistema](#-ejecución-del-sistema)
- [Ejemplo de Request](#-ejemplo-de-request)
- [Limpieza](#-limpieza)
- [Diagrama de Arquitectura](#-diagrama-de-arquitectura)
- [Solución de Problemas](#-solución-de-problemas-comunes)
- [Recursos Adicionales](#-recursos-adicionales)

## ⚙️ Prerrequisitos por Sistema Operativo

### 🔵 macOS
```bash
# 1. Instalar Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar dependencias
brew install python@3.10 rabbitmq kafka openjdk@11

# 3. Configurar PATH para Kafka
echo 'export PATH="/opt/homebrew/opt/kafka/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

Linux (Ubuntu/Debian)

# 1. Instalar dependencias
sudo apt update
sudo apt install -y python3 python3-pip rabbitmq-server openjdk-11-jdk

# 2. Instalar Kafka
wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
tar -xzf kafka_2.13-3.7.0.tgz
sudo mv kafka_2.13-3.7.0 /opt/kafka

# 3. Configurar PATH
echo 'export PATH="/opt/kafka/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

Windows (PowerShell como Admin)

# 1. Instalar Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 2. Instalar dependencias
choco install python rabbitmq kafka -y

# 3. Configurar variables de entorno
[System.Environment]::SetEnvironmentVariable("PATH", "$env:PATH;C:\kafka\bin", [System.EnvironmentVariableTarget]::Machine)

Configuración Inicial

1. Iniciar Servicios
macOS:

brew services start rabbitmq
brew services start kafka

Linux:

sudo systemctl start rabbitmq-server
/opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties &
/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties &

Windows:

rabbitmq-service start
Start-Process -FilePath "C:\kafka\bin\windows\zookeeper-server-start.bat" -ArgumentList "C:\kafka\config\zookeeper.properties"
Start-Process -FilePath "C:\kafka\bin\windows\kafka-server-start.bat" -ArgumentList "C:\kafka\config\server.properties"

2. Crear Cola y Tópico

# Cola en RabbitMQ
rabbitmqadmin declare queue name=payments_approved durable=true

# Tópico en Kafka
kafka-topics --create --topic pedidos --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

Entorno Python

1. Crear y activar entorno virtual
macOS/Linux:


python3 -m venv venv
source venv/bin/activate

Windows:

python -m venv venv
.\venv\Scripts\activate


2. Instalar dependencias

pip install fastapi uvicorn pika kafka-python python-dotenv pydantic

Ejecución del Sistema

1. Servicio REST:
uvicorn app.main:app --reload

Endpoint: http://localhost:8000/validate-payment

2. Consumidor RabbitMQ → Kafka:

python consumers/rabbit_to_kafka.py

Ejemplo de Request

curl -X POST "http://localhost:8000/validate-payment" \
  -H "Content-Type: application/json" \
  -d '{"document": "12345678", "amount": 1500}'

  Limpieza

  macOS:

  brew services stop rabbitmq kafka
  
  Linux:
  sudo systemctl stop rabbitmq-server
kill $(ps aux | grep '[k]afka' | awk '{print $2}')

Windows:

rabbitmq-service stop
taskkill /IM "java.exe" /F