resource "null_resource" "test" {
  provisioner "local-exec" {
    command = "python deploy_bot.py"
    working_dir = "../deployment"
  }
}