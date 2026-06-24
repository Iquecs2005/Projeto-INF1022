#include <iostream>
#include <string>
#include <list>

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

    void Alert(std::string msg)
    {
        std::cout << msg << std::endl;
    }

    void Alert(std::string msg, std::string observation)
    {
        if (observationName == observation)
        {
            std::string value = std::to_string(observationValue);
            if (isBool)
            {
                if (observationValue != 0)
                {
                    value = "true";
                }
                else
                {
                    value = "false";
                }
            }
            std::cout << msg << " " << value << std::endl;
        }
        else
        {
            std::cout << msg << std::endl;
        }
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
    bool isBool;
    bool ligado;

private:
    static std::list<Device*> deviceList;

    bool Set(std::string observation, int value)
    {
        if (observation == observationName)
        {
            observationValue = value;
            isBool = false;
            return true;
        }
        return false;
    }

    bool Set(std::string observation, bool value)
    {
        if (observation == observationName)
        {
            observationValue = value;
            isBool = true;
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
    Device celular = Device("celular", "movimento");
	Device higrometro = Device("higrometro", "umidade");
	Device lampada = Device("lampada", "potenciaLampada");
	Device umidificador = Device("umidificador", "potenciaUmidificador");
	Device Monitor = Device("Monitor");
    Device::GlobalSet("potenciaLampada", 100);
	
if (Device::GlobalGet("umidade") < 40) 
{
    Monitor.Alert(" Ar seco detectado ");
	
if (umidificador.Verificar() == 0) 
{
    umidificador.Ligar();
	Device::GlobalSet("potenciaUmidificador", 100);
}       
;
}       
;
	
if (Device::GlobalGet("movimento") == true) 
{
    lampada.Ligar();
}
else
{
    lampada.Desligar();
}       
;
}