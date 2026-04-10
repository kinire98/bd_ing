from dotenv import load_dotenv
import boto3
import json
import os

load_dotenv()
# Creamos el cliente de SQS
session = boto3.Session(
        aws_access_key_id=os.getenv("aws_access_key_id"),
        aws_secret_access_key=os.getenv("aws_secret_access_key"),
        aws_session_token=os.getenv("aws_session_token"),
        region_name='us-east-1'
    )
sqs = session.client('sqs')

# Definimos la URL de la cola
queue_url = 'MiBuzon'

# Creamos un diccionario (JSON) con los datos
datos_archivo = {
        "prioridad": "ALTA",
        "mensaje": "Mensaje de procesamiento, desde el script"
}

# Serializamos el diccionario
mensaje_serializado = json.dumps(datos_archivo)

# Enviamos el mensaje
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=mensaje_serializado
)
print("Respuesta prioridad alta:", response)


# Creamos un diccionario (JSON) con los datos
datos_archivo = {
        "prioridad": "BAJA",
        "mensaje": "Mensaje de procesamiento, desde el script"
}

# Serializamos el diccionario
mensaje_serializado = json.dumps(datos_archivo)

# Enviamos el mensaje
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=mensaje_serializado
)

print("Respuesta prioridad baja:", response)
# Creamos un diccionario (JSON) con los datos
datos_archivo = {
        "prioridad": "MEDIA",
        "mensaje": "Mensaje de procesamiento, desde el script"
}

# Serializamos el diccionario
mensaje_serializado = json.dumps(datos_archivo)

# Enviamos el mensaje
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=mensaje_serializado
)

print("Respuesta prioridad media:", response)
