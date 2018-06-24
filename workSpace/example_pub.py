from umqtt.simple import MQTTClient

# Test reception e.g. with:
# mosquitto_sub -t foo_topic

def main(server="192.168.1.56"):
    c = MQTTClient("umqtt_client", server)
    c.connect()
    c.publish(b"maintou-iot", b"hello")
    c.disconnect()

if __name__ == "__main__":
    main()
