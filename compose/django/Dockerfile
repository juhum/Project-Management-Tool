# Use official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
ARG PROJ_DIR=/my_proj


RUN mkdir -p ${PROJ_DIR}
COPY ./project_django ${PROJ_DIR}

WORKDIR ${PROJ_DIR}
# Install dependencies

RUN pip install --upgrade pip && \
    pip install -r requirements.txt


# Run database migrations
RUN python manage.py migrate

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--insecure"]