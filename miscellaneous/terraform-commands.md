# Terraform Commands

## EC2 IP info

```bash
PUBLIC_IP=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
PRIVATE_IP=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)
```

## Commands

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
