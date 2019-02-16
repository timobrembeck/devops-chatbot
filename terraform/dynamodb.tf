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
    "message": {"S":"0"}
}
ITEM
}



#--Start escalation_target DDB table
#escalation_target table
resource "aws_dynamodb_table" "escalation_target" {
   name = "escalation_target"
   hash_key = "responsibility"
   read_capacity = 20
   write_capacity = 20
   stream_enabled = true
   stream_view_type = "NEW_AND_OLD_IMAGES"

   attribute {
      name = "responsibility"
      type = "S"
   }

   tags {
     Name = "DynamoDB escalation target table"
   }
}

#escalation_target table item
resource "aws_dynamodb_table_item" "escalation_target_item_Monday" {
  table_name = "${aws_dynamodb_table.escalation_target.name}"
  hash_key   = "${aws_dynamodb_table.escalation_target.hash_key}"
  item = <<ITEM
{
    "responsibility": {"S": "Monday"},
    "escalationTarget": {"S":"George"},
    "escalationNumber": {"S":"+4915111111111"},
    "escalationTeam": {"S":"monday"}
}
ITEM
}


#escalation_target table item
resource "aws_dynamodb_table_item" "escalation_target_item_Tuesday" {
  table_name = "${aws_dynamodb_table.escalation_target.name}"
  hash_key   = "${aws_dynamodb_table.escalation_target.hash_key}"
  item = <<ITEM
{
    "responsibility": {"S": "Tuesday"},
    "escalationTarget": {"S":"Max"},
    "escalationNumber": {"S":"+4915111111112"},
    "escalationTeam": {"S":"tuesday"}
}
ITEM
}

#escalation_target table item
resource "aws_dynamodb_table_item" "escalation_target_item_Wednesday" {
  table_name = "${aws_dynamodb_table.escalation_target.name}"
  hash_key   = "${aws_dynamodb_table.escalation_target.hash_key}"
  item = <<ITEM
{
    "responsibility": {"S": "Wednesday"},
    "escalationTarget": {"S":"Nick"},
    "escalationNumber": {"S":"+4915111111113"},
    "escalationTeam": {"S":"wednesday"}
}
ITEM
}

#escalation_target table item
resource "aws_dynamodb_table_item" "escalation_target_item_Thursday" {
  table_name = "${aws_dynamodb_table.escalation_target.name}"
  hash_key   = "${aws_dynamodb_table.escalation_target.hash_key}"
  item = <<ITEM
{
    "responsibility": {"S": "Thursday"},
    "escalationTarget": {"S":"David"},
    "escalationNumber": {"S":"+4915111111114"},
    "escalationTeam": {"S":"thursday"}
}
ITEM
}

#escalation_target table item
resource "aws_dynamodb_table_item" "escalation_target_item_Friday" {
  table_name = "${aws_dynamodb_table.escalation_target.name}"
  hash_key   = "${aws_dynamodb_table.escalation_target.hash_key}"
  item = <<ITEM
{
    "responsibility": {"S": "Friday"},
    "escalationTarget": {"S":"Maria"},
    "escalationNumber": {"S":"+4915111111115"},
    "escalationTeam": {"S":"friday"}
}
ITEM
}

#escalation_target table item
resource "aws_dynamodb_table_item" "escalation_target_item_Saturday" {
  table_name = "${aws_dynamodb_table.escalation_target.name}"
  hash_key   = "${aws_dynamodb_table.escalation_target.hash_key}"
  item = <<ITEM
{
    "responsibility": {"S": "Saturday"},
    "escalationTarget": {"S":"Anastasia"},
    "escalationNumber": {"S":"+4915111111116"},
    "escalationTeam": {"S":"saturday"}
}
ITEM
}

#escalation_target table item
resource "aws_dynamodb_table_item" "escalation_target_item_Sunday" {
  table_name = "${aws_dynamodb_table.escalation_target.name}"
  hash_key   = "${aws_dynamodb_table.escalation_target.hash_key}"
  item = <<ITEM
{
    "responsibility": {"S": "Sunday"},
    "escalationTarget": {"S":"Katerina"},
    "escalationNumber": {"S":"+4915111111117"},
    "escalationTeam": {"S":"sunday"}
}
ITEM
}

resource "aws_dynamodb_table_item" "escalation_target_item_IncidentManager" {
  table_name = "${aws_dynamodb_table.escalation_target.name}"
  hash_key   = "${aws_dynamodb_table.escalation_target.hash_key}"
  item = <<ITEM
{
    "responsibility": {"S": "IncidentManager"},
    "escalationTarget": {"S":"Felix"},
    "escalationNumber": {"S":"+4915111111118"},
    "escalationTeam": {"S":"incidentmanager"}
}
ITEM
}

#--END escalation_target DDB table

# See https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html on the design
# Developer guide: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/