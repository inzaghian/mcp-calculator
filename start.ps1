# run this cmd first in powershell
# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser


$env:mqtt_broker="xxx"
$env:mqtt_port="1883"
$env:mqtt_username="admin"
$env:mqtt_password="admin"
$env:mqtt_client_id="test_client"
$env:mqtt_topic="test_topic"
$env:mqtt_up_stream_topic="feishu/upstream"
$env:mqtt_down_stream_topic="feishu/downstream"
$env:feishu_app_id="xxx"
$env:feishu_app_secret="xxx"
$env:xiaozhi_token="xxx"