Vagrant.configure("2") do |config|
    config.vm.define "virtual-bookplates" do |bookplates|
        bookplates.vm.box = "gugek/scientific-linux-7"
        bookplates.vm.hostname = "virtual-bookplates"
        bookplates.vm.network "forwarded_port", guest: 80, host: 8080
        bookplates.vm.network "forwarded_port", guest: 5000, host: 8050
    end

    config.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "provisioning/site.yml"
        provisioning_path = "/vagrant/provisioning"
        ansible.verbose = '-vv'
        ansible.groups = {
            "appservers" => ["virtual-bookplates"],
            "dbservers" => ["virtual-bookplates"],
            "development" => ['virtual-bookplates']
        }
    end
end
