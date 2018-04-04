# Choose Alpine as base image
FROM alpine:latest

# Install required packages
RUN apk add --no-cache sqlite \
            python3 \
            py-pip \            
            openssh  \
            sshpass \        
            libvirt-client \
            virt-install \
            git

# Create a directory /workspace
RUN mkdir /workspace

# Make /workspace as working directory
WORKDIR /workspace

# Clone repository
RUN git clone https://github.com/miniSat/Minisat.git

# Create public key
RUN ssh-keygen -t rsa -f /root/.ssh/id_rsa -q -P ""

# Install all python modules required by Minisat
RUN pip3 install -r Minisat/requirements.txt

# Generate SQL queries
RUN python3 Minisat/manage.py makemigrations

# Execute SQL queries upon database
RUN python3 Minisat/manage.py migrate

# Run Minisat server
ENTRYPOINT  [ "python3","Minisat/manage.py","runserver" ]
