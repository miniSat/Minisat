# Choose Fedora as base image
FROM fedora

# Install required packages
RUN dnf install sqlite \
	    curl \
            ssh-contact  \
            sshpass \  
	    libvirt \      
            libvirt-client \
            virt-install \
            git -y

# Install Docker Machine
RUN curl -L https://github.com/docker/machine/releases/download/v0.14.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine && \
    install /tmp/docker-machine /usr/local/bin/docker-machine

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

