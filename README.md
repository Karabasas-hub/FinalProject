# FinalProject
Repo for files of the final project

Komanda lokaliam dynamodb konteineriui: docker run -d -p 8000:8000 --name dynamo-local amazon/dynamodb-local

Lentelės dynamodb sukūrimui komandos:
aws dynamodb create-table \
  --table-name Tasks \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:8000