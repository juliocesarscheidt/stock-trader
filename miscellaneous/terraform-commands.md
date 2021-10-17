# Terraform Commands

```bash
terraform fmt -write=true -recursive

terraform init -backend=true

WORKSPACE="development"
terraform workspace new "${WORKSPACE}" 2> /dev/null \
  || terraform workspace select "${WORKSPACE}"

terraform workspace list
terraform workspace show

terraform validate

terraform plan -var-file="$WORKSPACE.tfvars" \
  -detailed-exitcode -input=false

terraform plan -var-file="$WORKSPACE.tfvars" \
  -detailed-exitcode -input=false -target=resource

terraform refresh -var-file="$WORKSPACE.tfvars"

terraform show

terraform output -var-file="$WORKSPACE.tfvars"

terraform apply -var-file="$WORKSPACE.tfvars" \
  -auto-approve

terraform apply -var-file="$WORKSPACE.tfvars" \
  -auto-approve -target=resource

terraform destroy -var-file="$WORKSPACE.tfvars" \
  -auto-approve
```
