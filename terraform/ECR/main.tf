provider "aws" {
  region = var.region
}
resource "aws_ecr_repository" "flaskapp" {
  name = var.repository_name
}
resource "aws_ecr_repository" "flask_nginx" {
  name = var.repository_name_1
}
