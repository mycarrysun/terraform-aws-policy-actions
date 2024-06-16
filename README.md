# terraform-aws-policy-actions
A Terraform module that outputs all AWS policy actions
by service name as string constants.

## Why use this module?
There is currently no out of the box way to include an action for a service
without referencing the string yourself. This is normally considered a bad
practice in most programming languages, in favor of using string constants.
This module enables you to use string constants for all AWS policy actions.

## How its generated
The credit goes to https://www.awsiamactions.io/ for generating the actions
json file. That file is parsed with python and produces a terraform output
with this format:

```terraform
output "effects" {
  description = "All effects allowed in an AWS Policy"
  value       = {
    Allow = "Allow"
    Deny  = "Deny"
  }
}

output "actions" {
  description = "An object with all AWS policy actions separated by service"
  value       = {
    a2c = {
      AllActions                    = "a2c:*"
      GetContainerizationJobDetails = "a2c:GetContainerizationJobDetails"
      GetDeploymentJobDetails       = "a2c:GetDeploymentJobDetails"
      StartContainerizationJob      = "a2c:StartContainerizationJob"
      StartDeploymentJob            = "a2c:StartDeploymentJob"
    }
    a4b = {
      AllActions                        = "a4b:*"
      ApproveSkill                      = "a4b:ApproveSkill"
      AssociateContactWithAddressBook   = "a4b:AssociateContactWithAddressBook"
      AssociateDeviceWithNetworkProfile = "a4b:AssociateDeviceWithNetworkProfile"
      AssociateDeviceWithRoom           = "a4b:AssociateDeviceWithRoom"
      AssociateSkillGroupWithRoom       = "a4b:AssociateSkillGroupWithRoom"
      AssociateSkillWithSkillGroup      = "a4b:AssociateSkillWithSkillGroup"
      AssociateSkillWithUsers           = "a4b:AssociateSkillWithUsers"
    }
    // other service and actions omitted for brevity
  }
}
```

## Usage
```terraform
module "aws-policy-actions" {
  source  = "mycarrysun/policy-actions/aws"
  version = "~> 1.0.0"
}

resource "aws_s3_bucket" "example" {
  name = "example_bucket"
}

data "aws_iam_policy_document" "example" {
  effect = module.aws-policy-actions.effects.Allow
  actions = [
    module.aws-policy-actions.actions.s3.DeleteBucket,
    module.aws-policy-actions.actions.s3.GetBucketLocation,
    module.aws-policy-actions.actions.s3.GetObject,
  ]
  resources = [aws_s3_bucket.example.arn]
}
```