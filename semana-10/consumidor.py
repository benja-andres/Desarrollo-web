import argparse
import json
import time
import xml.etree.ElementTree as ET

import stomp

DESTINO = "/queue/pedidos"


def interpretar(formato, body):
    """Desempaqueta el cuerpo según el formato y retorna un texto para mostrar."""
    if formato == "texto":
        return f"Texto: {body}"

    if formato == "fijo":
        if len(body) != 36:
            raise ValueError(f"Largo inválido: {len(body)} (se esperaban 36)")
        id_ = body[0:6].strip()
        cliente = body[6:26].strip()
        monto = body[26:36].strip()
        if not id_.isdigit():
            raise ValueError(f"id no numérico: '{id_}'")
        if not cliente:
            raise ValueError("cliente vacío")
        float(monto)  # lanza ValueError si no es número
        return f"Fijo -> id={int(id_)}, cliente={cliente}, monto={monto}"

    if formato == "json":
        datos = json.loads(body)
        return f"JSON -> {datos}"

    if formato == "xml":
        raiz = ET.fromstring(body)
        if raiz.tag != "pedido":
            raise ValueError(f"Raíz inesperada: <{raiz.tag}>")
        id_ = raiz.findtext("id")
        cliente = raiz.findtext("cliente")
        monto = raiz.findtext("monto")
        return f"XML -> id={id_}, cliente={cliente}, monto={monto}"

    raise ValueError(f"Formato desconocido: {formato}")


def detectar_formato(headers):
    formato = headers.get("x-formato")
    if formato:
        return formato.lower()
    content_type = headers.get("content-type", "")
    if "json" in content_type:
        return "json"
    if "xml" in content_type:
        return "xml"
    return "texto"


class Escuchador(stomp.ConnectionListener):
    def __init__(self, conexion):
        self.conexion = conexion

    def on_message(self, frame):
        ack_id = frame.headers["ack"]
        subscripcion = frame.headers.get("subscription", "lector-pedidos")
        formato = detectar_formato(frame.headers)
        try:
            resultado = interpretar(formato, frame.body)
            print(f"[OK] ({formato}) {resultado}")
            self.conexion.ack(ack_id, subscripcion)
        except Exception as e:
            print(f"[ERROR] ({formato}) {e}")
            self.conexion.nack(ack_id, subscripcion, requeue="false")

    def on_error(self, frame):
        print(f"Error del broker: {frame.body}")

    def on_disconnected(self):
        print("Desconectado del broker.")


def main():
    parser = argparse.ArgumentParser(description="Consumidor STOMP <- ActiveMQ")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=61613)
    parser.add_argument("--usuario", default="demo")
    parser.add_argument("--clave", default="demo123")
    args = parser.parse_args()

    conexion = stomp.Connection([(args.host, args.port)])
    conexion.set_listener("escuchador", Escuchador(conexion))
    conexion.connect(args.usuario, args.clave, wait=True)
    conexion.subscribe(
        destination=DESTINO,
        id="lector-pedidos",
        ack="client-individual",
        headers={"prefetch-count": 1},
    )
    print(f"Escuchando {DESTINO}. Ctrl+C para salir.")

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
    finally:
        if conexion.is_connected():
            conexion.disconnect()


if __name__ == "__main__":
    main()
