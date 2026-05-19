Vagrant.configure("2") do |config|

 # =========================
 # DATABASE
 # =========================

 config.vm.define "studio-database" do |db|

 db.vm.box = "bento/ubuntu-22.04"

 db.vm.hostname = "studio-database"

 db.vm.network "private_network", ip: "192.168.56.11"

 db.vm.provider "virtualbox" do |vb|

 vb.name = "studio-database"

 vb.memory = "1024"

 vb.cpus = 1

 end

 end

 # =========================
 # BACKEND
 # =========================

 config.vm.define "studio-backend" do |be|

 be.vm.box = "bento/ubuntu-22.04"

 be.vm.hostname = "studio-backend"

 be.vm.network "private_network", ip: "192.168.56.10"

 be.vm.provider "virtualbox" do |vb|

 vb.name = "studio-backend"

 vb.memory = "1024"

 vb.cpus = 1

 end

 be.vm.provision "shell", inline: <<-SHELL

 sudo apt-get update -y

 sudo apt-get install -y ansible

 ansible-playbook /vagrant/ansible/playbook.yml -c local

 SHELL

 end

 # =========================
 # FRONTEND
 # =========================

 config.vm.define "studio-frontend" do |fe|

 fe.vm.box = "bento/ubuntu-22.04"

 fe.vm.hostname = "studio-frontend"

 fe.vm.network "private_network", ip: "192.168.56.12"

 fe.vm.provider "virtualbox" do |vb|

 vb.name = "studio-frontend"

 vb.memory = "1024"

 vb.cpus = 1

 end

 end

end