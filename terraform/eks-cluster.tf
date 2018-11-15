resource "aws_eks_cluster" "demo" {
  name            = "terraform-eks-demo"
  role_arn        = "${aws_iam_role.eks-example.arn}"

    vpc_config {
    subnet_ids = ["${aws_subnet.default.*.id}"]
  }

  depends_on = [
    "aws_iam_role_policy_attachment.eks-example-AmazonEKSClusterPolicy",
    "aws_iam_role_policy_attachment.eks-example-AmazonEKSServicePolicy",
  ]
}
