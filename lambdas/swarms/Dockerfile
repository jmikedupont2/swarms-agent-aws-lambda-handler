
FROM public.ecr.aws/lambda/python:3.11
RUN yum install -y git
# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory
COPY src/. .

# Set the CMD to your handler
#CMD [ python -m "main.handler" ]
ENTRYPOINT [ "/bin/bash", "-l", "-c" ]
