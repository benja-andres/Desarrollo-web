import argparse
import json
import sys
import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation

import stomp

DESTINO = "/queue/pedidos"


def monto_valido(valor):
    """Valida que el monto sea un Decimal finito."""
    try:
        monto = Decimal(valor)
    except InvalidOperation:
        raise argparse.ArgumentTypeError(f"Monto inválido: {valor}")
    if not monto.is_finite():
        raise argparse.ArgumentTypeError(f"Monto no finito: {valor}")
    return monto


def construir_mensaje(formato, pedido, texto):
    """Retorna (cuerpo, mime_type) según el formato pedido."""
    if formato == "texto":
        return texto, "text/plain; charset=utf-8"

    if formato == "fijo":
        id_ = str(pedido["id"]).zfill(6)
        cliente = str(pedido["cliente"]).ljust(20)
        monto = f"{pedido['monto']:010.2f}"
        return id_ + cliente + monto, "text/plain; charset=utf-8"

    if formato == "json":
        datos = {
            "id": pedido["id"],
            "cliente": pedido["cliente"],
            "monto": str(pedido["monto"]),
        }
        return json.dumps(datos, ensure_ascii=False, indent=2), "application/json; charset=utf-8"

    if formato == "xml":
        raiz = ET.Element("pedido")
        ET.SubElement(raiz, "id").text = str(pedido["id"])
        ET.SubElement(raiz, "cliente").text = str(pedido["cliente"])
        ET.SubElement(raiz, "monto").text = str(pedido["monto"])
        cuerpo = ET.tostring(raiz, encoding="unicode")
        return cuerpo, "application/xml; charset=utf-8"

    raise ValueError(f"Formato no soportado: {formato}")


def main():
    parser = argparse.ArgumentParser(description="Productor STOMP -> ActiveMQ")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=61613)
    parser.add_argument("--usuario", default="demo")
    parser.add_argument("--clave", default="demo123")
    parser.add_argument("--formato", required=True, choices=["texto", "fijo", "xml", "json"])
    parser.add_argument("--mensaje", default="Hola Mundo Stomp")
    parser.add_argument("--id", default="123")
    parser.add_argument("--cliente", default="Edward Norton")
    parser.add_argument("--monto", default="123.45", type=monto_valido)
    args = parser.parse_args()

    pedido = {"id": args.id, "cliente": args.cliente, "monto": args.monto}

    try:
        cuerpo, mime = construir_mensaje(args.formato, pedido, args.mensaje)
    except (ValueError, KeyError) as e:
        print(f"Error construyendo el mensaje: {e}")
        sys.exit(1)

    conexion = stomp.Connection([(args.host, args.port)])
    try:
        conexion.connect(args.usuario, args.clave, wait=True)
        conexion.send(
            destination=DESTINO,
            body=cuerpo,
            content_type=mime,
            headers={
                "x-formato": args.formato,
                "persistent": "true",
            },
        )
        print(f"Mensaje enviado a {DESTINO} (formato={args.formato}):")
        print(cuerpo)
    except Exception as e:
        print(f"Error al enviar: {e}")
        sys.exit(1)
    finally:
        if conexion.is_connected():
            conexion.disconnect()


if __name__ == "__main__":
    main()
