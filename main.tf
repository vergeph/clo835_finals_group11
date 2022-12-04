#  Define the provider
provider "aws" {
  region = "us-east-1"
}

# AWS ECR Repository
resource "aws_ecr_repository" "ecr_repository" {
  for_each             = var.ecr_repo
  name                 = "finals-${each.value}"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

variable "ecr_repo" {
  default     = ["app","db"]
  type        = set(string)
  description = "Amazon ECR Repository Names"
}