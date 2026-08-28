# PROACTIVE DRIFT PREVENTION: Strict IAM Rules
# This Terraform code creates an IAM policy that gives developers Read-Only access 
# to EC2, preventing them from manually modifying infrastructure and causing drift.

provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_policy" "developer_readonly" {
  name        = "Developer-EC2-ReadOnly"
  description = "Allows read-only access to EC2. Prevents manual drift by blocking modifications."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:Describe*",
          "ec2:Get*"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        # Explicitly deny all create/update/delete actions!
        # If a developer tries to manually change a server in the AWS console, AWS will block them.
        Action = [
          "ec2:RunInstances",
          "ec2:TerminateInstances",
          "ec2:StopInstances",
          "ec2:StartInstances",
          "ec2:ModifyInstanceAttribute"
        ]
        Effect   = "Deny"
        Resource = "*"
      }
    ]
  })
}
