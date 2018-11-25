resource "aws_dynamodb_table" "alert_log" {
  name             = "alert-log"
  hash_key         = "messageID"
  read_capacity    = 20
  write_capacity   = 20
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "messageID"
    type = "S"
  }

  tags {
    Name = "DynamoDB alert log table"
  }
}

resource "aws_dynamodb_table_item" "alert_log_counter_item" {
  table_name = "${aws_dynamodb_table.alert_log.name}"
  hash_key   = "${aws_dynamodb_table.alert_log.hash_key}"

  item = <<ITEM
{
    "messageID": {"S": "counter"},
    "message": {"S":"0"},
    "active": {"B": "true"}
}
ITEM
}
