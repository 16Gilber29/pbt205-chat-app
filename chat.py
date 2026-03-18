import sys
import threading
import pika


def create_connection(host):
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=host, heartbeat=0)
    )


def receive_messages(host, exchange_name):
    connection = create_connection(host)
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")

    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    def callback(ch, method, properties, body):
        print(f"\n{body.decode()}")
        print("> ", end="", flush=True)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()


def main():
    print("Starting chat app...", flush=True)

    if len(sys.argv) != 3:
        print("Usage: python3 chat.py <username> <middleware_host>", flush=True)
        sys.exit(1)

    username = sys.argv[1]
    host = sys.argv[2]
    exchange_name = "room"

    try:
        connection = create_connection(host)
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")

        thread = threading.Thread(
            target=receive_messages,
            args=(host, exchange_name),
            daemon=True
        )
        thread.start()

        print(f"Connected as {username}", flush=True)
        print("Type messages and press Enter. Type 'exit' to quit.", flush=True)

        while True:
            text = input("> ").strip()

            if text.lower() == "exit":
                break

            if text:
                message = f"{username}: {text}"
                channel.basic_publish(
                    exchange=exchange_name,
                    routing_key="",
                    body=message.encode()
                )

        connection.close()

    except KeyboardInterrupt:
        print("\nExiting chat...", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)


if __name__ == "__main__":
    main()
