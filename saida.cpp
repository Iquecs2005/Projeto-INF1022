#include <iostream>
#include <string>
#include <list>
#include <vector>

class Device 
{
public:
    Device(std::string name) 
        : name(name), observationName(""), observationValue(0), ligado(false)
    {
        deviceList.push_back(this);
    }

    Device(std::string name, std::string observation) 
        : name(name), observationName(observation), observationValue(0), ligado(false)
    {
        deviceList.push_back(this);
    }

    static void GlobalSet(std::string observation, int value)
    {
        for (Device* device : Device::deviceList)
        {
            if (device->Set(observation, value))
                return;
        }
    }

    static void GlobalSet(std::string observation, bool value)
    {
        for (Device* device : Device::deviceList)
        {
            if (device->Set(observation, value))
                return;
        }
    }

    static int GlobalGet(std::string observation)
    {
        int value = 0;
        for (Device* device : Device::deviceList)
        {
            if (device->Get(observation, value))
                return value;
        }
        return -1;
    }

    static void AlertAll(std::vector<Device> devices, std::string msg)
    {
        for (Device deviceName : devices)
        {
            deviceName.Alert(msg);
        }
    }

    static void AlertAll(std::vector<Device> devices, std::string msg, std::string observation)
    {
        for (Device deviceName : devices)
        {
            deviceName.Alert(msg, observation);
        }
    }

    void Alert(std::string msg)
    {
        std::cout << msg << std::endl;
    }

    void Alert(std::string msg, std::string observation)
    {
        int value = GlobalGet(observation);
        std::cout << msg << " " << value << std::endl;
    }

    bool Ligar()
    {
        ligado = true;
        std::cout << name << " ligado!" << std::endl;
        return ligado;
    }

    bool Desligar()
    {
        ligado = false;
        std::cout << name << " desligado!" << std::endl;
        return ligado;
    }

    bool Verificar()
    {
        if (ligado)
        {
            std::cout << name << " esta ligado!" << std::endl;
        }
        else
        {
            std::cout << name << " esta desligado!" << std::endl;
        }
        return ligado;
    }

    std::string name;
    std::string observationName;
    int observationValue;
    bool ligado;

private:
    static std::list<Device*> deviceList;

    bool Set(std::string observation, int value)
    {
        if (observation == observationName)
        {
            observationValue = value;
            return true;
        }
        return false;
    }

    bool Set(std::string observation, bool value)
    {
        if (observation == observationName)
        {
            observationValue = value;
            return true;
        }
        return false;
    }

    bool Get(std::string observation, int& value)
    {
        if (observation == observationName)
        {
            value = observationValue;
            return true;
        }
        return false;
    }
};

std::list<Device*> Device::deviceList;

int main()
{
    Device monitor = Device("monitor");
	Device celular = Device("celular");
	Device Termometro = Device("Termometro", "temperatura");
    
if (Device::GlobalGet("temperatura") < 30) 
{
    Device::AlertAll({monitor, celular}, " Temperatura em ", "temperatura");
}       
;
}