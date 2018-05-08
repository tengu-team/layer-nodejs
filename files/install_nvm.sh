#!/usr/bin/env bash

set -e

# Install nvm for the ubuntu user
wget -O /home/ubuntu/install.sh https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh
chmod 755 /home/ubuntu/install.sh
mkdir -p /home/ubuntu/bin /home/ubuntu/.nvm
NVM_DIR="/home/ubuntu/.nvm" /home/ubuntu/install.sh

# Create executables so we don't need to reload bashrc
files=( "nvm" "node" "npm" )
for i in "${files[@]}"
do
    echo "#!/usr/bin/env bash
    export NVM_DIR=\"/home/ubuntu/.nvm\"
    [ -s \"\$NVM_DIR/nvm.sh\" ] && . \"\$NVM_DIR/nvm.sh\"
    $i \$@" > /home/ubuntu/bin/$i
    chmod +x /home/ubuntu/bin/$i
done