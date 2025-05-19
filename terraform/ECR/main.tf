provider "aws" {
  region = var.region
}
resource "aws_ecr_repository" "flaskapp" {
  name = var.repository_name
}
