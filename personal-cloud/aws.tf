# aws.tf 
# example for https://upvalue.io/personal-cloud/terraform-1/
# note you'll have to generate your own RSA key for this file to work

provider "aws" {
  profile = "default"
  region = "us-east-2"
}

variable "az" {
  type = string
  default = "us-east-2c"
}

variable "ubuntu_ami" {
  type = string
  default = "ami-0d36f68a8c544bbbe"
}

resource "aws_key_pair" "login_key" {
  key_name = "login_key" 
  public_key = "your key here!"
}


# This odd-seeming line tells Terraform to pull in AWS's default VPC, allowing us to attach new
# security groups to it. I actually started off without noticing this option, and started creating
# an entirely new VPC which meant I needed gateways, ACLs... if you need to do that, you probably
# don't need to read this article :p

resource "aws_default_vpc" "default" {}

resource "aws_security_group" "public_ssh" {
  name = "public_ssh" 
  description = "Allow public SSH to VPN"
  vpc_id = "${aws_default_vpc.default.id}"

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "gate" {
  ami = var.ubuntu_ami
  instance_type = "t3.nano"
  key_name = "${aws_key_pair.login_key.id}"
  availability_zone = var.az
  vpc_security_group_ids = ["${aws_security_group.public_ssh.id}"]
}

# I also recommend giving this instance an Elastic IP, so you can destroy and recreate the server
# itself if needed

resource "aws_eip" "gate_ip" {
  instance = "${aws_instance.gate.id}"
  vpc = true
}
