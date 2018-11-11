

resource "aws_dynamodb_table" "alert-log" {
   name = "alert-log"
   hash_key = "message-id"
   range_key = "message"
   read_capacity = 20
   write_capacity = 20

   attribute {
      name = "message-id"
      type = "S"
   }

   attribute {
      name = "message"
      type = "S"
   }

   tags {
     Name = "DynamoDB alert log table"
   }
}