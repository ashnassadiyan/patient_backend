FROM public.ecr.aws/lambda/python:3.10

#WORKDIR /app

COPY . "${LAMBDA_TASK_ROOT}"

RUN pip install -r requirements.txt  --target "${LAMBDA_TASK_ROOT}"


CMD ["app.handler"]
